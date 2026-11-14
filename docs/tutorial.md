# UNIFICA — instalação limpa no Windows com Docker Desktop

Este roteiro usa PowerShell, Docker Desktop com contêineres Linux e, opcionalmente,
o terminal integrado do VS Code. Execute cada etapa separadamente. Se uma
verificação falhar, resolva o problema antes de continuar.

Não é preciso instalar Python, Java, Flask, pip nem MySQL no Windows para executar
esta versão. O VS Code é um editor e terminal; ele não substitui o Docker.

## 0. Situação da versão e significado de instalação limpa

Instalação limpa significa uma máquina sem uma instalação anterior do UNIFICA,
não apagar dados de uma instalação que já funciona. Não exclua `.demo` ou volumes.

O remoto conferido no projeto é `https://github.com/kaua-devbr/SSO.git`.
Ainda existem mudanças locais não publicadas. Antes de distribuir este roteiro,
o responsável precisa revisar, commitar e enviar a versão pretendida ao GitHub.
O download não inclui alterações que existem apenas no computador do autor.

**Pendência conhecida:** a troca de senha via `UPDATE_PASSWORD` foi iniciada,
mas sua validação completa está pendente. Um teste ainda espera `/auth/conta`,
enquanto a implementação encaminha para `/auth/alterar-senha`. Portanto, não
interprete esse teste falhando como motivo para reinstalar o Docker, nem declare
a versão completamente validada até corrigir e executar a suíte.

O login e os dois contêineres saudáveis foram confirmados anteriormente pelo
usuário. Este documento não representa um teste realizado em outra máquina limpa.

## 1. Conferir o computador

Roteiro principal: Windows 11 de 64 bits em versão suportada pelo Docker Desktop,
processador com virtualização habilitada, internet e permissão para instalar programas.
Para outras versões do Windows, confira a matriz oficial antes de instalar.

- Docker Desktop lista 8 GB de RAM como requisito no Windows.
- Recomendação prática para apresentação com navegador e VS Code: 16 GB.
- Reserve, como margem de planejamento, pelo menos 15 GB livres para imagens,
  cache e ambiente Linux; não é uma medição do consumo máximo do projeto.
- AMD64/x86_64 é o caminho de referência. ARM64 exige instalador apropriado e
  verificação das imagens/dependências; esta revisão não validou uma máquina ARM64.
- As portas locais 5000 e 8081 precisam estar livres.

Abra o Gerenciador de Tarefas → Desempenho → CPU e confira “Virtualização”.
Se estiver desabilitada, será necessário habilitá-la no firmware do computador;
o procedimento depende do fabricante. Em notebook fornecido pela instituição,
combine antecipadamente as permissões e a instalação com o responsável.

Referência: https://docs.docker.com/desktop/setup/install/windows-install/

## 2. Preparar o WSL2

Se Docker Desktop já inicia e `docker info` funciona, não reinstale o WSL.
Em uma máquina sem WSL, abra PowerShell **como administrador** e execute:

```powershell
wsl --install --no-distribution
```

Isso instala o suporte WSL sem uma distribuição Ubuntu de uso pessoal; Docker
Desktop gerencia seu próprio ambiente. Não escreva `run` antes do comando.
Reinicie o Windows se solicitado. Depois execute:

```powershell
wsl --update
wsl --version
wsl --status
```

**Resultado esperado:** WSL instalado/atualizado e sem erro de recurso ou
virtualização. Se `--version` não for reconhecido, siga a atualização oficial do
WSL antes de prosseguir. Uma instalação nova pode ainda não ter distribuição
pessoal padrão; isso não exige instalar Ubuntu para este roteiro.

Referências:
- https://learn.microsoft.com/en-us/windows/wsl/basic-commands
- https://docs.docker.com/desktop/features/wsl/

## 3. Instalar Docker Desktop, Git e VS Code

Confira se o gerenciador de pacotes está disponível:

```powershell
winget --version
```

Se não estiver, instale/atualize o **Instalador de Aplicativo (App Installer)**
pela Microsoft Store ou utilize os instaladores oficiais indicados abaixo.

Execute um comando por vez e confira o resultado:

```powershell
winget install --id Docker.DockerDesktop --exact --source winget
```

```powershell
winget install --id Git.Git --exact --source winget
```

VS Code é opcional para executar, mas útil para abrir a pasta e o terminal:

