from os import environ

import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password=environ["UNIFICA_MYSQL_PASSWORD"],
    database="UNIFICA"
)

cursor = conexao.cursor()
