# UNIFICA | Portal escolar com login único

O **UNIFICA** é um projeto de TCC que reúne perfil, notas e frequência, calendário, comunicados e configurações em um portal escolar. O Flask serve as páginas, o Keycloak autentica os usuários via OpenID Connect e o MySQL guarda o esquema acadêmico. O boletim atual usa dados de demonstração.

## Instalação local no Windows

### 1. Prepare o computador

- Instale e abra o [Docker Desktop](https://www.docker.com/products/docker-desktop/) com contêineres Linux.
- Instale o [Git](https://git-scm.com/download/win) para clonar pelo terminal. Se preferir, baixe o projeto no GitHub em **Code → Download ZIP** e extraia a pasta.
- Use internet na primeira preparação para baixar as imagens e as dependências. O Python, o Keycloak e o servidor MySQL são executados em contêineres. O MySQL Workbench é opcional.

Abra o PowerShell no VS Code ou no Windows. Confira se o Docker está pronto:

```powershell
docker info --format '{{.OSType}}'
docker compose version
```

O primeiro comando deve mostrar `linux` e o segundo, a versão do Compose. Se o motor não responder, abra o Docker Desktop e aguarde a inicialização.

### 2. Baixe e abra o projeto

Na pasta em que deseja guardar o projeto, execute:

```powershell
git clone https://github.com/kaua-devbr/SSO.git
Set-Location .\SSO
```

Se baixou o ZIP, abra a pasta extraída que contém o `compose.yaml` no VS Code e use o terminal dessa pasta. Nos passos seguintes, execute cada etapa após a anterior terminar com sucesso.

### 3. Prepare as imagens e a configuração

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1
```

O script constrói a imagem do portal, baixa as imagens do Keycloak e do MySQL e gera a configuração local em `.demo/`. Aguarde a mensagem **Preparado**. A opção `-ExecutionPolicy Bypass` vale para o processo iniciado por esse comando.

### 4. Inicie o UNIFICA

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
docker compose ps
```

O script aguarda as verificações de saúde dos serviços. Na lista do Compose, confirme que `mysql`, `keycloak` e `portal` estão em execução e saudáveis.

### 5. Abra o portal e entre

1. Abra [http://localhost:5000](http://localhost:5000). O portal encaminha o login para o Keycloak em [http://localhost:8081](http://localhost:8081).
2. Consulte `.demo/acessos.txt` no seu computador para encontrar a conta de demonstração `zezinho` e sua senha inicial. Se já alterou a senha no Keycloak, use a senha nova.
3. Após entrar, abra **Notas e Frequência** ou outra página pelo menu lateral.

### 6. Confira se a instalação funcionou

```powershell
Invoke-RestMethod http://localhost:5000/healthz
docker compose exec -T portal python scripts/verificar.py
docker compose exec -T portal python scripts/verificar_mysql.py
```

O primeiro comando deve retornar o status `ok`. O segundo roda os testes do portal com o fluxo OIDC simulado. O terceiro faz consultas de leitura no MySQL para conferir a conexão, as sete tabelas e os perfis iniciais.

### 7. Pare e volte a usar

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\parar.ps1
```

Esse comando preserva os volumes e a configuração local. No próximo uso, abra o Docker Desktop e repita o **passo 4**. Depois de atualizar os arquivos do projeto, repita os **passos 3 e 4** para que a imagem incorpore as mudanças.

## Linux e macOS

Com Git, Bash e Docker com Compose instalados, verifique se o motor responde e usa contêineres Linux. Depois, execute:

```bash
git clone https://github.com/kaua-devbr/SSO.git
cd SSO
bash scripts/docker.sh preparar
bash scripts/docker.sh iniciar
docker compose ps
```

Abra [http://localhost:5000](http://localhost:5000) e siga os passos de login e verificação acima. No lugar de `Invoke-RestMethod`, use `curl http://localhost:5000/healthz`. Para parar, execute `bash scripts/docker.sh parar`.

## Se a instalação travar

| Sintoma | O que conferir |
| --- | --- |
| O terminal não encontra o Docker ou o motor não responde | Abra o Docker Desktop, aguarde e repita os comandos do passo 1. |
| Uma porta está ocupada | Verifique se outro serviço está usando as portas locais 5000, 8081 ou 3307. |
| MySQL está `unhealthy` ou o portal não iniciou | Rode `docker compose ps` e `docker compose logs --tail 100 mysql keycloak portal`. O portal aguarda o banco e o Keycloak. O SQL inicial é executado quando o MySQL inicializa um volume novo. Para um volume existente, consulte o [guia do MySQL](docs/MYSQL.md) antes de qualquer intervenção. |
| O Workbench não conecta | Use `127.0.0.1` na porta `3307` para acessar o MySQL deste projeto. |
| O Windows bloqueou o script `.ps1` | Use o comando completo do README com `powershell.exe -ExecutionPolicy Bypass -File`. |

O ambiente usa HTTP local. Mantenha `.demo/`, arquivos de ambiente e credenciais fora do GitHub.

## Documentação

- [Manual de execução](docs/EXECUCAO.md)
- [Apresentação e instalação offline](docs/APRESENTACAO.md)
- [MySQL e Workbench](docs/MYSQL.md)
- [Arquitetura e autenticação](docs/architecture.md) · [Fluxo SSO](docs/sso-flow.md)
- [Testes](docs/tests.md)
