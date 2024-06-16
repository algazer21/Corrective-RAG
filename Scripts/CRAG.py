import sys
import os

# Import script modules
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../Scripts')))
from datacleaner import data_cleaner
from RetrievalSystemWeb import CRAG

if __name__ == "__main__":  
    if len(sys.argv) != 2:
        print("ERROR, please use: python3 CRAG.py 'query'")
    else:
        arg1 = sys.argv[1]
    
    corpus,_,answers = data_cleaner()
    CRAG(
        query = arg1,
        corpus = corpus,
        answers = answers,
        safeURLs = ['keytruda.com','wikipedia'],
        printp = False
    )