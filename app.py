from secrets import token_hex

from flask import Flask

from unifica.portal.routes import portal

app = Flask(
    __name__,
    template_folder="unifica/templates",
    static_folder="unifica/static",
    static_url_path="/static",
)
app.config["SECRET_KEY"] = token_hex(32)
app.register_blueprint(portal)

if __name__ == "__main__":
    app.run()
