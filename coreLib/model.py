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

import pprint
from operator import itemgetter
from copy import deepcopy

from coreLib.utils import readJson,LOG_INFO 
#--------------------------------------------------------------------------------------------------------------------------------------------------
EPSILON=0.001
#EPSILON: Acceptable euclidean distance between translation probability vectors across iterations

#--------------------------------------------------------------------------------------------------------------------------------------------------
def init_translation_probabilities(words,FLAGS):
    LOG_INFO('Initializing Probabilities')
    p_val=1/len(words[FLAGS.LANG_B])
    return {word_a: {word_b: p_val for word_b in words[FLAGS.LANG_B]}for word_a in words[FLAGS.LANG_A]}

def get_words(corpus,FLAGS):
    def source_words(lang):
        for pair in corpus:
            for word in pair[lang].split():
                yield word
    return {lang: set(source_words(lang)) for lang in (FLAGS.LANG_B,FLAGS.LANG_A)}

#--------------------------------------------------------------------------------------------------------------------------------------------------
def train_iteration(corpus, words, total_s, prev_translation_probabilities,FLAGS):
    _PBAR=ProgressBar()
    counts = {word_a: {word_b: 0 for word_b in words[FLAGS.LANG_B]}for word_a in words[FLAGS.LANG_A]}
    totals = {word_b: 0 for word_b in words[FLAGS.LANG_B]}
    LOG_INFO('Getting Previous Translation Probabilities')
    translation_probabilities = deepcopy(prev_translation_probabilities)
    LOG_INFO('Setting Counts And Totals')
    for (a_s, b_s) in [(pair[FLAGS.LANG_A].split(), pair[FLAGS.LANG_B].split())for pair in corpus]:
        for a in a_s:
            total_s[a] = 0
            for b in b_s:
                total_s[a] += translation_probabilities[a][b]
        for a in a_s:
            for b in b_s:
                counts[a][b] += (translation_probabilities[a][b] / total_s[a])
                totals[b] += translation_probabilities[a][b] / total_s[a]

    LOG_INFO('Setting Translation Probabilities')
    for b in _PBAR(words[FLAGS.LANG_B]):
        for a in words[FLAGS.LANG_A]:
            translation_probabilities[a][b] = counts[a][b] / totals[b]
            
    return translation_probabilities

def table_distance(table_1, table_2):
    '''
    modelling the tables as vectors, whose indices are essentially some
    hashing function applied to each (row key, col key) pair, return the
    euclidean distance between them, where euclidean distance is defined as
    sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + ... + (a[n] - b[n])**2)
    assumes that table_1 and table_2 are identical in structure
    '''
    row_keys = table_1.keys()
    cols = list(table_1.values())
    col_keys = cols[0].keys()

    result = 0
    for (row_key, col_key) in zip(row_keys, col_keys):
        delta = (table_1[row_key][col_key] -
                 table_2[row_key][col_key]) ** 2
        result += delta

    return result ** 0.5

def is_converged(probabilties_prev, probabilties_curr, EPSILON):
    delta = table_distance(probabilties_prev, probabilties_curr)
    return delta < EPSILON
#--------------------------------------------------------------------------------------------------------------------------------------------------

def summarize_results(probabs,words,FLAGS):
    taken_word = {word_b: True for word_b in words[FLAGS.LANG_B]}
    res={}
    for a in words[FLAGS.LANG_A]:
        taken=False
        idx=0
        prob_b=sorted(probabs[a].items(), key=itemgetter(1), reverse=True)
        while not taken:
            if idx >= len(prob_b):
                idx=0
                break
            word_b=prob_b[idx][0]
            if taken_word[word_b]:
                taken_word[word_b]=False
                res.update({a:word_b})
                taken=True
                idx=0
            else:
                idx+=1
    return res
#--------------------------------------------------------------------------------------------------------------------------------------------------
def train_model(corpus,words,FLAGS):
    total_s = {word_a: 0 for word_a in words[FLAGS.LANG_A]} 
    prev_translation_probabilities = init_translation_probabilities(words,FLAGS)
    converged = False
    iterations = 0
    while not converged:
        LOG_INFO('Getting Translation Probabilities-ITR:{}'.format(iterations+1))
        translation_probabilities = train_iteration(corpus, words, total_s,prev_translation_probabilities,FLAGS)
        LOG_INFO('Checking Convergence-ITR:{}'.format(iterations+1))
        converged = is_converged(prev_translation_probabilities,translation_probabilities, EPSILON)
        prev_translation_probabilities = translation_probabilities
        iterations += 1
    return translation_probabilities

def train(FLAGS,STATS):
    corpus_dir=os.path.join(FLAGS.MODEL_DIR,'corpus.json')
    corpus = readJson(corpus_dir)
    # Words
    words=get_words(corpus,FLAGS)
    # word count    
    lang_a_word_count=len(words[FLAGS.LANG_A]) 
    lang_b_word_count=len(words[FLAGS.LANG_B])
    LOG_INFO('LANG-A-WORD-COUNT:{}'.format(lang_a_word_count))
    LOG_INFO('LANG-B-WORD-COUNT:{}'.format(lang_b_word_count))    
    # get probabilities
    probabilities = train_model(corpus,words,FLAGS) 
    # save model
    results=summarize_results(probabilities,words,FLAGS)
    MODEL_JSON=os.path.join(FLAGS.MODEL_DIR,'model.json')
    with open(MODEL_JSON,'w') as model_file:
        json.dump(results,model_file,indent=2,ensure_ascii=False)
    
    