import nltk
import pyspark
from pyspark import SparkConf
from pyspark.ml.fpm import FPGrowth, SparkContext
conf = SparkConf().setAppName("App")
conf = (conf.setMaster('local[*]')
        .set('spark.executor.memory', '8G')
        .set('spark.driver.memory', '12G')
        .set('spark.driver.maxResultSize', '10G'))
sc = SparkContext(conf=conf)

from pprint import pprint



from pyspark.shell import spark, sc
# Abrindo o banco de dados
import psycopg2
from pyspark.sql.types import *
from Paragrafo import Paragrafo
from nltk.stem import PorterStemmer
ps = PorterStemmer()

conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")
# Consulta principal que nos dá o corpus principal filtraldo pelos métodos da interseção anterior
cursor2 = conn.cursor()
Selecao = "SELECT DISTINCT(\"MT_CODIGO\"), \"MT_IMPLEMENTACAO\" "
Selecao += " FROM \"METODO\" WHERE "
Selecao += " \"MT_CODIGO\" IN ( "
Selecao += " SELECT DISTINCT(\"MT_CODIGO\") FROM  \"CONSULTARANK\"  WHERE \"CS_CODIGO\"=74  AND \"MT_RANK\"<100 )"
cursor2.execute(Selecao)
metodos0 = []
labelMetodosPrincipais = []
metodo = cursor2.fetchone()
tamanhoCorpusPrincipal = 0
paragrafo = Paragrafo()
metodos = []
while metodo is not None:
    itens = paragrafo.parsingUmParagrafo(metodo[1])
    #itens = [ps.stem(word) for word in itens]
    itens = set(itens)
    itens = list(itens)
    tupla = (metodo[0] , itens)
    metodos0.append(tupla)
    metodos+=itens
    metodo = cursor2.fetchone()
cursor2.close()

'''
fdist = nltk.FreqDist(metodos)

for word, frequency in fdist.most_common(50):
    print(u'{};{}'.format(word, frequency))

print(len(metodos0))
exit(0)
'''


df = spark.createDataFrame(metodos0, ["id","itens"])

#df = spark.createDataFrame([df1,df2,df3], ["id", "items"])
fpGrowth = FPGrowth(itemsCol="itens", minSupport=0.20, minConfidence=1)
model = fpGrowth.fit(df)

# Display frequent itemsets.
model.freqItemsets.show()

# Display generated association rules.
#model.associationRules.show()

'''
# transform examines the input items against all the association rules and summarize the
# consequents as prediction
model.transform(df).show()

file = open("c:\\temporario\\testfile.txt", "w")
file.write(str(model.transform(df).show(truncate=False)))
file.close()
'''