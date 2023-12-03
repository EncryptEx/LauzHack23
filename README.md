# OpenLogsLauz
Unleash the power of AI and let it cook (foundue, if possible) to brew the answers to all of your questions.

This is a project made in LauzHack 2023 at EPFL, Lausane, Switzerland

## Inspiration
We realized that most of our daily programming issues can be identified by looking carefully at the logs. But what a better way to automatize this boring and tedious task. 

## What it does
We have built a Telegram chatbot that lets you upload the log file you want to analyze and what would you like to know about it. It will return the answer to your question. A good example is: 

\*Uploads the log file\*

IN: ` Did the user 'jonny' remove any prrogram in his computer?`

OUT: ` Yes! The user jonny deleted the 'google-chrome-stable' on Nov 27 at 23:57:23`



## How we built
We splited the project into two main parts: the gptCore stuff, and the Telegram API, both programmed in Python3. 

## How to run

Install Python3, git and venv.

If you are using a Debian/ Debian-based OSs you can:
    su root
    apt install git
    apt install Python3
    apt install python-dotenv

Get a telegram bot API key and GPT API key. 
    You can follow these instructions to create a Telegram Bot: https://core.telegram.org/bots#how-do-i-create-a-bot.
    You can


Clone our repo by:

    git clone https://github.com/EncryptEx/LauzHack23

Create a virtualenviroment in python by:

    python3 -m venv env

Then, enter it and install the requirements

    source env/bin/activate
    pip install -r requirements.txt

Create a .venv file using the template in the .env.example file (or just delete the ".example" in the file) and add you API keyes.

And finally, just run the main file!

    python3 chatbot.py



Congrats!! The bot is ready to use.

## Challenges we ran into

We used LLMs (ChatGPT) to cerate a answer taking into account the log file we needed to send a request with a lot of tokens. We started by using chatgpt3.5-turbo with 4k tokens. As a quick fix, we upgraded the version to chatgpt4-turbo-preview with aproximentely 128k tokens of context, meaning that we could upload all the file without choping it in pices. This worked quite well with the downside of being quite expensive (1€/request). Because of that, we had to dongrade the version to chatgpt3.5-16k that is a bit slower but has 4 times the amount context tokens (16k context tokens). With that, we couldn't treat large log files so we opted to chop the files in pices and paralelize the ChatGPT API requests, losing some context but being sustantialy cheaper.

## Accomplishments that we made
## What we learned

We learned quite a lot about Telegram bots and Chat GPT api. We learned about context in LLMs.

## What's next
## Aknowledgements
