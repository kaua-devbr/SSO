from secrets import token_urlsafe
from urllib.parse import urlencode
from authlib.integrations.base_client.errors import OAuthError
from authlib.jose.errors import JoseError
from flask import Blueprint, abort, current_app, redirect, session, url_for
from requests.exceptions import RequestException
from auth.decorators import login_required
from config.oidc import oauth

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.get("/login")
def login():
    try:
        return oauth.keycloak.authorize_redirect(
            current_app.config["PUBLIC_URL"] + "/auth/callback",
            nonce=token_urlsafe(32),
        )
    except RequestException:
        abort(503, description="Keycloak indisponivel. Verifique se o servico esta iniciado.")

@auth.get("/callback")
def callback():
    try:
        token = oauth.keycloak.authorize_access_token()
    except (OAuthError, JoseError):
        abort(400, description="Login recusado ou expirado. Inicie uma nova tentativa.")
    except RequestException:
        abort(503, description="Nao foi possivel consultar o Keycloak.")
    identidade = token.get("userinfo")
    if not identidade or not identidade.get("sub"):
        abort(400, description="Identidade invalida.")
    session.clear()
    # A persistencia entre navegadores fica no Remember Me do Keycloak.
    # Ao perder o cookie local, uma nova autenticacao OIDC recupera a identidade.
    session.permanent = False
    session.update(
        logado=True,
        usuario_id=identidade["sub"],
        usuario=identidade.get("name") or identidade.get("preferred_username") or "Usuario",
        login=identidade.get("preferred_username") or identidade["sub"],
        nivel="normal",
        auth_provider="keycloak",
        form_token=token_urlsafe(32),
    )
    # Nenhum access/refresh/ID token e armazenado no cookie assinado do Flask.
    return redirect(url_for("portal.perfil"))

def encerrar_sessao():
    config = current_app.config
    parametros = urlencode({"client_id": config["OIDC_CLIENT_ID"],
                            "post_logout_redirect_uri": config["PUBLIC_URL"] + "/"})
    session.clear()
    # Sem id_token_hint, Keycloak pode pedir confirmacao da saida.
    return redirect(config["OIDC_ISSUER"] + "/protocol/openid-connect/logout?" + parametros, code=303)

@auth.post("/sair")
@login_required
def sair():
    return encerrar_sessao()

@auth.get("/conta")
@login_required
def conta():
    return redirect(current_app.config["OIDC_ISSUER"] + "/account/")
