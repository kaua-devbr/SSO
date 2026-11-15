# Requisitos para execução local

| Requisito | Uso |
| --- | --- |
| Docker com contêineres Linux e Compose com suporte a `up --wait` | Executar Flask, Keycloak e MySQL |
| PowerShell no Windows ou Bash no Linux e macOS | Rodar os scripts de preparação e inicialização |
| Portas locais 5000, 8081 e 3307 disponíveis | Acessar o portal, o Keycloak e o MySQL |
| Internet na primeira preparação online | Baixar as imagens e as dependências |
| Git ou download ZIP | Obter os arquivos do projeto |

Docker Desktop é o caminho documentado para Windows e macOS. No Linux, o Docker Engine com o plugin Compose atende ao fluxo. O Python, o Java e o servidor MySQL rodam nos contêineres. O Workbench é opcional.

Para executar sem internet, prepare previamente o Docker e leve as três imagens exportadas para a arquitetura do computador de destino. Consulte o [roteiro offline](APRESENTACAO.md).
