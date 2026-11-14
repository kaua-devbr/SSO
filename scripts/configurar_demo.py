"""Gera configuracao local sem sobrescrever chaves ou contas existentes."""
import json
from pathlib import Path
from secrets import token_urlsafe

ROOT = Path(__file__).resolve().parents[1]
destino = ROOT / ".demo"
destino.mkdir(exist_ok=True)
config = destino / "app.env"
realm_path = destino / "import/unifica-demo-realm.json"
keycloak_env = destino / "keycloak.env"
if config.exists():
    if not realm_path.exists() or not keycloak_env.exists():
        raise SystemExit("Instalacao incompleta: restaure .demo; nao regenere segredos isolados.")
    # Migra somente configuracoes da biblioteca removida, sem trocar credenciais.
    lines = config.read_text(encoding="utf-8").splitlines()
    remaining = [line for line in lines if not line.startswith("BIBLIOTECA_")]
    if remaining != lines:
        config.write_text("\n".join(remaining) + "\n", encoding="utf-8")
    realm = json.loads(realm_path.read_text(encoding="utf-8"))
    clients = realm.get("clients", [])
    remaining_clients = [client for client in clients if client.get("clientId") != "unifica-biblioteca"]
    if remaining_clients != clients:
        realm["clients"] = remaining_clients
        realm_path.write_text(json.dumps(realm, indent=2), encoding="utf-8")
    print("Configuracao existente preservada.")
else:
    if realm_path.exists() or keycloak_env.exists():
        raise SystemExit("Configuracao parcial encontrada. Restaure app.env antes de continuar.")
    secret = token_urlsafe(32)
    admin_password, demo_password = token_urlsafe(20), token_urlsafe(12)
    realm = {
        "realm": "unifica-demo", "enabled": True, "rememberMe": True,
        "registrationAllowed": False, "resetPasswordAllowed": False,
        "sslRequired": "external", "ssoSessionIdleTimeout": 1800,
        "ssoSessionMaxLifespan": 28800, "ssoSessionIdleTimeoutRememberMe": 604800,
        "ssoSessionMaxLifespanRememberMe": 2592000,
        "clients": [{
            "clientId": "unifica-portal", "enabled": True, "protocol": "openid-connect",
            "publicClient": False, "secret": secret, "standardFlowEnabled": True,
            "directAccessGrantsEnabled": False, "implicitFlowEnabled": False,
            "serviceAccountsEnabled": False,
            "redirectUris": ["http://localhost:5000/auth/callback"],
            "webOrigins": ["http://localhost:5000"],
            "attributes": {"pkce.code.challenge.method": "S256",
                           "post.logout.redirect.uris": "http://localhost:5000/"},
            "defaultClientScopes": ["web-origins", "acr", "profile", "roles", "email"],
        }],
        "users": [{"username": "aluno.teste", "enabled": True,
                   "firstName": "Aluno", "lastName": "Demonstracao",
                   "email": "aluno@example.test", "emailVerified": True,
                   "credentials": [{"type": "password", "value": demo_password, "temporary": False}]}],
    }
    (destino / "import").mkdir(exist_ok=True)
    realm_path.write_text(json.dumps(realm, indent=2), encoding="utf-8")
    keycloak_env.write_text(
        f"KC_BOOTSTRAP_ADMIN_USERNAME=admin\nKC_BOOTSTRAP_ADMIN_PASSWORD={admin_password}\n", encoding="utf-8")
    config.write_text(
        f"SECRET_KEY={token_urlsafe(48)}\nOIDC_CLIENT_ID=unifica-portal\nOIDC_CLIENT_SECRET={secret}\n"
        "OIDC_ISSUER=http://localhost:8081/realms/unifica-demo\nPUBLIC_URL=http://localhost:5000\n"
        "SESSION_COOKIE_SECURE=false\nDEMO_LOGIN_ENABLED=false\n", encoding="utf-8")
    (destino / "acessos.txt").write_text(
        f"APENAS DEMONSTRACAO LOCAL\nKeycloak: http://localhost:8081\nAdministrador: admin\nSenha: {admin_password}\n"
        f"Aluno: aluno.teste\nSenha: {demo_password}\n", encoding="utf-8")
    print("Configuracao criada. Consulte .demo/acessos.txt. Nao compartilhe .demo.")
