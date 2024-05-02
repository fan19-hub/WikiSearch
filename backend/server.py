from flask import Flask, request
from flask_cors import CORS
import json
from LLM import GPT3
from retrievedoc import *
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


# Initialization
print("Starting server...")
print("Loading retriever...This usually takes 3-4 minutes.")
myretriever = retriever()
print("1/3 done")


print("Loading chatbot...")
nobot = False
try:
    model = GPT3()
    with open("prompt.md", "r") as f:
        template = f.read()
    
except:
    nobot=True
    print("No OpenAI API key provided. Set no bot mode")


print("2/3 done")


print("App intializing...")
app = Flask(__name__)
CORS(app)
print("3/3 done, server started.")


# rest controllers
@app.route('/ad_search', methods=['POST'])
def ad_search():    
    # parse
    data = request.get_json()
    try:
        query = data["term"]
    except:
        return json.dumps({"msg": "invalid request"})
    
    # text retrieval
    res_list = myretriever.retrieve_alldocs(15,query)

    res= {      
        "search_res": res_list
    }

    return json.dumps(res)



@app.route('/bot_summary', methods=['POST'])
def bot_summary():    
    # parse
    data = request.get_json()
    try:
        query = data["query"]
        search_res = data["search_res"]
    except:
        return json.dumps({"msg": "invalid request"})
    
    # bot summary
    search_res = search_res[:1500]
    if nobot:
        return json.dumps({"bot_summary": "No OpenAI API key provided. Please provide a valid key"})
    try:
        prompt=template.format(QUERY = query, SEARCH_RES = search_res)
        bot_summary = model.generate(prompt, max_length=200)
    except:
        return json.dumps({"bot_summary": "Error in generating summary. Please check if the software is complete and the network is working."})

    res= {      
        "bot_summary": bot_summary
    }

    return json.dumps(res)



# main
if __name__ == '__main__':
    app.run()