from textblob import TextBlob
# Abrindo o banco de dados
import psycopg2
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")

class Nome(object):
    cursor7 = None
    listaNomesBD = None

    def __init__(self):
        self.listaNomesBD = []
        # Recupera a lista de nomes que estão no banco de dados
        cursor7 = conn.cursor()
        Selecao = "SELECT \"VC_PALAVRA\"";
        Selecao = Selecao + " FROM \"VOCABULARIO\" WHERE ";
        Selecao = Selecao + " (\"VC_TIPO\"='n')"

        cursor7.execute(Selecao)
        nomeBD = cursor7.fetchone()

        while nomeBD is not None:
            self.listaNomesBD.append(str(nomeBD[0]).lower())
            nomeBD = cursor7.fetchone()
        cursor7.close()
        self.listaNomesBD = set(self.listaNomesBD)

    def isNoum(self, nome):
        blob = TextBlob(str(nome))
        tipoPalavra = str(blob.tags).split(',')[1].replace('\'', '').replace(')', '').replace(']', '').strip()

        if (tipoPalavra.__contains__('NN') or (nome in self.listaNomesBD) ):
            return True
        else:
            return False

    def contaNomes(self, sentenca):

        contador=0
        for item in sentenca:
            if (self.isNoum(str(item))):
                contador+=1

        return contador
