"""Aplica explicitamente zezinho/1234 ao Keycloak LOCAL, preservando o usuario."""
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://localhost:8081"


def aplicar():
    env = {}
    for line in (ROOT / ".demo/keycloak.env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            env[key] = value
    data = urlencode({
        "grant_type": "password", "client_id": "admin-cli",
        "username": env["KC_BOOTSTRAP_ADMIN_USERNAME"],
        "password": env["KC_BOOTSTRAP_ADMIN_PASSWORD"],
    }).encode()
    request = Request(BASE + "/realms/master/protocol/openid-connect/token", data=data)
    with urlopen(request, timeout=15) as response:
        token = json.load(response)["access_token"]

    def api(path, method="GET", body=None):
        request = Request(BASE + "/admin/realms/unifica-demo" + path,
                          data=None if body is None else json.dumps(body).encode(),
                          headers={"Authorization": "Bearer " + token,
                                   "Content-Type": "application/json"}, method=method)
        with urlopen(request, timeout=15) as response:
            content = response.read()
            return json.loads(content) if content else None

    existing = api("/users?username=zezinho&exact=true")
    previous = api("/users?username=aluno.teste&exact=true")
    if existing and previous:
        raise RuntimeError("As duas contas existem. Nenhuma foi alterada; escolha a conta pelo painel.")
    if existing or previous:
        user = (existing or previous)[0]
        if user["username"] != "zezinho":
            settings = api("")
            editable = settings.get("editUsernameAllowed", False)
            try:
                if not editable:
                    api("", "PUT", {"editUsernameAllowed": True})
                api("/users/" + user["id"], "PUT", {"username": "zezinho", "firstName": "Zezinho"})
            finally:
                if not editable:
                    api("", "PUT", {"editUsernameAllowed": False})
    else:
        api("/users", "POST", {"username": "zezinho", "firstName": "Zezinho", "enabled": True})
        user = api("/users?username=zezinho&exact=true")[0]
    api("/users/" + user["id"] + "/reset-password", "PUT",
        {"type": "password", "value": "1234", "temporary": False})
    assert api("/users/" + user["id"])["username"] == "zezinho"

    # Atualiza registros locais somente depois de o provedor aceitar a alteracao.
    realm_path = ROOT / ".demo/import/unifica-demo-realm.json"
    realm = json.loads(realm_path.read_text(encoding="utf-8"))
    for entry in realm.get("users", []):
        if entry.get("username") in ("aluno.teste", "zezinho"):
            entry.update(username="zezinho", firstName="Zezinho",
                         credentials=[{"type": "password", "value": "1234", "temporary": False}])
    realm_path.write_text(json.dumps(realm, indent=2), encoding="utf-8")
    access_path = ROOT / ".demo/acessos.txt"
    if access_path.exists():
        text = access_path.read_text(encoding="utf-8")
        prefix, separator, _ = text.partition("Aluno:")
        if separator:
            access_path.write_text(prefix + "Aluno: zezinho\nSenha: 1234\n", encoding="utf-8")
    print("Conta local atualizada: zezinho / 1234. Identidade existente preservada.")


if __name__ == "__main__":
    try:
        aplicar()
    except HTTPError as error:
        raise SystemExit(f"Keycloak respondeu HTTP {error.code}. Confira a conta administrativa local; nenhum segredo foi exibido.")
