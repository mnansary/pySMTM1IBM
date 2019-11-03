"""
@author: MD.Nazmuddoha Ansary 
"""
from __future__ import print_function
from termcolor import colored

import os,sys 
import json
from glob import glob 
from coreLib.utils import readJson,LOG_INFO,dictify 
#--------------------------------------------------------------------------------------------------------------------------------------------------
def tokenize(sentence):
    return sentence.split()
def translate(tokens, model):
    return ['{}  '.format(model[word]) if word in model else word for word in tokens]
#--------------------------------------------------------------------------------------------------------------------------------------------------
def translate_sentence(model,sentence):
    tokens = tokenize(sentence)
    translated_tokens = translate(tokens, model)
    translated_tokens=''.join(translated_tokens)
    return translated_tokens

def evaluate(FLAGS):
    # DIRS 
    test_a=os.path.join(FLAGS.MODEL_DIR,'test.de')
    test_b=os.path.join(FLAGS.MODEL_DIR,'test.en')
    model_dir =glob(os.path.join(FLAGS.MODEL_DIR,'model*.json'))[0]
    result_json = os.path.join(FLAGS.MODEL_DIR,'results.json')
    # model
    model=readJson(model_dir)
    with open(test_a, 'r') as a, open(test_b, 'r') as b, open(result_json,'w') as outfile:
        while True:
            try:
                gt,sen = next(dictify(a,b))
                pred=translate_sentence(model,sen)
                # json formatting
                outfile.write('\t{')
                outfile.write('\n')
                # sentences 
                SEN='"{}":"{}",'.format('sen',sen)
                GT='"{}":"{}",' .format('gt',gt)
                PRED='"{}":"{}"' .format('pred',pred)
                # sen    
                outfile.write('\t\t{}'.format(SEN))
                outfile.write('\n') 
                # GT
                outfile.write('\t\t{}'.format(GT))
                outfile.write('\n') 
                # PRED
                outfile.write('\t\t{}'.format(PRED))
                outfile.write('\n') 
                outfile.write('\t},')
                outfile.write('\n')
            except StopIteration:
                # json_end
                outfile.write(']')
                break