# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import library
import re

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

# Creating two dictonaries that map the questions and the answers words to a unique integer

threshold = 20
questionsword2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        questionsword2int[word] = word_number
        word_number += 1
answersword2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        answersword2int[word] = word_number
        word_number += 1

# Adding the last tokens to these dictionaries
tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
for token in tokens:
    questionsword2int[token] = len(questionsword2int) - 1
for token in tokens:
    answersword2int[token] = len(answersword2int) - 1

# Creating the inverse dictionary of the answerword2int dictionary

answersints2words = {w_i: w for w, w_i in answersword2int.items()}

# Adding the end of the string token to the end of every answer
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS> '

# translating all the questions and the answers into integers
# and replacing all the words that were filtered out by <OUT>
questions_to_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionsword2int:
            ints.append(questionsword2int['<OUT>'])
        else:
            ints.append(questionsword2int[word])
        questions_to_int.append(ints)
answers_to_int = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answersword2int:
            ints.append(answersword2int['<OUT>'])
        else:
            ints.append(answersword2int[word])
        questions_to_int.append(ints)

# Sorting questions and answers by the length of the questions

sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1, 25 + 1):
    for i in enumerate(questions_to_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_to_int[i[0]])
            sorted_clean_answers.append(answers_to_int[i[0]])
