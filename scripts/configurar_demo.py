"""Gera uma instalacao local isolada. Executar novamente preserva as chaves."""
import json
from pathlib import Path
from secrets import token_urlsafe

ROOT = Path(__file__).resolve().parents[1]
destino = ROOT / ".demo"
destino.mkdir(exist_ok=True)
config = destino / "app.env"
if config.exists():
    if not (destino / "import/unifica-demo-realm.json").exists() or not (destino / "keycloak.env").exists():
        raise SystemExit("Instalacao incompleta: preserve .demo e restaure seus arquivos. Nao regenere segredos isolados.")
    print("Configuracao existente preservada.")
else:
    portal_secret, library_secret = token_urlsafe(32), token_urlsafe(32)
    admin_password, demo_password = token_urlsafe(20), token_urlsafe(12)
    clients = []
    for name, port, secret in [("unifica-portal", 5000, portal_secret), ("unifica-biblioteca", 5001, library_secret)]:
        clients.append({
            "clientId": name, "enabled": True, "protocol": "openid-connect",
            "publicClient": False, "secret": secret, "standardFlowEnabled": True,
            "directAccessGrantsEnabled": False, "implicitFlowEnabled": False,
            "serviceAccountsEnabled": False,
            "redirectUris": [f"http://localhost:{port}/auth/callback"],
            "webOrigins": [f"http://localhost:{port}"],
            "attributes": {"pkce.code.challenge.method": "S256",
                           "post.logout.redirect.uris": f"http://localhost:{port}/"},
            "defaultClientScopes": ["web-origins", "acr", "profile", "roles", "email"],
        })
    realm = {
        "realm": "unifica-demo", "enabled": True, "rememberMe": True,
        "registrationAllowed": False, "resetPasswordAllowed": False,
        "sslRequired": "external", "ssoSessionIdleTimeout": 1800,
        "ssoSessionMaxLifespan": 28800, "ssoSessionIdleTimeoutRememberMe": 604800,
        "ssoSessionMaxLifespanRememberMe": 2592000,
        "clients": clients,
        "users": [{"username": "aluno.teste", "enabled": True,
                   "firstName": "Aluno", "lastName": "Demonstracao",
                   "email": "aluno@example.test", "emailVerified": True,
                   "credentials": [{"type": "password", "value": demo_password, "temporary": False}]}],
    }
    (destino / "import").mkdir(exist_ok=True)
    (destino / "import/unifica-demo-realm.json").write_text(json.dumps(realm, indent=2), encoding="utf-8")
    (destino / "keycloak.env").write_text(
        f"KC_BOOTSTRAP_ADMIN_USERNAME=admin\nKC_BOOTSTRAP_ADMIN_PASSWORD={admin_password}\n", encoding="utf-8")
    config.write_text(
        f"SECRET_KEY={token_urlsafe(48)}\nOIDC_CLIENT_ID=unifica-portal\nOIDC_CLIENT_SECRET={portal_secret}\n"
        "OIDC_ISSUER=http://localhost:8081/realms/unifica-demo\nPUBLIC_URL=http://localhost:5000\n"
        f"BIBLIOTECA_SECRET_KEY={token_urlsafe(48)}\nBIBLIOTECA_OIDC_CLIENT_ID=unifica-biblioteca\n"
        f"BIBLIOTECA_OIDC_CLIENT_SECRET={library_secret}\nBIBLIOTECA_PUBLIC_URL=http://localhost:5001\n"
        "SESSION_COOKIE_SECURE=false\nDEMO_LOGIN_ENABLED=false\n", encoding="utf-8")
    (destino / "acessos.txt").write_text(
        f"APENAS DEMONSTRACAO LOCAL\nKeycloak: http://localhost:8081\nAdministrador: admin\nSenha: {admin_password}\n"
        f"Aluno: aluno.teste\nSenha: {demo_password}\n", encoding="utf-8")
    print("Configuracao criada. Consulte .demo/acessos.txt para as contas locais. Nao compartilhe .demo.")
