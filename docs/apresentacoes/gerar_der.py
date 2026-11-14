"""Gera apresentacao PDF vetorial do modelo proposto, sem acessar bancos."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = Path(__file__).parent / 'UNIFICA_Modelo_DER.pdf'
pdfmetrics.registerFont(TTFont('ArialLocal', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBoldLocal', 'C:/Windows/Fonts/arialbd.ttf'))
C = canvas.Canvas(str(OUT), pagesize=(960, 540))
C.setTitle('UNIFICA | Proposta de modelo DER e dicionário de dados')
C.setAuthor('Projeto UNIFICA')
NAVY='#18243D'; PURPLE='#6256DB'; PALE='#EEEDFF'; INK='#25334A'; MUTED='#52627A'
page=0
def para(text,x,y,w,size=17,color=INK,bold=False):
    p=Paragraph(text,ParagraphStyle('p',fontName='ArialBoldLocal' if bold else 'ArialLocal',fontSize=size,leading=size*1.32,textColor=HexColor(color)))
    aw,ah=p.wrap(w,450)
    p.drawOn(C,x,540-y-ah)
    return ah
def rect(x,y,w,h,color):
    C.setFillColor(HexColor(color));C.roundRect(x,540-y-h,w,h,10,fill=1,stroke=0)
def start(title,subtitle='PROPOSTA • MODELAGEM ANTES DA IMPLEMENTAÇÃO'):
    global page
    page+=1;C.setFillColor(white);C.rect(0,0,960,540,fill=1,stroke=0)
    rect(0,0,960,9,PURPLE)
    para('UNIFICA  /  BANCO DE DADOS',42,25,850,12,PURPLE,True)
    para(title,42,58,880,29,NAVY,True)
    para(subtitle,42,103,880,11,MUTED)
    C.setStrokeColor(HexColor('#DCE1EC'));C.line(42,40,918,40)
    para('TCC • SSO escolar | Dados fictícios | Modelo proposto, ainda não implementado',42,511,800,10,MUTED)
    para(f'{page:02}',878,508,40,13,PURPLE,True)
def end():C.showPage()
def bullets(items):
    y=151
    for head,body in items:
        rect(42,y,5,50,PURPLE)
        para(head,62,y,845,18,NAVY,True)
        h=para(body,62,y+27,845,15)
        y+=max(77,h+40)
def table(headers,rows,widths=None):
    widths=widths or [250,240,386]
    x0=42;y=145;rowh=min(45,318/(len(rows)+1))
    x=x0
    for h,w in zip(headers,widths):
        rect(x,y,w-3,rowh,PURPLE);para(h,x+10,y+8,w-22,13,'#FFFFFF',True);x+=w
    y+=rowh
    for i,row in enumerate(rows):
        x=x0
        for text,w in zip(row,widths):
            rect(x,y,w-3,rowh-2,PALE if i%2==0 else '#F6F8FB');para(text,x+10,y+7,w-22,12.5);x+=w
        y+=rowh
def note(text):para(text,44,464,870,12,MUTED)
def entity(x,y,title,fields,w=330):
    rect(x,y,w,112,PALE);rect(x,y,w,30,PURPLE)
    para(title,x+12,y+5,w-24,15,'#FFFFFF',True)
    for i,t in enumerate(fields):para(t,x+12,y+39+i*22,w-24,12)
def link(x1,y1,x2,y2,label,lx,ly):
    C.setStrokeColor(HexColor(MUTED));C.setLineWidth(2);C.line(x1,540-y1,x2,540-y2)
    para(label,lx,ly,190,12,PURPLE,True)

start('Do login ao cadastro escolar')
bullets([
('Objetivo desta apresentação','Definir quais dados o MySQL guardará, como as tabelas se relacionam e como o portal usará essas informações.'),
('Primeira entrega: cadastro e vínculos','Usuários, escolas, turmas, matrículas, perfis e preferências. Notas, frequência, calendário e comunicados entram depois.'),
('Decisão central','Keycloak autentica. MySQL organiza o cadastro escolar. Não duplicaremos senhas no banco do portal.'),
('Ferramentas escolhidas','MySQL Server + MySQL Workbench + MySQL Connector/Python. Nenhum banco foi criado ou alterado para produzir este material.')]);end()
start('O que existe hoje e o que será desenvolvido')
table(['Componente','Estado atual','Uso proposto'],[
('Login OIDC','Flask + Keycloak','Manter o provedor de identidade'),('CRUD Python','Rascunho incompleto','Reescrever consultas e transações'),('MySQL no Compose','Ainda não configurado','Adicionar serviço e volume próprios'),('Modelo SQL versionado','Não encontrado no projeto','Criar após validar este DER'),('Dados escolares','Exemplos no código/sessão','Persistir gradualmente no MySQL'),('Tela de perfil','Campos demonstrativos','Consultar cadastro do usuário')]);end()
start('Como ler um DER')
bullets([('Entidade → tabela','Exemplo: USUARIOS representa as pessoas cadastradas. Cada linha é um usuário.'),('Atributo → coluna','Exemplo: nome_completo é um texto; data_nascimento é uma data, não uma idade fixa.'),('PK e FK','PK identifica uma linha. FK aponta para uma linha existente em outra tabela e mantém o vínculo consistente.'),('Cardinalidade','1:N = uma escola pode ter várias turmas. N:N = usuários e turmas são ligados pela tabela MATRICULAS.')]);end()
start('DER principal • cadastro e vida escolar','LEGENDA: 1 = EXATAMENTE UM | 0..N = ZERO OU VÁRIOS | LINHAS REPRESENTAM CHAVES ESTRANGEIRAS')
entity(55,150,'ESCOLAS',['PK escola_id','nome, cidade, uf','ativo'],330)
entity(565,150,'TURMAS',['PK turma_id • FK escola_id','nome, ano_letivo','ativo'],330)
entity(55,350,'USUARIOS',['PK usuario_id','OIDC: issuer + sub','nome_completo, email, ativo'],330)
entity(565,350,'MATRICULAS',['PK matricula_id','FK usuario_id • FK turma_id','status, data_matricula'],330)
link(385,205,565,205,'1 → 0..N',422,177)
link(730,262,730,350,'1 → 0..N',745,294)
link(385,405,565,405,'1 → 0..N',422,377)
end()
start('O que esses relacionamentos significam')
table(['Relação','Regra','Exemplo fictício'],[
('Escola → turma','Cada turma pertence a 1 escola','Escola Horizonte → 2º A / 2026'),('Usuário → matrícula','Cada matrícula pertence a 1 usuário','Zezinho → matrícula 501'),('Turma → matrícula','Cada matrícula pertence a 1 turma','Turma 20 → matrícula 501'),('Usuário ↔ turma','N:N resolvido por matrículas','Histórico de 2025 e 2026'),('Usuário sem matrícula','Permitido: 0..N','Professor ou cadastro pendente'),('Matrícula duplicada','UNIQUE(usuario_id, turma_id)','Mesmo usuário não repete a turma')]);note('Permitir várias turmas simultâneas é uma hipótese a validar com a escola; a matriz de negócio ainda será aprovada.');end()
start('Dicionário • usuários (identidade e cadastro)')
table(['Campo','Tipo MySQL proposto','Regra / finalidade'],[
('usuario_id','BIGINT UNSIGNED','PK • AUTO_INCREMENT'),('oidc_issuer','VARCHAR(255)','NULL até vincular ao Keycloak'),('oidc_sub','VARCHAR(255)','NULL até vincular; não é o login'),('nome_completo','VARCHAR(150)','NOT NULL • nome de exibição local'),('email','VARCHAR(254)','NULL permitido • contato, não PK'),('data_nascimento','DATE','Opcional • calcular idade quando preciso'),('ativo','BOOLEAN','NOT NULL • padrão TRUE')]);note('UNIQUE(oidc_issuer, oidc_sub), comparação sensível a maiúsculas. Ambos nulos ou ambos preenchidos; limites são decisões do projeto.');end()
start('Dicionário • dados complementares do usuário')
table(['Campo','Tipo MySQL proposto','Regra / finalidade'],[
('apelido','VARCHAR(60)','Opcional • não confundir com username'),('cidade','VARCHAR(100)','Opcional • residência'),('uf','CHAR(2)','Opcional • UF brasileira, ex.: PE'),('genero','VARCHAR(50)','Opcional • preencher somente se necessário'),('criado_em','DATETIME','NOT NULL • data de criação em UTC'),('atualizado_em','DATETIME','NOT NULL • manter a cada atualização')]);note('Não guardar senha, token ou idade fixa. Não coletar CPF/endereço completo sem uma necessidade definida. UF pressupõe escopo brasileiro.');end()
start('Dicionário • escolas e turmas')
table(['Tabela.campo','Tipo MySQL proposto','Regra / finalidade'],[
('escolas.escola_id','BIGINT UNSIGNED','PK • AUTO_INCREMENT'),('escolas.nome','VARCHAR(150)','NOT NULL'),('escolas.cidade / uf','VARCHAR(100) / CHAR(2)','Opcionais'),('escolas.ativo','BOOLEAN','NOT NULL • padrão TRUE'),('turmas.turma_id / escola_id','BIGINT UNSIGNED','PK / FK obrigatória'),('turmas.nome / ano_letivo','VARCHAR(60) / SMALLINT UNSIGNED','Obrigatórios • exemplo: 2º A / 2026'),('turmas.ativo','BOOLEAN','NOT NULL • padrão TRUE')]);note('UNIQUE(escola_id, ano_letivo, nome). A mesma escola pode repetir “2º A” em anos diferentes.');end()
start('Dicionário • matrículas')
table(['Campo','Tipo MySQL proposto','Regra / finalidade'],[
('matricula_id','BIGINT UNSIGNED','PK • AUTO_INCREMENT'),('usuario_id','BIGINT UNSIGNED','FK → usuarios • NOT NULL'),('turma_id','BIGINT UNSIGNED','FK → turmas • NOT NULL'),('data_matricula','DATE','NOT NULL'),('status','VARCHAR(20)','ativa, concluida, cancelada ou transferida')]);note('Aplicar CHECK aos estados permitidos. A aplicação valida que o usuário pode ser matriculado como aluno; FK sozinha não verifica perfil.');end()
start('DER complementar • perfis e preferências','PERFIS LOCAIS PROPOSTOS: AINDA NÃO SÃO AS PERMISSÕES EFETIVAMENTE IMPLEMENTADAS NO PORTAL')
entity(42,157,'USUARIOS',['PK usuario_id','Cadastro da pessoa'],250)
entity(355,157,'USUARIO_PERFIS',['PK/FK usuario_id','PK/FK perfil_id'],250)
entity(668,157,'PERFIS',['PK perfil_id','nome UNIQUE'],250)
link(292,212,355,212,'1 : 0..N',290,275)
link(605,212,668,212,'0..N : 1',595,275)
entity(355,348,'PREFERENCIAS',['PK/FK usuario_id','tema, fonte'],250)
link(168,269,168,405,'1 : 0..1',60,325)
link(168,405,355,405,'',200,425)
note('Um usuário pode ter mais de um perfil; cada usuário possui no máximo um registro de preferências.');end()
start('Dicionário • perfis e preferências')
table(['Tabela.campo','Tipo MySQL proposto','Regra / finalidade'],[
('perfis.perfil_id','SMALLINT UNSIGNED','PK • AUTO_INCREMENT'),('perfis.nome','VARCHAR(30)','UNIQUE • aluno, professor, administrador'),('usuario_perfis.usuario_id','BIGINT UNSIGNED','FK → usuarios'),('usuario_perfis.perfil_id','SMALLINT UNSIGNED','FK → perfis • PK composta com usuario_id'),('preferencias.usuario_id','BIGINT UNSIGNED','PK e FK → usuarios'),('preferencias.tema','VARCHAR(10)','claro ou escuro • padrão claro'),('preferencias.fonte','VARCHAR(10)','normal ou grande • padrão normal')]);note('Perfis do portal terão regras explícitas. O usuário não poderá atribuir “administrador” a si mesmo. Conta admin do Keycloak é separada.');end()
start('Quem é responsável por cada informação?')
table(['Informação','Fonte principal proposta','Como o portal utiliza'],[
('Senha e autenticação','Keycloak','Recebe identidade OIDC validada'),('Identificador da identidade','Keycloak: issuer + sub','Liga login ao cadastro local'),('Nome e e-mail iniciais','Cadastro / identidade validada','Definir sincronização antes do CRUD'),('Escola, turma, matrícula','MySQL','Exibe vínculo e histórico escolar'),('Perfis do portal','MySQL, nesta proposta','Autoriza operações no backend'),('Tema e fonte','MySQL','Mantém escolhas entre sessões')]);note('Não vincular contas automaticamente apenas por e-mail. Vínculo inicial deve ser autorizado e confirmado pelo administrador responsável.');end()
start('Tipos de dados: escolher pela finalidade')
table(['Tipo','Uso','Exemplo fictício'],[
('BIGINT UNSIGNED','Identificador numérico positivo','usuario_id = 101'),('VARCHAR(n)','Texto com tamanho variável','nome_completo = Zezinho Silva'),('CHAR(2)','Código de tamanho fixo','uf = PE'),('DATE','Data sem horário','data_matricula = 2026-02-02'),('DATETIME','Data e hora; convenção UTC','criado_em = 2026-11-14 15:30:00'),('BOOLEAN','Valor lógico; validar 0/1','ativo = TRUE'),('DECIMAL(4,2)','Nota exata; expansão futura','nota = 8.75 • regra de 0 a 10')]);note('PK/FK não são tipos de dados: são restrições. VARCHAR permite tamanho máximo; NOT NULL determina obrigatoriedade.');end()
start('Integridade: regras que evitam inconsistências')
bullets([('Chaves e unicidade','PKs identificam registros; FKs impedem referências inexistentes; UNIQUE evita matrícula repetida e identidade duplicada.'),('Validação de domínio','CHECK para tema, fonte e status. Campos obrigatórios usam NOT NULL. Valores opcionais usam NULL, não textos como “não informado”.'),('Histórico preservado','Preferir desativar usuários, escolas e turmas. Usar RESTRICT nas relações escolares; não apagar matrículas por cascata.'),('Texto e transações','Usar InnoDB e utf8mb4. IDs OIDC precisam de comparação exata. Agrupar gravações relacionadas em transações com commit/rollback.')]);end()
start('Exemplo completo • do login à tela de perfil')
table(['Passo','Operação','Resultado'],[
('1. Autenticar','Keycloak valida a conta','Flask recebe issuer e sub válidos'),('2. Localizar cadastro','SELECT por issuer + sub','usuario_id = 101, ativo = TRUE'),('3. Verificar acesso','Consultar usuario_perfis','Perfil aluno → acesso permitido'),('4. Buscar vínculo','JOIN matrícula, turma e escola','Turma 20 • Escola Horizonte'),('5. Aplicar preferências','Consultar preferencias','Tema escuro, fonte grande'),('6. Renderizar','Flask envia dados ao template','Perfil preenchido pelo MySQL')]);note('Se não houver vínculo local: informar cadastro pendente. Não conceder perfil privilegiado nem matrícula automaticamente.');end()
start('Como as ferramentas trabalham juntas')
bullets([('MySQL Server','Executa SQL e persiste as tabelas. Proposta: terceiro serviço no Docker, com volume próprio e separado do Keycloak.'),('MySQL Workbench','Modela o DER, executa scripts SQL e permite inspecionar os registros. Não precisa ficar aberto para o portal funcionar.'),('MySQL Connector/Python','Biblioteca usada pelo Flask para consultar/gravar. Instalar na imagem; usar usuário da aplicação, parâmetros e conexões gerenciadas.'),('Flask + Keycloak','Flask aplica regras e renderiza páginas. Keycloak continua validando login e alterando senhas; não será substituído pelo MySQL do portal.')]);end()
start('Depois do núcleo • evolução planejada')
table(['Funcionalidade','Entidades futuras','Dados que serão fornecidos'],[
('Notas','disciplinas, ofertas, avaliações, notas','Disciplina, período, nota DECIMAL'),('Frequência','aulas e presenças','Data da aula, presença e justificativa'),('Calendário','eventos e públicos-alvo','Título, início/fim, turma destinatária'),('Comunicados','comunicados, destinos e leituras','Mensagem TEXT, autor, data de leitura')]);note('Estas tabelas ainda não integram o DER detalhado inicial. Antes de criá-las, definir regras de período, turma, disciplina e visibilidade.');end()
start('Decisões para aprovar antes do SQL')
bullets([('Escopo da primeira versão','Uma escola piloto. A tabela escolas permite evolução; isolamento completo entre escolas exige regras adicionais.'),('Papéis e matrículas','Confirmar se usuários podem ter vários perfis e turmas simultâneas. Esta proposta permite ambos, sem conceder acesso automaticamente.'),('Dados pessoais e sincronização','Validar necessidade de nascimento/gênero; definir quem edita nome/e-mail e se a mudança também será refletida no Keycloak.'),('Próxima entrega','Modelo físico no Workbench, script SQL versionado, MySQL no Compose, Connector/Python e testes do CRUD. Sem apagar dados existentes.')]);end()
start('Referências e limites da proposta')
para('Base do projeto',42,150,875,18,NAVY,True)
para('Inspeção de crud_usuarios/services/login.py e templates/perfil.html. O CRUD atual é incompleto; campos do perfil ainda incluem exemplos. Nenhuma conexão com MySQL foi executada nesta preparação.',42,181,875,15)
para('Documentação técnica oficial',42,250,875,18,NAVY,True)
para('MySQL 8.4 — tipos de dados<br/>https://dev.mysql.com/doc/refman/8.4/en/data-types.html<br/><br/>MySQL 8.4 — chaves estrangeiras<br/>https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html',42,280,875,13)
note('DER conceitual/lógico com sugestões físicas. Tamanhos, campos e regras são propostas do UNIFICA, não exigências universais do MySQL.');end()
C.save()
print(f'{OUT} | {page} slides')
