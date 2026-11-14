from secrets import token_urlsafe
from urllib.parse import parse_qs, urlencode, urlsplit
from authlib.integrations.base_client.errors import OAuthError
from authlib.jose.errors import JoseError
from flask import Blueprint, abort, current_app, flash, redirect, request, session, url_for
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
    change_user = session.get("password_changes", {}).get(request.args.get("state"))
    if change_user and change_user != identidade["sub"]:
        session.clear()
        abort(400, description="A conta autenticada mudou. Entre novamente com sua conta.")
    preferences = {key: session[key] for key in ("tema", "fonte", "comunicados_lidos") if key in session} if change_user else {}
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
    if change_user:
        session.update(preferences)
        status = request.args.get("kc_action_status")
        if status == "success":
            flash("Senha alterada. Use a nova senha no proximo login.", "sucesso")
        elif status == "cancelled":
            flash("Alteracao de senha cancelada.", "aviso")
        else:
            flash("Fluxo de senha encerrado. Confira o resultado informado pelo Keycloak.", "aviso")
        return redirect(url_for("portal.configuracoes"))
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


@auth.get("/alterar-senha")
@login_required
def alterar_senha():
    """Solicita troca da propria senha no provedor, sem exigir papel administrativo."""
    try:
        response = oauth.keycloak.authorize_redirect(
            current_app.config["PUBLIC_URL"] + "/auth/callback",
            nonce=token_urlsafe(32),
            kc_action="UPDATE_PASSWORD",
            login_hint=session.get("login"),
        )
    except RequestException:
        abort(503, description="Keycloak indisponivel. Tente alterar a senha novamente mais tarde.")
    state = parse_qs(urlsplit(response.location).query)["state"][0]
    changes = dict(list(session.get("password_changes", {}).items())[-4:])
    changes[state] = session["usuario_id"]
    session["password_changes"] = changes
    return response
