olá mundo eu voltei ao trabalho

# UNIFICA — portal escolar com Keycloak

O portal Flask e o Keycloak executam em Docker. O login ativo é exclusivamente
pelo Keycloak; não é necessário instalar Python no computador.

## Comece aqui

**Banco escolar:** veja [MySQL e Workbench](docs/MYSQL.md). Execute preparar
antes de iniciar esta versão: o Compose passa a incluir o MySQL. A integração
das telas ao cadastro será a próxima etapa.

**Primeira instalação em outro computador:** siga o
[roteiro de instalação limpa no Windows](docs/tutorial.md), com pré-requisitos,
comandos, resultados esperados e diagnóstico. Leia também as pendências conhecidas
antes de considerar a versão pronta para apresentação.

Leia [o manual completo de execução](docs/EXECUCAO.md): pastas, primeira instalação,
atualização, URLs HTTP/HTTPS, autenticação, dados, GitHub, offline e diagnóstico.

Com Docker Desktop aberto, no terminal dentro da pasta extraída do projeto:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\preparar.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\iniciar.ps1
```

Execute iniciar somente após preparar terminar com sucesso. Abra
http://localhost:5000. Consulte as credenciais em `.demo/acessos.txt` localmente.
Nas próximas vezes basta iniciar. Após alterar código, prepare e inicie novamente.
Não execute `python app.py` para usar este modo Docker.

- [Índice da documentação](docs/README.md)
- [Apresentação e pacote offline](docs/APRESENTACAO.md)
- [Arquitetura](docs/architecture.md)
- [Fluxo de autenticação](docs/sso-flow.md)
- [Testes e limites](docs/tests.md)

Não publique `.demo`, `.env` nem senhas. O ambiente é local, com HTTP e
Keycloak em modo de desenvolvimento. Não existe hospedagem pública configurada.
