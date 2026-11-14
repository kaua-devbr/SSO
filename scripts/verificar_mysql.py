"""Verificacao somente leitura da conexao e do esquema inicial."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.database import conectar


def verificar():
    connection = conectar()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE()")
            tables = {row[0] for row in cursor.fetchall()}
            expected = {"usuarios", "escolas", "turmas", "matriculas", "perfis", "usuario_perfis", "preferencias"}
            if not expected <= tables:
                raise RuntimeError("Esquema incompleto: faltam " + ", ".join(sorted(expected-tables)))
            cursor.execute("SELECT nome FROM perfis ORDER BY nome")
            if {row[0] for row in cursor.fetchall()} != {"aluno", "professor", "administrador"}:
                raise RuntimeError("Perfis iniciais ausentes ou diferentes do esperado.")
            print("MySQL: conexao, sete tabelas e perfis iniciais OK. Nenhum dado alterado.")
        finally:
            cursor.close()
    finally:
        connection.close()


if __name__ == "__main__":
    try:
        verificar()
    except Exception as error:
        # Nao imprimir argumentos da conexao nem segredos.
        raise SystemExit("Falha na verificacao MySQL (" + type(error).__name__ + "). Confira servico, configuracao e inicializacao.")
