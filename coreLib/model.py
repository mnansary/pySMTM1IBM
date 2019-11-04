"""
@author: MD.Nazmuddoha Ansary 
"""
from __future__ import print_function
from termcolor import colored

from progressbar import ProgressBar
import os,sys 
import json
from glob import glob 
import shutil
import collections
import pprint
from operator import itemgetter
from copy import deepcopy

from coreLib.utils import readJson,LOG_INFO,dump_data,create_dir 

#---------------------------------------------------------------------------------------------------------------------
class IBMM1(object):
    def __init__(self,LA,LB,corpus_dir,model_dir,elipson=0.0001):
        self.la=LA
        self.lb=LB
        self.corpus_dir=corpus_dir
        self.model_dir=model_dir
        self.model_json=os.path.join(self.model_dir,'model.json')
        self.elipson=elipson
        
    def __get_words(self):
        self.corpus=readJson(self.corpus_dir)
        def source_words(lang):
            for pair in self.corpus:
                for word in pair[lang].split():
                    yield word    
        self.words={lang: set(source_words(lang)) for lang in (self.la,self.lb)}
    
    def __init_translation_probabilities(self):
        p_val=1/len(self.words[self.la])
        return {word_a:{word_b: p_val for word_b in self.words[self.lb]}for word_a in self.words[self.la]}
        
    
    def __iterate(self,prev_translation_probabilities):
        counts   = {word_a: {word_b: 0 for word_b in self.words[self.lb]}for word_a in self.words[self.la]}
        totals_b = {word_b: 0 for word_b in self.words[self.lb]}
        translation_probabilities = deepcopy(prev_translation_probabilities)
        for (a_s, b_s) in [(pair[self.la].split(), pair[self.lb].split())for pair in self.corpus]:
            for a in a_s:
                self.totals_a[a]=0
                for b in b_s:
                    self.totals_a[a] += translation_probabilities[a][b]            
                    
            for a in a_s:
                for b in b_s:
                    _val= translation_probabilities[a][b] / self.totals_a[a]
                    counts[a][b] += _val
                    totals_b[b]    += _val

        for b in self.words[self.lb]:
            for a in self.words[self.la]:
                translation_probabilities[a][b] = counts[a][b] / totals_b[b]
        return translation_probabilities

    def __check_convergence(self,translation_probabilities,prev_translation_probabilities):
        result=0
        for a in self.words[self.la]:
            for b in translation_probabilities[a]:
                delta=(translation_probabilities[a][b]-prev_translation_probabilities[a][b]) ** 2
                result+=delta
        result= result ** 0.5
        return (result < self.elipson,result)

            
    def __model_train(self):
        self.totals_a = {word_a: 0 for word_a in self.words[self.la]} 
        prev_translation_probabilities = self.__init_translation_probabilities()
        converged = False
        iterations = 0
        while not converged:    
            translation_probabilities = self.__iterate(prev_translation_probabilities)
            converged,result = self.__check_convergence(translation_probabilities,prev_translation_probabilities)
            prev_translation_probabilities = translation_probabilities
            iterations += 1
            LOG_INFO('ITR:{} Delta:{}'.format(iterations,result),rep=False)
            
        dump_data(os.path.join(self.model_dir,'probabs_final.json'),translation_probabilities)
        
    def __save_model(self):
        res={}
        probabs=readJson(os.path.join(self.model_dir,'probabs_final.json'))
        for a in self.words[self.la]:
            dict_a=probabs[a]
            b=sorted(dict_a.items(), key=itemgetter(1),reverse=True)[0][0]
            dict_mdl={a:b}
            res.update(dict_mdl)        
        dump_data(self.model_json,res)


    def train(self):
        self.__get_words()
        self.__model_train()
        self.__save_model()



