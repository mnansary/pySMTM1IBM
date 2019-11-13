"""
@author: MD.Nazmuddoha Ansary 
"""
from __future__ import print_function
from termcolor import colored

import os,sys 
import json
from glob import glob 
from coreLib.utils import readJson,LOG_INFO,dictify,dump_data 


#--------------------------------------------------------------------------------------------------------------------------------------------------
import argparse
parser = argparse.ArgumentParser(description='IBM MODEL 1 Implementation For Europarl(Tested on German-English) ')
parser.add_argument("test_a",help='language a test file')
parser.add_argument("test_b",help='language b test file')
parser.add_argument("model_dir",help='model.json location')
args = parser.parse_args()
test_a=args.test_a
test_b=args.test_b
model_dir=args.model_dir

base_model_dir,_=os.path.split(model_dir)
result_json=os.path.join(base_model_dir,'translation.json')
#--------------------------------------------------------------------------------------------------------------------------------------------------
def eval_precision_recall(result_json):
    results=readJson(result_json)
    correct_count=0
    reference_count=0
    length_count=0
    for data in results:
        length_count+=len(data['sentence'].split())
        reference_count+=len(data['reference'].split())
        pred_words=data['output'].split()
        ref_sentence=data['reference']
        for pred_word in pred_words:
            if pred_word in ref_sentence:
                correct_count+=1
                #ref_sentence=ref_sentence.replace(pred_word,'')
                
    LOG_INFO('RECALL:{} %'.format(100*(correct_count/reference_count)))
    LOG_INFO('PRECISION:{} %'.format(100*(correct_count/length_count)))
    return length_count/reference_count
#--------------------------------------------------------------------------------------------------------------------------------------------------    
def eval_BELU(result_json,BELU_GRAM=4):
    results=readJson(result_json)
    precisions=[]
    for gram in range(1,BELU_GRAM+1):
        correct_count=0
        length_count=0
        for data in results:
            gram_length=len(data['output'].split())+1-gram
            length_count+=gram_length
            for i in range(gram_length):
                phrase=' '.join(data['output'].split()[i:i+gram]) 
                if phrase in data['reference']:
                    correct_count+=1
        
        gram_precision=correct_count/length_count
        precisions.append(gram_precision)
    
    for idx in range(len(precisions)):
        LOG_INFO("BELU-{}-GRAM-Precision:{} %".format(idx+1,100*precisions[idx]))
#--------------------------------------------------------------------------------------------------------------------------------------------------    
def calc_Levenshtein_distance(result_json):
    LOG_INFO('Levenshtein distance Parameters:')
    results=readJson(result_json)
    total_del=0
    total_ins=0
    total_sub=0
    total_mat=0
    for data in results:
        nb_del=0
        nb_ins=0
        nb_mat=0
        nb_sub=0
        len_ref=len(data['reference'].split())
        len_out=len(data['output'].split())
        # del and ins
        if len_ref>len_out:
            nb_ins=len_ref-len_out
        elif len_out>len_ref:
            nb_del=len_out-len_ref
        else:
            nb_ins=0
            nb_del=0
        # matches and subs
        pred_words=data['output'].split()
        ref_sentence=data['reference']
        for pred_word in pred_words:
            if pred_word in ref_sentence:
                nb_mat+=1
        nb_sub=len_out-nb_mat
        #LOG_INFO('{}'.format(ref_sentence),p_color='yellow')
        #LOG_INFO('{}'.format(data['output']),p_color='red')
        #LOG_INFO('Number of Matches:{}'.format(nb_mat))
        #LOG_INFO('Number of Substitution:{}'.format(nb_sub))
        #LOG_INFO('Number of Insertion:{}'.format(nb_ins))
        #LOG_INFO('Number of Deletion:{}'.format(nb_del))
        total_del+=nb_del
        total_ins+=nb_ins
        total_sub+=nb_sub
        total_mat+=nb_mat
    LOG_INFO('Total Number of Matches:{}'.format(total_mat))
    LOG_INFO('Total Number of Substitution:{}'.format(total_sub))
    LOG_INFO('Total Number of Insertion:{}'.format(total_ins))
    LOG_INFO('Total Number of Deletion:{}'.format(total_del))

#--------------------------------------------------------------------------------------------------------------------------------------------------    
def translation(test_a,test_b,model_dir):
    # model
    model=readJson(model_dir)
    Data=[]
    with open(test_a, 'r') as a, open(test_b, 'r') as b:
        while True:
            try:
                sen,gt = next(dictify(a,b))
                pred=sen
                for word in sen.split():
                    if word in model:
                        pred=pred.replace(word,model[word])
                pred_dict={"sentence":' '.join(sen.split()),
                            "output":' '.join(pred.split()),
                            "reference":' '.join(gt.split())}
                Data.append(pred_dict)     
            except StopIteration:
                break
    dump_data(result_json,Data)

if __name__ == "__main__":
    translation(test_a,test_b,model_dir)
    BELU_penalty=eval_precision_recall(result_json)
    BELU_penalty=min(1,BELU_penalty)
    LOG_INFO("BELU-Penalty:{}".format(BELU_penalty))
    eval_BELU(result_json)
    calc_Levenshtein_distance(result_json)
