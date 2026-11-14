"""Segunda aplicacao independente para demonstrar SSO; nao implementa emprestimos."""
from flask import Blueprint, Flask, render_template_string
from auth.auth import auth
from auth.decorators import login_required
from config.oidc import configurar_oidc
from config.settings import configurar_app

app = Flask(__name__)
configurar_app(app, biblioteca=True)
configurar_oidc(app)
portal = Blueprint("portal", __name__)

@portal.get("/")
def login():
    return render_template_string('''<!doctype html><html lang="pt-BR"><meta charset="utf-8">
    <title>Biblioteca escolar</title><h1>Biblioteca escolar</h1>
    <p>Segunda aplicacao do UNIFICA.</p><a href="{{ url_for('auth.login') }}">Entrar com a conta escolar</a></html>''')

@portal.get("/perfil")
@login_required
def perfil():
    return render_template_string('''<!doctype html><html lang="pt-BR"><meta charset="utf-8">
    <title>Biblioteca escolar</title><h1>Ola, {{ session.usuario }}!</h1>
    <p>Voce entrou na biblioteca pela mesma identidade escolar.</p>
    <ul><li>Dom Casmurro — catalogo demonstrativo</li><li>O Auto da Compadecida — catalogo demonstrativo</li></ul>
    <form method="post" action="{{ url_for('auth.sair') }}">
    <input type="hidden" name="form_token" value="{{ session.form_token }}"><button>Sair</button></form></html>''')

app.register_blueprint(auth)
app.register_blueprint(portal)

if __name__ == "__main__":
    app.run(port=5001)
