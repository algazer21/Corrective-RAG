import nltk
import google.generativeai as genai
from rank_bm25 import BM25Okapi
from openai import OpenAI
from nltk.tokenize import word_tokenize
nltk.download('punkt')

def callGemini():
    """
    Call Gemini-pro reading the API key. 
    Return the model module and safety settings.
    """

    with open("../APIS/Gemini.txt", 'r') as file: apiG = file.readline().strip()
    genai.configure(api_key=apiG)
    model = genai.GenerativeModel('gemini-pro')
    safety= {'HARASSMENT':'block_none','HARM_CATEGORY_HATE_SPEECH':'block_none',
                  'HARM_CATEGORY_HARASSMENT':'block_none','HARM_CATEGORY_SEXUALLY_EXPLICIT':'block_none',
                  'HARM_CATEGORY_DANGEROUS_CONTENT':'block_none'}
    return model,safety

def generGemini(prompt):
    """
    Generate text using gemini pro and the input prompt.
    Return text response.
    """

    model,safety = callGemini()
    response = model.generate_content(prompt,safety_settings=safety)
    return response.text

def evaluator(query,corpus,answers,printp=True):
    """ Evaluates whether the corpus is relevant to the query
    Args:
        query:      String query to evaluate
        corpus:     Documents array to search for information
        answers:    Answers array from the corpus without the questions
        safety:     Dic safety setting for Gemini generation
        printp:        Bool variable. If True print the complete prompt
    """

    #Prompt instructions for evaluate the query-answer pair
    instructions = """Does the following document have exact information to answer the following query?
    Please choose one of the two possible options: Yes, or No.
    """
    model,safety = callGemini()                             #Calling Gemini

    #Extract the most relevant document using bm25
    doc_tokens = [word_tokenize(doc.lower()) for doc in corpus]
    bm25 = BM25Okapi(doc_tokens)
    query_tokens = word_tokenize(query.lower())
    top_docs = bm25.get_top_n(query_tokens, corpus, n=1)
    question = top_docs[0]                                  #Most relevant document
    indx = corpus.index(question)                           #Most relevant document index
    context = answers[indx]                                 #Most relevant answer

    #Final prompt for Gemini and Evaluation
    prompt = f"{instructions}\n\n\
        Question: {query}\n\n\
        Document: {context}\n\n\
        Evaluation: [Select one: Yes, No]:"
    response = model.generate_content(prompt,safety_settings=safety)

    if printp:
        print(prompt)
        print(response.text)
    return context if response.text == "Yes" else False


def CRAG(query,corpus,answers):
    """
    Calls the evaluator model given a query, a corpus and the set of answers.
    Then, calls the generation model if the evaluator model autorizes.
    Returns the system response.
    Args:
        query:      String query to evaluate
        corpus:     Documents array to search for information
        answers:    Answers array from the corpus without the questions
        client:     GPT client
    """
    #Calls the evaluator
    context = evaluator(query,corpus,answers)

    #Define model and prompt
    with open("../APIS/gpt.txt", 'r') as file: apik = file.readline().strip()
    client = OpenAI(api_key = apik)
    model = "gpt-3.5-turbo"
    prompt = f"""
    Please generate an informative and concise response to the following query.
    Use the provided context information to ensure your response is accurate and relevant.

    Context: {context}
    """
    #If context != False, we will call GPT to generate a response given a query and the context
    if context:
        completion = client.chat.completions.create(
                model=model,
                messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
                ],
                max_tokens=120
            )
        print("\n\n GENERATOR RESPONSE:")
        print(completion.choices[0].message.content)
    else:
        print("I cant answer this prompt due a lack of proper information in the database")