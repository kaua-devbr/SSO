# Como validar a instalação

Na raiz do projeto, depois de preparar a imagem e iniciar os três serviços, execute:

```powershell
docker compose ps
Invoke-RestMethod http://localhost:5000/healthz
docker compose exec -T portal python scripts/verificar.py
docker compose exec -T portal python scripts/verificar_mysql.py
docker compose exec -T portal python scripts/testar_config_mysql.py
```

| Verificação | Resultado esperado |
| --- | --- |
| Compose e `/healthz` | Três serviços saudáveis e status `ok` no Flask |
| `verificar.py` | 12 testes aprovados com OIDC simulado. A suíte cobre login, sessão, páginas, arquivos estáticos, logout e o redirecionamento de alteração de senha. |
| `verificar_mysql.py` | Conexão, sete tabelas e perfis iniciais confirmados por consultas de leitura |
| `testar_config_mysql.py` | Quatro testes de configuração e transações usando arquivos temporários e conexão simulada |

Se a saída de `verificar.py` ainda mostrar que o teste espera `/auth/conta` ao selecionar **Alterar senha**, atualize a imagem do portal e execute o teste novamente. O código atual espera `/auth/alterar-senha`.

```powershell
docker compose build portal
docker compose up -d --no-deps portal
docker compose exec -T portal python scripts/verificar.py
```

## Validação pelo navegador

1. Abra o portal em uma janela privada. Confirme o redirecionamento ao Keycloak, entre com a conta de demonstração e verifique o retorno ao perfil.
2. Abra todas as páginas pelo menu. Em **Notas e Frequência**, confira a média, a frequência e a disposição das tabelas em uma janela estreita.
3. No calendário, selecione outra data. Em comunicados, use os filtros e marque avisos como lidos. Em configurações, altere tema e fonte.
4. Use **Alterar senha** com uma conta de teste. Confirme o retorno ao portal, saia e entre usando a nova senha.
5. Em uma janela normal, teste **Lembrar de mim** fechando o navegador por completo e abrindo o portal novamente. Depois teste **Sair da conta** e confirme o logout no Keycloak se for solicitado.

Antes da apresentação, repita a [instalação limpa](tutorial.md) em outro computador.
