"""Testa configuracao e ciclo de conexao sem servidor e sem dados reais."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from config import database
from configurar_mysql import configurar


class ConfigMySQLTests(unittest.TestCase):
    def test_generation_preserves_oidc_and_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".demo").mkdir()
            oidc = root / ".demo/app.env"
            oidc.write_text("SECRET_KEY=fixture\n")
            configurar(root)
            first = {p.name: p.read_bytes() for p in (root / ".demo").iterdir()}
            configurar(root)
            self.assertEqual(first, {p.name: p.read_bytes() for p in (root / ".demo").iterdir()})
            server = dict(line.split("=", 1) for line in (root / ".demo/mysql.env").read_text().splitlines())
            client = dict(line.split("=", 1) for line in (root / ".demo/database.env").read_text().splitlines())
            self.assertEqual(server["MYSQL_PASSWORD"], client["UNIFICA_MYSQL_PASSWORD"])
            self.assertNotEqual(server["MYSQL_ROOT_PASSWORD"], server["MYSQL_PASSWORD"])
            self.assertEqual(oidc.read_text(), "SECRET_KEY=fixture\n")

    def test_partial_config_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".demo").mkdir()
            original = root / ".demo/mysql.env"
            original.write_text("preservar")
            with self.assertRaises(RuntimeError):
                configurar(root)
            self.assertEqual(original.read_text(), "preservar")
            self.assertFalse((root / ".demo/database.env").exists())

    def test_transaction_commit_and_close(self):
        connection = Mock()
        with patch.object(database, "conectar", return_value=connection):
            with database.transacao() as received:
                self.assertIs(received, connection)
        connection.commit.assert_called_once()
        connection.rollback.assert_not_called()
        connection.close.assert_called_once()

    def test_transaction_rollback_and_close(self):
        connection = Mock()
        with patch.object(database, "conectar", return_value=connection):
            with self.assertRaises(ValueError):
                with database.transacao():
                    raise ValueError("fixture")
        connection.commit.assert_not_called()
        connection.rollback.assert_called_once()
        connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
