# UNIFICA - executar com Docker

## O que mudou

A biblioteca foi removida. Existem apenas dois servicos: portal Flask (Waitress)
e Keycloak. Python, bibliotecas e servidor web ficam dentro da imagem Docker.
Nao e preciso instalar Python, pip, Java ou MySQL no computador de apresentacao.

O pacote e para execucao local em computadores compativeis com Docker usando
conteineres Linux e Docker Compose v2 com suporte a --wait. No Windows, o Docker
Desktop e seu backend WSL 2/virtualizacao precisam estar funcionando, nao apenas
instalados. No Linux pode ser usado Docker Engine com Compose. No macOS, Docker
Desktop. A disponibilidade das imagens para a arquitetura do processador deve
ser conferida na preparacao; nao se promete compatibilidade com qualquer hardware.

## Windows: primeira execucao com internet

Abra Docker Desktop e espere o motor iniciar. Pare o Flask antigo (Ctrl+C no
terminal onde foi iniciado) para liberar a porta 5000. Na pasta do projeto:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
~~~

Execute a segunda linha somente se a primeira terminar com sucesso.
Os scripts procuram docker no PATH e nos caminhos usuais do Docker Desktop.
A politica Bypass vale apenas para esse processo, sem alterar a politica global.

preparar baixa/constroi as imagens e gera chaves e contas locais pelo Python
dentro do Docker. iniciar aguarda a saude dos dois servicos e abre o navegador.
Os servicos nao dependem de manter o terminal PowerShell aberto.

- Portal: http://localhost:5000
- Keycloak: http://localhost:8081
- Credenciais locais: .demo/acessos.txt

Use aluno.teste e a senha gerada. O administrador do Keycloak e separado.
Nao envie .demo, .env ou suas senhas para GitHub ou grupos.
Os scripts nao alteram variaveis permanentes do Windows nem exigem SECRET_KEY
configurada manualmente. As configuracoes usadas pelo Compose ficam em .demo.

## Proximas vezes

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
~~~

Depois de reiniciar o computador, primeiro inicie Docker Desktop.
As chaves ficam em .demo e o banco do Keycloak no volume Docker keycloak_data.
Nao apague .demo nem o volume entre execucoes.
Para atualizar o codigo da imagem, execute preparar.ps1 com internet e iniciar.ps1.
Um docker compose restart sozinho NAO incorpora alteracoes do codigo.

## Parar

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\parar.ps1
~~~

Isso para os dois servicos sem apagar dados.
Nao use docker compose down -v se deseja preservar as contas.

## Linux e macOS

Com Docker ativo e permissao de acesso ao motor:

~~~bash
bash scripts/docker.sh preparar
bash scripts/docker.sh iniciar
# Ao terminar:
bash scripts/docker.sh parar
~~~

O script Bash cria os arquivos com o UID/GID do usuario e nao precisa de Python
no host. No Linux, configure previamente o acesso ao Docker conforme as regras
da instituicao; os scripts nao alteram permissoes do sistema.

## Sem internet / notebook da apresentacao

Na maquina de preparacao, ja testada com internet:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\exportar-offline.ps1
~~~

Isso gera offline/imagens.tar com AMBAS as imagens, mais offline/manifest.json
com SHA-256 e arquitetura. Nao sao mais necessarios wheels ou Python no destino.
Copie o projeto e offline para o notebook; exclua .git, .venv, .validation-deps,
.env e .demo. O computador novo gera suas proprias chaves e contas.
O Docker Desktop precisa estar instalado e inicializado antes da apresentacao.

No destino:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1 -Offline
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
~~~

Linux/macOS: bash scripts/docker.sh preparar --offline.
Para exportar nesses sistemas: bash scripts/docker.sh exportar-offline.
O pacote precisa corresponder a arquitetura do Docker de destino (por exemplo
amd64 ou arm64). Os scripts conferem hash e arquitetura antes de carregar.
A preparacao offline nao baixa pacotes; iniciar usa --pull never --no-build.

O arquivo imagens.tar NAO faz parte do codigo fonte: so e criado depois de
construir/baixar as imagens e executar a exportacao. Teste em outra maquina com
a internet desligada antes de considerar o pendrive pronto.

## Por que as portas ficam no servico Keycloak

No ambiente local, o portal usa network_mode: service:keycloak.
Isso compartilha o namespace de rede entre os dois conteineres, nao com o host.
O Keycloak escuta na porta 8081 e o Waitress na 8000 desse namespace.
O Compose publica 8081 e mapeia 5000 para 8000 somente no loopback do computador.

Dessa forma http://localhost:8081 significa o mesmo servico para o navegador
e para o cliente OIDC do Flask. Nao e necessario editar hosts, usar IP fixo,
host.docker.internal ou desativar validacao do emissor do token.
A configuracao e para acesso no proprio computador, nao pela rede da escola.
Se mudar portas/hosts, ajuste em conjunto Compose, PUBLIC_URL, OIDC_ISSUER e
redirect URIs no Keycloak; trocar apenas uma porta quebra a autenticacao.

