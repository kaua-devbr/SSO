# Fluxo de autenticação

1. Ao abrir o portal sem sessão, o Flask redireciona para `/auth/login`.
2. A Authlib inicia o Authorization Code Flow com PKCE S256, `state` e `nonce`.
3. O Keycloak autentica o usuário ou reaproveita a sessão do provedor. O navegador volta para `/auth/callback` com um código temporário.
4. O Flask troca o código e valida a identidade. Cria a sessão local e abre `/perfil`. O cookie Flask é assinado e guarda dados da sessão. Os tokens OIDC permanecem fora do cookie.
5. **Sair da conta** envia um POST com token de formulário, limpa a sessão do Flask e solicita o logout ao Keycloak, que pode pedir confirmação.

## Sessão e conta

**Lembrar de mim** pertence ao Keycloak. Se o navegador perder a sessão do Flask, o portal pode autenticar novamente sem pedir a senha enquanto a sessão do provedor estiver válida.

Em **Configurações**, **Alterar senha** leva a `/auth/alterar-senha`. A rota solicita `UPDATE_PASSWORD` ao Keycloak para a própria conta e retorna às configurações após o fluxo. `/auth/conta` abre o console de conta do Keycloak.

A demonstração inclui um cliente, `unifica-portal`. Para demonstrar login compartilhado entre sistemas diferentes, seria necessário configurar outro cliente no mesmo realm.

Veja a [configuração do Keycloak](keycloack-configuration.md).