```powershell
winget install --id Microsoft.VisualStudioCode --exact --source winget
```

Leia os termos e responda às solicitações dos instaladores. Uso educacional
está previsto entre as modalidades gratuitas do Docker Desktop; instituições
devem conferir as condições aplicáveis. Este guia não aceita licenças por você.

Alternativas oficiais de download:
- https://docs.docker.com/desktop/setup/install/windows-install/
- https://git-scm.com/downloads/win
- https://code.visualstudio.com/download
- https://docs.docker.com/subscription-billing/desktop-license/

Reinicie se solicitado. Feche e reabra PowerShell e VS Code para carregar o PATH.

## 4. Iniciar e verificar Docker Desktop

Abra **Docker Desktop** pelo menu Iniciar. Complete a configuração inicial e
aguarde o motor iniciar. Use o backend WSL2 e contêineres Linux. Se houver a
opção “Switch to Linux containers”, selecione-a. Não instale outro Docker Engine
dentro de Ubuntu para seguir este roteiro.

Em um PowerShell novo, execute:

```powershell
docker --version
docker compose version
docker info --format '{{.OSType}}'
git --version
```

**Resultado esperado:** versões nos três comandos de versão; `linux` no comando
`docker info`. Apenas `docker --version` funcionar não comprova que o motor iniciou.

Verifique também os recursos exigidos pelo projeto:

```powershell
docker compose up --help | Select-String -Pattern '--wait','--wait-timeout','--pull'
```

As opções devem aparecer. Caso contrário, atualize o Docker Desktop/Compose.
Não prossiga se houver erro de comunicação com o motor.

## 5. Baixar o projeto publicado

Escolha uma pasta sua. O exemplo usa Documentos, localizado pelo Windows:

```powershell
$pastaDocumentos = [Environment]::GetFolderPath('MyDocuments')
Set-Location -LiteralPath $pastaDocumentos
git clone https://github.com/kaua-devbr/SSO.git UNIFICA
```

Se a pasta `UNIFICA` já existir, não a apague. Confira se é uma instalação antiga
ou escolha outro nome. Atenção: outra pasta na mesma máquina ainda usa as mesmas
portas e o mesmo nome Compose `unifica-demo`; não representa uma instalação isolada.

Somente após clone bem-sucedido:

```powershell
Set-Location -LiteralPath (Join-Path $pastaDocumentos 'UNIFICA')
git remote -v
git rev-parse --short HEAD
```

O último comando registra a revisão baixada, útil para comparar com a revisão
testada pelo autor. Se o repositório for privado, será necessário acesso autorizado.

Alternativa sem Git: GitHub → Code → Download ZIP → Extrair tudo. Abra a pasta
interna que contém `compose.yaml`, não o ZIP nem a pasta imediatamente acima.

No VS Code, use **Arquivo → Abrir Pasta**, selecione essa pasta, depois
**Terminal → Novo Terminal** e escolha **PowerShell**. O comando `code .` também
pode abrir a pasta se o comando VS Code estiver disponível no PATH.

Confira os arquivos sem mostrar segredos:

```powershell
Get-Location
Test-Path .\compose.yaml
Test-Path .\Dockerfile
Test-Path .\requirements-lock.txt
Test-Path .\scripts\preparar.ps1
Test-Path .\scripts\iniciar.ps1
```

**Resultado esperado:** todos os `Test-Path` retornam `True`. Se algum retornar
`False`, confira a pasta ou a versão baixada antes de continuar.

## 6. Verificar as portas

```powershell
Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalPort -in 5000,8081 } |
    Select-Object LocalAddress,LocalPort,OwningProcess
```

Em instalação limpa, não deve haver listener nessas portas. Se houver, identifique
o processo pelo PID no Gerenciador de Tarefas. Encerre somente o serviço que você
reconhece e pode parar. Se for Flask iniciado manualmente, use Ctrl+C naquele terminal.
Não mate processos arbitrários nem altere só uma porta do Compose: o login depende
de URLs coerentes entre portal e Keycloak.

## 7. Preparar o UNIFICA — primeira execução

