# MySQL do UNIFICA — primeira etapa

O projeto agora prepara um terceiro serviço: `mysql:8.4`, da linha LTS 8.4.
O banco escolar é `UNIFICA`, com volume próprio `mysql_data` (normalmente
`unifica-demo_mysql_data`). O Keycloak mantém seu banco/volume existentes.
Esta etapa cria a estrutura e a conexão Python; as telas ainda usam os exemplos
anteriores e não foram conectadas ao novo CRUD.

## 1. Arquivos e responsabilidades

| Arquivo | Finalidade |
|---|---|
| [`structure.sql`](../crud_usuarios/database/init/structure.sql) | Sete tabelas, relações, regras e três perfis iniciais |
| `config/database.py` | Conectar sob demanda e gerenciar commit, rollback e fechamento |
| `scripts/configurar_mysql.py` | Gerar credenciais locais separadas sem mudar chaves OIDC |
| `scripts/verificar_mysql.py` | Verificar conexão, tabelas e perfis, somente por leitura |
| `scripts/testar_config_mysql.py` | Testes isolados de geração e transações, sem banco real |
| `.demo/mysql.env` | Configuração do servidor e segredo administrativo, não versionado |
| `.demo/database.env` | Conexão da aplicação, não versionada |

O rascunho antigo `crud_usuarios/services/login.py` e sua conexão global não são
utilizados pela nova infraestrutura. Não execute aquele CRUD: ele contém SQL
incompleto. Na próxima etapa, suas operações serão reescritas com parâmetros,
validação e a conexão de `config/database.py`.

## 2. Criar o banco pelo Docker

Abra Docker Desktop e execute na raiz do projeto, uma linha por vez:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1
```

Depois de a preparação concluir:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
docker compose ps
docker compose exec -T portal python scripts/verificar_mysql.py
```

Resultado esperado: `mysql`, `keycloak` e `portal` saudáveis; verificação confirma
sete tabelas e os três perfis. Nenhum aluno nem administrador escolar recebe
registro ou privilégios automaticamente. Zezinho continua sendo a conta do
Keycloak; seu vínculo escolar será cadastrado na integração futura.

O banco nasce automaticamente quando o MySQL inicia com o volume vazio. Os
scripts em `/docker-entrypoint-initdb.d` não são reaplicados em volumes existentes.
Não apague um volume para aplicar uma alteração de estrutura: mudanças futuras
precisarão de migrações versionadas. O SQL não usa DROP nem apaga dados existentes.

## 3. Conectar no MySQL Workbench

Instale/abra MySQL Workbench no computador. Não é preciso instalar um segundo
MySQL Server: o servidor já estará no Docker. Crie uma conexão com:

| Campo | Valor |
|---|---|
| Connection Name | UNIFICA local |
| Connection Method | Standard (TCP/IP) |
| Hostname | 127.0.0.1 |
| Port | 3307 |
| Username | unifica_app |
| Default Schema | UNIFICA |
| Password | Valor de UNIFICA_MYSQL_PASSWORD em .demo/database.env, consultado somente no seu computador |

Não publique nem envie esse arquivo. Essa credencial é do banco e não é a senha
de Zezinho. Não use `root` na conexão cotidiana da aplicação.
Clique em Test Connection, abra a conexão e atualize a lista SCHEMAS.

Execute estas consultas de leitura no editor SQL:

```sql
USE UNIFICA;
SHOW TABLES;
SELECT perfil_id, nome FROM perfis ORDER BY perfil_id;
SELECT COUNT(*) AS usuarios_cadastrados FROM usuarios;
```

Inicialmente há sete tabelas, três perfis e nenhum usuário escolar.
Para inspecionar a estrutura: `SHOW CREATE TABLE matriculas;`.
O usuário `unifica_app` tem SELECT, INSERT, UPDATE e DELETE em UNIFICA, mas não
CREATE, ALTER ou DROP. Mudanças de esquema são trabalho administrativo.
Caso precise administrar no servidor, use `docker compose exec mysql mysql -u root -p`
e forneça o segredo administrativo local no prompt; não o coloque no comando.

