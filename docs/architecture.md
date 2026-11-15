# Arquitetura do UNIFICA

| Serviço | Responsabilidade | Endereço local |
| --- | --- | --- |
| Portal | Flask e Jinja servidos por Waitress | http://localhost:5000 |
| Keycloak | Identidade, login e senha via OpenID Connect | http://localhost:8081 |
| MySQL | Esquema acadêmico e perfis iniciais | `127.0.0.1:3307` no Workbench |

O portal escuta na porta interna 8000. Ele compartilha a rede do Keycloak com `network_mode: service:keycloak`, o que permite usar o mesmo emissor OIDC no navegador e no Flask. O Compose publica as portas do portal e do Keycloak no serviço `keycloak`. O conector Python usa `mysql:3306` na rede do Compose.

O volume `keycloak_data` guarda as contas e configurações do provedor. O volume `mysql_data` guarda o banco escolar. A preparação gera a configuração de cada instalação em `.demo/`.

O portal exige uma sessão Keycloak para as páginas escolares. Notas e frequência são calculadas a partir dos dados de demonstração em `portal/boletim.py`. Calendário e comunicados também usam exemplos. Aparência e leitura de comunicados ficam na sessão do Flask. A ligação das telas ao MySQL e as permissões escolares por perfil estão previstas para uma etapa futura.

Veja o [manual de execução](EXECUCAO.md), o [fluxo SSO](sso-flow.md) e o [guia do banco](MYSQL.md).
