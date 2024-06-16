import pandas as pd

def data_cleaner():
    """
    Load data from 'Dataset' directory and returns a clean complete corpus and a pair of separate
    arrays of questions and answers. 
    """
    data_dir = "../Dataset/DS_exam.xlsx"
    data = pd.read_excel(data_dir, skiprows = [0,1], header = None)     #Take only usefull rows
    col = pd.concat([data.iloc[0][:5], data.iloc[1][5:]])               #Organize data columns
    data = data[2:]
    data.reset_index(drop=True, inplace=True)                     
    data.columns = col                                                  #Update data columns

    data = data.drop(index = 22)                                        #Instance without answer
    data = data.reset_index(drop=True)
    na_quest = data[data.Question.isnull()].index                       #Indices from null questions
    na_answ = data[data['Answer/Solution'].isnull()].index              #Indices from null answers


    corpus = [f"Question: {data.Question.iloc[i]}:\n Answer: {data['Answer/Solution'].iloc[i]}"\
              for i in range(len(data))]  #Q/A Corpus
    
    questions = list(data.Question)
    answers = list(data['Answer/Solution'])

    for i,Q in zip(na_answ,data.Question.iloc[na_answ]):
        corpus[i] = Q.replace("Q: ","Question: ").replace("A: ","Answer: ")
        questions[i] = Q.split("\n ")[0].replace("Q: ","")
        answers[i] = Q.split("\n   A:")[1]
    for i,A in zip(na_quest,data['Answer/Solution'].iloc[na_quest]):
        corpus[i] = A.replace("Q: ","Question: ").replace("A: ","Answer: ")
        questions[i] = A.split("\n ")[0].replace("Q: ","")
        answers[i] = A.split("\n   A:")[1]
    
    print(f"{len(corpus)} Question/Answer pairs extracted!")
    return(corpus,questions,answers)
