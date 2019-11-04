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
from coreLib.model import IBMM1
#from coreLib.translator import evaluate
#--------------------------------------------------------------------------------------------------------------------------------------------------
import argparse
parser = argparse.ArgumentParser(description='IBM MODEL 1 Implementation For Europarl(Tested on German-English) ',
                                formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("exec_flag", 
                        help='''
                            Execution Flag for running 
                            Available Flags: prep,train
                            1)prep      = create test and train json data
                            2)train     = train the model 
                          ''')
args = parser.parse_args()
#--------------------------------------------------------------------------------------------------------------------------------------------------
config_data=readJson('config.json')
class FLAGS:
    LANG_A      = config_data['FLAGS']['LANG_A']
    LANG_B      = config_data['FLAGS']['LANG_B']
    MODEL_DIR   = config_data['FLAGS']['MODEL_DIR']
    
class STATS:
    INFILE_A        = config_data['STATS']['INFILE_A']
    INFILE_B        = config_data['STATS']['INFILE_B']
    FILTER_A        = config_data['STATS']['FILTER_A']
    FILTER_SIZE     = config_data['STATS']['FILTER_SIZE']
#--------------------------------------------------------------------------------------------------------------------------------------------------
def main(args,FLAGS,STATS):
    start_time=time.time()
    if args.exec_flag=='prep':
        europarl_jsonify(FLAGS,STATS)   
    elif args.exec_flag=='train':
        corpus_dir=os.path.join(FLAGS.MODEL_DIR,'corpus.json')
        model=IBMM1(FLAGS.LANG_A,FLAGS.LANG_B,corpus_dir,FLAGS.MODEL_DIR)
        model.train()
    else:
        raise ValueError('check EXEC_FLAG')

    LOG_INFO('Total Time Taken: {} s'.format(time.time()-start_time))

if __name__ == "__main__":
    main(args,FLAGS,STATS)

    