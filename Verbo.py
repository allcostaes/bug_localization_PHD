from textblob import TextBlob
# Abrindo o banco de dados
import psycopg2
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")

class Verbo(object):
    cursor7 = None
    listaVerbosBD = None

    def __init__(self):
        self.listaVerbosBD = []
        # Recupera a lista de verbos que estão no banco de dados
        cursor7 = conn.cursor()
        Selecao = "SELECT \"VC_PALAVRA\"";
        Selecao = Selecao + " FROM \"VOCABULARIO\" WHERE ";
        Selecao = Selecao + " (\"VC_TIPO\"='v i')   OR  (\"VC_TIPO\"='v t')"

        cursor7.execute(Selecao)
        metodoBD = cursor7.fetchone()

        while metodoBD is not None:
            self.listaVerbosBD.append(str(metodoBD[0]).lower())
            metodoBD = cursor7.fetchone()
        cursor7.close()
        self.listaVerbosBD = set(self.listaVerbosBD)

    def isVerb(self, verbo):
        blob = TextBlob(str(verbo))
        tipoPalavra = str(blob.tags).split(',')[1].replace('\'', '').replace(')', '').replace(']', '').strip()

        if (tipoPalavra.__contains__('VB') or (verbo in self.listaVerbosBD) ):
            return True
        else:
            return False

    def contaVerbos(self, sentenca):

        contador=0
        for item in sentenca:
            if (self.isVerb(str(item))):
                contador+=1

        return contador
