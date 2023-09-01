from nltk.corpus import stopwords
import psycopg2
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")
class Palavra(object):

    palavra = None
    stopList= None

    ##########################################################################################################################################
    def __init__(self):
        self.stopList = self.geraStopList()

    ##########################################################################################################################################

    def geraStopList(self):

        cursor = conn.cursor()
        selecao =  "SELECT \"ST_DESCRICAO\" ";
        selecao += " FROM \"STOPWORDS\" WHERE ";
        selecao += " \"ST_CONJUNTO\"=" + str(2)
        selecao += "OR \"ST_CONJUNTO\"=" + str(3)

        cursor.execute(selecao)
        stw = cursor.fetchone()
        stopList = []


        while stw is not None:
            stopList.append(str(stw))
            stw = cursor.fetchone()
        return stopList

    ##########################################################################################################################################
    def isGoodWord(self, word):
        if ((word not in self.stopList) and (len(word) > 3) ):
            return True
        else:
            return False
    ##########################################################################################################################################