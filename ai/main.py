from time import sleep
from openai import OpenAI
import os
client = OpenAI() 

from dotenv import load_dotenv

load_dotenv()

limit = 128000 # depends on the model


messag = None # Set to none each time you want to start a new conversation
history_bot = None
history_user = None
def analizeLog(prompt):
    global messag, history_bot, history_user
    if(messag == None):
        messag=[{"role": "system", "content": "You are a chatbot"}]
    
        ## build a chat history: you can CONDITION the bot on the style of replies you want to see - also getting weird behaviors... such as KanyeGPT
        history_bot = ["Yes, I'm ready! Please provide the log to scan."]
    
        # ask ChatGPT to return STRUCTURED, parsable answers that you can extract easily - often better providing examples of desired behavior (1-2 example often enough)
        history_user = ["""I'll give you by parts a log file and ask you some questions. 
                    Just answer 'OK' if the input does NOT START WITH 'EOF'. 
                    After the log (when you recieved the 'EOF') we'll ask some questions, an example input = (in the log file) Nov 27 22:52:56 exampleuser sudo:    jonny : TTY=pts/0 ; PWD=/home/jonny ; USER=root ; COMMAND=/usr/bin/apt purge google-chrome-stable, did the user jonny delete any program; 
                    output = the user jonny deleted google chrome on November 27 22:52:56. """]
        # Remember that you should answer 'OK' unless you see EOF in the start of the prompt, that means that question is ready to be answered since the log file has been already sent by its entirety
    

        for user_message, bot_message in zip(history_user, history_bot):
            messag.append({"role": "user", "content": str(user_message)})
            messag.append({"role": "system", "content": str(bot_message)})
    messag.append({"role": "user", "content": str(prompt)})

    response = client.chat.completions.create(model="gpt-4-1106-preview",
        messages=messag)
    result = ''
    for choice in response.choices:
        result += choice.message.content
   
    messag.append({"role": "system", "content": str(result)})
   
   
    return result




def askGPT(filePath, question):
    aux = question+"\n "
    isFirsttime = True
    iCounter = 0
    aux = ""
    with open(filePath, "r") as f:
        aux = f.read()
        while len(aux) >= limit:
            print(analizeLog(aux[:limit]))
            aux = aux[limit:]
            sleep(1)

    if aux:
        print(analizeLog(aux))
    print(analizeLog("EOF From the previous sent log, "+question))


client.api_key = os.getenv("OPENAI_API_KEY")

# fp = "/home/jaume/Desktop/CODE/LauzHack23/bot/examples/auth.log"
# question = "Did the user jonny delete any program?"

# print(askGPT(fp, question))