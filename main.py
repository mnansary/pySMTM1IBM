#!/usr/bin/env python3
"""
@author: MD.Nazmuddoha Ansary  
"""
from __future__ import print_function
from termcolor import colored

import os,sys 
import json
import time
from glob import glob
import random
from progressbar import ProgressBar

from coreLib.utils import europarl_jsonify,readJson,LOG_INFO
from coreLib.trainer import train
from coreLib.translator import evaluate
#--------------------------------------------------------------------------------------------------------------------------------------------------
import argparse
parser = argparse.ArgumentParser(description='IBM MODEL 1 Implementation For Europarl(Tested on German-English) ',
                                formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("exec_flag", 
                    help='''
                            Execution Flag for running 
                            Available Flags: prep,train,eval
                            1)prep      = create test and train json data
                            2)train     = train the model 
                            3)eval      = evaluates new data
                          ''')
args = parser.parse_args()
#--------------------------------------------------------------------------------------------------------------------------------------------------
config_data=readJson('config.json')
class FLAGS:
    LANG_A      = config_data['FLAGS']['LANG_A']
    LANG_B      = config_data['FLAGS']['LANG_B']
    MODEL_DIR   = config_data['FLAGS']['MODEL_DIR']
    TEST_JSON   = config_data['FLAGS']['TEST_JSON']
class STATS:
    INFILE_A        = config_data['STATS']['INFILE_A']
    INFILE_B        = config_data['STATS']['INFILE_B']
    DATA_JSON_DIR   = config_data['STATS']['DATA_JSON_DIR']
    SENTENCE_COUNT  = config_data['STATS']['SENTENCE_COUNT']
    MAX_LENGTH      = config_data['STATS']['MAX_LENGTH']

#--------------------------------------------------------------------------------------------------------------------------------------------------
def create_json_data(FLAGS,STATS):
    # train Data
    LOG_INFO('Preprocessing Train Data')
    europarl_jsonify(FLAGS,STATS)

def check_json_data(STATS):
    _pbar=ProgressBar()
    # JSON_DIR
    data_dirs=glob(os.path.join(STATS.DATA_JSON_DIR,'*.json'))
    for data_dir in _pbar(data_dirs):
        try:
            _ = readJson(data_dir)
        except Exception as e:
            LOG_INFO('Error Reading Data:{}'.format(data_dir))
            print(e)
        

#--------------------------------------------------------------------------------------------------------------------------------------------------
def main(args,FLAGS,STATS):
    start_time=time.time()
    
    if args.exec_flag=='prep':
        create_json_data(FLAGS,STATS)
        check_json_data(STATS)
    
    elif args.exec_flag=='train':
        LEN=len(glob(os.path.join(STATS.DATA_JSON_DIR,'*.json')))
        NUM=random.randint(0,LEN)
        train(FLAGS,STATS,NUM)    
    
    elif args.exec_flag=='eval':
        evaluate(FLAGS)
    
    else:
        raise ValueError('NOT IMPLEMENTED YET')

    LOG_INFO('Total Time Taken: {} s'.format(time.time()-start_time))

if __name__ == "__main__":
    main(args,FLAGS,STATS)
