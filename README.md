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
    - [**Custom messages**](#custom-messages)
## Introduction
The goal is to do a simple Discord bot that plays youtube videos in a voice chat.<br>

Copyright : <br>
2019 Valentin B. on github.

### **TODO List**
- [ ] More customization
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
- [Custom messages](#Custom-names)


### **Custom command names**
TODO

### **Custom messages**
TODO