# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import library
import numpy as np
import tensorflow as tf
import re
import time

#import dataset
lines=open('movie_lines.txt',encoding='utf-8',errors='ignore').read().split('\n')
conversations=open('movie_conversations.txt',encoding='utf-8',errors='ignore').read().split('\n')

#creating a dictonary that maps each line and its id

id2line={}
for line in lines:
    _line=line.split('+++$+++')
    if len(_line)==5:
        id2line[_line[0]]=_line[4]
        
        
#creating a list of all of the conversations 
        
conversations_ids=[]
for conversation in conversations[:-1]:
    _conversation=conversation.split('+++$+++')[-1][1:-1].replace(" ' ", "").replace(" " , "")
    conversations_ids.append(_conversation.split(','))
    
#Getting separately the questions and the answers

questions=[]
answers=[]
for conversation in conversations_ids:
    for i in range(len(conversation)-1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])

#Doing a first cleaning of texts

def clean_text(text):
    text=text.lower()
    text=re.sub(r"i'm","i am",text)
    text=re.sub(r"he's","he is",text)
    text=re.sub(r"she's","she is",text)
    text=re.sub(r"thats's","that is",text)
    text=re.sub(r"whats's","what is",text)
    text=re.sub(r"where's","where is",text)
    text=re.sub(r"\'ll","will",text)
    text=re.sub(r"\'ve","have",text)
    text=re.sub(r"\'re","are",text)
    text=re.sub(r"\'d","would",text)
    text=re.sub(r"won't","will not",text)
    text=re.sub(r"can't","can not",text)
    text=re.sub(r"[-()\"#/@;:<>{}+=~|.?]","",text)
    return text

#cleaning questions

clean_questions=[]
for question in questions:
    clean_questions.append(clean_text(question))

#cleaning answer

clean_answers=[]
for answer in answers:
    clean_answers.append(clean_text(answer))
#creating a dictonary that maps each word to its number of occurances

word2count={}
for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word]=1
        else:
            word2count[word]+=1

for an in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word]=1
        else:
            word2count[word]+=1