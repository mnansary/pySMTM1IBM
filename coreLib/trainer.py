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
    '''
    Given words generate the first set of translation probabilities,
    which can be accessed as
    p(e|s) <=> translation_probabilities[e][s]
    we first assume that for an `e` and set of `s`s, it is equally likely
    that e will translate to any s in `s`s
    '''
    LOG_INFO('Initializing Probabilities')
    p_val=1/len(words[FLAGS.LANG_B])
    return {word_b: {word_a: p_val for word_a in words[FLAGS.LANG_A]}
                for word_b in words[FLAGS.LANG_B]}


def get_words(corpus,FLAGS):
    def source_words(lang):
        for pair in corpus:
            for word in pair[lang].split():
                yield word
    return {lang: set(source_words(lang)) for lang in (FLAGS.LANG_B,FLAGS.LANG_A)}

#--------------------------------------------------------------------------------------------------------------------------------------------------
def train_iteration(corpus, words, total_s, prev_translation_probabilities,FLAGS):
    LOG_INFO('Getting Previous Translation Probabilities')
    translation_probabilities = deepcopy(prev_translation_probabilities)
    
    _PBAR=ProgressBar()
    
    counts = {word_en: {word_fr: 0 for word_fr in words[FLAGS.LANG_A]}
              for word_en in words[FLAGS.LANG_B]}
    
    totals = {word_fr: 0 for word_fr in words[FLAGS.LANG_A]}
    LOG_INFO('Setting Counts And Totals')
    for (es, fs) in [(pair[FLAGS.LANG_B].split(), pair[FLAGS.LANG_A].split())for pair in corpus]:
        
        for e in es:
            total_s[e] = 0

            for f in fs:
                total_s[e] += translation_probabilities[e][f]

        for e in es:
            for f in fs:
                counts[e][f] += (translation_probabilities[e][f] /
                                 total_s[e])
                totals[f] += translation_probabilities[e][f] / total_s[e]

    LOG_INFO('Setting Translation Probabilities')
    for f in _PBAR(words[FLAGS.LANG_A]):
        for e in words[FLAGS.LANG_B]:
            translation_probabilities[e][f] = counts[e][f] / totals[f]
            
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
    '''
    Decide when the model whose final two iterations are
    `probabilties_prev` and `probabilties_curr` has converged
    '''
    delta = table_distance(probabilties_prev, probabilties_curr)
    return delta < EPSILON
#--------------------------------------------------------------------------------------------------------------------------------------------------

def summarize_results(translation_probabilities):
    '''
    from a dict of source: {target: p(source|target}, return
    a list of mappings from source words to the most probable target word
    '''
    return {
        # for each english word
        # sort the words it could translate to; most probable first
        k: sorted(v.items(), key=itemgetter(1), reverse=True)
        # then grab the head of that == `(most_probable, p(k|most probable)`
        [0]
        # and the first of that pair (the actual word!)
        [0]
        for (k, v) in translation_probabilities.items()
    }

#--------------------------------------------------------------------------------------------------------------------------------------------------
def train_model(corpus,words,FLAGS):
    total_s = {word_en: 0 for word_en in words['{}'.format(FLAGS.LANG_B)]} 
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
    return translation_probabilities, iterations

def train(FLAGS,STATS,NUM):
    # data_dir
    data_dir=os.path.join(STATS.DATA_JSON_DIR,'{}.json'.format(NUM))
    corpus_dir=os.path.join(FLAGS.MODEL_DIR,'corpus.json')
    # copy
    shutil.copy(data_dir,corpus_dir)
    
    LOG_INFO('Reading Data:{}-NO:{}'.format(corpus_dir,NUM))
    # Corpus
    corpus = readJson(corpus_dir)
    # Words
    words=get_words(corpus,FLAGS)
    # word count    
    lang_a_word_count=len(words[FLAGS.LANG_A]) 
    lang_b_word_count=len(words[FLAGS.LANG_B])
    LOG_INFO('LANG-A-WORD-COUNT:{}'.format(lang_a_word_count))
    LOG_INFO('LANG-B-WORD-COUNT:{}'.format(lang_b_word_count))    
    # get probabilities
    probabilities, iterations = train_model(corpus,words,FLAGS) 
    # results
    result_table = summarize_results(probabilities)
    # save model
    MODEL_JSON=os.path.join(FLAGS.MODEL_DIR,'model_itr_{}_num_{}.json'.format(iterations,NUM))
    LOG_INFO('Saving Model:{}'.format(MODEL_JSON))
    with open(MODEL_JSON,'w') as model_file:
        json.dump(result_table,model_file,indent=2,ensure_ascii=False)
