"""Conexoes MySQL sob demanda. Importar este modulo nao abre o banco."""
from contextlib import contextmanager
from os import environ


def conectar():
    import mysql.connector
    password = environ.get("UNIFICA_MYSQL_PASSWORD")
    if not password:
        raise RuntimeError("Configuracao MySQL ausente. Execute scripts/preparar.ps1.")
    return mysql.connector.connect(
        host=environ.get("UNIFICA_MYSQL_HOST", "mysql"),
        port=int(environ.get("UNIFICA_MYSQL_PORT", "3306")),
        user=environ.get("UNIFICA_MYSQL_USER", "unifica_app"),
        password=password,
        database=environ.get("UNIFICA_MYSQL_DATABASE", "UNIFICA"),
        connection_timeout=5, charset="utf8mb4", autocommit=False,
        time_zone="+00:00",
    )


@contextmanager
def transacao():
    """Uso futuro pelo CRUD: confirma ao concluir, desfaz ao falhar e fecha."""
    connection = conectar()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
