# Arquitetura atual

O navegador acessa o portal em http://localhost:5000. O portal usa Flask,
Jinja e Waitress, importando `app:app` na porta interna 8000. O Keycloak em
http://localhost:8081 fornece autenticação OIDC; não fornece as páginas escolares.

O Compose possui tres servicos: portal, keycloak e mysql. Portal e Keycloak compartilham namespace de
rede por `network_mode: service:keycloak`. As portas são publicadas no serviço
Keycloak somente no loopback do host. As imagens e sistemas de arquivos são distintos.

O volume keycloak_data conserva o banco local do Keycloak. `.demo` contém
configuração inicial e segredos gerados na máquina. O portal não usa MySQL neste
fluxo; crud_usuarios permanece separado e incompleto. Os dados escolares são
exemplos e preferências/leitura ficam na sessão.

Consulte [o manual](EXECUCAO.md) para pastas, rede, persistência e limites.

O servico mysql utiliza volume mysql_data e expoe 127.0.0.1:3307 para Workbench.
O conector Python acessa mysql:3306. O esquema inicial tem sete tabelas;
a integracao das telas ainda esta pendente. Veja [MYSQL.md](MYSQL.md).
