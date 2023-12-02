
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()


client = OpenAI()


def analizeLog(prompt):
    messag=[{"role": "system", "content": "You are a chatbot"}]
    
    ## build a chat history: you can CONDITION the bot on the style of replies you want to see - also getting weird behaviors... such as KanyeGPT
    history_bot = ["Yes, I'm ready! Please provide the TCPdump log."]
    
    # ask ChatGPT to return STRUCTURED, parsable answers that you can extract easily - often better providing examples of desired behavior (1-2 example often enough)
    history_user = ["i'll give you a TCPdump log and ask you som questions. for each question answer it. for example if input = (in the log file) Nov 27 22:52:56 exampleuser sudo:    jonny : TTY=pts/0 ; PWD=/home/jonny ; USER=root ; COMMAND=/usr/bin/apt purge google-chrome-stable, did the user jonny delete any program; output = the user jonny deleted google chrome on November 27 22:52:56"]
    

    for user_message, bot_message in zip(history_user, history_bot):
        messag.append({"role": "user", "content": str(user_message)})
        messag.append({"role": "system", "content": str(bot_message)})
    messag.append({"role": "user", "content": str(prompt)})

    response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messag)
    result = ''
    for choice in response.choices:
        result += choice.message.content
    history_bot.append(result)
    history_user.append(str(prompt))
    return result


