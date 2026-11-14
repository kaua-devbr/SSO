# Fluxo de autenticação

1. GET / redireciona para /auth/login quando não há sessão Keycloak no portal.
2. Authlib inicia Authorization Code Flow com PKCE S256, state e nonce.
3. O navegador mostra o login do Keycloak ou aproveita sua sessão existente.
4. /auth/callback troca o código e valida a identidade OIDC.
5. O Flask registra identidade, provedor e token de formulário na sessão e abre /perfil.
6. POST /sair ou /auth/sair exige token de formulário e encaminha ao logout do provedor.

O formulário local e a página intermediária foram retirados do fluxo. A senha
é gerenciada pelo Keycloak em /auth/conta. O cookie Flask é assinado, não
criptografado, e não contém access/refresh/ID tokens. Remember Me pertence ao
Keycloak; não significa sessão sem prazo. Não há backchannel logout nem
revalidação remota a cada página. O nível após OIDC ainda é normal para todos.

O pacote contém um cliente aplicativo. SSO entre sistemas exige adicionar outro
cliente ao mesmo realm. Consulte [o manual](EXECUCAO.md) para detalhes das URLs.
