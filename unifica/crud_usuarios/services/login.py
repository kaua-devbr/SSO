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