# ---------------------------------------------------------------------------------------------------------------
import sys
import logging
import time
import itertools
import principaldvSumNGS
# ---------------------------------------------------------------------------------------------------------------
# Abrindo o banco de dados
import psycopg2

# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info("INÍCIO DE EXECUÇÃO")

    conn1 = psycopg2.connect("dbname='bdados7' user='postgres' host='192.168.0.251' password='123456'")
    #Deleta resultados anteriores
    cursor1 = conn1.cursor()
    Delecao = "SELECT \"MB_IMPLEMENTACAO\", \"CF_CODIGO\" FROM  \"METODO_BRUTO\" WHERE \"CF_CODIGO\"=31"
    cursor1.execute(Delecao)

    metodo = cursor1.fetchone()
    tamanhoCorpus = 0
    conn2 = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")
    cursor2 = conn2.cursor()
    while metodo is not None:
        # Deleta resultados anteriores

        Insercao =  "INSERT INTO  \"METODO\" (\"MT_IMPLEMENTACAO\", \"CF_CODIGO\") "
        Insercao += "VALUES ('"+str(metodo[0])+"',"+str(metodo[1])+") "
        cursor2.execute(Insercao)
        metodo = cursor1.fetchone()
    conn2.commit()

    logging.info("FIM DE  EXECUÇÃO")
    conn1.close()
    conn2.close()




