from config.settings import configurar_app
from flask import Flask
from portal.routes import portal
from config.oidc import configurar_oidc
from auth.auth import auth

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

configurar_app(app)

configurar_oidc(app)
app.register_blueprint(auth)
app.register_blueprint(portal)



if __name__ == "__main__":
    app.run()
