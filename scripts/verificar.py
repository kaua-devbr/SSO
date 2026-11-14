"""Testes locais sem MySQL/Keycloak real; tokens de teste sao assinados e validados."""
import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
# Somente este processo usa estas configuracoes ficticias.
os.environ.pop("UNIFICA_ENV_FILE", None)
os.environ.update(SECRET_KEY="test-only-portal", OIDC_CLIENT_SECRET="test-only-client",
                  OIDC_ISSUER="https://identity.example.test/realms/test",
                  OIDC_CLIENT_ID="unifica-portal",
                  PUBLIC_URL="http://localhost:5000",
                  SESSION_COOKIE_SECURE="false", DEMO_LOGIN_ENABLED="false")

from authlib.jose import JsonWebKey, jwt
from config.oidc import oauth

from app import app
app.config["TESTING"] = True


class PortalTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.key = JsonWebKey.generate_key("RSA", 2048, is_private=True, options={"kid": "test"})
        self.remote = oauth.create_client("keycloak")
        self.metadata = {
            "issuer": app.config["OIDC_ISSUER"],
            "authorization_endpoint": app.config["OIDC_ISSUER"] + "/auth",
            "token_endpoint": app.config["OIDC_ISSUER"] + "/token",
            "jwks_uri": app.config["OIDC_ISSUER"] + "/certs",
            "id_token_signing_alg_values_supported": ["RS256"],
        }
        self.meta_patch = patch.object(self.remote, "load_server_metadata", return_value=self.metadata)
        self.meta_patch.start()
        self.addCleanup(self.meta_patch.stop)

    def authenticate(self, change=None):
        response = self.client.get("/auth/login")
        self.assertEqual(response.status_code, 302)
        query = parse_qs(urlsplit(response.location).query)
        self.assertEqual(query["code_challenge_method"], ["S256"])
        self.assertEqual(query["redirect_uri"], [app.config["PUBLIC_URL"] + "/auth/callback"])
        now = int(time.time())
        claims = dict(iss=app.config["OIDC_ISSUER"], aud=app.config["OIDC_CLIENT_ID"],
                      sub="student-123", name="Aluno Teste", preferred_username="aluno.teste",
                      iat=now, exp=now + 300, nonce=query["nonce"][0])
        if change:
            claims.update(change)
        token = jwt.encode({"alg": "RS256", "kid": "test"}, claims, self.key).decode()
        with patch.object(self.remote, "fetch_access_token", return_value={"id_token": token, "access_token": "test"}), \
             patch.object(self.remote, "fetch_jwk_set", return_value={"keys": [self.key.as_dict()]}):
            result = self.client.get("/auth/callback", query_string={"state": query["state"][0], "code": "test"})
        return result

    def test_login_and_pages(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertTrue(self.client.get("/perfil").location.endswith("/auth/login"))
        self.assertEqual(self.authenticate().status_code, 302)
        paths = ["/perfil", "/inicio", "/notas", "/calendario", "/comunicados", "/configuracoes"]
        for path in paths:
            self.assertEqual(self.client.get(path).status_code, 200, path)
        with self.client.session_transaction() as session:
            self.assertEqual(session["usuario_id"], "student-123")
            self.assertFalse(session.permanent)
            self.assertNotIn("access_token", session)
            self.assertNotIn("id_token", session)

    def test_bad_nonce(self):
        self.assertEqual(self.authenticate({"nonce": "wrong"}).status_code, 400)

    def test_bad_audience(self):
        self.assertEqual(self.authenticate({"aud": "other-client"}).status_code, 400)

    def test_bad_issuer(self):
        self.assertEqual(self.authenticate({"iss": "https://other.example.test"}).status_code, 400)

    def test_expired(self):
        self.assertEqual(self.authenticate({"exp": int(time.time()) - 600}).status_code, 400)

    def test_bad_state(self):
        result = self.client.get("/auth/callback?state=not-issued&code=test")
        self.assertEqual(result.status_code, 400)
        with self.client.session_transaction() as session:
            self.assertFalse(session.get("logado"))

    def test_logout_csrf_and_account(self):
        self.authenticate()
        self.assertEqual(self.client.post("/auth/sair").status_code, 400)
        self.assertEqual(self.client.get("/auth/conta").location, app.config["OIDC_ISSUER"] + "/account/")
        with self.client.session_transaction() as session:
            csrf = session["form_token"]
        result = self.client.post("/auth/sair", data={"form_token": csrf})
        self.assertEqual(result.status_code, 303)
        self.assertTrue(result.location.startswith(app.config["OIDC_ISSUER"] + "/protocol/openid-connect/logout?"))
        with self.client.session_transaction() as session:
            self.assertFalse(session.get("logado"))

    def test_files_and_config(self):
        for folder in ["auth", "config", "portal", "crud_usuarios", "scripts"]:
            for file in (ROOT / folder).rglob("*.py"):
                ast.parse(file.read_text(encoding="utf-8"))
        for file in (ROOT / "templates").glob("*.html"):
            app.jinja_env.get_template(file.name)
        for file in (ROOT / "static").rglob("*"):
            if file.is_file():
                with self.client.get("/static/" + file.relative_to(ROOT / "static").as_posix()) as response:
                    self.assertEqual(response.status_code, 200)
        self.assertNotIn("mysql.connector", sys.modules)

    def test_generator_preserves_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            script = root / "scripts/configurar_demo.py"
            shutil.copyfile(ROOT / "scripts/configurar_demo.py", script)
            subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
            original = (root / ".demo/app.env").read_bytes()
            subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
            self.assertEqual(original, (root / ".demo/app.env").read_bytes())
            realm = json.loads((root / ".demo/import/unifica-demo-realm.json").read_text())
            self.assertEqual(len(realm["clients"]), 1)
            self.assertTrue(realm["rememberMe"])
            self.assertEqual(realm["clients"][0]["clientId"], "unifica-portal")

    def test_generator_migrates_old_library_without_changing_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            script = root / "scripts/configurar_demo.py"
            shutil.copyfile(ROOT / "scripts/configurar_demo.py", script)
            subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
            env_path = root / ".demo/app.env"
            original = env_path.read_text()
            env_path.write_text(original + "BIBLIOTECA_SECRET_KEY=obsolete\n")
            realm_path = root / ".demo/import/unifica-demo-realm.json"
            realm = json.loads(realm_path.read_text())
            portal_secret = realm["clients"][0]["secret"]
            realm["clients"].append({"clientId": "unifica-biblioteca"})
            realm_path.write_text(json.dumps(realm))
            subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
            self.assertEqual(env_path.read_text(), original)
            migrated = json.loads(realm_path.read_text())
            self.assertEqual(len(migrated["clients"]), 1)
            self.assertEqual(migrated["clients"][0]["secret"], portal_secret)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=2)
