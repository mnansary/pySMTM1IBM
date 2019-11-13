# IBM STM Model 1

    Version: 0.1.0 
    Author : Md. Nazmuddoha Ansary    
                  

### Version and Requirements
* Create a Virtualenv and ***pip3 install -r requirements.txt***

###  DataSet
 **europarl-v7_de-en** *(german-english)* from [European Parliament Proceedings Parallel Corpus 1996-2011](https://www.statmt.org/europarl/)     

###  Execution
* UNZIP the downloaded data
* Change desired Values in ***config.json***  based on **Language**  
> *(visit [this link](https://www.statmt.org/europarl/) for sentence count)*
* Example: ***config.json***    
            
        {
            "FLAGS":
            {
                "LANG_A"         : "de",
                "LANG_B"         : "en",
                "MODEL_DIR"      : "/home/ansary/WORK/MT/MODEL_DIR/"
            },
            "STATS":
            {
                "INFILE_A"       : "/home/ansary/WORK/MT/Data/europarl-v7.de-en.de",
                "INFILE_B"       : "/home/ansary/WORK/MT/Data/europarl-v7.de-en.en",
                "FILTER_A"       : "/home/ansary/WORK/MT/Data/test.de",
                "FILTER_SIZE"    : 5
            }
        }





* Preprocessing and Training: **main.py**

                usage: main.py [-h] exec_flag

                IBM MODEL 1 Implementation For Europarl(Tested on German-English) 

                positional arguments:
                exec_flag   
                                                        Execution Flag for running 
                                                        Available Flags: prep,train
                                                        1)prep      = create test and train json data
                                                        2)train     = train the model 
                                                        

                optional arguments:
                -h, --help  show this help message and exit

* Evaluation: **evaluate.py** 

                usage: evaluate.py [-h] test_a test_b model_dir

                IBM MODEL 1 Implementation For Europarl(Tested on German-English)

                positional arguments:
                test_a      language a test file
                test_b      language b test file
                model_dir   model.json location

                optional arguments:
                -h, --help  show this help message and exit


The **evalute.py** script calculates:
1. Precision 
2. Recall 
3. BLEU score of 1-4 gram models
4. Levenshtein distance parameters 
    *    No. of Matches 
    *    No. of Insertion
    *    No. of Deletion
    *    No. of Substitution

**Example Results:**

![](/MODEL_DIR/RESULTS.png?raw=true)

**ENVIRONMENT**  

    OS          : Ubuntu 18.04.3 LTS (64-bit) Bionic Beaver        
    Memory      : 7.7 GiB  
    Processor   : Intel® Core™ i5-8250U CPU @ 1.60GHz × 8    
    Graphics    : Intel® UHD Graphics 620 (Kabylake GT2)  
    Gnome       : 3.28.2  

# Acknowledgement
**This repo is heavily borrowed from [Andrew Shaw's](https://github.com/shawa) IMPLEMENTATION OF IBM MODEL 1**
>*Simple implementation of the EM Algorithm, applied to IBM Model 1 for statistical machine translation.*
