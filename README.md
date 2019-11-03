# IBM STM Model 1

    Version: 0.0.1 
    Author : Md. Nazmuddoha Ansary    
                  
![](/info/python.ico?raw=true )



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
                "MODEL_DIR"      : "/home/ansary/WORK/MT/IBM-Model-1/MODEL_DIR/",
                "TEST_JSON"      : "/home/ansary/WORK/MT/IBM-Model-1/MODEL_DIR/test.json"
            },
            "STATS":
            {
                "INFILE_A"       : "/home/ansary/WORK/MT/de-en/europarl-v7.de-en.de",
                "INFILE_B"       : "/home/ansary/WORK/MT/de-en/europarl-v7.de-en.en",
                "DATA_JSON_DIR"  : "/home/ansary/WORK/MT/Data/",
                "SENTENCE_COUNT" : 1920209,
                "MAX_LENGTH"     : 10000
            }
        }




* run **main.py**

                usage: main.py [-h] exec_flag

                IBM MODEL 1 Implementation For Europarl(Tested on German-English) 

                positional arguments:
                exec_flag   
                                                        Execution Flag for running 
                                                        Available Flags: prep,train,eval
                                                        1)prep      = create test and train json data
                                                        2)train     = train the model 
                                                        3)eval      = evaluates new data
                                                        

                optional arguments:
                -h, --help  show this help message and exit




**Results:Preprocessing**
* run **./main.py prep**
* The **STATS{DATA_JSON_DIR}** should have the following folder tree:

            Data
            ├── 0.json
            ├── 1.json
            ├── 2.json
            ├── 3.json
            -----------------
            -----------------
            -----------------

**Results:Check**
* run **./main.py check**
* manually correct the ***{some number}.json*** with **Invalid control character at:** error
> remove space from start of the two error sentences
![](/info/cor.png?raw=true )


**Results:Train**
* run **./main.py train**
* The **FLAGS{MODEL_DIR}** should have the following folder tree:

                MODEL_DIR
                ├── corpus.json
                └── model_itr_{itr-number}_num_{train_file_number}.json


**ENVIRONMENT**  

    OS          : Ubuntu 18.04.3 LTS (64-bit) Bionic Beaver        
    Memory      : 7.7 GiB  
    Processor   : Intel® Core™ i5-8250U CPU @ 1.60GHz × 8    
    Graphics    : Intel® UHD Graphics 620 (Kabylake GT2)  
    Gnome       : 3.28.2  

# Acknowledgement
**This repo is heavily borrowed from [Andrew Shaw's](https://github.com/shawa) IMPLEMENTATION OF IBM MODEL 1**
>*Simple implementation of the EM Algorithm, applied to IBM Model 1 for statistical machine translation.*
