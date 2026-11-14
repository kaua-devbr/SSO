# UNIFICA — Aprendendo o projeto por dentro

## Guia de leitura

Este livro acompanha o código disponível em 12 de novembro de 2026. O objetivo é permitir que um estudante entenda a aplicação, execute o portal, acompanhe uma requisição e faça alterações conscientes. Os exemplos usam o projeto real. Quando uma seção propõe uma implementação futura ou um exercício, isso é indicado no texto.

“Comandos” tem vários sentidos neste material. No terminal, são instruções executadas por PowerShell, Python ou Git. Em Python, estudamos funções, instruções e expressões. Em HTML, estudamos elementos e atributos. Em CSS, estudamos seletores, propriedades e valores. O catálogo final registra o vocabulário encontrado nos arquivos ativos, com exemplos extraídos do código. Ele cobre o projeto inspecionado; as linguagens completas têm muitos outros recursos.

Leia na ordem das partes na primeira passagem. Depois, use a busca do VS Code para localizar um nome como `request.form`, `grid-template-columns` ou `form_token`. Para visualizar o Markdown, abra este arquivo e pressione Ctrl+Shift+V.

## Sumário

1. [O projeto e sua arquitetura](#parte-1--o-projeto-e-sua-arquitetura)
2. [Ambiente e terminal](#parte-2--ambiente-e-terminal)
3. [HTML e formulários](#parte-3--html-e-formulários)
4. [Jinja e páginas dinâmicas](#parte-4--jinja-e-páginas-dinâmicas)
5. [CSS e apresentação](#parte-5--css-e-apresentação)
6. [Python e Flask](#parte-6--python-e-flask)
7. [Funcionalidades passo a passo](#parte-7--funcionalidades-passo-a-passo)
8. [MySQL e o CRUD em desenvolvimento](#parte-8--mysql-e-o-crud-em-desenvolvimento)
9. [SSO e Keycloak](#parte-9--sso-e-keycloak)
10. [Git e colaboração](#parte-10--git-e-colaboração)
11. [Verificação e diagnóstico](#parte-11--verificação-e-diagnóstico)
12. [Exercícios com respostas](#parte-12--exercícios-com-respostas)
13. Catálogo dos elementos, atributos, propriedades e chamadas encontrados no projeto.

## Parte 1 — O projeto e sua arquitetura

### 1.1 O problema que o UNIFICA pretende resolver

O UNIFICA é um portal escolar com proposta de login único. O aluno deve chegar a um ambiente comum para consultar informações e acessar serviços escolares. No produto planejado, o Keycloak centralizará a autenticação. O Flask entrega o portal e o MySQL está previsto para armazenar dados usados pelo CRUD.

Atualmente, a autenticação usa duas contas de demonstração em uma lista Python. Os eventos e comunicados são definidos no código. O portal já demonstra navegação, filtros, preferências e troca de senha temporária. A existência dessas telas permite estudar a interação entre navegador e servidor antes de conectar os serviços externos.

### 1.2 O caminho de uma requisição

Ao abrir `/calendario?dia=2026-11-09`, o navegador envia uma requisição HTTP GET. O Flask encontra a função associada a `/calendario`. O decorador de autenticação verifica a sessão. A função converte o parâmetro `dia` em uma data, prepara as semanas e chama `render_template`. O Jinja transforma o template em HTML. O navegador interpreta esse HTML e busca o CSS e as imagens indicados nele.

O navegador recebe o resultado renderizado. A lista Python de eventos permanece no servidor. Ao selecionar outro dia, um link produz uma nova requisição com outra data. Esse mecanismo explica por que o calendário funciona mesmo sem um arquivo JavaScript próprio.

### 1.3 Quais pastas realmente participam da execução

| Caminho | Responsabilidade observada |
|---|---|
| `app.py` | Cria o Flask, define as pastas, registra o Blueprint e inicia o servidor quando executado diretamente. |
| `unifica/portal/routes.py` | Concentra rotas, contas de demonstração, eventos, comunicados e regras dos formulários. |
| `unifica/auth/decorators.py` | Implementa a verificação de sessão e do token dos formulários protegidos. |
| `unifica/templates/` | Contém as páginas efetivamente renderizadas. |
| `unifica/static/css/` | Contém os estilos carregados por essas páginas. |
| `unifica/static/img/` | Contém os ícones usados no menu. |
| `unifica/crud_usuarios/services/` | Contém uma conexão MySQL e funções de CRUD ainda incompletas. O portal não as importa. |
| `unifica/config/` | Reserva módulos de configuração ainda vazios. |
| `deploy/keycloak/realm-school.json` | Arquivo vazio reservado à configuração futura. Ainda não é uma exportação de realm utilizável. |
| `tests/` | Reserva testes. Os arquivos Python inspecionados estão vazios. |
| `docs/` | Material de estudo e documentação do projeto. |

Na revisão atual também existem `auth/`, `config/`, `portal/` e `templates/` na raiz, provenientes da estrutura anterior. `app.py` importa explicitamente `unifica.portal.routes` e usa `unifica/templates`. Alterar o antigo `templates/login.html` pode produzir a impressão de que nada mudou porque a aplicação lê outro arquivo. O mesmo vale para os estilos em `templates/static/`.

Arquivos `__init__.py` vazios continuam tendo função estrutural: identificam pacotes Python convencionais. O conteúdo vazio, sozinho, não demonstra que um arquivo seja dispensável.

### 1.4 Estado das entregas

| Recurso | Estado real |
|---|---|
| Login e saída | Funcionam com contas de demonstração. |
| Perfil | Nome e nível vêm da sessão; outros dados são exemplos fixos. |
| Calendário | Navegação e seleção funcionam sobre eventos fixos de novembro de 2026. |
| Comunicados | Busca, categorias e leitura funcionam durante a sessão. |
| Aparência | Tema e tamanho de fonte são guardados na sessão e usados nas páginas que herdam a base. |
| Troca de senha | Altera o hash em memória no processo atual. Reiniciar restaura as senhas iniciais. |
| Notas e frequência | Página com mensagem de ausência de dados. |
| Mostrar senha | Botão desenhado, sem manipulador JavaScript observado. |
| Lembrar de mim | Checkbox enviado pelo formulário, mas sem tratamento na rota. |
| Recuperar senha | Link `href="#"`, sem fluxo de recuperação implementado. |
| Adicionar Gmails | Botão sem formulário ou ação implementada. |
| MySQL e SSO | Estrutura inicial; integração ao portal pendente. |

## Parte 2 — Ambiente e terminal

### 2.1 Preparação no Windows

Abra a pasta `C:\Users\Kaua Alexandre\Documents\SSO` no VS Code. Abra Terminal > New Terminal. Os comandos abaixo usam PowerShell e pressupõem um Python instalado e acessível. O código do CRUD contém `match`, introduzido no Python 3.10; use uma versão compatível com esse recurso e com as dependências escolhidas.

```powershell
Set-Location -LiteralPath 'C:\Users\Kaua Alexandre\Documents\SSO'
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install Flask
.\.venv\Scripts\python.exe app.py
```

`Set-Location` muda a pasta atual. `-LiteralPath` interpreta o caminho literalmente. Aspas mantêm os espaços do nome do usuário dentro de um único argumento. `python --version` verifica qual interpretador o terminal encontra. `-m venv .venv` executa o módulo `venv` e cria um ambiente isolado. A chamada ao Python dentro de `.venv` garante que a instalação e a execução usam o mesmo ambiente.

`-m pip install Flask` instala o Flask e suas dependências, incluindo Jinja e Werkzeug. O arquivo `app.py` usa essas bibliotecas. Flask-Session não faz parte dos imports atuais. A instalação de Flask-Session do exemplo da aula não é necessária para esta implementação.

Acesse `http://127.0.0.1:5000/` enquanto o processo estiver rodando. `127.0.0.1` representa o próprio computador. A porta padrão é 5000. Ctrl+C encerra o servidor no terminal. O processo precisa continuar aberto durante o uso do portal.

### 2.2 Comandos equivalentes e diagnóstico do Python

| Comando | Para que serve |
|---|---|
| `Get-Location` | Mostra a pasta atual do terminal. |
| `Get-ChildItem` | Lista os arquivos e diretórios dessa pasta. |
| `Get-Command python` | Mostra qual executável o PowerShell encontra. |
| `py --version` | Verifica o lançador Python do Windows, se estiver instalado. |
| `py -m venv .venv` | Alternativa para criar o ambiente usando o lançador. |
| `.\.venv\Scripts\Activate.ps1` | Ativa o ambiente na sessão atual, quando a política do PowerShell permite. |
| `deactivate` | Desativa um ambiente previamente ativado. |
| `.\.venv\Scripts\python.exe -m pip show Flask` | Mostra a instalação do Flask nesse interpretador. |
| `.\.venv\Scripts\python.exe -m pip list` | Lista pacotes instalados no ambiente. |
| `.\.venv\Scripts\python.exe -m flask --app app routes` | Lista rotas registradas pela aplicação. |
| `.\.venv\Scripts\python.exe -m flask --app app run` | Inicia a mesma aplicação pela ferramenta de linha de comando do Flask. |
| `.\.venv\Scripts\python.exe -m flask --app app run --port 5001` | Usa outra porta, útil quando 5000 já está ocupada. |

Ativar o ambiente é opcional quando seu executável é chamado pelo caminho completo. Se `python` abrir a Microsoft Store, o alias encontrado não está fornecendo um interpretador utilizável. Verifique a instalação antes de continuar.

### 2.3 Dependências e arquivos locais

O repositório inspecionado não contém um arquivo de dependências com versões fixadas. Registrar dependências será uma melhoria de reprodutibilidade. `python -m pip freeze` imprime as versões instaladas; `python -m pip freeze > requirements.txt` grava essa saída. Execute isso em um ambiente dedicado ao projeto, pois todos os pacotes daquele ambiente serão listados. Depois, `python -m pip install -r requirements.txt` instala os pacotes registrados.

O `.gitignore` atual trata caches de Python. Ao criar `.venv`, acrescente `.venv/` ao arquivo antes de preparar um commit amplo. O ambiente é reconstruído pelas dependências e não precisa ser enviado ao GitHub. O comando `git status --short` mostra o que ainda seria incluído ou alterado.

## Parte 3 — HTML e formulários

### 3.1 Como ler uma tag

Considere `<a class="botao" href="/perfil">Ver perfil</a>`. `a` é o elemento de ligação, `class` associa um nome usado pelo CSS, `href` define o destino e `Ver perfil` é o conteúdo. O fechamento `</a>` termina o elemento. Elementos como `input`, `img`, `meta` e `link` são vazios e não envolvem conteúdo com uma tag de fechamento.

O `<!doctype html>` ativa o modo padrão de interpretação HTML. `<html lang="pt-BR">` informa o idioma principal. `<head>` agrupa metadados, título e referências de estilos. `<body>` contém a interface. `<meta charset="UTF-8">` permite representar os caracteres usados em português. A declaração `viewport` orienta a largura de layout em telas móveis.

O arquivo salvo também precisa estar em UTF-8. Declarar o charset não corrige bytes que já foram gravados em outra codificação. No VS Code, confira a codificação na barra inferior se surgirem caracteres estranhos.

### 3.2 Estrutura semântica das telas

`main` identifica o conteúdo principal. `aside` abriga o menu lateral. `nav` agrupa links de navegação. `header` introduz uma página ou seção. `section` reúne um assunto, enquanto `article` representa um item independente, como um evento. `footer` apresenta conteúdo de rodapé. `div` e `span` são agrupadores genéricos; `div` organiza blocos e `span` é útil em trechos pequenos.

Os elementos `h1`, `h2`, `h3` e `h4` expressam níveis de títulos. `p` representa um parágrafo, `strong` destaca importância, `small` apresenta informação auxiliar e `ul` com `li` forma a lista de comunicados. A hierarquia ajuda tanto a leitura visual quanto a navegação assistiva.

### 3.3 O contrato entre formulário e Python

No login, o campo usa `name="login"`. O Python busca esse valor com `request.form.get("login", "")`. Esses nomes precisam corresponder. `id="login"` tem outra função: permite que `<label for="login">` se associe ao campo. Clicar no rótulo direciona o foco para o input.

```html
<form method="POST" action="{{ url_for('portal.login') }}">
    <label for="login">Login</label>
    <input id="login" name="login" type="text" required>
    <input name="senha" type="password" required>
    <button type="submit">Entrar</button>
</form>
```

Esse recorte ilustra os mesmos nomes usados no projeto. `method` define como enviar os dados e `action` define o destino. Um formulário GET coloca parâmetros na URL, como a busca de comunicados. Um POST envia os campos no corpo da requisição, como o login. O método HTTP sozinho não fornece criptografia; HTTPS é o transporte apropriado para credenciais em um ambiente publicado.

`type="password"` mascara o texto na tela. `required`, `minlength` e `maxlength` instruem a validação do navegador. O servidor também verifica a entrada, porque requisições podem ser feitas sem passar pela interface. `placeholder` mostra uma dica temporária; o rótulo continua sendo a identificação permanente do campo.

### 3.4 Tipos e estados dos campos

`type="text"` recebe texto geral. `type="search"` sinaliza um campo de pesquisa. `type="checkbox"` representa uma seleção booleana, mas só produz efeito no produto quando o servidor trata seu nome. `type="hidden"` envia dados que não aparecem como um campo editável. Um usuário pode modificar um campo oculto com ferramentas do navegador, portanto ele não é uma fonte confiável por estar escondido.

No perfil, `readonly` impede a edição normal do campo pela interface. O atributo `value` define o valor exibido. As escolhas de tema e fonte usam `select` com elementos `option`; o atributo `selected` determina qual alternativa aparece selecionada. A opção que o usuário escolher será enviada com o nome do `select`.

`autocomplete="current-password"` orienta gerenciadores de senha sobre o campo atual. `new-password` identifica a nova senha. `button type="submit"` envia o formulário. `button type="button"` depende de uma ação programada ou outro mecanismo explícito; o botão Mostrar senha ainda não tem essa implementação.

### 3.5 Alterar senha com HTML nativo

O elemento `details` cria uma região expansível. Seu `summary` é o controle clicável. O atributo `open` faz a região iniciar aberta. O template de configurações acrescenta `open` quando há mensagens da categoria `erro-senha`, para mostrar os campos após uma tentativa inválida.

Esse comportamento de abrir e fechar é fornecido pelo navegador. Enviar a nova senha continua exigindo uma requisição POST ao Flask. O formulário possui `acao="senha"`, representada por um campo oculto, para que a rota diferencie essa ação das preferências visuais.

### 3.6 Acessibilidade e imagens

`alt` fornece uma alternativa textual para imagens. Os ícones que já acompanham textos descritivos usam `alt=""` para evitar repetição. `aria-label` nomeia controles, `aria-labelledby` referencia o identificador de um título, e `aria-current` marca a página ou data selecionada. `aria-hidden="true"` esconde detalhes decorativos da árvore de acessibilidade.

`role="alert"` sinaliza mensagens urgentes, como erro de formulário. `role="status"` indica uma atualização de estado. O papel `search` identifica a busca. Esses atributos devem complementar elementos HTML apropriados e foco visível.

Os desenhos do login usam SVG embutido. `svg` define a área, `viewBox` estabelece coordenadas internas, `path` usa instruções em `d` para desenhar, `circle` define centro e raio e `rect` define um retângulo. `fill`, `stroke` e `stroke-width` controlam preenchimento e traço. `currentColor` aproveita a cor CSS do elemento. O catálogo final mostra os atributos encontrados.

## Parte 4 — Jinja e páginas dinâmicas

### 4.1 Onde o template é executado

Jinja roda no servidor quando o Flask renderiza uma página. `{{ nome }}` imprime um valor. `{% if ... %}` controla o conteúdo produzido. O usuário recebe HTML já resolvido. Abrir o arquivo de template diretamente pelo Explorador de Arquivos não executa Flask nem Jinja.

O Flask configura escape automático para os templates HTML usuais. Isso transforma caracteres especiais de valores textuais em entidades apropriadas ao contexto HTML. Ao exibir entrada do usuário, mantenha esse comportamento e evite usar `safe` sem uma justificativa técnica e tratamento do conteúdo.

Referência de sintaxe e herança: [documentação do Jinja](https://jinja.palletsprojects.com/en/stable/templates/).

### 4.2 Herança usada no UNIFICA

`{% extends 'base.html' %}` seleciona o layout comum. `base.html` define os blocos `titulo`, `estilos` e `conteudo`. Cada página preenche esses espaços. Assim, uma alteração no menu compartilhado pode alcançar calendário, comunicados, perfil e configurações.

O perfil preenche `estilos` para carregar `perfil.css` além de `global.css`. Login e erro têm documentos HTML completos próprios. Por isso, as preferências gravadas nos atributos do `html` da base não se aplicam automaticamente a essas duas páginas.

### 4.3 Expressões que aparecem nas telas

| Sintaxe | Leitura e aplicação |
|---|---|
| `{{ url_for('portal.perfil') }}` | Gera a URL pelo nome da rota. |
| `{{ url_for('static', filename='css/global.css') }}` | Gera a URL de um recurso estático. |
| `{% block conteudo %}` e `{% endblock %}` | Delimitam uma região substituível da base. |
| `{% for ... %}` e `{% endfor %}` | Repetem HTML para cada item de uma coleção. |
| `{% if ... %}`, `{% else %}`, `{% endif %}` | Escolhem qual trecho aparece. |
| `{% for ... %} ... {% else %}` | Mostram conteúdo alternativo quando a coleção está vazia. |
| `{% set mensagens = ... %}` | Guarda um resultado em variável do template. |
| `session.get('tema', 'claro')` | Lê o tema com um valor padrão. |
| `session.usuario[0]` | Lê a primeira letra do nome armazenado na sessão. |
| `'img/' ~ icone` | Concatena texto no Jinja para formar o caminho da imagem. |
| `categoria == chave` | Testa igualdade para marcar um filtro. |
| `id not in lidos` | Testa se o aviso ainda está sem leitura registrada. |
| `valor if condição else alternativa` | Escolhe um valor em uma expressão. |
| `mensagens \| selectattr('0', 'equalto', 'erro-senha') \| list` | Filtra tuplas pela categoria na posição zero e materializa a lista para testar se há resultados. |
| `get_flashed_messages(with_categories=true)` | Obtém mensagens e suas categorias para renderização. |

### 4.4 Um menu construído por dados

Na base, cada entrada da lista contém endpoint, texto e nome de imagem. O `for rota, texto, icone in ...` desempacota os três valores. `request.endpoint == rota` identifica a página atual e adiciona `aria-current="page"`. O CSS seleciona esse atributo para destacar o item.

Para incluir uma página, crie uma rota que renderize o template, adicione a entrada correspondente à lista e confira se a imagem existe. Um endpoint é o nome interno, como `portal.calendario`; `/calendario` é o endereço público. O prefixo `portal` vem do nome do Blueprint.

## Parte 5 — CSS e apresentação

### 5.1 Regras, seletores e cascata

Uma regra como `.botao { padding: .45rem .75rem; }` escolhe elementos com a classe `botao` e define espaço interno. Antes das chaves está o seletor. Dentro, cada declaração contém propriedade e valor. O ponto e vírgula separa declarações.

`body` seleciona uma tag. `.portal` seleciona uma classe. `.portal h1` seleciona títulos dentro do portal. `.botao.principal` exige as duas classes no mesmo elemento. `.configuracoes section + section` seleciona uma seção imediatamente após outra seção. `>` seleciona filhos diretos; um espaço permite qualquer nível descendente. Uma vírgula agrupa seletores independentes.

`[data-tema="escuro"]` depende do valor de um atributo HTML. `:hover` corresponde ao ponteiro sobre o elemento. `:focus-visible` ajuda a exibir foco de teclado. `:root` seleciona a raiz do documento. `:is(button, input, select)` agrupa alternativas dentro de um seletor. `::before`, quando presente no CSS, gera uma caixa visual antes do conteúdo do elemento.

A cascata combina origem, importância, especificidade e ordem. Em regras comparáveis, uma regra mais específica pode prevalecer mesmo quando aparece antes. O perfil carrega estilos próprios com seletores globais, como `nav a`; os seletores mais específicos de `global.css` reduzem colisões, mas mudanças precisam ser conferidas visualmente.

### 5.2 Modelo de caixa e medidas

Todo elemento produz caixas. `width` e `height` definem dimensões; `padding` é o espaço interno; `border` é a borda e `margin` é o espaço externo. Com `box-sizing: border-box`, largura e altura incluem padding e borda. Isso ajuda a evitar que um painel ultrapasse o espaço disponível.

Em quatro valores, padding e margin seguem a ordem topo, direita, baixo, esquerda. Em dois valores, o primeiro vale para topo e baixo, e o segundo para esquerda e direita. `margin: 0 auto` pode centralizar uma caixa com largura limitada. Margens automáticas também têm comportamento útil em Flexbox, como empurrar o botão Sair para o fim da barra lateral.

| Unidade ou função | Uso no projeto |
|---|---|
| `px` | Medida CSS fixa, útil para bordas e ícones. |
| `rem` | Escala em relação ao tamanho da fonte raiz. |
| `%` | Relação com um valor de referência que depende da propriedade. |
| `vh` | Fração da altura do viewport. |
| `dvh` | Altura dinâmica do viewport, útil em navegadores móveis. |
| `vw` | Fração da largura do viewport. |
| `fr` | Fração do espaço distribuído por uma grade CSS. |
| `min(a, b)` | Escolhe o menor dos limites calculados. |
| `clamp(mínimo, preferido, máximo)` | Permite crescimento dentro de limites. |
| `calc(...)` | Faz cálculos entre medidas compatíveis. |

### 5.3 Grid, Flexbox e o calendário

O corpo do portal usa `display: grid` com `grid-template-columns: 185px minmax(0, 1fr)`. A primeira coluna reserva espaço para o menu. A segunda ocupa o restante e pode reduzir até zero, evitando que um tamanho mínimo implícito force largura excessiva.

A agenda tem duas colunas em telas largas. A grade dos dias usa `repeat(7, minmax(0, 1fr))`: sete colunas iguais para os dias da semana. `gap` separa células sem introduzir margens individuais. `place-items: center` centraliza o número do dia na célula.

Flexbox organiza controles em uma direção. `display: flex`, `align-items: center` e `justify-content: space-between` alinham elementos e distribuem espaço. `flex-wrap: wrap` permite quebrar controles em outra linha. O menu usa `flex-direction: column` para organizar marca, navegação e saída verticalmente.

### 5.4 Posicionamento

`position: relative` cria uma referência para filhos posicionados. O ponto de evento usa `position: absolute` dentro da célula relativa do dia. `bottom` posiciona esse indicador próximo da borda inferior. A barra lateral usa `position: sticky` com `top: 0`, mantendo-se visível conforme o comportamento do contêiner de rolagem.

`overflow: auto` permite rolar o menu quando seu conteúdo excede a altura. `overflow: hidden` corta conteúdo que excede uma caixa; seu uso precisa ser conferido para não esconder controles. Alguns seletores em `perfil.css` pertencem ao layout antigo, como `.container` e `.menu`, e não têm correspondência direta no template de perfil atual.

### 5.5 Tema e tamanho da fonte

As propriedades personalizadas começam com `--`, por exemplo `--fundo` e `--texto`. O CSS lê uma delas com `var(--fundo)`. O tema claro define uma paleta na raiz; o seletor `:root[data-tema="escuro"]` substitui as cores. Alterar o tema no formulário provoca um POST, grava `session['tema']` e renderiza novamente a base com o atributo atualizado.

O tamanho grande usa `font-size: 118.75%` na raiz. Com uma base de 16 pixels, isso equivale a 19 pixels. Medidas em `rem` acompanham essa mudança. Textos definidos apenas em pixels podem precisar de regras complementares, como já ocorre em partes do perfil.

### 5.6 Responsividade e detalhes visuais

As regras `@media` modificam o layout conforme a largura disponível. Em `global.css`, até 850 pixels a agenda passa a uma coluna. Até 620 pixels o menu fica compacto, com ícones e nomes acessíveis. Existem limites adicionais em CSS de login, erro e perfil.

`border-radius` arredonda cantos, `box-shadow` desenha sombras e `transition` suaviza mudanças. `object-fit: contain` preserva a proporção de uma imagem dentro de uma caixa. `filter: brightness(0) invert(1)` torna ícones claros no tema escuro. `outline` destaca foco sem ocupar o mesmo espaço de uma borda.

Para descobrir por que uma cor não mudou, abra as ferramentas de desenvolvedor do navegador, selecione o elemento e confira as regras aplicadas. Uma declaração riscada foi superada na cascata. Confira também qual arquivo CSS foi carregado.

Referência complementar: [CSS no MDN](https://developer.mozilla.org/en-US/docs/Web/CSS).

## Parte 6 — Python e Flask

### 6.1 Valores e estruturas encontrados no código

Uma string é texto, como `'maria'`. Um inteiro representa valores como o identificador `2`. Booleanos são `True` e `False`. `None` representa ausência de valor, como a inexistência de um mês navegável além do limite.

Listas usam colchetes e mantêm uma sequência mutável. `USUARIOS_DEMO` é uma lista de dicionários. Um dicionário relaciona chaves e valores, como `usuario['nome']`. Tuplas usam posições fixas, como cada comunicado `(id, categoria, titulo, texto, tempo)`. Conjuntos, criados por `set`, evitam duplicatas e são usados para os identificadores já lidos.

`MESES[selecionado.month - 1]` converte o mês de 1 a 12 em um índice de 0 a 11. `item[0]` acessa o primeiro valor da tupla. `[:100]` cria uma fatia com até os cem primeiros caracteres da busca. `len(nova)` conta caracteres da senha na string Python, e não bytes do transporte.

### 6.2 Controle de fluxo

`if`, `elif` e `else` selecionam caminhos. `for` percorre coleções. `return` termina a função e devolve um resultado. `try` e `except ValueError` tratam falhas de conversão de data. `raise ValueError` provoca a mesma categoria de falha quando o ano está fora dos limites.

`and` exige condições verdadeiras em conjunto, `or` aceita alternativas, `not` inverte a interpretação booleana, `in` testa participação e `not in` testa ausência. Esses operadores fazem avaliação de curto-circuito. Em `if not token or not compare_digest(...)`, a comparação só ocorre se existir um token.

O CRUD usa `match` e `case` para escolher uma operação com base no conteúdo de uma variável. No estado atual, essa variável ainda não foi definida. `pass` é uma instrução vazia que permite manter um bloco sintaticamente válido.

### 6.3 Funções, imports e pacotes

`def` define uma função. Parâmetros são valores recebidos, como `view` em `login_required(view)`. `*args` reúne argumentos posicionais e `**kwargs` reúne argumentos nomeados. A função interna `protected` recebe esses argumentos e os encaminha para a função original.

`from modulo import nome` importa uma função ou objeto específico. `from .conexao import conexao` é um import relativo ao pacote atual. `__package__` ajuda o código do CRUD a escolher entre import relativo e execução direta do arquivo. Executar um módulo com `python -m pacote.modulo` fornece o contexto de pacote; importar o CRUD atual também tenta abrir uma conexão ao banco.

### 6.4 Entendendo app.py

`Flask(__name__, ...)` cria o objeto da aplicação. `__name__` identifica o módulo. `template_folder` aponta para os templates ativos. `static_folder` aponta para os recursos públicos e `static_url_path='/static'` define o prefixo das URLs desses recursos.

`token_hex(32)` gera 32 bytes aleatórios representados em hexadecimal, resultando em 64 caracteres. Essa chave é atribuída a `SECRET_KEY`. Como uma nova chave é criada ao iniciar o processo, cookies assinados antes de um reinício deixam de ser válidos naquele novo processo.

`register_blueprint(portal)` registra o conjunto de rotas definido em outro módulo. `if __name__ == '__main__'` faz `app.run()` executar apenas quando o arquivo é iniciado diretamente. A ferramenta `flask --app app` importa o objeto e fornece sua própria forma de iniciar o servidor de desenvolvimento.

### 6.5 Blueprint e decoradores

`Blueprint('portal', __name__)` organiza um conjunto de rotas. `@portal.get('/perfil')` registra uma rota GET. `@portal.post('/sair')` registra POST. `@portal.route(..., methods=['GET', 'POST'])` aceita ambos. O nome completo de endpoint combina o nome do Blueprint e o nome da função.

Os decoradores são aplicados de baixo para cima. No perfil, `@login_required` envolve primeiro a função; o registro de rota recebe essa função protegida. `@wraps(view)` preserva nome e metadados da função original. Isso é importante para o Flask distinguir endpoints em vez de enxergar várias funções chamadas `protected`.

### 6.6 Objetos do Flask usados nas rotas

| Objeto ou chamada | Responsabilidade |
|---|---|
| `request.method` | Identifica o método HTTP atual. |
| `request.args.get(...)` | Lê parâmetros da URL. |
| `request.form.get(...)` | Lê os campos de formulário enviados no corpo. |
| `request.endpoint` | Identifica a rota que está atendendo a requisição. |
| `session.get(...)` | Lê um valor da sessão com padrão opcional. |
| `session[chave] = valor` | Atualiza um valor da sessão. |
| `session.clear()` | Esvazia os dados dessa sessão. |
| `render_template(...)` | Renderiza um arquivo Jinja com variáveis nomeadas. |
| `url_for(...)` | Constrói uma URL a partir de endpoint e parâmetros. |
| `redirect(..., code=303)` | Devolve uma resposta que manda o navegador fazer uma nova navegação. |
| `flash(texto, categoria)` | Guarda uma mensagem para apresentação por um template. |
| `abort(400)` | Interrompe a requisição com erro HTTP 400. |
| `app_errorhandler(...)` | Registra tratamento de erro com alcance na aplicação. |

### 6.7 Sessão e ciclo de vida

A implementação padrão do Flask grava dados de sessão em um cookie assinado. A assinatura detecta alterações indevidas; o conteúdo pode ser lido pelo cliente. Por isso, dados secretos, como uma senha em texto puro, não devem ser armazenados na sessão. O código atual guarda nome, nível, estado de login, token de formulário e preferências.

Esses dados pertencem ao navegador/sessão. O logout chama `session.clear()` e apaga preferências e leitura de comunicados junto com a autenticação. Um novo login também limpa os dados anteriores. As alterações feitas no dicionário global do usuário, como o novo hash de senha, pertencem ao processo Python e sobrevivem a esse logout, mas desaparecem ao reiniciar o processo.

Referência do comportamento padrão: [sessões do Flask](https://flask.palletsprojects.com/en/stable/quickstart/#sessions).

### 6.8 Hash e proteção de formulários

`generate_password_hash` transforma uma senha em uma representação adequada à verificação posterior. `check_password_hash` verifica se uma candidata corresponde ao hash. Os padrões de algoritmo e custo dependem da versão do Werkzeug instalada. O projeto não fixa esses parâmetros.

O token `token_urlsafe(32)` é criado ao autenticar. Formulários protegidos enviam o token em um input oculto. O decorador compara o recebido com o da sessão usando `compare_digest` sobre bytes gerados por `encode`. A requisição sem token ou com token diferente recebe 400. Essa verificação busca reduzir requisições de formulário forjadas; ela aparece nas rotas protegidas e não é aplicada à rota de login atual.

O campo `nivel` é exibido, mas o decorador só verifica o estado de login. Uma conta `normal` e uma conta `adm` têm acesso às mesmas rotas deste portal. Autorização por papel ainda precisa ser implementada. A proteção atual deve ser tratada como parte de um protótipo, com revisão própria antes de publicação para usuários reais.

## Parte 7 — Funcionalidades passo a passo

### 7.1 Mapa completo das rotas

| URL | Método | Função | Resultado |
|---|---|---|---|
| `/` | GET | `login` | Formulário; com sessão ativa, redireciona ao perfil. |
| `/` | POST | `login` | Verifica conta, cria sessão ou mostra mensagem de erro. |
| `/perfil` | GET | `perfil` | Exibe nome, nível e dados de exemplo. |
| `/inicio` | GET | `inicio` | Exibe saudação e atalhos. |
| `/notas` | GET | `notas` | Exibe estado sem registros. |
| `/calendario` | GET | `calendario` | Monta o mês e os eventos do dia escolhido. |
| `/comunicados` | GET | `comunicados` | Aplica busca e categoria. |
| `/comunicados` | POST | `comunicados` | Marca avisos como lidos. |
| `/configuracoes` | GET | `configuracoes` | Exibe aparência, senha e informações do sistema. |
| `/configuracoes` | POST | `configuracoes` | Salva preferências ou altera a senha de demonstração. |
| `/sair` | POST | `sair` | Limpa a sessão e redireciona ao login. |
| `/static/<caminho>` | GET | `static` | Entrega CSS e imagens. |

As rotas do portal, exceto login e recursos estáticos, usam `login_required`. GET costuma aceitar HEAD automaticamente no Flask e as rotas podem fornecer OPTIONS automaticamente. O navegador normalmente usa os métodos apresentados na tabela.

### 7.2 Login

As contas iniciais são `zezinho` com senha `1234`, nível `adm`, e `maria` com senha `4321`, nível `normal`. O login passa por `strip().lower()`, removendo espaços nas extremidades e convertendo letras para minúsculas. A senha é comparada como recebida e deve ter até 128 caracteres para alcançar a verificação de hash.

Se a conta corresponde, a sessão é limpa e recebe `logado`, `nivel`, `usuario`, `login` e `form_token`. A resposta 303 aponta para `/perfil`. Se nenhuma conta corresponde, a rota registra uma mensagem e renderiza o login com status 400. Uma pessoa já logada é encaminhada ao perfil antes de processar novas credenciais.

### 7.3 Calendário

`request.args.get('dia', '2026-11-06')` fornece a data recebida ou a data inicial fixa. `date.fromisoformat` interpreta `AAAA-MM-DD`. A aplicação aceita anos de 1900 a 2100. Entradas inválidas voltam para 6 de novembro de 2026.

`replace(day=1)` encontra o primeiro dia do mês. Subtrair um dia e voltar ao dia 1 encontra o mês anterior. Somar 32 dias ao primeiro dia garante chegar ao mês seguinte; outro `replace(day=1)` encontra seu início. Os links são omitidos quando ultrapassariam os limites de anos aceitos.

`Calendar(firstweekday=6)` usa domingo como primeira coluna. Na biblioteca, segunda-feira é 0 e domingo é 6. `monthdatescalendar` devolve semanas completas com objetos `date`; datas de meses vizinhos completam as bordas. O template exibe espaços vazios nessas posições.

`weekday()` ajuda a escolher o nome do dia. `isoformat()` produz a data para o link. `strftime('%d/%m/%Y')` produz uma data legível. A formatação `:02d` garante dois dígitos, como `06`. Selecionar um dia consulta `EVENTOS.get(selecionado, [])`; uma lista vazia produz “Sem eventos neste dia”.

### 7.4 Comunicados

Os avisos são tuplas com cinco posições. O filtro valida a categoria contra `CATEGORIAS`; um nome desconhecido volta para `todos`. A busca elimina espaços externos, limita a entrada a cem caracteres e usa `casefold()` para comparar sem distinguir maiúsculas e minúsculas. A normalização não remove acentos, portanto certas buscas com grafia diferente podem não coincidir.

O operador `in` verifica se o texto procurado está no título ou no corpo. Uma busca vazia corresponde a todos os textos. A compreensão de lista mantém apenas os avisos que atendem simultaneamente à categoria e à busca.

No POST, o botão envia `comunicado` com um identificador ou `todos`. Os IDs existentes são adicionados a um conjunto. `sorted` converte o resultado para uma lista ordenada que pode ser guardada na sessão. O botão “Marcar todos” percorre todos os comunicados, incluindo os que não aparecem no filtro atual. Depois, o redirecionamento conserva categoria e busca.

Os rótulos “Há 2 dias” e semelhantes são texto fixo de demonstração; não são recalculados pelo relógio. Avisos com ID desconhecido não são incluídos na coleção de lidos.

### 7.5 Aparência e senha

O formulário de aparência envia `acao=aparencia`. A rota aceita apenas `claro` ou `escuro` para tema e `normal` ou `grande` para fonte. Combinações inválidas não atualizam a preferência e a rota redireciona sem mensagem específica de erro. Os valores válidos são refletidos nos atributos `data-tema` e `data-fonte` da base.

O formulário de senha envia `acao=senha`. A rota encontra a conta com `next(...)`, usando o login da sessão. A região `with senha_lock` serializa alterações concorrentes dentro do mesmo processo. O lock não coordena processos diferentes nem substitui uma transação no banco.

A ordem das verificações é senha atual, comprimento da nova senha entre 8 e 128, igualdade com a confirmação e diferença em relação à senha atual. A primeira falha gera uma mensagem. No sucesso, o hash é substituído e `date.today()` registra a data do servidor. Essa data segue o relógio do ambiente onde o Python está rodando.

### 7.6 Erros e limites

Os handlers 404 e 500 renderizam `erro.html` com o código correspondente. 404 representa um endereço inexistente. 500 indica uma falha interna não tratada. O código 400 do token inválido não tem template personalizado registrado; a resposta padrão do Flask pode aparecer.

O link `javascript:history.back()` usa a API de histórico do navegador para voltar à página anterior. É o JavaScript explícito observado nessa tela. Abrir `/sair` pela barra de endereços faz GET e pode resultar em 405, porque a rota aceita POST.

## Parte 8 — MySQL e o CRUD em desenvolvimento

### 8.1 O que a conexão executa

`from os import environ` permite ler variáveis do ambiente. `environ['UNIFICA_MYSQL_PASSWORD']` exige essa variável. A ausência produz `KeyError`. `mysql.connector.connect` recebe host, usuário, senha e banco. No código atual, host é local, usuário é `root` e o banco é `UNIFICA`.

A conexão acontece no nível superior do módulo. Importar `conexao.py` já tenta acessar o banco e criar um cursor. Por esse motivo, uma checagem de sintaxe deve usar compilação em vez de importar o CRUD para experimentar. O portal Flask atual não depende dessa importação.

Para estudar a integração em um banco de desenvolvimento, a dependência seria instalada com `python -m pip install mysql-connector-python`. A variável pode ser definida na sessão PowerShell por `$env:UNIFICA_MYSQL_PASSWORD = 'senha-do-banco-de-teste'`, substituindo o exemplo localmente. Esse comando não cria banco, tabelas ou usuários.

### 8.2 Vocabulário SQL

| Instrução ou chamada | Função |
|---|---|
| `INSERT INTO` | Insere uma linha na tabela informada. |
| `SELECT` | Consulta colunas e linhas. |
| `UPDATE ... SET` | Modifica valores das linhas selecionadas. |
| `DELETE FROM` | Remove linhas selecionadas. |
| `WHERE` | Restringe as linhas atingidas por uma condição. |
| `%s` | Marcador de parâmetro usado pelo conector nesses exemplos. |
| `conexao.cursor()` | Cria um objeto para executar comandos na conexão. |
| `cursor.execute(sql, valores)` | Executa uma instrução com seus parâmetros. |
| `cursor.fetchall()` | Obtém todas as linhas restantes do resultado. |
| `conexao.commit()` | Confirma alterações da transação. |

Parâmetros separam valores do texto SQL. Por exemplo, `cursor.execute('SELECT nome FROM aluno WHERE email = %s', (email,))` fornece uma tupla de um item; a vírgula é necessária para que seja uma tupla. Esse exemplo pressupõe a existência da tabela e da coluna. O projeto não inclui um esquema SQL suficiente para comprovar essa estrutura.

### 8.3 Diagnóstico de cada função atual

| Função | Intenção | Pendência concreta |
|---|---|---|
| `Cadastrar_usuario` | Inserir aluno com nove campos | Possui nove marcadores e uma tupla vazia. Precisa receber e validar os valores. |
| `Deletar_usuario` | Remover um registro | O trecho `WHERE *VALOR` não constitui uma condição SQL válida. Falta chave de identificação. |
| `Deletar_notas` | Remover notas | Repete a consulta de aluno e não define tabela de notas. |
| `Consultar_usuario` | Consultar dados | Repete a condição inválida e descarta o resultado de `fetchall`. |
| `Atualizar_dados` | Atualizar um campo | Usa `consulta` sem definição, tabela `personagens`, coluna `id_Personagem` e parâmetros vazios. |

Essas funções podem ser compiladas como Python, mas isso não comprova que executem SQL válido. Concluir o CRUD exige definir esquema, assinaturas de função, validação, tratamento de falha, retorno de resultados e ciclo de vida de conexões. Uma exceção durante a transação também exige uma decisão de rollback antes de reutilizar a conexão.

O módulo mantém um cursor global. Em uma futura aplicação com várias requisições simultâneas, o gerenciamento de conexão e cursor deve ser desenhado para esse uso. O código atual de formulário não chama as funções de CRUD.

Referência da biblioteca: [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/).

## Parte 9 — SSO e Keycloak

### 9.1 Conceitos para o TCC

SSO permite aproveitar uma autenticação central para acessar aplicações participantes. O Keycloak atua como provedor de identidade. Um realm organiza usuários, clientes e configurações. Um client representa uma aplicação integrada. O OpenID Connect acrescenta informação de identidade ao fluxo baseado em OAuth 2.0.

O fluxo planejado pode usar Authorization Code com PKCE. O portal redireciona o usuário ao provedor, o usuário autentica ali e o provedor retorna um código para uma URI previamente registrada. A aplicação troca esse código conforme a configuração do cliente e valida a resposta usando uma biblioteca apropriada. O estado da solicitação e os parâmetros de proteção do fluxo precisam ser verificados.

Um ID token descreve a autenticação para o cliente. Um access token autoriza acesso a recursos conforme suas permissões. Refresh tokens, quando emitidos e permitidos, participam da renovação. O projeto atual não implementa esse fluxo nem mantém esses tokens.

### 9.2 Como isso se encaixaria nas pastas

`unifica/config/oidc.py` pode reunir parâmetros do cliente e do provedor. `unifica/auth/` pode receber rotas de entrada, callback e saída integradas ao Keycloak. `deploy/keycloak/` pode guardar uma exportação revisada da configuração do realm. As páginas do portal continuam usando a identidade autenticada para apresentar o conteúdo.

O desenho deve decidir quais dados pertencem ao provedor e quais pertencem ao banco escolar. Senhas de autenticação central e informações escolares têm responsabilidades diferentes. A ligação entre a identidade externa e o aluno local deve usar um identificador estável apropriado, e o logout precisa ter comportamento definido entre portal e provedor.

### 9.3 O que ainda precisa ser construído

É necessário criar e configurar o realm, registrar o cliente, definir URIs de redirecionamento, integrar uma biblioteca OIDC, implementar callback, validar a identidade recebida, mapear papéis e decidir persistência de sessão. O arquivo `realm-school.json` atual está vazio e não pode ser tratado como uma configuração pronta para importar.

O acesso a uma biblioteca escolar também depende da existência desse outro serviço e de sua integração ao provedor. O arquivo de documentação reservado para essa integração ainda não descreve uma implementação efetiva.

Referência para a etapa futura: [Keycloak e OpenID Connect](https://www.keycloak.org/securing-apps/oidc-layers).

## Parte 10 — Git e colaboração

### 10.1 Pasta, repositório, commit e remoto

A pasta contém arquivos de trabalho. O repositório Git registra versões desses arquivos. Um commit reúne um conjunto de mudanças com mensagem e autoria. Uma branch aponta para uma sequência de commits. Um remoto é um nome local associado a uma URL, geralmente `origin`.

Na inspeção desta edição, `origin` aponta para `https://github.com/kaua-devbr/SSO.git`. A configuração pode mudar, então confira `git remote -v` antes de publicar. O histórico anterior da conversa não deve ser usado como prova de qual destino está configurado hoje.

### 10.2 Comandos de leitura

| Comando | Explicação |
|---|---|
| `git status` | Exibe branch e alterações preparadas ou pendentes. |
| `git status --short --branch` | Mostra um resumo compacto com informações da branch. |
| `git diff` | Mostra mudanças dos arquivos rastreados ainda fora do índice. |
| `git diff --cached` | Mostra o conteúdo preparado para o próximo commit. |
| `git diff --check` | Procura problemas de espaços e marcadores de conflito no diff. |
| `git log --oneline -5` | Mostra os cinco commits recentes em formato compacto. |
| `git show <commit>` | Exibe metadados e alterações de um commit escolhido. |
| `git branch -vv` | Lista branches e relações de acompanhamento. |
| `git remote -v` | Mostra URLs de leitura e envio. |
| `git ls-files` | Lista os caminhos rastreados pelo repositório. |

### 10.3 Publicar mudanças de documentação

```powershell
git status
git add docs/LIVRO_UNIFICA.md
git diff --cached
git commit -m "Documenta arquitetura e funcionamento do UNIFICA"
git push
```

`git add` prepara a versão atual do arquivo no índice. Uma edição posterior exige outro `add` para entrar no mesmo commit. `commit -m` cria a versão local com a mensagem fornecida. `push` envia commits para o destino configurado. Na primeira publicação de uma branch, `git push -u origin nome-da-branch` também estabelece seu acompanhamento.

Um commit não implica envio automático no Git padrão. Isso depende de uma ação de Push, de uma operação Commit & Push no editor ou de um hook explicitamente instalado. Ao trabalhar em equipe, `git fetch origin` atualiza o conhecimento local sobre o remoto. `git pull --ff-only` atualiza a branch apenas quando o histórico pode avançar diretamente; se houver divergência, interrompe a operação para resolução explícita.

### 10.4 Branches e alterações de destino

`git switch -c nome` cria e seleciona uma branch. `git switch nome` seleciona uma existente. `git cherry-pick <commit>` aplica a mudança de um commit à branch atual e pode gerar conflitos. `git remote set-url origin URL` troca a URL de um remoto existente. `git remote add origin URL` cria uma conexão que ainda não existe. `git remote remove origin` remove essa configuração local.

`git bundle create arquivo.bundle main` empacota objetos e referências para transporte. `git bundle verify arquivo.bundle` verifica o pacote e seus pré-requisitos no repositório atual. `git fetch caminho-do-bundle main` importa objetos do pacote. Um bundle pode carregar histórico antigo e não precisa acompanhar a documentação normal do projeto.

Ao remover arquivos rastreados, o próximo commit precisa registrar as exclusões. O `.gitignore` atua principalmente sobre arquivos ainda não rastreados; acrescentar um padrão não remove retroativamente arquivos que já estão no histórico. Confirme sempre a lista do índice antes de publicar.

### 10.5 O mesmo fluxo no VS Code

Abra Source Control com Ctrl+Shift+G. Revise os diffs, prepare arquivos com o botão `+`, escreva uma mensagem e faça Commit. Use Push ou Commit & Push para enviar. O editor e o terminal operam sobre o mesmo repositório da pasta aberta. Se abrir outra cópia, como `TCC_SSO-publicar`, estará trabalhando em outra pasta e em outro estado local.

Referência operacional: [repositórios e remotos no VS Code](https://code.visualstudio.com/docs/sourcecontrol/repos-remotes).

## Parte 11 — Verificação e diagnóstico

### 11.1 Três níveis diferentes de verificação

Compilar Python verifica sintaxe. Importar o módulo verifica também a disponibilidade de bibliotecas e efeitos executados na importação. Fazer requisições à aplicação verifica rotas e renderização. Uma etapa não substitui automaticamente a próxima. Um arquivo de CRUD sintaticamente válido ainda pode conter SQL inválido.

Para compilar os arquivos do portal sem executar suas funções, use o exemplo abaixo em um arquivo temporário ou no Python. `compile` não grava arquivos `.pyc` e não executa o código compilado.

```python
from pathlib import Path

arquivos = [Path('app.py'), *Path('unifica').rglob('*.py')]
for arquivo in arquivos:
    compile(arquivo.read_bytes(), str(arquivo), 'exec')
print('Sintaxe verificada')
```

### 11.2 Roteiro de teste manual

| Passo | Resultado esperado |
|---|---|
| Abrir `/perfil` em sessão nova | Redirecionamento ao login. |
| Entrar com senha errada | Mensagem de credenciais inválidas e status 400. |
| Entrar com `maria` e `4321` após reinício | Perfil com nome Maria e nível normal. |
| Abrir novembro de 2026 e selecionar dia 6 | Dois eventos no painel. |
| Selecionar dia sem evento | Mensagem de ausência de eventos. |
| Passar de dezembro para o mês seguinte | Janeiro do ano seguinte. |
| Usar `?dia=texto` | Retorno à data padrão. |
| Buscar `Geografia` nos comunicados | Aviso correspondente. |
| Filtrar categoria sem resultado para a busca | Mensagem de nenhum comunicado encontrado. |
| Marcar um aviso e recarregar | O estado lido continua na mesma sessão. |
| Selecionar tema escuro e salvar | Páginas que herdam a base usam a paleta escura. |
| Informar senha atual incorreta | Erro e formulário de senha aberto. |
| Trocar por senha válida, sair e entrar | A nova senha funciona no mesmo processo. |
| Reiniciar o servidor | Senhas iniciais restauradas e sessão anterior inválida. |
| Visitar caminho inexistente | Página de erro com status 404. |

### 11.3 Exemplo de teste HTTP local

O trecho a seguir é um exercício executável com Flask instalado. Ele usa o cliente de teste da aplicação e verifica uma requisição real dentro do processo, sem abrir conexão com MySQL. Os testes próprios do repositório ainda estão vazios nesta edição.

```python
from app import app

with app.test_client() as cliente:
    resposta = cliente.get('/')
    assert resposta.status_code == 200

    resposta = cliente.post('/', data={'login': 'maria', 'senha': '4321'})
    assert resposta.status_code == 303
    assert resposta.headers['Location'].endswith('/perfil')

    resposta = cliente.get('/calendario?dia=2026-11-06')
    assert resposta.status_code == 200
    assert 'Apresentação'.encode() in resposta.data

    with cliente.session_transaction() as sessao:
        token = sessao['form_token']
    resposta = cliente.post('/sair', data={'form_token': token})
    assert resposta.status_code == 303
```

Esse exemplo pressupõe um processo recém-iniciado, com as contas iniciais. Ele não altera a senha. Um teste de alteração de senha deve restaurar o estado de demonstração ao terminar para não afetar outros testes no mesmo processo.

### 11.4 Como investigar erros frequentes

| Sintoma | Investigação |
|---|---|
| `ModuleNotFoundError: flask` | Confira o interpretador selecionado e instale Flask nele. |
| `TemplateNotFound` | Confira o nome passado a `render_template` e `template_folder`. |
| CSS sem efeito | Confira a URL em Network, o status HTTP e o arquivo ativo em `unifica/static`. |
| `BuildError` | Confira o endpoint passado a `url_for` e o registro do Blueprint. |
| Login funciona e depois desaparece | Confira reinícios do processo e a geração de nova `SECRET_KEY`. |
| POST retorna 400 | Confira o token do formulário e se a sessão ainda é válida. |
| `KeyError: UNIFICA_MYSQL_PASSWORD` | O módulo de conexão foi importado sem a variável exigida. |
| Erro de sintaxe SQL | Revise os rascunhos do CRUD e a correspondência de parâmetros. |
| `non-fast-forward` no Git | Compare histórico local e remoto antes de resolver a divergência. |
| Arquivo alterado não aparece no site | Confira se está editando a cópia ativa e se o servidor foi reiniciado. |

O projeto não traz uma suíte funcional que valide automaticamente todas as páginas. A documentação registra o comportamento observado no código; o resultado visual e o fluxo completo devem ser conferidos com Flask instalado e navegador.

## Parte 12 — Exercícios com respostas

### 12.1 HTML e Jinja

**Exercício.** Troque apenas `name="login"` por `name="usuario"` no template e explique o resultado antes de testar.

**Resposta.** A rota procura `request.form.get('login', '')`. Como o formulário passa a enviar outra chave, a rota recebe o padrão vazio e falha na autenticação. Alterar apenas `id` não teria esse efeito no servidor, mas exigiria atualizar o `for` do label.

**Exercício.** Explique por que um aviso deixa de mostrar o ponto após ser marcado como lido.

**Resposta.** O POST inclui seu ID na lista guardada na sessão. No próximo GET, a rota envia essa lista ao template. A condição `id not in lidos` passa a ser falsa e o HTML do indicador deixa de ser emitido.

### 12.2 CSS

**Exercício.** Mude o valor de `--destaque` no tema escuro e identifique quais componentes respondem.

**Resposta.** Os componentes que usam `var(--destaque)` dentro da raiz com `data-tema='escuro'` passam a usar a nova cor. Elementos com cores literais ou que não dependem dessa variável não acompanham a alteração.

**Exercício.** Por que o calendário usa sete colunas, mesmo quando uma semana possui poucos dias daquele mês?

**Resposta.** A grade representa dias da semana. Datas vizinhas completam a semana, mas são renderizadas como posições vazias quando não pertencem ao mês selecionado. A geometria é mantida.

### 12.3 Python e estado

**Exercício.** Por que usar `set` ao marcar avisos?

**Resposta.** O conjunto elimina repetições. Marcar o mesmo aviso duas vezes mantém apenas um identificador. Ao terminar, `sorted` produz uma lista ordenada para guardar na sessão.

**Exercício.** Alterar o nível da conta para `adm` libera alguma rota nova?

**Resposta.** O código atual não testa níveis nas rotas. A autenticação permite o acesso às páginas protegidas e o nível é exibido no perfil. Uma política de autorização ainda precisa ser criada.

**Exercício.** Por que a senha nova funciona depois do logout, mas desaparece após reiniciar o Flask?

**Resposta.** O logout limpa a sessão do navegador. O hash alterado está no dicionário em memória do processo. O reinício recria a lista com os hashes das senhas iniciais.

### 12.4 Próximos estudos com critério de conclusão

Uma extensão útil é implementar o botão Mostrar senha e testar teclado e leitor de tela. Outra é criar um teste automatizado de autorização quando houver regras de administrador. Para o banco, comece pelo esquema e por uma consulta de leitura que devolva resultados claros antes de ligar formulários de escrita.

Ao concluir uma funcionalidade, atualize seu estado na Parte 1, registre os campos recebidos, os resultados esperados e o que é persistido. A documentação deve acompanhar o comportamento que o usuário realmente consegue observar.


## Parte 13 — Catálogo completo do código inspecionado

### Elementos HTML e SVG presentes nos templates ativos

| Elemento | Função prática |
|---|---|
| `html` | Raiz que recebe idioma e atributos de aparência. |
| `head` | Região de metadados, título e folhas de estilo. |
| `meta` | Declara codificação e orientação de viewport. |
| `title` | Nome exibido na aba do navegador. |
| `link` | Conecta o HTML à folha de estilo. |
| `body` | Contém a interface da página. |
| `main` | Delimita o conteúdo principal. |
| `aside` | Agrupa a barra lateral. |
| `nav` | Agrupa links de navegação ou filtros. |
| `a` | Cria um link para rota, recurso ou histórico. |
| `img` | Carrega uma imagem por URL. |
| `div` | Agrupa blocos sem significado semântico específico. |
| `span` | Agrupa pequenos trechos inline. |
| `header` | Introduz a página, cartão ou seção. |
| `footer` | Agrupa conteúdo do rodapé. |
| `section` | Delimita assunto ou conjunto temático. |
| `article` | Representa um evento independente. |
| `h1` | Título principal da página. |
| `h2` | Título de seção ou componente. |
| `h3` | Subtítulo usado no perfil. |
| `h4` | Identificação de grupos de dados do perfil. |
| `p` | Parágrafo de texto. |
| `strong` | Informação com importância destacada. |
| `small` | Informação auxiliar, como horário relativo. |
| `ul` | Lista sem numeração. |
| `li` | Item da lista de comunicados. |
| `form` | Agrupa os campos enviados em uma requisição. |
| `input` | Campo de texto, senha, busca, checkbox ou valor oculto. |
| `label` | Identifica um campo, por associação for/id ou por envolvimento. |
| `button` | Controle acionável que pode enviar um formulário. |
| `select` | Lista de opções para tema ou fonte. |
| `option` | Alternativa que fornece o valor selecionado. |
| `details` | Região que pode ser expandida e recolhida. |
| `summary` | Controle de abertura da região details. |
| `svg` | Área de desenho vetorial. |
| `path` | Caminho desenhado por instruções e coordenadas. |
| `circle` | Círculo definido por centro e raio. |
| `rect` | Retângulo usado no ícone de cadeado. |

### Atributos encontrados e seus efeitos

| Atributo | Significado |
|---|---|
| `action` | Destino que recebe os campos do formulário. |
| `alt` | Alternativa textual da imagem. |
| `aria-current` | Indica qual item representa a página, data ou escolha atual. |
| `aria-hidden` | Controla se o elemento participa da árvore de acessibilidade. |
| `aria-label` | Nome acessível fornecido diretamente. |
| `aria-labelledby` | Identificador do elemento cujo texto nomeia a região. |
| `autocomplete` | Sugere o papel do campo ao preenchimento automático. |
| `charset` | Codificação declarada no documento. |
| `class` | Classes usadas por seletores CSS. |
| `content` | Valor associado ao metadado. |
| `cx` e `cy` | Coordenadas do centro de um círculo SVG. |
| `d` | Sequência de comandos do caminho SVG. |
| `data-fonte` e `data-tema` | Dados personalizados lidos pelos seletores CSS. |
| `fill` | Cor de preenchimento do desenho. |
| `for` | ID do campo identificado pelo label. |
| `height` e `width` | Dimensões de uma forma SVG neste projeto. |
| `href` | URL de um link ou folha de estilo. |
| `id` | Identificador de um elemento dentro do documento. |
| `lang` | Idioma principal. |
| `maxlength` e `minlength` | Limites de comprimento na validação nativa. |
| `method` | Método HTTP de envio. |
| `name` | Nome do campo enviado ou nome de metadado. |
| `open` | Estado inicialmente aberto de details. |
| `placeholder` | Dica exibida enquanto o campo está vazio. |
| `r` | Raio do círculo. |
| `readonly` | Campo de leitura pela interface. |
| `rel` | Relação do recurso com a página, como stylesheet. |
| `required` | Exigência de preenchimento na validação do navegador. |
| `role` | Papel semântico informado a tecnologias assistivas. |
| `rx` | Arredondamento horizontal dos cantos do retângulo SVG. |
| `selected` | Opção inicialmente selecionada. |
| `src` | Endereço do arquivo de imagem. |
| `stroke` | Cor do traço. |
| `stroke-linecap` | Forma das extremidades de segmentos. |
| `stroke-linejoin` | Forma das junções dos segmentos. |
| `stroke-width` | Espessura do traço. |
| `type` | Tipo do input ou comportamento do botão. |
| `value` | Valor inicial ou valor enviado pelo controle. |
| `viewBox` | Sistema de coordenadas interno do SVG. |
| `x` e `y` | Coordenadas iniciais do retângulo SVG. |

### Comandos dos caminhos SVG do login

O atributo `d` usa uma pequena linguagem de desenho. Letras maiúsculas indicam coordenadas absolutas; minúsculas indicam deslocamentos relativos à posição atual. Os desenhos desta revisão usam `M` para mover o ponto inicial, `L` ou `l` para segmentos de reta, `H` ou `h` para segmentos horizontais, `V` ou `v` para verticais, `c` para curvas de Bézier cúbicas, `s` para continuação suavizada dessas curvas, `a` para arcos elípticos e `z` para fechar o caminho. Por exemplo, `M2 9l10-5` move até a posição (2, 9) e desenha uma linha deslocando 10 unidades na horizontal e -5 na vertical. Os números são coordenadas da área definida pelo viewBox.

### JavaScript presente e previsto

O portal ativo resolve suas interações principalmente com links, formulários HTTP e details. A expressão `history.back()` da página de erro pede ao navegador que volte uma posição no histórico da aba. Não há arquivo JavaScript ativo carregado pelos templates inspecionados. Os arquivos vazios em `templates/static/js/` pertencem à estrutura antiga. Implementar Mostrar senha exigiria, por exemplo, capturar o clique do botão e alternar o atributo type do input entre password e text; esse comportamento ainda é um exercício futuro.

### 13.1 Propriedades CSS

Cada propriedade aparece com seu significado e um valor real do projeto. As regras posteriores registram outros usos da mesma propriedade.

| Propriedade | Significado | Primeiro exemplo encontrado |
|---|---|---|
| `--acento` | Variável personalizada da paleta ou sombra, consultada por var(). | `#4031c6` em `global.css` |
| `--ativo` | Variável personalizada da paleta ou sombra, consultada por var(). | `#a4a3ef` em `global.css` |
| `--background` | Variável personalizada da paleta ou sombra, consultada por var(). | `#E9EDF2` em `erro.css` |
| `--borda` | Variável personalizada da paleta ou sombra, consultada por var(). | `#dce2ec` em `global.css` |
| `--border` | Variável personalizada da paleta ou sombra, consultada por var(). | `#D5D9DF` em `erro.css` |
| `--botao` | Variável personalizada da paleta ou sombra, consultada por var(). | `#e1e4ff` em `global.css` |
| `--destaque` | Variável personalizada da paleta ou sombra, consultada por var(). | `#cdcef6` em `global.css` |
| `--fundo` | Variável personalizada da paleta ou sombra, consultada por var(). | `#fff` em `global.css` |
| `--menu` | Variável personalizada da paleta ou sombra, consultada por var(). | `#f0f1fc` em `global.css` |
| `--perigo` | Variável personalizada da paleta ou sombra, consultada por var(). | `#a02135` em `global.css` |
| `--primary` | Variável personalizada da paleta ou sombra, consultada por var(). | `#5558ED` em `erro.css` |
| `--primary-hover` | Variável personalizada da paleta ou sombra, consultada por var(). | `#4446D8` em `erro.css` |
| `--secundario` | Variável personalizada da paleta ou sombra, consultada por var(). | `#53637c` em `global.css` |
| `--sombra` | Variável personalizada da paleta ou sombra, consultada por var(). | `7px 10px 15px #20243e30` em `global.css` |
| `--suave` | Variável personalizada da paleta ou sombra, consultada por var(). | `#f4f6f9` em `global.css` |
| `--surface` | Variável personalizada da paleta ou sombra, consultada por var(). | `#FFFFFF` em `erro.css` |
| `--text-primary` | Variável personalizada da paleta ou sombra, consultada por var(). | `#111827` em `erro.css` |
| `--text-secondary` | Variável personalizada da paleta ou sombra, consultada por var(). | `#737B88` em `erro.css` |
| `--texto` | Variável personalizada da paleta ou sombra, consultada por var(). | `#20243e` em `global.css` |
| `accent-color` | Cor de destaque dos controles nativos. | `#3F55C5` em `login.css` |
| `align-items` | Alinhamento dos itens no eixo transversal de Flexbox ou eixo de bloco de Grid. | `center` em `erro.css` |
| `background` | Atalho de configuração do fundo. | `var(--background)` em `erro.css` |
| `background-color` | Cor do fundo da caixa. | `#ffffff` em `login.css` |
| `border` | Largura, estilo e cor das bordas. | `1px solid var(--border)` em `erro.css` |
| `border-bottom` | Borda inferior. | `2px solid var(--borda)` em `global.css` |
| `border-color` | Cor das bordas. | `var(--acento)` em `global.css` |
| `border-left` | Borda esquerda. | `4px solid transparent` em `global.css` |
| `border-left-color` | Cor da borda esquerda. | `var(--acento)` em `global.css` |
| `border-radius` | Arredondamento dos cantos. | `20px` em `erro.css` |
| `border-top` | Borda superior. | `3px solid var(--texto)` em `global.css` |
| `bottom` | Deslocamento a partir da borda inferior para posicionamento. | `.28rem` em `global.css` |
| `box-shadow` | Sombra definida por deslocamentos, desfoque e cor. | `0 10px 40px rgba(0, 0, 0, 0.06)` em `erro.css` |
| `box-sizing` | Regra de inclusão de padding e borda no tamanho declarado. | `border-box` em `erro.css` |
| `color` | Cor do texto e valor usado por currentColor. | `var(--text-primary)` em `erro.css` |
| `color-scheme` | Esquema de cores anunciado ao navegador para controles nativos. | `light` em `global.css` |
| `column-gap` | Espaço entre colunas. | `20px` em `perfil.css` |
| `cursor` | Formato do ponteiro. | `pointer` em `global.css` |
| `display` | Modelo de layout, como Grid ou Flexbox, ou ocultação com none. | `flex` em `erro.css` |
| `filter` | Efeitos visuais aplicados ao elemento. | `brightness(0) invert(1)` em `global.css` |
| `flex` | Atalho de crescimento, redução e tamanho base de item flexível. | `1 1 230px` em `global.css` |
| `flex-direction` | Direção principal de Flexbox. | `column` em `erro.css` |
| `flex-shrink` | Fator de redução de item flexível. | `0` em `login.css` |
| `flex-wrap` | Permissão de quebra dos itens em linhas. | `wrap` em `global.css` |
| `font` | Atalho de propriedades tipográficas. | `1rem/1.45 Arial, sans-serif` em `global.css` |
| `font-family` | Família de fonte e alternativas. | `'Inter', Arial, sans-serif` em `erro.css` |
| `font-size` | Tamanho da fonte. | `42px` em `erro.css` |
| `font-weight` | Peso da fonte. | `700` em `erro.css` |
| `gap` | Espaço entre itens ou trilhas. | `14px` em `erro.css` |
| `grid-template-columns` | Quantidade e dimensões das colunas. | `185px minmax(0, 1fr)` em `global.css` |
| `grid-template-rows` | Dimensões das linhas explícitas da grade. | `none` em `global.css` |
| `height` | Altura da caixa. | `76px` em `erro.css` |
| `justify-content` | Distribuição de espaço no eixo principal de Flexbox ou inline de Grid. | `center` em `erro.css` |
| `justify-items` | Alinhamento de itens no eixo inline de Grid. | `center` em `global.css` |
| `left` | Deslocamento pela borda esquerda. | `39px` em `perfil.css` |
| `letter-spacing` | Espaçamento entre caracteres. | `-1px` em `login.css` |
| `line-height` | Altura das linhas de texto. | `1.7` em `erro.css` |
| `list-style` | Marcadores de lista. | `none` em `global.css` |
| `margin` | Espaço externo da caixa. | `0` em `erro.css` |
| `margin-bottom` | Espaço externo no lado inferior. | `14px` em `erro.css` |
| `margin-left` | Espaço externo no lado esquerdo. | `37px` em `perfil.css` |
| `margin-right` | Espaço externo no lado direito. | `.4rem` em `global.css` |
| `margin-top` | Espaço externo no lado superior. | `36px` em `erro.css` |
| `max-width` | Limite máximo da largura. | `480px` em `erro.css` |
| `min-height` | Limite mínimo da altura. | `100vh` em `erro.css` |
| `min-width` | Limite mínimo da largura. | `0` em `global.css` |
| `object-fit` | Ajuste da imagem à caixa mantendo ou alterando proporções conforme o valor. | `contain` em `global.css` |
| `outline` | Contorno externo, usado para foco. | `2px solid var(--acento)` em `global.css` |
| `outline-offset` | Afastamento do contorno. | `3px` em `global.css` |
| `overflow` | Tratamento do conteúdo excedente, com corte ou rolagem. | `auto` em `global.css` |
| `padding` | Espaço interno da caixa. | `0` em `erro.css` |
| `padding-bottom` | Espaço interno no lado inferior. | `2rem` em `global.css` |
| `padding-left` | Espaço interno no lado esquerdo. | `23px` em `perfil.css` |
| `padding-top` | Espaço interno no lado superior. | `1rem` em `global.css` |
| `place-items` | Atalho de alinhamento nos dois eixos de Grid. | `center` em `global.css` |
| `position` | Modelo de posicionamento. | `sticky` em `global.css` |
| `row-gap` | Espaço entre linhas. | `1rem` em `global.css` |
| `text-align` | Alinhamento do texto e conteúdo inline. | `center` em `erro.css` |
| `text-decoration` | Decoração como sublinhado. | `none` em `erro.css` |
| `top` | Deslocamento pela borda superior. | `0` em `global.css` |
| `transition` | Transição visual entre estados. | `0.2s` em `erro.css` |
| `white-space` | Tratamento de espaços e quebras. | `nowrap` em `login.css` |
| `width` | Largura da caixa. | `100%` em `erro.css` |

### 13.2 Índice completo dos seletores e declarações

Localize aqui uma classe do HTML e acompanhe quais propriedades dão forma ao componente. As regras dentro de @media dependem também da largura de tela definida no arquivo original.


#### erro.css

| Seletor | Declarações |
|---|---|
| `:root` | `--primary: #5558ED; --primary-hover: #4446D8; --background: #E9EDF2; --surface: #FFFFFF; --text-primary: #111827; --text-secondary: #737B88; --border: #D5D9DF;` |
| `*` | `margin: 0; padding: 0; box-sizing: border-box;` |
| `body` | `min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px; background: var(--background); font-family: 'Inter', Arial, sans-serif; color: var(--text-primary);` |
| `.error-container` | `width: 100%; max-width: 480px; padding: 48px 40px; background: var(--surface); border-radius: 20px; text-align: center; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.06);` |
| `.error-icon` | `width: 76px; height: 76px; margin: 0 auto 28px; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: #e4b1b1; color: #E54848; font-size: 42px; font-weight: 700;` |
| `.error-container h1` | `margin-bottom: 14px; font-size: 26px; font-weight: 700;` |
| `.error-message` | `margin-bottom: 22px; color: var(--text-secondary); font-size: 15px; line-height: 1.7;` |
| `.error-code` | `margin-bottom: 28px; color: var(--text-secondary); font-size: 13px;` |
| `.error-code strong` | `color: var(--text-primary);` |
| `.error-actions` | `display: flex; flex-direction: column; gap: 14px;` |
| `.primary-button, .secondary-button` | `padding: 14px; border-radius: 9px; text-decoration: none; font-size: 14px; font-weight: 600; transition: 0.2s;` |
| `.primary-button` | `background: var(--primary); color: white;` |
| `.primary-button:hover` | `background: var(--primary-hover);` |
| `.secondary-button` | `border: 1px solid var(--border); color: var(--text-secondary);` |
| `.secondary-button:hover` | `background: #F6F7FB;` |
| `footer` | `margin-top: 36px; color: #A0A6AF; font-size: 12px;` |
| `.error-container` | `padding: 36px 24px;` |
| `.error-container h1` | `font-size: 22px;` |

#### global.css

| Seletor | Declarações |
|---|---|
| `:root` | `color-scheme: light; --fundo: #fff; --texto: #20243e; --secundario: #53637c; --menu: #f0f1fc; --ativo: #a4a3ef; --suave: #f4f6f9; --borda: #dce2ec; --destaque: #cdcef6; --acento: #4031c6; --botao: #e1e4ff; --perigo: #a02135; --sombra: 7px 10px 15px #20243e30;` |
| `:root[data-tema="escuro"]` | `color-scheme: dark; --fundo: #171a29; --texto: #f0f1ff; --secundario: #bfc9de; --menu: #22263b; --ativo: #41417a; --suave: #252a3d; --borda: #434960; --destaque: #34375b; --acento: #bcb4ff; --botao: #323663; --perigo: #ff9cab; --sombra: 7px 10px 15px #0005;` |
| `:root[data-fonte="grande"]` | `font-size: 118.75%;` |
| `.portal, .portal *` | `box-sizing: border-box;` |
| `.portal` | `display: grid; grid-template-columns: 185px minmax(0, 1fr); align-items: start; min-height: 100vh; margin: 0; background: var(--fundo); color: var(--texto); font: 1rem/1.45 Arial, sans-serif;` |
| `.portal h1` | `margin: 0 0 .65rem; font-size: clamp(1.65rem, 3vw, 2.2rem); line-height: 1.15;` |
| `.portal h2` | `margin: 0 0 .65rem; font-size: 1.2rem; line-height: 1.2;` |
| `.portal a` | `color: inherit;` |
| `.portal :focus-visible` | `outline: 2px solid var(--acento); outline-offset: 3px;` |
| `.portal :is(button, input, select)` | `font: inherit;` |
| `.portal button, .portal summary` | `cursor: pointer;` |
| `.portal-menu` | `position: sticky; top: 0; display: flex; flex-direction: column; height: 100vh; height: 100dvh; overflow: auto; background: var(--menu); padding: .75rem 0;` |
| `.portal-marca` | `display: grid; justify-items: center; margin-bottom: clamp(1rem, 12vh, 5rem); text-decoration: none; line-height: 1.15;` |
| `.portal-marca img` | `width: 84px; height: 62px; object-fit: contain;` |
| `.portal-marca strong` | `font-size: 1.55rem; margin-top: .45rem;` |
| `.portal-marca small` | `color: var(--secundario); font-size: .65rem; font-weight: 700;` |
| `.portal-menu nav` | `display: grid; gap: .15rem; padding: 0 .25rem 0 0;` |
| `.portal-menu nav a, .portal-sair button` | `display: flex; align-items: center; justify-content: flex-start; gap: .7rem; height: auto; min-height: 42px; padding: .5rem .85rem .5rem 1.15rem; border-left: 4px solid transparent; font-size: .8rem; text-decoration: none;` |
| `.portal-menu nav a[aria-current], .portal-menu nav a:hover` | `background: var(--ativo); border-left-color: var(--acento); border-radius: 0 6px 6px 0;` |
| `.portal-menu nav a[aria-current]` | `font-weight: 700;` |
| `.portal-menu nav img, .portal-sair img` | `width: 18px; height: 18px; object-fit: contain;` |
| `[data-tema="escuro"] .portal-menu nav img, [data-tema="escuro"] .portal-sair img` | `filter: brightness(0) invert(1);` |
| `.portal-sair` | `margin-top: auto; padding-top: 1rem;` |
| `.portal-sair button` | `color: var(--perigo); background: transparent; border: 0; font-weight: 700;` |
| `.portal-conteudo` | `width: min(100%, 1160px); min-width: 0; margin: 0 auto; padding: clamp(1rem, 5vw, 3.2rem);` |
| `.portal .perfil-conteudo` | `width: 100%; height: auto;` |
| `.portal .perfil-conteudo .dados` | `grid-template-columns: repeat(auto-fit, minmax(min(100%, 140px), 1fr)); height: auto; grid-template-rows: none; padding-bottom: 2rem; row-gap: 1rem;` |
| `.portal .perfil-conteudo .campo input` | `max-width: 100%;` |
| `[data-tema="escuro"] .perfil-conteudo .gmail` | `background: var(--suave);` |
| `[data-tema="escuro"] .perfil-conteudo :is(h3, h4, p)` | `color: var(--texto);` |
| `[data-tema="escuro"] .perfil-conteudo input` | `background: var(--suave); color: var(--texto);` |
| `[data-fonte="grande"] .perfil-conteudo :is(h4, p, input, button)` | `font-size: .86rem;` |
| `.painel` | `border: 1px solid var(--borda); border-radius: 15px; padding: clamp(.7rem, 2vw, 1.4rem); margin: 0;` |
| `.atalhos` | `display: flex; flex-wrap: wrap; gap: 1rem;` |
| `.atalhos a` | `text-decoration: none; background: var(--suave);` |
| `.botao` | `display: inline-block; color: var(--acento); background: var(--botao); border: 1px solid transparent; border-radius: 8px; padding: .45rem .75rem; font-weight: 700; text-decoration: none;` |
| `.portal a.botao` | `color: var(--acento);` |
| `.botao:hover` | `border-color: var(--acento);` |
| `.botao.principal` | `background: var(--acento); color: var(--fundo);` |
| `.agenda` | `display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr); gap: 1rem;` |
| `.mes` | `display: grid; grid-template-columns: 2rem 1fr 2rem; align-items: center; text-align: center; gap: .4rem; margin-bottom: 1rem;` |
| `.mes h2` | `margin: 0; font-size: 1rem;` |
| `.mes .botao` | `padding: .15rem; font-size: 1.25rem;` |
| `.grade` | `display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: clamp(.15rem, .6vw, .45rem);` |
| `.dia-semana` | `text-align: center; color: var(--secundario); font-size: .7rem;` |
| `.dia` | `display: grid; position: relative; place-items: center; min-height: clamp(2.15rem, 6vw, 4.3rem); border: 1px solid transparent; border-radius: 8px; background: var(--suave); text-decoration: none; font-size: .85rem;` |
| `a.dia:hover, .dia[aria-current="date"]` | `background: var(--botao); border-color: var(--acento);` |
| `.dia[aria-current="date"]` | `font-weight: 700;` |
| `.ponto` | `display: inline-block; width: .5rem; height: .5rem; border-radius: 50%; background: var(--acento);` |
| `.dia .ponto` | `position: absolute; bottom: .28rem; width: .25rem; height: .25rem;` |
| `.eventos h2` | `color: var(--secundario); font-size: .95rem;` |
| `.eventos article` | `margin-top: .65rem; background: var(--suave); border-left: 3px solid var(--acento); padding: .45rem 1rem; border-radius: 0 8px 8px 0;` |
| `.eventos article strong` | `color: var(--acento); font-size: .82rem;` |
| `.eventos p` | `margin: 0; font-size: .88rem;` |
| `.avisos` | `max-width: 700px; margin: auto;` |
| `.barra-avisos, .titulo-avisos` | `display: flex; align-items: center; gap: .9rem; justify-content: space-between; flex-wrap: wrap;` |
| `.barra-avisos` | `margin-bottom: 2rem;` |
| `.titulo-avisos h1` | `margin: 0;` |
| `.busca` | `flex: 1 1 230px; display: flex; gap: .35rem;` |
| `.busca input` | `width: 100%; min-width: 0;` |
| `.portal :is(input, select)` | `border: 1px solid var(--borda); color: var(--texto); background: var(--suave); border-radius: 6px; padding: .5rem;` |
| `.avatar` | `display: grid; place-items: center; width: 2.5rem; height: 2.5rem; border-radius: 50%; background: var(--botao); text-decoration: none; font-weight: 700;` |
| `.portal .filtros` | `display: flex; flex-wrap: wrap; gap: .3rem; padding: 0; margin: 1.15rem 0 .5rem;` |
| `.portal .filtros a` | `display: block; height: auto; padding: .4rem .6rem; border-radius: 6px; color: var(--secundario); font-size: .83rem; text-decoration: none;` |
| `.portal .filtros a[aria-current]` | `color: var(--fundo); background: var(--texto);` |
| `.lista-avisos` | `padding: 0; list-style: none;` |
| `.lista-avisos li` | `display: flex; flex-wrap: wrap; justify-content: space-between; gap: .65rem; padding: 1rem .25rem; border-bottom: 2px solid var(--borda);` |
| `.lista-avisos h2` | `font-size: 1rem; margin: 0 0 .15rem;` |
| `.lista-avisos h2 .ponto` | `margin-right: .4rem;` |
| `.lista-avisos p` | `margin: 0;` |
| `.aviso-acoes` | `display: grid; justify-items: start; gap: .3rem; color: var(--secundario); font-size: .8rem;` |
| `.configuracoes` | `max-width: 840px; margin: auto;` |
| `.configuracoes section + section` | `margin-top: clamp(2rem, 7vh, 5rem); border-top: 3px solid var(--texto); padding-top: .9rem;` |
| `.configuracoes section > :is(h1, h2)` | `text-align: center; font-size: 1.65rem;` |
| `.configuracoes .destaque` | `background: var(--destaque); border: 0; border-radius: 25px; padding: 1rem clamp(1rem, 4vw, 2.4rem);` |
| `.configuracoes .painel + .painel` | `margin-top: 1rem;` |
| `.configuracoes .seguranca, .preferencias .painel` | `box-shadow: var(--sombra);` |
| `.seguranca` | `text-align: center;` |
| `.seguranca > p` | `font-size: .82rem; margin: .55rem 0 0;` |
| `.form-senha` | `display: grid; gap: .7rem; max-width: 380px; margin: 1rem auto; text-align: left;` |
| `.form-senha label` | `display: grid; gap: .25rem;` |
| `.form-senha p` | `margin: 0; font-size: .8rem;` |
| `.preferencias label` | `display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; justify-content: space-between; font-weight: 700;` |
| `.preferencias select` | `width: min(100%, 300px); text-align: center;` |
| `.preferencias > button` | `margin-top: 1rem;` |
| `.mensagem` | `padding: .65rem; background: var(--suave); border-left: 3px solid var(--acento);` |
| `.mensagem.erro-senha` | `border-color: var(--perigo);` |
| `.agenda` | `grid-template-columns: 1fr;` |
| `.portal` | `grid-template-columns: 58px minmax(0, 1fr);` |
| `.portal-marca img` | `width: 43px; height: 40px;` |
| `.portal-marca :is(strong, small), .portal-menu nav span, .portal-sair span` | `display: none;` |
| `.portal-menu nav a, .portal-sair button` | `justify-content: center; padding: .45rem; width: 100%;` |

#### login.css

| Seletor | Declarações |
|---|---|
| `*` | `margin: 0; padding: 0; box-sizing: border-box;` |
| `body` | `font-family: Arial, Helvetica, sans-serif; background-color: #ffffff; color: #111a30; min-height: 100vh; display: flex; justify-content: center; align-items: flex-start;` |
| `.login-container` | `width: 100%; max-width: 456px; padding: 39px 28px 24px;` |
| `.header` | `display: flex; align-items: center; gap: 12px; margin-bottom: 36px;` |
| `.logo` | `width: 40px; height: 40px; background-color: #3F55C5; border-radius: 12px; display: flex; align-items: center; justify-content: center;` |
| `.logo svg` | `width: 24px; height: 24px; color: white;` |
| `.header-text h2` | `font-size: 16px; font-weight: 600;` |
| `.header-text p` | `font-size: 12px; color: #64748b;` |
| `.welcome` | `margin-bottom: 36px;` |
| `.welcome h1` | `font-size: 29px; font-weight: 700; letter-spacing: -1px; margin-bottom: 9px;` |
| `.welcome p` | `font-size: 14px; color: #64748b;` |
| `.login-form` | `display: flex; flex-direction: column; gap: 27px;` |
| `.form-group` | `display: flex; flex-direction: column; gap: 10px;` |
| `.form-group label` | `font-size: 14px; font-weight: 500;` |
| `.input-container` | `height: 50px; padding: 0 14px; display: flex; align-items: center; gap: 12px; border: 1px solid #cbd5e1; border-radius: 12px; transition: border-color 0.2s;` |
| `.input-container:focus-within` | `border-color: #3F55C5;` |
| `.input-container svg` | `width: 17px; height: 17px; color: #8ba0bd; flex-shrink: 0;` |
| `.input-container input` | `width: 100%; height: 100%; border: none; outline: none; background: transparent; font-size: 14px; color: #111a30;` |
| `.input-container input::placeholder` | `color: #8ba0bd;` |
| `.form-group small` | `font-size: 12px; color: #8ba0bd;` |
| `.password-toggle` | `display: flex; align-items: center; justify-content: center; background: none; border: none; cursor: pointer;` |
| `.password-toggle svg` | `width: 19px; height: 19px;` |
| `.form-options` | `display: flex; align-items: center; justify-content: space-between; margin-top: 2px; font-size: 13px;` |
| `.remember` | `display: flex; align-items: center; gap: 10px; cursor: pointer;` |
| `.remember input` | `width: 18px; height: 18px; accent-color: #3F55C5; cursor: pointer;` |
| `.form-options a` | `color: #3F55C5; text-decoration: none; font-weight: 500;` |
| `.login-button` | `height: 53px; display: flex; align-items: center; justify-content: center; gap: 12px; background-color: #3F55C5; color: white; border: none; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; box-shadow: 0 5px 12px rgba(40, 96, 237, 0.22); transition: background-color 0.2s;` |
| `.login-button:hover` | `background-color: #3F55C5;` |
| `.login-button span` | `font-size: 20px;` |
| `.footer` | `display: flex; align-items: center; gap: 12px; margin-top: 29px;` |
| `.footer .line` | `flex: 1; height: 1px; background-color: #dce3ee;` |
| `.footer p` | `font-size: 11px; color: #8ba0bd; letter-spacing: 1px; white-space: nowrap;` |
| `.login-container` | `padding: 32px 24px;` |
| `.welcome h1` | `font-size: 26px;` |
| `.login-error` | `color: #b51e25;` |

#### perfil.css

| Seletor | Declarações |
|---|---|
| `*` | `margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif;` |
| `body` | `background-color: #f0f1f5; min-height: 100vh; display: flex; justify-content: center; align-items: center;` |
| `.container` | `width: 1162px; height: 653px; display: flex; background-color: white; overflow: hidden;` |
| `.menu` | `width: 195px; height: 99%; background-color: #f1f1ff; position: relative; flex-shrink: 0;` |
| `.logo` | `margin-top: 8px; margin-left: 37px; margin-bottom: 85px;` |
| `.logo img` | `width: 100px; height: 70px; object-fit: contain; display: block;` |
| `.logo h2` | `font-size: 25px; color: #20243b;` |
| `.logo p` | `font-size: 10px; color: gray; font-weight: bold;` |
| `nav` | `padding: 0 0 0 6px;` |
| `nav a` | `height: 42px; display: flex; align-items: center; gap: 18px; padding-left: 23px; text-decoration: none; color: #303348; font-size: 12px;` |
| `nav a img` | `width: 17px; height: 17px;` |
| `nav a.selecionado` | `background-color: #9799ee; color: #17133e; font-weight: bold; border-radius: 6px; border-left: 5px solid #4555ed; padding-left: 18px;` |
| `.sair` | `position: absolute; bottom: 27px; left: 39px; background: none; border: 0; padding: 0; cursor: pointer; display: flex; align-items: center; gap: 12px; color: #b51e25; font-size: 13px; font-weight: bold;` |
| `.sair img` | `width: 20px; height: 20px;` |
| `.conteudo` | `width: 967px; height: 100%; display: flex; flex-direction: column;` |
| `.usuario` | `height: 180px; min-height: 180px; display: flex; align-items: center; padding-left: 58px; padding-top: 10px;` |
| `.foto` | `width: 52px; height: 52px; border-radius: 50%; background-color: #495be5; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px;` |
| `.usuario-info` | `margin-left: 5px;` |
| `.usuario-info h3` | `font-size: 18px; color: #111;` |
| `.usuario-info p` | `font-size: 12px; color: #77788a; font-weight: bold;` |
| `.dados` | `height: 285px; min-height: 285px; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: 105px 105px; padding: 33px 35px 0; column-gap: 20px;` |
| `.campo` | `display: flex; flex-direction: column; align-items: center;` |
| `.campo h4` | `font-size: 16px; margin-bottom: 5px; color: #111;` |
| `.campo input` | `width: 170px; height: 39px; border: none; border-radius: 30px; background-color: #cecff8; text-align: center; color: #77788a; font-size: 11px; font-weight: bold;` |
| `.gmail` | `flex: 1; background-color: #e2f0fa; padding: 0 22px; position: relative;` |
| `.gmail h3` | `font-size: 16px; color: #111; position: absolute; top: -17px; left: 0;` |
| `.lista-gmail` | `padding-top: 47px;` |
| `.lista-gmail p` | `font-size: 12px; font-weight: bold; margin-bottom: 17px; color: #111;` |
| `.lista-gmail button` | `margin-left: 4px; padding: 16px 8px; border: none; background-color: #dedfff; color: #4d5eea; font-size: 14px; font-weight: bold; cursor: pointer;` |
| `.lista-gmail button:hover` | `background-color: #c9cbfa;` |
| `body` | `align-items: flex-start;` |
| `.container` | `width: 100%; height: auto; min-height: 100vh;` |
| `.menu` | `width: 75px; min-width: 75px;` |
| `.logo` | `margin-left: 10px;` |
| `.logo img` | `width: 50px;` |
| `.logo h2, .logo p` | `display: none;` |
| `nav a` | `justify-content: center; padding: 0;` |
| `nav a.selecionado` | `padding: 0;` |
| `nav a img` | `width: 20px; height: 20px;` |
| `nav a` | `font-size: 0;` |
| `.sair` | `left: 25px;` |
| `.sair` | `font-size: 0;` |
| `.conteudo` | `width: calc(100% - 75px);` |
| `.usuario` | `padding-left: 15px;` |
| `.dados` | `height: auto; min-height: 285px; grid-template-columns: repeat(2, 1fr); padding: 20px 5px; gap: 25px 5px;` |
| `.campo input` | `width: 125px;` |
| `.gmail` | `min-height: 190px;` |

### 13.3 Código Python com comentários de leitura por bloco

Os trechos abaixo preservam o código desta revisão para acompanhar os capítulos anteriores. Eles formam uma fotografia da implementação; a versão executada continua sendo a dos arquivos originais.


#### app.py


```python
from secrets import token_hex

from flask import Flask

from unifica.portal.routes import portal

app = Flask(
    __name__,
    template_folder="unifica/templates",
    static_folder="unifica/static",
    static_url_path="/static",
)
app.config["SECRET_KEY"] = token_hex(32)
app.register_blueprint(portal)

if __name__ == "__main__":
    app.run()
```

#### unifica/auth/decorators.py

- `login_required` — Envolve uma função e valida sessão e token antes de executá-la.

```python
from functools import wraps
from secrets import compare_digest

from flask import abort, redirect, request, session, url_for


def login_required(view):
    @wraps(view)
    def protected(*args, **kwargs):
        if not session.get("logado"):
            return redirect(url_for("portal.login"))
        if request.method == "POST":
            token = session.get("form_token")
            submitted = request.form.get("form_token", "")
            if not token or not compare_digest(token.encode(), submitted.encode()):
                abort(400)
        return view(*args, **kwargs)

    return protected
```

#### unifica/portal/routes.py

- `login` — Confere formulário e cria sessão. A normalização do identificador ocorre antes da comparação de hash.
- `perfil` — Renderiza nome e nível da sessão.
- `inicio` — Entrega a página de atalhos.
- `notas` — Entrega a página de ausência de registros.
- `calendario` — Interpreta data, calcula meses e prepara semanas e eventos.
- `comunicados` — Processa leitura no POST e filtros no GET.
- `configuracoes` — Escolhe aparência ou senha pelo campo acao e redireciona após processar.
- `sair` — Limpa a sessão e retorna ao login.
- `erro_portal` — Renderiza o código de erro preservando o status HTTP.

```python
from calendar import Calendar
from datetime import date, timedelta
from secrets import token_urlsafe
from threading import Lock

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from unifica.auth.decorators import login_required

portal = Blueprint("portal", __name__)

USUARIOS_DEMO = [
    {"login": "zezinho", "senha": generate_password_hash("1234"), "nivel": "adm", "nome": "Zezinho"},
    {"login": "maria", "senha": generate_password_hash("4321"), "nivel": "normal", "nome": "Maria"},
]
senha_lock = Lock()

MESES = (
    "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
    "agosto", "setembro", "outubro", "novembro", "dezembro",
)
DIAS = ("Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo")
EVENTOS = {
    date(2026, 11, 6): [
        ("09:00–10:00", "Reunião de Alinhamento Semanal"),
        ("14:30–16:00", "Apresentação do Projeto"),
    ],
    date(2026, 11, 9): [("10:00", "Atividade de Geografia")],
    date(2026, 11, 12): [("14:00", "Entrega de PNT Desktop")],
    date(2026, 11, 16): [("09:00", "Reunião de turma")],
    date(2026, 11, 20): [("10:00", "Aulão para o Enem")],
    date(2026, 11, 25): [("13:00", "Apresentações da turma")],
    date(2026, 11, 30): [("09:00", "Encerramento do mês")],
}
CATEGORIAS = {
    "todos": "Todos",
    "prazos": "Prazos e Entregas",
    "avisos": "Avisos Importantes",
    "calendario": "Calendário",
}
COMUNICADOS = [
    (1, "calendario", "Calendário Acadêmico", "Confira as novas datas do calendário acadêmico.", "Há 2 dias"),
    (2, "prazos", "Atividade Pendente", "Entrega do trabalho de Geografia até sexta-feira.", "Há 3 dias"),
    (3, "avisos", "Aviso Importante", "Mudança na sala de aula de Programação.", "Há 1 semana"),
    (4, "prazos", "Atividade Pendente", "Entrega do trabalho de PNT Desktop até amanhã.", "Há 2 semanas"),
    (5, "avisos", "Aviso Importante", "Aulão para o Enem na próxima quinta-feira.", "Há 3 semanas"),
]


@portal.route("/", methods=["GET", "POST"])
def login():
    if session.get("logado"):
        return redirect(url_for("portal.perfil"))

    if request.method == "GET":
        return render_template("login.html")

    identificador = request.form.get("login", "").strip().lower()
    senha = request.form.get("senha", "")

    for usuario in USUARIOS_DEMO:
        if usuario["login"] == identificador and len(senha) <= 128 and check_password_hash(usuario["senha"], senha):
            session.clear()
            session["logado"] = True
            session["nivel"] = usuario["nivel"]
            session["usuario"] = usuario["nome"]
            session["login"] = usuario["login"]
            session["form_token"] = token_urlsafe(32)
            return redirect(url_for("portal.perfil"), code=303)

    flash("Login ou senha inválidos.")
    return render_template("login.html"), 400


@portal.get("/perfil")
@login_required
def perfil():
    return render_template("perfil.html", nome=session["usuario"], nivel=session["nivel"])


@portal.get("/inicio")
@login_required
def inicio():
    return render_template("dashboard.html")


@portal.get("/notas")
@login_required
def notas():
    return render_template("notas.html")


@portal.get("/calendario")
@login_required
def calendario():
    try:
        selecionado = date.fromisoformat(request.args.get("dia", "2026-11-06"))
        if not 1900 <= selecionado.year <= 2100:
            raise ValueError
    except ValueError:
        selecionado = date(2026, 11, 6)

    primeiro = selecionado.replace(day=1)
    anterior = (primeiro - timedelta(days=1)).replace(day=1)
    seguinte = (primeiro + timedelta(days=32)).replace(day=1)
    return render_template(
        "calendario.html",
        selecionado=selecionado,
        titulo_mes=f"{MESES[selecionado.month - 1].capitalize()} de {selecionado.year}",
        titulo_dia=f"{DIAS[selecionado.weekday()]}, {selecionado.day:02d} de {MESES[selecionado.month - 1]}",
        semanas=Calendar(firstweekday=6).monthdatescalendar(selecionado.year, selecionado.month),
        anterior=anterior if anterior.year >= 1900 else None,
        seguinte=seguinte if seguinte.year <= 2100 else None,
        eventos=EVENTOS,
    )


@portal.route("/comunicados", methods=["GET", "POST"])
@login_required
def comunicados():
    categoria = request.args.get("categoria", "todos")
    if categoria not in CATEGORIAS:
        categoria = "todos"
    busca = request.args.get("busca", "").strip()[:100]
    if request.method == "POST":
        lidos = set(session.get("comunicados_lidos", []))
        comunicado = request.form.get("comunicado")
        lidos.update(item[0] for item in COMUNICADOS if comunicado in ("todos", str(item[0])))
        session["comunicados_lidos"] = sorted(lidos)
        return redirect(url_for("portal.comunicados", categoria=categoria, busca=busca), code=303)

    resultados = [
        item for item in COMUNICADOS
        if (categoria == "todos" or item[1] == categoria)
        and busca.casefold() in f"{item[2]} {item[3]}".casefold()
    ]
    return render_template(
        "comunicados.html", comunicados=resultados, categorias=CATEGORIAS,
        categoria=categoria, busca=busca, lidos=session.get("comunicados_lidos", []),
    )


@portal.route("/configuracoes", methods=["GET", "POST"])
@login_required
def configuracoes():
    usuario = next(item for item in USUARIOS_DEMO if item["login"] == session["login"])
    if request.method == "POST":
        if request.form.get("acao") == "aparencia":
            tema = request.form.get("tema")
            fonte = request.form.get("fonte")
            if tema in ("claro", "escuro") and fonte in ("normal", "grande"):
                session["tema"] = tema
                session["fonte"] = fonte
                flash("Preferências salvas.", "sucesso")
        elif request.form.get("acao") == "senha":
            atual = request.form.get("senha_atual", "")
            nova = request.form.get("nova_senha", "")
            confirmacao = request.form.get("confirmacao", "")
            with senha_lock:
                if len(atual) > 128 or not check_password_hash(usuario["senha"], atual):
                    flash("A senha atual está incorreta.", "erro-senha")
                elif not 8 <= len(nova) <= 128:
                    flash("A nova senha deve ter entre 8 e 128 caracteres.", "erro-senha")
                elif nova != confirmacao:
                    flash("A confirmação deve ser igual à nova senha.", "erro-senha")
                elif nova == atual:
                    flash("Escolha uma senha diferente da atual.", "erro-senha")
                else:
                    usuario["senha"] = generate_password_hash(nova)
                    usuario["senha_atualizada"] = date.today()
                    flash("Senha de demonstração alterada.", "sucesso")
        return redirect(url_for("portal.configuracoes"), code=303)

    return render_template("configuracoes.html", senha_atualizada=usuario.get("senha_atualizada"))


@portal.post("/sair")
@login_required
def sair():
    session.clear()
    return redirect(url_for("portal.login"), code=303)


@portal.app_errorhandler(404)
@portal.app_errorhandler(500)
def erro_portal(erro):
    return render_template("erro.html", codigo=erro.code), erro.code
```

#### unifica/crud_usuarios/services/conexao.py


```python
from os import environ

import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password=environ["UNIFICA_MYSQL_PASSWORD"],
    database="UNIFICA"
)

cursor = conexao.cursor()
```

#### unifica/crud_usuarios/services/login.py

- `Cadastrar_usuario` — Rascunho de inserção com parâmetros ainda vazios.
- `Deletar_usuario` — Rascunho de exclusão com condição SQL incompleta.
- `Deletar_notas` — Rascunho que ainda repete a tabela de alunos.
- `Consultar_usuario` — Rascunho de consulta com condição inválida e resultado sem retorno.
- `Atualizar_dados` — Rascunho de atualização que exige correção de variável, tabela e parâmetros.

```python
if __package__:
    from .conexao import conexao
else:
    from conexao import conexao

cursor = conexao.cursor()

def Cadastrar_usuario():
    cursor = conexao.cursor()
    login = "INSERT INTO aluno(nome,idade,apelido,turma,genero,estado,email,senha,escola) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    valores = ()
    cursor.execute(login,valores)
    conexao.commit()

def Deletar_usuario():
    cursor = conexao.cursor()
    deletar = "DELETE FROM aluno WHERE *VALOR (%s,%s,%s)"
    valores = ()
    cursor.execute(deletar,valores)
    conexao.commit()


def Deletar_notas():
    cursor = conexao.cursor()
    deletar = "DELETE FROM aluno WHERE *VALOR (%s,%s,%s)"
    valores = ()
    cursor.execute(deletar,valores)
    conexao.commit()

def Consultar_usuario():
    cursor = conexao.cursor()
    consultar = "SELECT * FROM aluno WHERE *VALOR (%s,%s,%s)"
    valores = ()
    cursor.execute(consultar,valores)
    cursor.fetchall()

def Atualizar_dados():
    match consulta:
        case "nome":
            editar = 'UPDATE personagens SET nome = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "id":
            editar = 'UPDATE personagens SET id = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "idade":
            editar = 'UPDATE personagens SET idade = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "escola":
            editar = 'UPDATE personagens SET escola = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "senha":
            editar = 'UPDATE personagens SET senha = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "apelido":
            editar = 'UPDATE personagens SET apelido = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "genero":
            editar = 'UPDATE personagens SET genero = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "estado":
            editar = 'UPDATE personagens SET estado = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "email":
            editar = 'UPDATE personagens SET email = %s WHERE id_Personagem = %s'
            valores = ()
            cursor.execute(editar,valores)
            conexao.commit()
        case "":
            pass

# OBS: * = editar quando Flask for finalizado
```

### 13.4 Referência de todas as chamadas Python

O índice registra as chamadas realmente encontradas, inclusive métodos encadeados. Relacione cada chamada aos capítulos de Python, funcionalidades e CRUD. Uma chamada depende do objeto à esquerda do ponto: get() em uma sessão lê estado; get() em um Blueprint registra uma rota.


#### app.py

- `Flask` — Cria a aplicação.
- `app.register_blueprint` — Registra o grupo de rotas.
- `app.run` — Inicia o servidor local.
- `token_hex` — Gera a chave da aplicação.

#### unifica/auth/decorators.py

- `abort` — Interrompe com código HTTP.
- `compare_digest` — Compara os tokens recebidos em bytes.
- `redirect` — Devolve redirecionamento HTTP.
- `request.form.get` — Lê campo do formulário.
- `session.get` — Lê valor da sessão.
- `submitted.encode` — Converte string em bytes para comparar tokens.
- `token.encode` — Converte string em bytes para comparar tokens.
- `url_for` — Gera endereço pelo endpoint.
- `view` — Executa a função original protegida com os argumentos recebidos.
- `wraps` — Preserva metadados da função original.

#### unifica/crud_usuarios/services/conexao.py

- `conexao.cursor` — Cria cursor MySQL.
- `mysql.connector.connect` — Abre conexão ao MySQL.

#### unifica/crud_usuarios/services/login.py

- `conexao.commit` — Confirma transação.
- `conexao.cursor` — Cria cursor MySQL.
- `cursor.execute` — Executa SQL com parâmetros.
- `cursor.fetchall` — Lê linhas restantes do resultado.

#### unifica/portal/routes.py

- `(primeiro + timedelta(days=32)).replace` — Produz uma data com o dia substituído.
- `(primeiro - timedelta(days=1)).replace` — Produz uma data com o dia substituído.
- `Blueprint` — Cria o conjunto de rotas.
- `Calendar` — Configura o primeiro dia da semana.
- `Calendar(firstweekday=6).monthdatescalendar` — Produz semanas completas com objetos date.
- `Lock` — Cria o bloqueio usado com with na alteração de senha.
- `MESES[selecionado.month - 1].capitalize` — Coloca inicial do mês em maiúscula.
- `busca.casefold` — Normaliza caixa para comparação textual na busca.
- `check_password_hash` — Verifica senha candidata.
- `date` — Cria data por ano, mês e dia.
- `date.fromisoformat` — Interpreta a data ISO da URL.
- `date.today` — Obtém a data do servidor.
- `f'{item[2]} {item[3]}'.casefold` — Normaliza caixa para comparação textual na busca.
- `flash` — Registra mensagem para renderização.
- `generate_password_hash` — Gera hash de senha.
- `len` — Conta caracteres.
- `lidos.update` — Acrescenta IDs ao conjunto.
- `next` — Obtém a primeira conta que atende ao gerador; a ausência levantaria StopIteration.
- `portal.app_errorhandler` — Registra tratamento de erro.
- `portal.get` — Registra rota GET.
- `portal.post` — Registra rota POST.
- `portal.route` — Registra rota e métodos.
- `redirect` — Devolve redirecionamento HTTP.
- `render_template` — Produz HTML com os dados fornecidos.
- `request.args.get` — Lê parâmetro da URL.
- `request.args.get('busca', '').strip` — Remove espaços nas extremidades.
- `request.form.get` — Lê campo do formulário.
- `request.form.get('login', '').strip` — Remove espaços nas extremidades.
- `request.form.get('login', '').strip().lower` — Converte letras do identificador para minúsculas.
- `selecionado.replace` — Produz uma data com o dia substituído.
- `selecionado.weekday` — Obtém o índice do dia da semana.
- `session.clear` — Limpa estado da sessão.
- `session.get` — Lê valor da sessão.
- `set` — Cria conjunto de IDs sem duplicatas.
- `sorted` — Produz lista ordenada de IDs.
- `str` — Converte ID numérico para texto.
- `timedelta` — Representa deslocamento em dias.
- `token_urlsafe` — Gera token de formulário.
- `url_for` — Gera endereço pelo endpoint.
- `usuario.get` — Lê a data opcional de alteração de senha.

### 13.5 Referências adicionais

- [Elementos HTML](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements)
- [Referência CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference)
- [Tutorial Python](https://docs.python.org/3/tutorial/)
- [Segurança no Flask](https://flask.palletsprojects.com/en/stable/web-security/)
- [Utilitários e hashes no Werkzeug](https://werkzeug.palletsprojects.com/en/stable/utils/)
- [Execução parametrizada no MySQL Connector](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html)
- [Referência do Git](https://git-scm.com/docs)
