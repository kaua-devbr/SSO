# UNIFICA — manual de execução e organização

> A demonstração usa Flask, Keycloak e MySQL. Consulte o [README](../README.md) para o início rápido e o [guia do banco](MYSQL.md) para o esquema e o Workbench.

Este é o guia principal da versão Docker. O portal Flask apresenta as páginas
escolares; o Keycloak autentica as pessoas pelo OpenID Connect (OIDC).
Há um único login ativo: o do Keycloak. A Biblioteca foi retirada do pacote.

## 1. O que precisa existir no computador

- Projeto completo, baixado como ZIP e extraído ou clonado do GitHub.
- Docker funcionando com contêineres Linux e Compose com suporte a `--wait`.
- No Windows, Docker Desktop iniciado, com virtualização/backend configurados.
- Internet na primeira preparação, salvo se houver um pacote offline previamente exportado.
- Portas locais 5000 e 8081 disponíveis.

Não é necessário instalar Python, pip, Java ou MySQL no computador para esta
demonstração. Os scripts não instalam o Docker nem configuram a virtualização.
O destino precisa ser um computador compatível com as imagens Docker; isso não
inclui executar diretamente em um celular. O pacote local não publica um site na internet.

## 2. Primeira execução no Windows

### 2.1 Baixar e abrir a pasta correta

No GitHub, baixe o ZIP e extraia tudo, ou use `git clone URL-DO-REPOSITORIO`.
Não execute dentro do ZIP. A pasta correta contém `compose.yaml`, `Dockerfile`,
`app.py` e `scripts`. Abra o PowerShell nessa pasta.

No computador original:

```powershell
Set-Location -LiteralPath 'C:\Users\Kaua Alexandre\Documents\SSO'
Get-ChildItem
```

Em outra máquina, substitua o caminho pelo local onde extraiu o projeto. Não é
necessário manter o nome do usuário nem esse caminho absoluto.

### 2.2 Preparar

Abra Docker Desktop e aguarde o motor ficar pronto. Encerre um Flask antigo
iniciado fora do Docker, se ele estiver ocupando a porta 5000.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1
```

O script verifica Docker/Compose, constrói `unifica-portal:demo`, baixa a imagem
do Keycloak e executa o gerador de configuração dentro de um contêiner temporário.
Esse gerador cria `.demo` com as chaves, o realm e as credenciais iniciais.
Repetir a preparação preserva as chaves existentes. `Bypass` afeta somente esse
processo PowerShell; não altera permanentemente a política do Windows.

### 2.3 Iniciar

Somente depois de a preparação terminar com sucesso:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
```

O Compose inicia o Keycloak, espera seu realm responder e inicia o portal.
O script aguarda os dois serviços ficarem saudáveis e abre o navegador.
O terminal pode ser fechado: os serviços continuam no Docker.

### 2.4 Entrar

Abra **http://localhost:5000**. O portal encaminha diretamente para a página do
Keycloak. Entre com `zezinho` e a senha de demonstracao `1234`. Consulte tambem as credenciais administrativas localmente:

```powershell
Get-Content .\.demo\acessos.txt
```

Esse arquivo também contém o administrador do Keycloak, que é uma conta separada.
Não copie seu conteúdo para GitHub, capturas de tela ou grupos.
Se a senha foi alterada no Keycloak, use a nova: `acessos.txt` registra a senha
inicial e não é atualizado automaticamente pelo Keycloak.

Após autenticar, o navegador volta para `/auth/callback` e depois para `/perfil`.
Se o Keycloak já reconhece sua sessão, ele pode retornar sem mostrar o formulário.

## 3. Uso diário, parada e atualização

Após reiniciar o computador, abra Docker Desktop e execute `iniciar.ps1` novamente.
Não precisa repetir a preparação em cada uso. Não execute `python app.py` para
usar a versão Docker: esse comando chama o Python do Windows, fora da imagem,
e pode falhar por dependências/variáveis ausentes ou disputar a porta 5000.

