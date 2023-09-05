# Authors

- Ernesto Barría
- Sebastián Gutiérrez

# Description

Placeholder

# Installation

-Open Powershell as Administrator

-Execute `pip install -r requirements.txt`

-Create a python virtual environment with `python -m venv .env`

-Execute `Set-ExecutionPolicy RemoteSigned` -> `O`

-Activate virtual environment: `get-acl .env\Scripts\activate`

# How to use

-Execute `python mp.py --help` to see commands

-Execute `python mp.py {command} --help` to see how to use command

-Execute `python mp.py config` to configurate master password

    -Write master password
    
    -Rewrite master password
    
-Execute `python mp.py add {password} {flag1} {flag2} ... {flagn}` to see add password to the database

-Execute `python mp.py search` to search by flag in database

-Execute `python mp.py remaining` to see time left in current session