Com Docker Desktop aberto, execute na raiz do projeto:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1
```

A primeira execução precisa de internet. O script:

1. Confere motor Linux e Compose.
2. Constrói a imagem `unifica-portal:demo`, instalando Python/dependências dentro dela.
3. Baixa `quay.io/keycloak/keycloak:26.8.2`.
4. Executa o gerador de configuração dentro de um contêiner temporário.
5. Cria `.demo` com configuração local, conta inicial e segredos internos.
6. Valida o Compose sem imprimir a configuração resolvida.

`Bypass` vale para esse processo PowerShell, sem mudar permanentemente a política
do computador. Uma política institucional pode impedir a execução mesmo assim;
nesse caso, solicite ao responsável a liberação apropriada.

**Resultado esperado:** mensagem “Preparado” e saída de sucesso. Confira logo após:

```powershell
$LASTEXITCODE
Test-Path .\.demo\app.env
Test-Path .\.demo\keycloak.env
Test-Path .\.demo\import\unifica-demo-realm.json
```

Espere `0` e três `True`. Não abra nem copie os arquivos `.env` para diagnóstico.
Se falhar, não execute iniciar; consulte a seção de problemas. Não crie chaves
manualmente nem apague `.demo` para tentar corrigir uma preparação parcial.

## 8. Iniciar e confirmar a saúde

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
```

O script inicia em segundo plano e espera o Keycloak antes do portal. O limite
de espera é 360 segundos. A primeira partida pode levar alguns minutos; não
feche o terminal enquanto o comando ainda aguarda. Após concluir, o navegador abre.

```powershell
docker compose ps
(Invoke-RestMethod -Uri 'http://localhost:5000/healthz').status
```

**Resultado esperado:** serviços `portal` e `keycloak` executando e saudáveis;
`ok` no endpoint de saúde. Essa sonda não substitui o teste de autenticação.

Se o limite de espera expirar:

```powershell
docker compose logs --tail 100 keycloak
docker compose logs --tail 100 portal
```

Não apague volumes. Se os serviços estiverem apenas terminando de inicializar,
aguarde e execute iniciar novamente. Se houver erro, corrija a causa indicada.

## 9. Entrar e testar as páginas

Abra **http://localhost:5000**. Use sempre `localhost` neste ambiente, em vez de
alternar com `127.0.0.1`. O navegador irá para `localhost:8081` durante o login
e voltará ao portal. Isso é esperado: são dois serviços distintos.

Na versão atual do gerador, novas instalações criam a conta pública de demonstração
`zezinho`, com senha inicial `1234`. Se uma cópia antiga criar outro usuário,
confira a revisão baixada. Consulte `.demo/acessos.txt` somente localmente se
precisar das credenciais administrativas; não envie seu conteúdo em mensagens.

Depois de entrar:

- Abra perfil, início, notas, calendário, comunicados e configurações.
- Selecione uma data no calendário e filtre os comunicados.
- Altere tema/fonte e confira o resultado.
- Teste sair e confirme o logout no Keycloak se solicitado.
- Entre marcando Remember Me, feche o navegador sem clicar em Sair e reabra a raiz.

Senhas alteradas posteriormente não voltam automaticamente à senha inicial.
Não execute `ajustar_usuario_demo.py` como parte da instalação normal: ele é
uma migração explícita que redefine a credencial da conta de demonstração.

O cadastro de outras contas ocorre no Keycloak. O CRUD MySQL não está integrado
nesta demonstração. A troca de senha pelo botão novo precisa da validação
registrada na seção 0 antes de ser considerada concluída.

## 10. Executar a suíte e interpretar o resultado

```powershell
docker compose exec -T portal python scripts/verificar.py
```

Esse Python roda dentro do contêiner. Não execute `python app.py` no Windows.
A suíte simula o provedor para validar o código; não altera o banco Keycloak nem
o MySQL. Um resultado satisfatório termina com `OK` e código de saída zero.

**Na revisão local examinada, existe a expectativa antiga de `/auth/conta` no
teste de senha.** Até a correção, a suíte pode terminar com falha nesse caso.
Isso é pendência de código/teste, não evidência de instalação incorreta.
Não remova nem ignore o teste para declarar sucesso.

## 11. Parar, reiniciar e atualizar