Para parar preservando dados:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\parar.ps1
```

Após modificar Python, HTML, CSS ou scripts, execute novamente `preparar.ps1` e
`iniciar.ps1`. O código é copiado para a imagem durante o build; não há montagem
do código com atualização automática. `docker compose restart` sozinho não
incorpora arquivos modificados no computador.

Para evitar abrir automaticamente o navegador:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1 -SemNavegador
```

## 4. O que o Docker está fazendo

### 4.1 Imagem, contêiner, Compose e volume

**Imagem** é o pacote com programa e dependências. **Contêiner** é a execução
desse pacote. **Compose** descreve e inicia os dois serviços juntos.
**Volume** conserva dados fora da vida útil de um contêiner.

| Componente | Função no UNIFICA |
|---|---|
| `Dockerfile` | Parte de Python 3.12 slim, instala `requirements-lock.txt`, copia o código e inicia Waitress como usuário sem privilégios administrativos |
| `unifica-portal:demo` | Imagem construída localmente para o portal |
| `portal` | Serviço Flask servido pelo Waitress na porta interna 8000 |
| `keycloak` | Imagem `quay.io/keycloak/keycloak:26.8.2`, iniciada com `start-dev --import-realm` |
| `compose.yaml` | Rede, portas, dependência de inicialização, sondas e volume |
| `keycloak_data` | Volume nomeado com os dados locais do Keycloak; neste projeto normalmente aparece como `unifica-demo_keycloak_data` |
| `.demo` | Arquivos no computador com configuração e credenciais; não é o banco ativo do Keycloak |

O banco local do Keycloak fica no volume. Não existe serviço MySQL neste Compose.
O CRUD MySQL é um módulo separado e ainda não está integrado a esse fluxo.
`/healthz` verifica a resposta do portal sem iniciar autenticação; não comprova
sozinho que o login está funcionando. A sonda do Keycloak verifica seu discovery OIDC.

### 4.2 Rede compartilhada entre os dois contêineres

O portal usa `network_mode: service:keycloak`. Eles compartilham o espaço de
rede, mas continuam sendo processos e sistemas de arquivos separados.
Isso não significa compartilhar a rede inteira do computador.

O Keycloak escuta em 8081 e o Waitress em 8000. Por isso as duas publicações de
porta estão declaradas no serviço Keycloak: 8081 → 8081 e 5000 → 8000.
Somente `127.0.0.1` do computador é publicado, para acesso local.

Essa escolha permite que `http://localhost:8081` alcance o mesmo Keycloak tanto
no navegador quanto no Flask dentro do contêiner. Em contêineres com redes
separadas, `localhost` normalmente apontaria apenas para o próprio contêiner.
O endereço do emissor OIDC precisa ser consistente: não basta trocar o hostname
do Keycloak por um nome interno somente em uma parte da autenticação.

## 5. Por que os endereços mudam

### 5.1 HTTP, HTTPS, portas e caminhos

Os endereços locais atuais usam **HTTP**, não HTTPS. HTTPS acrescenta criptografia
TLS e exige uma configuração de certificados. Docker não transforma HTTP em
HTTPS automaticamente. Nesta demonstração, os serviços estão restritos ao
próprio computador; para publicar, será necessária uma configuração de produção.

Em `http://localhost:8081/realms/unifica-demo`, `http` é o protocolo,
`localhost` identifica o próprio computador, `8081` é a porta e o restante é
o caminho do realm, um espaço de contas e configurações do Keycloak.

| Endereço/caminho | Quem atende | Para que serve |
|---|---|---|
| `http://localhost:5000/` | Portal | Entrada, redireciona para login ou perfil |
| `http://localhost:5000/auth/login` | Portal | Inicia a solicitação OIDC |
| `http://localhost:8081/realms/unifica-demo/protocol/openid-connect/auth` | Keycloak | Endpoint de autorização, que apresenta ou recupera o login |
| Caminhos `/login-actions/...` em 8081 | Keycloak | Etapas internas do formulário; não devem ser salvos como link de entrada |
| `http://localhost:5000/auth/callback` | Portal | Recebe o código temporário e conclui a autenticação |
| `http://localhost:5000/perfil` | Portal | Página após o login |
| `http://localhost:8081/realms/unifica-demo/account/` | Keycloak | Gerenciamento da conta e senha |
| `http://localhost:8081/admin/` | Keycloak | Administração de realms, usuários e clientes |
| `http://localhost:5000/healthz` | Portal | Sonda técnica sem dados pessoais |

