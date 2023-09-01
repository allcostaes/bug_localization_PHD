# ---------------------------------------------------------------------------------------------------------------
# Abrindo o banco de dados
import logging

import psycopg2
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")

class Consulta(object):

    def selecionaConsultas(self, cf_codigo):
        logging.info("PROCESSANDO CONSULTAS")
        # Seleciona as consultas relativas ao código fonte
        cursor2 = conn.cursor()
        Selecao = "SELECT \"CS_CODIGO\", \"CS_CODIGOORIGINAL\", \"CS_IMPLEMENTACAO\" "
        Selecao += " FROM \"CONSULTA\" WHERE "
        Selecao += " (\"CF_CODIGO\"=" + str(cf_codigo) + ") "
        #Selecao += " (\"CF_CODIGO\"=" + str(cf_codigo) + ") AND (\"CS_CODIGO\"=35 OR \"CS_CODIGO\"=74 OR \"CS_CODIGO\"=72  OR  \"CS_CODIGO\"=29 OR \"CS_CODIGO\"=15 OR \"CS_CODIGO\"=57 OR \"CS_CODIGO\"=50 OR \"CS_CODIGO\"=82) "
        #Selecao += " AND  (\"CF_CODIGO\"=" + str(cf_codigo) + ") AND ( (\"CS_CODIGO\"=74) OR  (\"CS_CODIGO\"=10)) "

        Selecao += " ORDER BY \"CS_CODIGO\""
        cursor2.execute(Selecao)
        resultsetConsultas = cursor2



        return resultsetConsultas

