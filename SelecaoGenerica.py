# Abrindo o banco de dados
import psycopg2
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")

class SelecaoGenerica(object):

    def selecionaUmRegistro(self, selecao):

        # Seleciona as consultas relativas ao código fonte
        cursor = conn.cursor()
        cursor.execute(selecao)
        resultadoConsulta = cursor.fetchone()
        return str(resultadoConsulta)

