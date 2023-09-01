# ---------------------------------------------------------------------------------------------------------------
import sys
import logging
import time
import itertools
from multiprocessing import Pool, Process
# ---------------------------------------------------------------------------------------------------------------
# Abrindo o banco de dados
import psycopg2
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")
# ---------------------------------------------------------------------------------------------------------------
def paralelo(cfCodigo, numTopicos, ab_codigo, tentativa):

    from Principal import Principal
    principal = Principal()
    principal.principal(cfCodigo, numTopicos, ab_codigo, tentativa)


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info("INÍCIO DE EXECUÇÃO")
    '''
    #    for i in range(10):
    # Deleta resultados anteriores
    cursor1 = conn.cursor()
    Delecao = "DELETE FROM \"CONSULTARANK\" WHERE \"AB_CODIGO\">=11 AND \"AB_CODIGO\"<=15 "
    cursor1.execute(Delecao)
    conn.commit()
    Delecao = "DELETE FROM \"MRRRANK\" WHERE \"AB_CODIGO\">=11 AND \"AB_CODIGO\"<=15 "
    cursor1.execute(Delecao)
    conn.commit()
    cursor1.close()
    '''



    for j in range(1, 11):  # j é o número de tentativas
        for i in range(101, 107):  # é o código do software
            jobs = []
            p1 = Process(target=paralelo, args=((i, 100, 36, j)))
            jobs.append(p1)
            p2 = Process(target=paralelo, args=((i, 200, 37, j)))
            jobs.append(p2)
            p3 = Process(target=paralelo, args=((i, 300, 38, j)))
            jobs.append(p3)




            p4 = Process(target=paralelo, args=((i, 400, 39, j)))
            jobs.append(p4)
            p5 = Process(target=paralelo, args=((i, 500, 40, j)))
            jobs.append(p5)
            for job in jobs:
                job.start()

            for job in jobs:
                job.join()

    logging.info("FIM DE  EXECUÇÃO")
    conn.close()