As URLs de login incluem parâmetros como `client_id`, `redirect_uri`, `scope`,
`state`, `nonce` e `code_challenge`. Eles identificam o portal, indicam o retorno
autorizado e protegem a transação. Não são uma senha que o aluno deve memorizar.
O código recebido no callback é temporário e é trocado pelo Flask por tokens.
Use a raiz do portal como favorito, não uma URL temporária copiada do login.

Sempre use `localhost` nesta configuração. Embora `127.0.0.1` também aponte
para a máquina, trocar os nomes no navegador pode alterar cookies e conflitar
com os retornos exatos registrados. Não mude apenas a porta: Compose,
`PUBLIC_URL`, `OIDC_ISSUER` e URIs do cliente precisam permanecer coerentes.

### 5.2 Por que o visual do login é diferente

A tela de autenticação é renderizada pelo Keycloak, fora de `templates` do Flask.
O portal renderiza as páginas escolares. Editar o CSS do portal não modifica
automaticamente o tema do Keycloak. Um tema personalizado no Keycloak é uma
etapa futura; não precisamos reintroduzir um formulário local para personalizá-lo.

## 6. Uma única autenticação

O formulário local com usuários em memória foi desativado e seu código removido
das rotas. A página intermediária com botão também saiu do fluxo. Os layouts
antigos estão preservados em `docs/historico/login` para consulta, sem serem
servidos pelo Flask. A antiga variável `DEMO_LOGIN_ENABLED` não habilita mais login local.

1. O usuário abre `/`; sem sessão Keycloak reconhecida pelo portal, vai para `/auth/login`.
2. Authlib gera a solicitação com state, nonce e PKCE S256.
3. O Keycloak valida a senha ou reconhece sua sessão já existente.
4. O callback valida a resposta OIDC e grava a identidade na sessão Flask.
5. O portal permite acessar páginas protegidas.
6. **Alterar senha** chama `/auth/alterar-senha` e solicita `UPDATE_PASSWORD` ao Keycloak. O link de gerenciamento de conta usa `/auth/conta`.
7. Sair exige POST com token de formulário, limpa a sessão local e encaminha
   ao logout do Keycloak. Pode haver confirmação antes de retornar ao portal.

O Flask usa cookie de sessão assinado, com HttpOnly e SameSite=Lax. Assinatura
impede adulteração, mas não criptografa seu conteúdo. Access/refresh/ID tokens
não são armazenados nesse cookie. O servidor verifica state, nonce, assinatura,
emissor, destinatário e expiração durante o login.

“Lembrar de mim” pertence ao Keycloak. A configuração inicial prevê sessão
persistente com limite de inatividade de 7 dias e duração máxima de 30 dias;
isso não é login eterno. Cookies apagados, navegação privada, expiração ou
logout podem exigir nova senha. F5 e fechar apenas a guia normalmente mantêm
a sessão mesmo sem marcar a opção. O preenchimento automático de senha pelo
navegador é outro recurso, independente da sessão.

Uma sessão Flask já criada não é revalidada no Keycloak a cada página. Revogação
imediata entre sistemas, backchannel logout e mapeamento de perfis ainda não
estão implementados. Há apenas um aplicativo cliente neste pacote; demonstrar
SSO entre dois sistemas exigirá integrar outro cliente ao mesmo realm.

## 7. Pastas e arquivos: mapa do projeto

