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

#--------------------------------------------------------------------------------------------------------------------------------------------------
def recall_precision(test_a,test_b,model_dir):
    base_dir=os.path.dirname(model_dir)
    result_json =os.path.join(base_dir,'recall.json') 
    # model
    model=readJson(model_dir)
    data=[]
    words_sen=[]
    with open(test_a, 'r') as a, open(test_b, 'r') as b:
        while True:
            try:
                sen,_ = next(dictify(a,b))
                words_sen+=sen.split()                        
            except StopIteration:
                break
    count=0
    for word in words_sen:
        if word in model:
            pred=model[word]
        else:
            pred="NOT FOUND"
            count+=1
        data_dict={"org":word,"mdl":pred}
        data.append(data_dict)
    recall_val=(1-(count/len(words_sen)))*100
    dump_data(result_json,data)
    LOG_INFO('RECALL:{}'.format(recall_val))

def translation(test_a,test_b,model_dir):
    # model
    model=readJson(model_dir)
    with open(test_a, 'r') as a, open(test_b, 'r') as b:
        while True:
            try:
                sen,gt = next(dictify(a,b))
                LOG_INFO('sen:{}'.format(sen),p_color='green')
                LOG_INFO('gt:{}'.format(gt),p_color='red')
                pred=sen
                for word in sen.split():
                    if word in model:
                        pred=pred.replace(word,model[word])
                LOG_INFO('pred:{}'.format(pred),p_color='yellow')
                
            except StopIteration:
                break

if __name__ == "__main__":
    recall_precision(test_a,test_b,model_dir)
    translation(test_a,test_b,model_dir)