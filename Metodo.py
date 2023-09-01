import logging

from nltk import PorterStemmer

from Palavra import Palavra
from Paragrafo import Paragrafo

# Abrindo o banco de dados
import psycopg2
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")


# ---------------------------------------------------------------------------------------------------------------
# remove common words and tokenize


# ---------------------------------------------------------------------------------------------------------------
class Metodo(object):

    cf_codigo = None
    cb_codigo = None
    mtsCorpusPrincipal = None
    mtsCorpusSecundario = None



    ##########################################################################################################################################
    def __init__(self, cf_codigo):
        self.cf_codigo = cf_codigo

    ##########################################################################################################################################
    def selecionaMetodos(self):
        metodoRuim = "/**     * Set the default width for Fig Shadow.     *     * @param width    the Fig shadow width     * @deprecated by MVW in V0.21.3.Use ProjectSettings instead.     */    public static void setDefaultShadowWidth(int width) {        Configuration.setInteger(KEY_DEFAULT_SHADOW_WIDTH, width);    }"
        from Paragrafo import Paragrafo
        paragrafo=Paragrafo

        # Consulta principal que nos dá o corpus principal filtraldo pelos métodos da interseção anterior
        cursor2 = conn.cursor()
        selecao =  "SELECT \"MT_CODIGO\", \"MT_IMPLEMENTACAO\" ";
        selecao += " FROM \"METODO\" WHERE ";
        selecao += " (\"CF_CODIGO\"=" + str(self.cf_codigo) + ")  AND \"MT_CODIGO\"<>0   "
        selecao += " ORDER BY \"MT_CODIGO\""

        cursor2.execute(selecao)
        metodos = []
        labelMetodos = []
        metodo = cursor2.fetchone()
        tamanhoCorpus=0

        while metodo is not None:
            metodos.append(metodo[1])
            labelMetodos.append("mtCodigo-"+str(metodo[0]))
            metodo = cursor2.fetchone()
            tamanhoCorpus = tamanhoCorpus+1
        cursor2.close()
        paragrafo = Paragrafo()
        metodos = paragrafo.parsingVariosParagrafos(metodos)

        '''
        with open("c:\\temporario\\metodos.txt", "w") as f:
            for item in metodos:
                f.write(str(" ".join(item))+"\n")
        f.close()

        exit(0)
        '''
        return metodos, labelMetodos, tamanhoCorpus


##########################################################################################################################################
    def selecionaMetodosSemelhantes(self):
        metodoRuim = "/**     * Set the default width for Fig Shadow.     *     * @param width    the Fig shadow width     * @deprecated by MVW in V0.21.3.Use ProjectSettings instead.     */    public static void setDefaultShadowWidth(int width) {        Configuration.setInteger(KEY_DEFAULT_SHADOW_WIDTH, width);    }"
        from Paragrafo import Paragrafo
        paragrafo=Paragrafo

        # Consulta principal que nos dá o corpus principal filtraldo pelos métodos da interseção anterior
        cursor2 = conn.cursor()
        selecao =  "SELECT \"MT_CODIGO\", \"MT_IMPLEMENTACAO\" ";
        selecao += " FROM \"METODO\" WHERE ";
        selecao += " ((\"CF_CODIGO\"=" + str(11) + ") OR (\"CF_CODIGO\"=" + str(21) + "))  AND \"MT_CODIGO\"<>0   "
        selecao += " ORDER BY \"MT_CODIGO\""

        cursor2.execute(selecao)
        metodos = []
        labelMetodos = []
        metodo = cursor2.fetchone()
        tamanhoCorpus=0

        while metodo is not None:
            metodos.append(metodo[1])
            labelMetodos.append("mtCodigo-"+str(metodo[0]))
            metodo = cursor2.fetchone()
            tamanhoCorpus = tamanhoCorpus+1
        cursor2.close()
        paragrafo = Paragrafo()
        metodos = paragrafo.parsingVariosParagrafos(metodos)

        '''
        with open("c:\\temporario\\metodos.txt", "w") as f:
            for item in metodos:
                f.write(str(" ".join(item))+"\n")
        f.close()

        exit(0)
        '''
        return metodos, labelMetodos



