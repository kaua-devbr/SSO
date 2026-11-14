# UNIFICA: demonstracao local e acesso pela internet

## O que este pacote entrega

Portal Flask na porta 5000, segunda aplicacao Biblioteca na 5001 e Keycloak
isolado na 8081, com realm unifica-demo. O login oficial agora usa OIDC.
O ambiente existente na porta 8080 nao e apagado ou reutilizado.
As contas zezinho/maria ficam disponiveis somente se DEMO_LOGIN_ENABLED=true.
O pacote local nao conecta ao MySQL: os dados escolares sao demonstrativos.
O CRUD existente continua incompleto e nao faz parte desta demonstracao SSO.

## Preparar antes da apresentacao, com internet

1. Usar Windows 10/11 de 64 bits, Python 3.12 de 64 bits no PATH e Docker Desktop
   instalado, iniciado e usando conteineres Linux. Verificar os requisitos do
   Docker no notebook, inclusive virtualizacao e permissao de instalacao.
2. No terminal PowerShell, entrar na pasta SSO.
3. Executar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
```

A opcao Bypass vale apenas para esse processo; nao altera a politica global.
O script cria .venv e .demo. As senhas sao aleatorias e ficam em
.demo/acessos.txt. O app.env preserva as chaves entre reinicializacoes.
Nao publique nem envie .demo, .env ou arquivos de logs. Nao use dados reais.
O arquivo explicitamente selecionado por UNIFICA_ENV_FILE tem prioridade sobre
variaveis antigas do Windows. Fora da demo, variaveis do sistema prevalecem
sobre .env. Isso evita reutilizar por engano o client antigo na porta 8080.

requirements.txt lista as dependencias diretas. requirements-lock.txt fixa tambem
as dependencias transitivas usadas nos testes; os scripts e a imagem usam o lock.

O script iniciar abre o navegador e executa Waitress em processos de fundo;
os erros ficam em .demo/portal-error.log e .demo/biblioteca-error.log.
Abra http://localhost:5000 e entre com aluno.teste e a senha em acessos.txt.

## Preparar o pendrive para funcionar sem internet

Na maquina de preparacao, com tudo instalado, execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\exportar-offline.ps1
```

O script exporta a imagem Keycloak para offline/keycloak.tar e baixa os pacotes
Python em offline/wheels. Registra versao e arquitetura em offline/ambiente.txt
e hashes em offline/SHA256.txt. Os pacotes sao especificos para esse Python e
sistema operacional: use a mesma versao principal/secundaria e arquitetura no
notebook. Use uma pasta offline nova se mudar o ambiente de preparacao.

Copie o projeto inteiro e offline, mas exclua .git, .venv, .validation-deps e
.demo. Copie tambem os instaladores oficiais do Python e Docker apropriados ao
notebook; eles NAO sao incluidos ou instalados pelos scripts. Docker Desktop e
seu backend devem ser instalados e testados antes: o pacote nao resolve WSL,
virtualizacao, reinicializacoes ou politicas institucionais automaticamente.

No notebook, com Python e Docker ja prontos:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1 -Offline
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
```

O modo Offline usa pip --no-index e docker load. A inicializacao usa --pull never.
Assim, nenhum download de dependencia e necessario durante a demonstracao.
Uma nova maquina recebe suas proprias chaves e contas. Para repetir a execucao
na mesma maquina, preserve .demo e o volume Docker.

## Roteiro para a banca

1. Abra http://localhost:5000 e clique em Entrar com a conta escolar.
2. Confira que a tela de senha esta em localhost:8081. Entre como aluno.teste.
3. Abra Inicio e clique em Abrir biblioteca escolar, ou abra localhost:5001.
4. Clique em Entrar com a conta escolar na biblioteca. O Keycloak deve reconhecer
   a sessao e autenticar sem repetir a senha. Cada app tem client, chave e cookie
   diferentes: nao e uma simples reutilizacao do cookie do Flask.
5. Abra Configuracoes no portal e Gerenciar conta para demonstrar a central de conta.
6. Para testar persistencia, marque Remember Me na tela do Keycloak ao autenticar,
   feche o navegador e reabra /perfil. O cookie local OIDC e de sessao; o Keycloak
   pode recuperar a identidade com uma nova ida e volta, respeitando seus limites.
7. Saia pelo botao e confirme a saida no Keycloak se solicitado.

Lembrar de mim: idle de sete dias e limite maximo de trinta dias no realm demo.
Sem lembrar: idle de trinta minutos e limite maximo de oito horas no Keycloak.
Navegadores podem restaurar cookies de sessao ou apagar cookies persistentes.
Nao use janela anonima para testar persistencia. Use sempre localhost, nao alterne
com 127.0.0.1. Mantenha o relogio do computador correto para validacao dos tokens.

## Limites honestos desta etapa

- Login SSO, conta e logout iniciado pela aplicacao foram preparados. Nao existe
  back-channel logout: sair de um app encerra a sessao central, mas o cookie local
  ja aberto no outro app pode continuar aceito ate expirar. Nao apresente isso como
  single logout completo. Remover essa limitacao requer sessoes revogaveis no
  servidor e validacao das notificacoes de logout.
- Todos os usuarios OIDC recebem nivel normal; ainda falta mapear e aplicar papeis.
- A biblioteca e um catalogo demonstrativo, nao implementa emprestimos.
- O modo start-dev e seu armazenamento dev-file sao apenas para demonstracao.
- O README e este guia descrevem o estado atual; o livro PDF anterior precede estas mudancas.

## Parar sem apagar dados

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\parar.ps1
```