## 4. Tabelas criadas

| Tabela | Finalidade |
|---|---|
| usuarios | Cadastro, identidade OIDC opcional e dados de perfil; sem senha |
| escolas | Escola e localização |
| turmas | Turma, escola e ano letivo |
| matriculas | Relação entre aluno e turma e situação da matrícula |
| perfis | Catálogo aluno/professor/administrador |
| usuario_perfis | Relação N:N entre usuários e perfis |
| preferencias | Tema e fonte por usuário |

IDs principais são BIGINT UNSIGNED; perfil_id é SMALLINT UNSIGNED. Textos usam
utf8mb4; identidade OIDC tem comparação binária. DATETIME usa a convenção UTC.
Chaves estrangeiras preservam a integridade e usam RESTRICT para impedir apagar
registros referenciados. UNIQUE evita matrículas repetidas e identidades duplicadas.
CHECK restringe status, tema, fonte e flags. O vínculo OIDC exige issuer/sub
ambos nulos ou ambos preenchidos; e-mail não identifica automaticamente uma conta.

Ainda cabe ao futuro backend validar perfis para matrícula, datas de nascimento,
UF, quem pode alterar cada campo e quais registros cada usuário pode consultar.
As tabelas de perfis, sozinhas, não implementam autorização. O portal continua
atribuindo seu nível atual até essa integração ser desenvolvida.

## 5. Rede e persistência

Workbench no Windows usa `127.0.0.1:3307`. Python dentro do portal usa
`mysql:3306`, não localhost. O portal compartilha a rede do Keycloak, que está
na rede padrão do Compose junto ao MySQL. O nome `mysql` é resolvido nessa rede.

Credenciais novas do banco são independentes do Keycloak. Repetir preparar
preserva ambos os arquivos MySQL e todas as chaves OIDC. Configuração parcial
gera erro em vez de sobrescrever segredos. Não apague `.demo` nem altere um
segredo isoladamente: mudar um arquivo não redefine senhas no volume existente.

Use `parar.ps1` para parar os três serviços sem apagar dados. Nunca use
`docker compose down -v` como parada comum. Outra máquina recebe um banco novo,
não uma cópia dos dados deste computador. Backup/migração de dados é etapa separada.

## 6. Diagnóstico

```powershell
docker compose logs --tail 100 mysql
docker compose exec -T portal python scripts/verificar_mysql.py
docker compose exec -T portal python scripts/testar_config_mysql.py
```

- Porta 3307 ocupada: identifique o serviço conflitante; não pare processos desconhecidos.
- Access denied: confira credencial local e se o volume é de uma instalação antiga.
- Tabelas ausentes: consulte o log de inicialização; não remova o volume para tentar novamente.
- Conexão pelo Workbench falha: confira porta 3307, serviço saudável e Test Connection.
- MySQL demora: inicialização pode levar minutos; os scripts aguardam saúde, com limite global de 360 segundos.

## 7. Offline e validação

Reexporte o pacote offline depois da preparação atual: agora ele precisa conter
portal, Keycloak e MySQL. Pacotes antigos com apenas duas imagens não bastam.
Inclua `crud_usuarios/database/init` ao copiar o código. Continue usando uma arquitetura compatível.

O servidor e a execução real do SQL precisam ser validados com Docker. Testes
de configuração e análise estática não substituem `verificar_mysql.py` no banco
rodando. A pendência independente de testes da troca de senha continua separada
da implantação deste esquema.

Validação desta entrega: quatro testes isolados passaram (geração/preservação,
recusa de configuração parcial, commit e rollback com fechamento). Compose e
sintaxe PowerShell/Python foram conferidos; o Connector/Python foi importado.
Um analisador MySQL reconheceu as sete definições de tabelas; GRANT/REVOKE não
foram validados por esse analisador. Não foi possível iniciar Docker nesta sessão,
portanto criação no servidor, permissões efetivas e acesso pelo Workbench ainda
precisam ser confirmados após executar os comandos da seção 2.

Referências:
- https://hub.docker.com/_/mysql
- https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html
- https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
