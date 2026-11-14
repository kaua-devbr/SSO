# Testes da versão Docker

Após reconstruir e iniciar a imagem atual:

```powershell
docker compose exec -T portal python scripts/verificar.py
```

A suíte verifica login OIDC com tokens de teste assinados, PKCE, rejeição de
nonce/state/emissor/destinatário/expiração inválidos, páginas protegidas,
remoção do login local, sonda /healthz, logout com CSRF, templates, estáticos,
sintaxe Python e preservação/migração de configuração. Não acessa MySQL nem
altera o realm em execução. O provedor é simulado: não substitui login real.

Teste manualmente login, logout confirmado, Remember Me, alteração de senha,
navegação, calendário, comunicados e aparência. Pare/inicie os serviços e confirme
persistência das contas. Por fim, baixe uma cópia limpa em outra máquina.

O usuário confirmou previamente dois contêineres Healthy e login aluno.teste.
Isso se refere à versão anterior à retirada da página intermediária: a imagem
precisa ser reconstruída para validar o fluxo mais recente no navegador.

Consulte [EXECUCAO.md](EXECUCAO.md) para comandos e problemas frequentes.

## Resultado desta revisão

Os 12 testes automatizados passaram em Python 3.12 com as dependências de
requirements-lock.txt. Foram conferidas também a sintaxe Python e PowerShell,
os links locais da documentação e a preservação dos layouts arquivados.
Os recursos estáticos referenciados nas páginas renderizadas existem e os
arquivos estáticos foram servidos pelo cliente de teste Flask.

Não foi executado build/Compose nesta sessão, pois o executável Docker não
estava acessível. A instalação real já relatada pelo usuário precisa reconstruir
a imagem e confirmar no navegador o novo redirecionamento direto ao Keycloak.
Nenhum dado do MySQL, segredo de .demo ou volume do Keycloak foi alterado.