Isso encerra os processos registrados e para o Keycloak. Nao execute docker compose
down -v: essa opcao apagaria o volume. Ao reiniciar o computador, abra Docker Desktop
e execute iniciar.ps1. Nao e necessario gerar novas chaves.
Importacao de realm ocorre na primeira criacao; se ele ja existe, Keycloak nao
sobrescreve as configuracoes. Alteracoes futuras devem ser feitas pelo painel,
mantendo segredos consistentes; nao apague .demo para tentar atualizar o realm.

## Diagnostico

| Sintoma | Verificacao |
|---|---|
| Docker nao encontrado | Instalar Docker Desktop e reabrir terminal |
| Docker nao responde | Abrir Docker Desktop e aguardar o motor |
| Porta ocupada | Parar servidor antigo; nao iniciar duas copias |
| Keycloak nao fica pronto | docker compose logs keycloak |
| invalid_redirect_uri | Client deve autorizar exatamente /auth/callback do seu PUBLIC_URL |
| invalid_client | Segredo do client e configuracao do Flask devem coincidir |
| Login expira ou state invalido | Comecar novamente em /auth/login, sem trocar host ou chave |
| Falha de wheel offline | Usar Python e arquitetura de offline/ambiente.txt |
| Usuario/senha invalido | Consultar acessos.txt; realm local e separado do realm antigo |

## Hospedagem com internet

O Dockerfile executa a aplicacao com Waitress na porta 8000. Ele nao embute
segredos, dados locais ou o Keycloak. A publicacao real depende de escolher um
servidor/provedor, dominio e certificados; nenhuma URL publica foi criada.

1. Hospedar Keycloak em modo de producao, com HTTPS, banco suportado persistente
   (por exemplo PostgreSQL), backups e administrador configurado. Nao publicar
   compose.yaml local nem suas contas de demonstracao como ambiente de producao.
2. Criar realm e os clients unifica-portal e unifica-biblioteca, com Standard Flow,
   autenticacao do client e PKCE S256; Direct Access Grants desativado.
3. Cadastrar redirects exatos, por exemplo https://portal.seudominio/auth/callback
   e https://biblioteca.seudominio/auth/callback, cada qual no respectivo client.
   Registrar tambem a URL raiz com barra final para retorno do logout.
4. Configurar no gerenciador de segredos/variaveis do provedor os campos de
   .env.example. OIDC_ISSUER deve ser HTTPS e acessivel pelo navegador e servidores.
   PUBLIC_URL e BIBLIOTECA_PUBLIC_URL devem conter suas URLs publicas HTTPS.
   SESSION_COOKIE_SECURE=true e DEMO_LOGIN_ENABLED=false.
5. Construir a imagem: docker build -t unifica-web .
6. Publicar dois servicos usando essa imagem. Portal usa o comando padrao.
   Biblioteca usa waitress-serve --listen=0.0.0.0:8000 biblioteca:app.
   O provedor/reverse proxy termina HTTPS e encaminha para a porta 8000.
7. Gerar chaves diferentes para portal e biblioteca e preserva-las; usar segredos
   dos clients desse ambiente. Nao copiar segredos locais para a hospedagem.
8. Validar o roteiro completo com duas aplicacoes e realizar os testes de seguranca
   e logout faltantes antes de admitir usuarios reais.

Para executar manualmente no desenvolvimento: copiar .env.example para .env,
preencher os valores e instalar requirements.txt. Depois python app.py e, em
outro terminal, python biblioteca.py. Apenas criar .env nao cria clients no Keycloak.

## Verificacoes automatizadas e ensaio ainda necessario

Depois de preparar o ambiente:

```powershell
.\.venv\Scripts\python.exe scripts/verificar.py
.\.venv\Scripts\python.exe scripts/verificar.py --biblioteca
```

Os testes usam chaves RSA e tokens assinados de teste; simulam os endpoints do
provedor. Verificam PKCE na requisicao, nonce, state, emissor, destinatario,
expiracao, paginas, arquivos estaticos, CSRF, saida e preservacao das chaves geradas.
Nao se conectam ao MySQL nem alteram configuracoes reais do Keycloak.
Na preparacao deste pacote, passaram 9 testes do portal e 9 da biblioteca, alem
da analise sintatica dos scripts PowerShell. Docker nao estava disponivel nesse
ambiente: build da imagem, importacao real do realm, retorno pelo navegador e
execucao offline em outro computador ainda devem ser ensaiados. O arquivo
offline/keycloak.tar NAO acompanha o codigo: sera criado por exportar-offline.ps1.

## Fontes oficiais

- https://www.keycloak.org/getting-started/getting-started-docker
- https://www.keycloak.org/server/importExport
- https://www.keycloak.org/server/hostname
- https://docs.authlib.org/en/latest/oauth2/client/web/flask.html
