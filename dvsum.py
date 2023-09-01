from datetime import datetime
import logging
import gensim
from LabeledLineSentence import LabeledLineSentence
from Metodo import Metodo
from gensim import corpora, models
# ---------------------------------------------------------------------------------------------------------------
# Abrindo o banco de dados
import psycopg2
conn = psycopg2.connect("dbname='bdados12' user='postgres' host='192.168.0.251' password='123456'")
import numpy as np

class dvsum(object):

    cb_codigo = None
    cf_codigo = None
    numTopicos= None
    ab_codigo = None
    dvSumModel= None
    MODDURACAO = None
    tamanhoCorpusPrincipal = None

    # ----------------------------------------------------------------------------------------------------------------
    def pattern2vector(self, vocabulario, tokens, word2vec, AVG=False):
        pattern_vector = np.zeros(word2vec.layer1_size)
        n_words = 0
        if len(tokens) > 1:
            for t in tokens:
                try:
                    if (t.strip() in vocabulario):
                        vector = word2vec[t.strip()]
                        pattern_vector = np.add(pattern_vector, vector)
                        n_words += 1
                except ValueError:
                    continue
            if AVG is True:
                pattern_vector = np.divide(pattern_vector, n_words)
        elif len(tokens) == 1:
            try:
                pattern_vector = word2vec[tokens[0].strip()]
            except KeyError:
                pass
        return pattern_vector

    # ----------------------------------------------------------------------------------------------------------------



    def __init__(self, cf_codigo, numTopicos):
        self.cf_codigo = cf_codigo
        self.numTopicos = numTopicos

        logging.info("CRIANDO MODELO W2VSUM PRINCIPAL")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        logging.info("GERANDO CORPUS DE MÉTODOS PARA W2VSUM - INÍCIO")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        metodo = Metodo(self.cf_codigo)
        (metodos, labelMetodos, self.tamanhoCorpusPrincipal) = metodo.selecionaMetodos()
        ######################     INÍCIO  W2VSUM     #######################################################
        logging.info("GERANDO CORPUS DE MÉTODOS PARA W2VSUM - FINAL")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        it = LabeledLineSentence(metodos, labelMetodos)
        self.dvSumModel = gensim.models.Doc2Vec(size=self.numTopicos, workers=8, negative=50)
        self.dvSumModel.build_vocab(it)
        # training of model

        import math
        # training of model
        fmt = '%Y-%m-%d %H:%M:%S'
        tiMOD = datetime.strptime(datetime.now().strftime(fmt), fmt)




        for epoch in range(10):
            self.dvSumModel.train(it, total_examples=self.dvSumModel.corpus_count, epochs=self.dvSumModel.iter)
            localCycle=math.floor(1+(epoch/(2*self.dvSumModel.iter)))
            localX = math.fabs((epoch/self.dvSumModel.iter)-2*localCycle+1)
            localLR=0.001+(0.006-0.001)*max(0, (1-localX))
            self.dvSumModel.alpha = localLR

        # tempo gasto para treinar o modelo
        tfMOD = datetime.strptime(datetime.now().strftime(fmt), fmt)
        if tiMOD > tfMOD:
            self.MODDURACAO = tiMOD - tfMOD
        else:
            self.MODDURACAO = tfMOD - tiMOD

        logging.info("FINALIZANDO A  CRIAÇÃO DO MODELO W2VSUM ")
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        #############################    FIM  W2V   #################################################

    def retornaRankDoc(self, consultaImpl):
        vocabulario = self.dvSumModel.wv.vocab

        print("Qtde temos da consulta:" + str(len(set(consultaImpl))))
        print("Consulta parsing:" + str(consultaImpl))

        p1 = self.pattern2vector(vocabulario, consultaImpl, self.dvSumModel, False)
        # logging.info("Iniciando o cálculo de similaridades")

        sims = self.dvSumModel.docvecs.most_similar([p1], topn=self.tamanhoCorpusPrincipal)

        rankDoc = []

        for item in sims:
            #print(item)
            mtCodigo = str(item[0]).replace('mtCodigo-','').replace('\'','')
            rankDoc.append(int(mtCodigo))
        return rankDoc, vocabulario, self.MODDURACAO