Parar ao terminar:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\parar.ps1
```

Esse comando preserva contas e configurações. Não use `docker compose down -v`:
`-v` remove volumes e pode apagar as contas locais.

No próximo uso, abra Docker Desktop e execute apenas `iniciar.ps1`. O terminal
pode ser fechado depois que iniciar concluir. Desligar o computador encerra os
serviços; abrir somente o navegador não os inicia novamente.

Após modificar ou receber código novo, confira alterações locais antes de atualizar:

```powershell
git status
```

Em um clone sem alterações locais, para receber a branch atual sem criar merge:

```powershell
git pull --ff-only
```

Se o Git informar conflito/divergência, pare e resolva preservando seu trabalho.
Depois de receber a atualização, execute preparar e, se concluir com sucesso,
iniciar novamente. `docker compose restart` sozinho não atualiza código da imagem.

## 12. Execução sem internet

Em uma máquina com o projeto atualizado e imagens prontas/testadas:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\exportar-offline.ps1
```

Isso gera `offline/imagens.tar` e `offline/manifest.json`. O TAR não está no GitHub.
Copie o código e a pasta offline para o destino, sem `.demo`, `.env` ou `.git`.
Não confunda copiar uma instalação nova com migrar o banco de uma instalação antiga.

O destino precisa ter Docker Desktop/WSL prontos antes de ficar sem internet.
O pacote deve corresponder à arquitetura do motor de destino. No destino:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1 -Offline
```

Depois de sucesso:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
```

O script confere hash e arquitetura antes de importar. Teste com a rede desligada
antes de levar à apresentação. Imagens antigas exportadas não incluem código novo.

## 13. Diagnóstico rápido

| Mensagem/sintoma | Verificação e ação |
|---|---|
| `run` não reconhecido | Digite o comando diretamente, por exemplo `wsl --install --no-distribution` |
| `winget` não encontrado | Atualize App Installer ou use os instaladores oficiais |
| `docker`/`git` não encontrado | Reabra VS Code/terminal após instalar; confira instalação e PATH |
| Motor Docker não responde | Abra Desktop e resolva os avisos do backend WSL/virtualização |
| Saída `windows` em OSType | Troque para Linux containers |
| `-File ... does not exist` | Confira `Get-Location` e `Test-Path`; não execute fora da pasta do projeto |
| Pasta de clone já existe | Não exclua; identifique instalação existente ou use uma máquina limpa |
| Erro de build/pull | Confira internet, espaço, proxy/firewall e a disponibilidade das imagens |
| Porta ocupada | Identifique o processo; pare o serviço conflitante conhecido |
| `dotenv` ausente ao executar Python | Use o script Docker; não use o Python do Windows nesse roteiro |
| `invalid_client` | Chaves/cliente podem estar incoerentes; não regenere segredos isoladamente |
| `invalid_redirect_uri` | Confira URLs exatas do cliente, hostname e porta; use localhost |
| Tela antiga após editar | Reconstrua a imagem com preparar e depois iniciar |
| Senha inicial recusada | Verifique revisão/conta e se a senha já foi alterada |
| Falha de teste na rota de senha | Confira pendência conhecida; não reinstale para corrigir código |
| Hash offline diferente | Copie novamente o pacote exportado íntegro |
| Arquitetura offline diferente | Exporte imagens para a arquitetura do destino |

Para procurar ajuda, informe a etapa e a mensagem de erro, ocultando dados pessoais,
credenciais e URLs de callback com códigos. Não compartilhe `.demo`, `.env`,
tokens nem a saída completa de `docker compose config`. Para validar configuração,
prefira `docker compose config --quiet`.

## 14. Critérios para liberar a apresentação

- Mesma revisão do código testada e publicada no GitHub.
- Clone/download completo, sem depender de arquivos locais do autor.
- Preparação concluída e serviços saudáveis.
- `/healthz` responde `ok`.
- Login, páginas, logout e persistência testados no navegador.
- Pendência da senha corrigida e suíte inteira com `OK`.
- Parada/início preservam contas e senhas.
- Instalação repetida em outra máquina limpa.
- Para offline, teste adicional sem conexão com a internet.

Esses critérios reduzem erros previsíveis. Este guia não garante ausência absoluta
de falhas de hardware, rede, permissões institucionais ou mudanças externas.
Não foi realizada uma instalação limpa real em outra máquina durante esta revisão.

## Documentos complementares

- [Funcionamento, pastas e arquitetura](EXECUCAO.md)
- [Apresentação e offline](APRESENTACAO.md)
- [Testes](tests.md)
- [Índice](README.md)

O roteiro principal acima é Windows + Docker Desktop. Para Linux/macOS, consulte
EXECUCAO.md; os comandos PowerShell de instalação não devem ser usados nesses sistemas.
