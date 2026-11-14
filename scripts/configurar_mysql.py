"""Gera apenas segredos MySQL; nunca altera as chaves OIDC existentes."""
from pathlib import Path
from secrets import token_urlsafe

ROOT = Path(__file__).resolve().parents[1]


def configurar(root=ROOT):
    directory = root / ".demo"
    directory.mkdir(exist_ok=True)
    server = directory / "mysql.env"
    client = directory / "database.env"
    if server.exists() != client.exists():
        raise RuntimeError("Configuracao MySQL parcial. Restaure o arquivo ausente; nao regenere credenciais.")
    if server.exists():
        print("Configuracao MySQL existente preservada.")
        return
    password = token_urlsafe(32)
    server.write_text(
        f"MYSQL_ROOT_PASSWORD={token_urlsafe(48)}\nMYSQL_DATABASE=UNIFICA\n"
        f"MYSQL_USER=unifica_app\nMYSQL_PASSWORD={password}\n", encoding="utf-8")
    client.write_text(
        "UNIFICA_MYSQL_HOST=mysql\nUNIFICA_MYSQL_PORT=3306\n"
        "UNIFICA_MYSQL_USER=unifica_app\nUNIFICA_MYSQL_DATABASE=UNIFICA\n"
        f"UNIFICA_MYSQL_PASSWORD={password}\n", encoding="utf-8")
    print("Configuracao MySQL criada. Credenciais somente em .demo; nao compartilhe.")


if __name__ == "__main__":
    configurar()
