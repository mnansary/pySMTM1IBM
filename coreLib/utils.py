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
TAG_CHARS= '#!$%&()*+,-./:;<=>?@[]^_`{|}~"'+ "0123456789'\\" 
#--------------------------------------------------------------------------------------------------------------------------------------------------
def dictify(sentences_a,sentences_b):
    for (sentence_a, sentence_b) in zip(sentences_a, sentences_b):
        s_a=sentence_a.rstrip()        
        s_b=sentence_b.rstrip()
        for tag in TAG_CHARS:
            s_a=str(s_a).replace(tag,'')
            s_b=str(s_b).replace(tag,'')
        yield s_a,s_b
#--------------------------------------------------------------------------------------------------------------------------------------------------
def get_filter_data(filter_file):
    words=[]
    with open(filter_file,'r') as fd:
        for sentence in fd:
            s=sentence.rstrip()
            for tag in TAG_CHARS:
                s=str(s).replace(tag,'')            
            for word in s.split():
                words.append(word)
    return words
#--------------------------------------------------------------------------------------------------------------------------------------------------
def europarl_jsonify(FLAGS,STATS):
    words=get_filter_data(STATS.FILTER_A)
    LOG_INFO('Starting to jsonify')
    sen=0
    with open(STATS.INFILE_A, 'r') as a, open(STATS.INFILE_B, 'r') as b:
        JSON_FILE=os.path.join(FLAGS.MODEL_DIR,'corpus.json')
        # write mode
        with open(JSON_FILE,'w') as outfile:
            # json_begin
            outfile.write('[')
            outfile.write('\n')     
            
            while True:
                try:
                    # get sentences
                    s_a,s_b = next(dictify(a,b))
                    write_flag=False
                    # filter sentence
                    for word in words:
                        if word in s_a:
                            write_flag=True
                            words.remove(word)
                    if write_flag:
                        sen+=1
                        LOG_INFO('SENTENCE:{}'.format(sen))
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
                        if len(words)==0:
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
            print(words)
        
#--------------------------------------------------------------------------------------------------------------------------------------------------