| Pasta/arquivo | Responsabilidade e situação |
|---|---|
| `app.py` | Monta Flask, aplica configurações e registra os blueprints; Waitress importa `app:app` |
| `auth/` | `auth.py`: login, callback, logout e conta; `decorators.py`: proteção de rotas e POST com token de formulário |
| `config/` | `settings.py`: variáveis e cookies; `oidc.py`: cliente Authlib e discovery OIDC |
| `portal/` | `routes.py`: páginas, calendário, comunicados, aparência e entrada do portal |
| `templates/` | HTML Jinja ativo: base, dashboard, perfil, notas, calendário, comunicados, configurações e erro |
| `static/css/` | Estilos global, perfil e erro |
| `static/img/` | Logo e ícones existentes; nomes preservados |
| `scripts/` | Preparação, execução, parada, exportação offline, gerador e testes |
| `crud_usuarios/` | Estrutura reservada ao CRUD MySQL; não é autenticação e não entra na imagem atual |
| `keycloak/realm-school.json` | Arquivo legado/reservado; não é a origem do realm usado pelo Compose atual |
| `deploy/` | Diretório reservado, atualmente sem arquivos; não é usado pelo Compose local |
| `docs/` | Guias e documentação técnica; livro/PDF antigos preservados como material histórico |
| `docs/historico/login/` | HTML/CSS das telas de login retiradas do fluxo |
| `.demo/` | Gerado localmente; contém segredos e importação inicial, ignorado pelo Git |
| `offline/` | Gerado somente na exportação: imagens e manifesto; ignorado pelo Git |
| `__pycache__/` | Cache automático do Python; não é código-fonte, ignorado pelo Git |
| `__init__.py` | Marca pacotes Python; os arquivos vazios não representam funcionalidades adicionais |
| `requirements.txt` | Dependências declaradas para consulta/desenvolvimento |
| `requirements-lock.txt` | Versões usadas para construir a imagem |
| `.env.example` | Modelo sem segredos para execução manual/hospedagem; não precisa preencher no fluxo Docker |
| `.gitignore` | Evita versionar segredos, caches e pacotes locais |
| `.dockerignore` | Evita incluir segredos e arquivos desnecessários no contexto da imagem |

Pastas vazias não são transportadas pelo Git. Isso não prejudica a execução:
nenhum serviço depende de `deploy/` existir vazio. As pastas usadas são copiadas
pelo Dockerfile; não mova `templates` ou `static` sem ajustar essa configuração.

### 7.1 O papel dos scripts

| Script | O que executa |
|---|---|
| `docker-comum.ps1` | Localiza Docker, confere motor Linux e Compose; suporte dos outros scripts |
| `preparar.ps1` | Build/pull ou importação offline, geração local e validação do Compose |
| `configurar_demo.py` | Gera realm, cliente, aluno e chaves; preserva configurações já existentes |
| `ajustar_usuario_demo.py` | Migração explícita da conta local para zezinho/1234; altera a senha no Keycloak ativo e os registros locais, não roda automaticamente ao iniciar |
| `iniciar.ps1` | `compose up` em segundo plano, aguarda saúde e abre o portal |
| `parar.ps1` | `compose stop`, sem excluir dados |
| `exportar-offline.ps1` | Salva imagens em TAR e registra hash SHA-256 e arquitetura |
| `docker.sh` | Oferece os mesmos comandos principais no Linux/macOS |
| `verificar.py` | Testes isolados com provedor simulado e tokens assinados; não acessa MySQL |

## 8. Funcionalidades reais e dados de demonstração

O perfil usa a identidade recebida do Keycloak. Calendário e comunicados usam
dados de demonstração definidos no Python. O calendário permite selecionar dias
e meses; comunicados têm busca, filtro e marcação de leitura. Preferências de
aparência e leitura ficam na sessão e podem ser perdidas ao sair; não são um
registro permanente no MySQL. As páginas de notas/dashboard não representam
uma integração com um sistema acadêmico real.

As contas e senhas pertencem ao Keycloak e persistem no volume. O portal atribui
`nivel=normal` após OIDC; autorização administrativa por papéis é trabalho futuro.

## 9. Transferência pelo GitHub e proteção dos dados

Antes de publicar:

```powershell
git status
git remote -v
git add .
git diff --cached --name-only
```

Confira que arquivos com segredos (`.demo`, `.env`) não aparecem. O `.gitignore`
não deixa de rastrear um segredo que já tenha sido commitado anteriormente.
Depois de revisar os arquivos e confirmar o remoto correto:

```powershell
git commit -m "Documenta execucao Docker e unifica login no Keycloak"
git push
```

Commit salva localmente; push envia ao GitHub. Outra pessoa precisa baixar a
versão publicada e preparar sua própria instalação. Cada maquina gera suas chaves internas e a conta de demonstracao zezinho/1234: não recebe automaticamente seus usuários, alterações de senha,
cookies nem o volume Docker. Código portátil não é backup do banco.

