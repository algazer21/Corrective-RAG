import nltk
import google.generativeai as genai
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
from openai import OpenAI
import textwrap
import time
import http.client
import json
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


def evaluator(query,corpus,answers):
    """ Evaluates whether the corpus is relevant to the query.
        Returns the relevant context if True, else returns False
    Args:
        query:      String query to evaluate
        corpus:     Documents array to search for information
        answers:    Answers array from the corpus without the questions
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
    
    if response.text == "Yes":
        return context,False
    else:
        return query,True


def CRAG(query,corpus,answers,safeURLs):
    """
    Calls the evaluator model given a query, a corpus and the set of answers.
    Then, calls the generation model if the evaluator model autorizes.
    Returns the system response.
    Args:
        query:      String query to evaluate
        corpus:     Documents array to search for information
        answers:    Answers array from the corpus without the questions
        safeURLs:   List of safe websites to search for information. If it is empty it will search anywhere.
    """
    #Calls the evaluator
    context,boo = evaluator(query,corpus,answers)
    
    #Define model and prompt
    with open("../APIS/gpt.txt", 'r') as file: apik = file.readline().strip()
    client = OpenAI(api_key = apik)
    model = "gpt-4o"#3.5-turbo"

    if boo:
        time.sleep(1.5)
        context,errors = WebRequest(context,safeURLs)
    else:
        errors = False

    prompt = f"""
    Please generate an informative and concise response to the following query.
    Use the provided context information to ensure your response is accurate and relevant.

    Context: {context}
    """

    completion = client.chat.completions.create(
                model=model,
                messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
                ],
                max_tokens=120
            )
    return completion.choices[0].message.content,errors,boo


def WebRequest(query,safeURLs = []):
    """
    Make a Web request of a query summary in provided safe URLs.
        Args:
            query:    text to web search
            safeURLs: list of safe websites to search for information. If it is empty it will search anywhere.
    """

    #Summarize query for web search
    promptQ = "Summarize this query to a maximum of 4 words to perform an internet search: \nQuery: "
    queryW = generGemini(promptQ+query)
    #print(f"Web Query: {queryW}")

    #Call the API search
    with open("../APIS/serper.txt", 'r') as file: apiw = file.readline().strip()
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": queryW})
    headers = {'X-API-KEY': apiw,'Content-Type': 'application/json'}
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response_dict = json.loads(data.decode("utf-8"))
    
    #Extract snippets from safe URLs
    webCorpus = ""
    webSecureCorpus = ""
    for sni in response_dict['organic']:
        for urls in safeURLs:
            if urls in sni["link"]:
                webSecureCorpus += " "+sni['snippet']
        webCorpus += " "+sni['snippet']
    
    errors = False
    if safeURLs:
        if len(webSecureCorpus)>0:
            webCorpus = webSecureCorpus
        else:
            errors = True
            #print("Error, no results found for the provided URLs")
    #print(textwrap.fill(webCorpus[:200]))
    
    #Summarize web corpus
    promptZ = f"Summarize this corpus to a maximum of 2 sentences to try to answer ONLY this query: \nCorpus: {webCorpus} \nQuery: {query} \nResponse: "
    response = generGemini(promptZ)
    return response,errors