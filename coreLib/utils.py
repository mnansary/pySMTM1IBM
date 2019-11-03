"""
@author: MD.Nazmuddoha Ansary 
"""
from __future__ import print_function
from termcolor import colored

import os,sys 
import json
import math
import re
from progressbar import ProgressBar
#--------------------------------------------------------------------------------------------------------------------------------------------------
def readJson(file_name):
    return json.load(open(file_name))
def LOG_INFO(log_text,p_color='green'):
    print(colored('#    LOG:','blue')+colored(log_text,p_color))
def create_dir(base_dir,ext_name):
    new_dir=os.path.join(base_dir,ext_name)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    return new_dir
#--------------------------------------------------------------------------------------------------------------------------------------------------
count = 0
TAG_CHARS= '#!$%&()*+,-./:;<=>?@[]^_`{|}~"0123456789' 
#--------------------------------------------------------------------------------------------------------------------------------------------------
def incr():
    global count
    count += 1
def dictify(sentences_a,sentences_b):
    for (sentence_a, sentence_b) in zip(sentences_a, sentences_b):
        incr()
        s_a=sentence_a.rstrip()        
        s_b=sentence_b.rstrip()
        for tag in TAG_CHARS:
            s_a=str(s_a).replace(tag,'')
            s_b=str(s_b).replace(tag,'')
        yield s_a,s_b
#--------------------------------------------------------------------------------------------------------------------------------------------------

def europarl_jsonify(FLAGS,STATS):
    '''
        Format the raw data to json with explicit formatting
    '''
    _PBAR=ProgressBar()
    global count
    LOG_INFO('Starting to jsonify: {} and {}'.format(STATS.INFILE_A,STATS.INFILE_B))
    # count the number of files needed to store the data
    FILE_COUNT=math.ceil(STATS.SENTENCE_COUNT/STATS.MAX_LENGTH)
    LOG_INFO('Total Number of json files:{}'.format(FILE_COUNT),p_color='yellow')
    
    with open(STATS.INFILE_A, 'r') as a, open(STATS.INFILE_B, 'r') as b:
        LOG_INFO('Writing Data to JSON ')
        for fn_id in _PBAR(range(FILE_COUNT)):
            # data to write
            SEN_NUM = STATS.SENTENCE_COUNT - (fn_id*STATS.MAX_LENGTH)  
            DATA_COUNT=min(SEN_NUM,STATS.MAX_LENGTH)
            # json
            JSON_FILE=os.path.join(STATS.DATA_JSON_DIR,'{}.json'.format(fn_id))
            # write mode
            with open(JSON_FILE,'w') as outfile:
                # json_begin
                outfile.write('[')
                outfile.write('\n')
                
                while True:
                    try:
                        # get sentences
                        s_a,s_b = next(dictify(a,b))
                        # json formatting
                        outfile.write('\t{')
                        outfile.write('\n')
                        # sentences 
                        line_a='"{}":"{}",'.format(FLAGS.LANG_A,s_a)
                        line_b='"{}":"{}"' .format(FLAGS.LANG_B,s_b)
                        # lang-a
                        outfile.write('\t\t{}'.format(line_a))
                        outfile.write('\n') 
                        # lang-b
                        outfile.write('\t\t{}'.format(line_b))
                        outfile.write('\n') 
                        # formatting for last sentence
                        if count == DATA_COUNT:
                            outfile.write('\t}')
                            outfile.write('\n')
                            break
                        else: 
                            outfile.write('\t},')
                            outfile.write('\n')
                    
                    except StopIteration:
                        break
                # json_end
                outfile.write(']')
            # reset counter
            count = 0
            
#--------------------------------------------------------------------------------------------------------------------------------------------------
