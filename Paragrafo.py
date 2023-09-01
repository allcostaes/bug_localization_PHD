import logging
import re

from nltk import PorterStemmer
import wordninja
from Palavra import Palavra
from Verbo import Verbo

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
class Paragrafo(object):

    palavra = None

    def __init__(self):
        self.palavra = Palavra()

    ##########################################################################################################################################
    def parsingVariosParagrafos(self, paragrafos0):

        logging.info("INICIANDO PARSING DE PARAGRAFOS")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        paragrafos1 = []

        for item in paragrafos0:
            tmp0 = re.sub('[^a-zA-Z]+', ' ', str(item))
            tmp0 = re.sub('(?!^)([A-Z][a-z]+)', r' \1', tmp0).strip()
            tmp0 = tmp0.lower()
            paragrafos1.append(tmp0)
        paragrafos2 = []

        for item in paragrafos1:
            tmp0 = str(item).split()
            tmp1 = [word.strip() for word in tmp0 if self.palavra.isGoodWord(word.strip())]
            paragrafos2.append(tmp1)

        logging.info("FINALIZANDO PARSING DE MÉTODOS")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        return paragrafos2

    ##########################################################################################################################################
    def parsingUmParagrafo(self, paragrafo0):
        # remove pontuações e números
        tmp0 = re.sub('[^a-zA-Z]+', ' ', str(paragrafo0))
        # separa camelCase
        tmp0 = re.sub('(?!^)([A-Z][a-z]+)', r' \1', tmp0).strip()
        # converte para minúsculo
        tmp0 = tmp0.lower()
        tmp1 = str(tmp0).split()
        #remove stopwords
        tmp2 = [word for word in tmp1 if self.palavra.isGoodWord(word)]
        paragrafo1 =  tmp2

        return paragrafo1

    ##########################################################################################################################################
    def parsingUmParagrafoStemming(self, paragrafo0):
        # remove pontuações e números
        tmp0 = re.sub('[^a-zA-Z]+', ' ', str(paragrafo0))
        # separa camelCase
        tmp0 = re.sub('(?!^)([A-Z][a-z]+)', r' \1', tmp0).strip()
        # converte para minúsculo
        tmp0 = tmp0.lower()
        tmp1 = str(tmp0).split()
        #remove stopwords
        tmp2 = [word for word in tmp1 if self.palavra.isGoodWord(word)]
        stemmer = PorterStemmer()
        tmp3 = [' '.join(wordninja.split(word)) for word in tmp2]
        tmp4 = [stemmer.stem(word) for word in tmp3]

        return tmp4







