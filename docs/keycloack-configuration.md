# Configuração do Keycloak local

O arquivo que gera a instalação é `scripts/configurar_demo.py`. Ele escreve
`.demo/import/unifica-demo-realm.json` para importação inicial pelo Compose.
`keycloak/realm-school.json` não é usado neste fluxo.

- Realm: unifica-demo.
- Cliente confidencial: unifica-portal.
- Standard Flow ativo; PKCE S256; Direct Access Grants e Implicit desativados.
- Callback: http://localhost:5000/auth/callback.
- Retorno do logout: http://localhost:5000/.
- Emissor: http://localhost:8081/realms/unifica-demo.
- Conta inicial: zezinho; senha de demonstracao 1234, registrada em .demo/acessos.txt.
- Administrador bootstrap: separado, para o console de administração.

Não edite acessos.txt esperando mudar uma senha: altere-a pelo Keycloak.
Em **Configurações**, **Alterar senha** solicita `UPDATE_PASSWORD` ao Keycloak. **Gerenciar conta** abre o console da própria conta. Administradores podem gerenciar usuários pelo console administrativo.

O gerador preserva chaves existentes. O realm já importado não é sobrescrito ao
reiniciar. Alterações no JSON afetam novas instalações, não automaticamente o
banco ativo. Não remova o volume para aplicar uma simples alteração de senha.

O segredo do cliente e SECRET_KEY são chaves internas, não senhas do aluno.
O modo start-dev é para execução local; veja [EXECUCAO.md](EXECUCAO.md).
