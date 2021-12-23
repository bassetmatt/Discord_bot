# Discord bot project
- [Discord bot project](#discord-bot-project)
  - [Introduction](#introduction)
    - [**TODO List**](#todo-list)
  - [Requierments](#requierments)
    - [**Python version**](#python-version)
    - [**Librairies**](#librairies)
  - [The Bot](#the-bot)
    - [**Token activation**](#token-activation)
    - [**How to run it**](#how-to-run-it)
    - [**How to use it in discord**](#how-to-use-it-in-discord)
  - [Customization](#customization)
    - [**Custom command names**](#custom-command-names)
    - [**Custom messages and reactions**](#custom-messages-and-reactions)
## Introduction
The goal is to do a simple Discord bot that plays youtube videos in a voice chat.<br>

Copyright : <br>
2019 Valentin B. on github.

### **TODO List**
- [ ] Playlist support
- [ ] Possibility to go back in the queue
- [x] More customization
- [x] Custom messages

---
## Requierments

### **Python version**

Coded using Python 3.10 .<br>
(TODO check) 3.5 might be enough.

### **Librairies**
Some librairies such as :
- discord
- pynacl 
- youtube-dl
- dotenv
<br>
`pip install discord pynacl youtube-dl python-dotenv`

---
## The Bot

To make it work, be sure to have created a Discord application, many simple tutorials exist online.

### **Token activation**
To make the code work on your personal bot, get the token of the bot, and paste it in a `.env` file that must be in `/src`. <br>
The syntax to use in the file is : `DISCORD_TOKEN=Owf5Qg`.

### **How to run it**
Run the file `main.py` with any python interpreter.

### **How to use it in discord**
First you have to check what is your pre-command operator <br>
You can configure it in the .env file with the syntax `COMMAND_SYMBOL=!` and replace `!` with whatever you want, any length.


---
## Customization
- [Custom command names](#Custom-command-names)
- [Custom messages and reactions](#Custom-names-and-reactions)


### **Custom command names**
Go edit the file `settings.json` in the `config` subdirectory and change the names that you want to change. <br>
You can also give aliases to functions.

### **Custom messages and reactions**
Same as names, same file.<br>
You can send several messages by putting them into a list like : `["msg1","msg2"]`<br>
The same goes for reactions, you can have them as single characters, or as lists, see the default file to understand better<br>
And if you don't want messages or reaction, don't delete the field but keep them as empty strings.