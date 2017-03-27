from subprocess import Popen
import os

def main():
    Popen(['hug', '-f', os.getcwd() + '/nodelistener.py'])
