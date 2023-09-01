from datetime import datetime
import nltk

from Paragrafo import Paragrafo
from Consulta import Consulta

# ---------------------------------------------------------------------------------------------------------------
# Abrindo o banco de dados
import psycopg2

from SelecaoGenerica import SelecaoGenerica
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")

class Principal(object):
    #----------------------------------------------------------------------------------------------------------------
    def principal(self, cf_codigo, numTopicos, ab_codigo, tentativa):
        fmt = '%Y-%m-%d %H:%M:%S'
        tiMRR = datetime.strptime(datetime.now().strftime(fmt), fmt)


        from dvsum import dvsum
        dvsum = dvsum(cf_codigo, numTopicos)

        somatoriaRanking = 0
        totalConsultas = 0

        consulta = Consulta()
        resultsetConsultas = consulta.selecionaConsultas(cf_codigo)
        consulta = resultsetConsultas.fetchone()


        while consulta is not None:

            print("###############################################################")
            totalConsultas = totalConsultas + 1
            paragrafo = Paragrafo()
            consultaImpl = paragrafo.parsingUmParagrafo(consulta[2])

            rankDoc=[]
            print("#XXXXXXXXXXXXXXXXX  PROCESSAMENTO dvsum      XXXXXXXXXXXXXXXXXX")
            (rankDoc, vocabulario, MODDURACAO) = dvsum.retornaRankDoc(consultaImpl)



            # Guarda o rank encontrado para uma dada consulta/código fonte/abordagem
            cursor3 = conn.cursor()
            posicaoRanking=1

            for rd in rankDoc:
                inclusao = "INSERT INTO \"CONSULTARANK\" "
                inclusao += "(\"CS_CODIGO\", \"AB_CODIGO\", \"MT_CODIGO\", \"MT_RANK\", \"TENTATIVA\") "
                inclusao += " VALUES(" + str(consulta[0]) + "," + str(ab_codigo) + "," + str(rd) + "," + str(posicaoRanking) + "," + str(tentativa) + ") "
                cursor3.execute(inclusao)
                posicaoRanking=posicaoRanking+1
            conn.commit()
            cursor3.close()

            # Recuperando os métodos goldsets para cada consulta
            goldsets = []
            cursor4 = conn.cursor()
            Selecao = "SELECT  \"MT_CODIGO\" ";
            Selecao += " FROM \"GOLDSET\" WHERE ";
            Selecao += " (\"CS_CODIGO\"=" + str(consulta[0]) + ")"
            cursor4.execute(Selecao)
            goldset = cursor4.fetchone()
            while goldset is not None:
                goldsets.append(goldset[0])
                goldset = cursor4.fetchone()
            cursor4.close()

            # Descobrindo a posição do primeiro método relevante
            posicaoPrimeiroMetodo = -1
            contador = 1
            selecaoGenerica = SelecaoGenerica()

            #print("Consulta com parsing:"+str(pattern_1))

            for rd in rankDoc:
                if (rd in goldsets):
                    posicaoPrimeiroMetodo = contador

                    #print("---------")
                    #print("Primeiro método:"+str(rd))
                    selecao = "SELECT \"MT_IMPLEMENTACAO\" FROM \"METODO\" WHERE \"MT_CODIGO\"="+str(rd)
                    metodoParsed = paragrafo.parsingUmParagrafo(selecaoGenerica.selecionaUmRegistro(selecao))
                    #print("qtde termos 1 método: "+str(len(paragrafo.parsingUmParagrafo(metodoParsed))))
                    print("---------")

                    print("Posição primeiro método:"+str(posicaoPrimeiroMetodo))
                    print("Implementação primeiro método:"+str(metodoParsed))
                    print("Qtde temos primeiro método:" + str(len(set(metodoParsed))))
                    print("Consulta: "+str(consulta))
                    print("Qtde temos da consulta original:"+str(len(set(consultaImpl))))
                    print("Consulta original parsing:" + str(consultaImpl))

                    break

                contador = contador + 1

            consulta = resultsetConsultas.fetchone()
            somatoriaRanking = somatoriaRanking + (1 / posicaoPrimeiroMetodo)


        resultsetConsultas.close()
        MRR = (1 / totalConsultas) * somatoriaRanking

        # tempo gasto para calcular o MRR
        tfMRR = datetime.strptime(datetime.now().strftime(fmt), fmt)
        if tiMRR > tfMRR:
            MRRDURACAO = tiMRR - tfMRR
        else:
            MRRDURACAO = tfMRR - tiMRR



        print("Total de consultas: " + str(totalConsultas))
        print("Somatória do 1 elemento encontrado: " + str(somatoriaRanking))
        print("MRR:" + str(MRR))

        # Atualiza o MRR para o software em um dado número de tópicos
        cursor3 = conn.cursor()
        Inclusao = "INSERT INTO \"MRRRANK\" VALUES (" + str(cf_codigo) + "," + str(ab_codigo) + "," + str(MRR) + "," + str(tentativa) + ",'" + str(MRRDURACAO) + "','" + str(MODDURACAO) + "') "

        # print(Atualizacao)
        cursor3.execute(Inclusao)
        conn.commit()
        cursor3.close()




