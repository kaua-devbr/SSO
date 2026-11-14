from authlib.integrations.flask_client import OAuth

oauth = OAuth() # Ele cria a variavel com a função


def configurar_oidc(app):
    if not app.config.get("OIDC_CLIENT_SECRET"):
        raise RuntimeError(
            "Defina a variável OIDC_CLIENT_SECRET antes de iniciar."
        )

    oauth.init_app(app) # o app dentro das () é pra conectar no flask que tá no app.py

    issuer = app.config["OIDC_ISSUER"].rstrip("/")

    oauth.register(
        name="keycloak",
        client_id=app.config["OIDC_CLIENT_ID"],
        client_secret=app.config["OIDC_CLIENT_SECRET"],
        server_metadata_url=(
            f"{issuer}/.well-known/openid-configuration" # Descobe as autenticação e as chaves
        ),
        client_kwargs={
            "scope": "openid profile email",
            "code_challenge_method": "S256",
        },
    )