Não apague `.demo` em uma instalação já usada: gerar um novo segredo sem mudar
o cliente existente pode quebrar o login. Importação de realm na inicialização
não sobrescreve um realm que já existe. Editar o JSON não muda automaticamente
as contas ativas; use o painel do Keycloak para alterações no ambiente existente.

## 10. Linux, macOS e execução offline

Com Docker e Compose disponíveis:

```bash
bash scripts/docker.sh preparar
bash scripts/docker.sh iniciar
bash scripts/docker.sh parar
```

Para preparar a apresentação sem internet, em uma máquina com imagens prontas:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\exportar-offline.ps1
```

Copie o código e `offline/`, sem `.demo`, `.env` ou `.git`. No destino compatível:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1 -Offline
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
```

O destino ainda precisa do Docker funcionando. O pacote é validado por hash e
arquitetura; um pacote amd64 não é considerado intercambiável com arm64 pelo
script. No Bash, use `exportar-offline` e `preparar --offline`. O TAR é grande,
não está no GitHub e só existe depois da exportação. Teste sem internet antes
da apresentação. Novas credenciais estarão no `.demo/acessos.txt` do destino.

## 11. Diagnóstico e testes

```powershell
docker --version
docker info
docker compose version
docker compose ps
docker compose logs --tail 100 portal
docker compose logs --tail 100 keycloak
docker compose logs --tail 100 mysql
docker compose config --quiet
docker compose exec -T portal python scripts/verificar.py
docker compose exec -T portal python scripts/verificar_mysql.py
```

Os primeiros comandos conferem ferramentas e serviços; `logs` ajuda a localizar
erros; `config --quiet` valida sem exibir configurações resolvidas com segredos.
Os testes rodam isoladamente no processo Python de teste e não mudam o banco.

| Sintoma | Como agir |
|---|---|
| Script não existe | Conferir pasta extraída e `Get-ChildItem .\scripts`; usar caminho absoluto entre aspas |
| `No module named dotenv` ao rodar Python no Windows | Usar `iniciar.ps1`; dependências estão na imagem |
| Docker não encontrado | Abrir Desktop e novo terminal; conferir instalação e PATH |
| Motor indisponível | Esperar Desktop iniciar e conferir o backend/virtualização |
| Porta ocupada | Encerrar o servidor antigo; não iniciar Flask manual e Docker juntos |
| Página antiga após editar HTML | Reconstruir com `preparar.ps1`, depois `iniciar.ps1` |
| `invalid_client` | Conferir segredo/cliente de `.demo` e realm ativo sem expor valores |
| Retorno inválido | Conferir `http://localhost:5000/auth/callback` no cliente |
| Erro 503 no login | Consultar logs e saúde do Keycloak |
| Senha inicial não funciona após alteração | Usar a senha atual do Keycloak; o TXT não é sincronizado |

Teste manual: entrar, visitar todas as páginas, alterar aparência, filtrar e marcar
comunicados, selecionar datas, abrir a conta do Keycloak, sair confirmando a saída,
testar Remember Me e reiniciar serviços sem perder contas. Em seguida faça uma
instalação limpa em outro computador. `Healthy` não substitui esses testes.

Não use `docker compose down -v` para uma parada comum: `-v` remove os volumes
e pode apagar as contas locais. O comando de parada fornecido preserva os dados.

## 12. Publicação futura com HTTPS

Será necessário um servidor/provedor acessível, domínio, certificados, proxy
HTTPS, Keycloak em modo produção e banco persistente apropriado. Configurar
`PUBLIC_URL` para o portal HTTPS, `OIDC_ISSUER` para o realm HTTPS,
`SESSION_COOKIE_SECURE=true` e os retornos exatos do cliente. A rede compartilhada
do Compose local não deve ser copiada sem planejamento para essa arquitetura.

Esta entrega não criou hospedagem, domínio ou HTTPS. O Compose usa `start-dev`
e acesso local. O objetivo atual é instalação reproduzível para desenvolvimento
e apresentação; produção exige decisões adicionais de segurança e operação.
