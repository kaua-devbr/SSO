# Layouts históricos de login

Estes arquivos foram movidos sem alterar o conteúdo:

- `login.html`: formulário local anterior.
- `login_sso.html`: página intermediária anterior, com botão para iniciar OIDC.
- `login.css`: estilos dessas páginas.

Não são servidos pelo Flask nem copiados para a imagem do portal. As expressões
Jinja permanecem como referência de estudo; abrir os arquivos diretamente no
navegador não equivale a executar o aplicativo. O formulário local não possui
mais uma rota de autenticação ativa. O Keycloak fornece o login atual.

Consulte [o manual atual](../../EXECUCAO.md).