## Testes de apresentacao

1. Abrir localhost:5000 e clicar Entrar com a conta escolar.
2. Conferir que a senha e solicitada em localhost:8081.
3. Entrar como aluno.teste e verificar perfil, inicio, calendario e comunicados.
4. Em Configuracoes, abrir Gerenciar conta e alterar senha.
5. Marcar Remember Me no login do Keycloak, fechar o navegador e reabrir /perfil.
   O Flask usa cookie de sessao para OIDC; ao perder esse cookie, pede novamente
   a autenticacao ao Keycloak, que pode reconhecer sua sessao persistente.
6. Sair e confirmar o logout no Keycloak se solicitado.
7. Parar e iniciar os servicos e confirmar que contas e senhas continuam iguais.

A biblioteca e seu atalho foram removidos. O portal continua integrado via OIDC,
mas agora nao existe uma segunda aplicacao neste pacote para demonstrar SSO
entre sistemas. O CRUD MySQL ainda e incompleto e nao participa desses testes.
As permissoes OIDC continuam no nivel normal; papeis por perfil sao trabalho futuro.

## Migracao da versao anterior

O gerador preserva todas as chaves e as contas existentes e remove apenas as
configuracoes da biblioteca do arquivo app.env e do JSON usado em novas importacoes.
Se o realm ja existe no volume, o Keycloak nao sobrescreve sua configuracao na
inicializacao. Um client antigo da biblioteca pode permanecer la, sem uso;
nao apagamos seu banco para remove-lo.

Se havia processos Python/Waitress iniciados pelos scripts antigos, encerre-os
antes da nova execucao; docker compose stop nao controla processos fora do Docker.

## Diagnostico

~~~powershell
docker --version
docker info
docker compose version
docker compose ps
docker compose logs --tail 100
~~~

| Problema | Acao |
|---|---|
| Docker nao encontrado | Reabrir terminal apos instalacao; scripts tambem buscam o executavel em locais comuns |
| Motor nao responde | Abrir Docker Desktop; verificar WSL 2/virtualizacao e mensagens do aplicativo |
| Windows containers | Trocar para Linux containers |
| Porta 5000/8081 ocupada | Parar servidores antigos; nao executar python app.py junto com Compose |
| Keycloak unhealthy | Consultar docker compose logs keycloak; primeira inicializacao pode demorar |
| invalid_client | Comparar configuracao do client no painel e .demo/app.env; nao gere chaves novas isoladamente |
| invalid_redirect_uri | Autorizar exatamente http://localhost:5000/auth/callback no client local |
| Pacote offline incompatível | Gerar arquivo para a mesma arquitetura do notebook |
| Falha durante build/pull | Verificar internet, proxy/firewall e disponibilidade das versoes fixadas |

Nao execute docker compose config sem --quiet em capturas ou logs compartilhados,
pois a configuracao resolvida pode mostrar os segredos de env_file.

## Hospedagem com internet

Dockerfile continua utilizavel para hospedar apenas o portal com Waitress:8000.
A publicacao depende de servidor/provedor, dominio, HTTPS e Keycloak de producao.
Nenhuma URL publica foi criada.

1. Hospedar Keycloak em modo producao com HTTPS e banco persistente suportado.
2. Criar client confidencial unifica-portal, Standard Flow e PKCE S256, sem Direct Grants.
3. Registrar https://SEU-PORTAL/auth/callback e a raiz com barra para retorno do logout.
4. Configurar as variaveis de .env.example no gerenciador de segredos do servidor.
   OIDC_ISSUER deve apontar ao Keycloak HTTPS, PUBLIC_URL ao portal HTTPS e
   SESSION_COOKIE_SECURE=true. Preservar SECRET_KEY e OIDC_CLIENT_SECRET.
5. Construir Dockerfile e publicar a porta interna 8000 atras do proxy HTTPS.

O compose.yaml local usa start-dev, dados ficticios e loopback: nao e um deploy
de producao. Nao copie as senhas locais para o ambiente publico.

## Validacao automatizada

Os testes em scripts/verificar.py usam tokens RSA assinados de teste e simulam
o provedor; nao substituem um login real pelo navegador.

~~~powershell
docker compose exec -T portal python scripts/verificar.py
~~~

Eles verificam nonce/state, emissor, destinatario, expiracao, paginas, arquivos
estaticos, logout/CSRF e geracao/migracao das chaves. Nao acessam MySQL.

## Fontes oficiais

- https://docs.docker.com/compose/how-tos/networking/
- https://docs.docker.com/compose/how-tos/startup-order/
- https://www.keycloak.org/server/importExport
- https://www.keycloak.org/getting-started/getting-started-docker
