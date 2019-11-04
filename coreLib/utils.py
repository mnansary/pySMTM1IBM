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
def LOG_INFO(log_text,p_color='green',rep=True):
    if rep:
        print(colored('#    LOG:','blue')+colored(log_text,p_color))
    else:
        print(colored('#    LOG:','blue')+colored(log_text,p_color),end='\r')
def create_dir(base_dir,ext_name):
    new_dir=os.path.join(base_dir,ext_name)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    return new_dir
def dump_data(file_path,data):
    with open(file_path,'w') as fd:
        json.dump(data,fd,indent=2,ensure_ascii=False)
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
    words=words*STATS.FILTER_SIZE
    LOG_INFO('Starting to jsonify')
    JSON_FILE=os.path.join(FLAGS.MODEL_DIR,'corpus.json')    
    data=[]
    sen=0
    sen_as=[]
    sen_bs=[]
    with open(STATS.INFILE_A, 'r') as a, open(STATS.INFILE_B, 'r') as b:
        while True:
            try:
                # get sentences
                s_a,s_b = next(dictify(a,b))
                # filter sentence
                for word in words:   
                    if word in s_a:
                        if s_a not in sen_as:
                            sen+=1
                            sen_as.append(s_a)
                            sen_bs.append(s_b)           
                            words.remove(word)
                            LOG_INFO('Sentence Count:{}'.format(sen),rep=False)  
            except StopIteration:
                break
    for (s_a,s_b) in zip(sen_as,sen_bs):
        sen_dict={FLAGS.LANG_A:s_a,FLAGS.LANG_B:s_b}
        data.append(sen_dict)
    
    dump_data(JSON_FILE,data)
#--------------------------------------------------------------------------------------------------------------------------------------------------