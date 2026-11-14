"""Configuracao por ambiente; a demo explicita tem prioridade sobre o Windows."""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import dotenv_values
ROOT = Path(__file__).resolve().parents[1]

def configurar_app(app):
    arquivo = os.environ.get("UNIFICA_ENV_FILE")
    valores = dict(dotenv_values(ROOT / ".env"))
    valores.update(os.environ)
    if arquivo:
        valores.update(dotenv_values(arquivo))
    chave = valores.get("SECRET_KEY")
    segredo = valores.get("OIDC_CLIENT_SECRET")
    if not chave or not segredo:
        raise RuntimeError("Configure as chaves no .env ou execute scripts/preparar.ps1.")
    app.config.update(
        SECRET_KEY=chave,
        OIDC_CLIENT_ID=valores.get("OIDC_CLIENT_ID", "unifica-portal"),
        OIDC_CLIENT_SECRET=segredo,
        OIDC_ISSUER=valores.get("OIDC_ISSUER", "http://localhost:8080/realms/unifica").rstrip("/"),
        PUBLIC_URL=valores.get("PUBLIC_URL", "http://localhost:5000").rstrip("/"),
        SESSION_COOKIE_NAME="unifica_portal",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=valores.get("SESSION_COOKIE_SECURE", "false").lower() == "true",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        DEMO_LOGIN_ENABLED=valores.get("DEMO_LOGIN_ENABLED", "false").lower() == "true",
    )
