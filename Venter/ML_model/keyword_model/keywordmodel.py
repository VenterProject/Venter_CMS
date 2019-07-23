
# # """
# # Created on Mon Jun 10 17:15:22 2019

# # @author: Anushri Arora
# # """

import json
import os
import time

import numpy as np
from gensim.models import KeyedVectors
from nltk.corpus import stopwords

from Backend.settings import BASE_DIR


def similarityIndex(s1, s2, wordmodel):
    
    #To compare the two sentences for their similarity using the gensim wordmodel 
    #and return a similarity index
    
    if s1 == s2:
        return 1.0

    s1words = s1.split()
    s2words = s2.split()

    s1words = set(s1words)
    for word in s1words.copy():
        if word in stopwords.words('english'):
            s1words.remove(word)
    
    s2words = set(s2words)
    for word in s2words.copy():
        if word in stopwords.words('english'):
            s2words.remove(word)

    s1words = list(s1words)
    s2words = list(s2words)

    s1set = set(s1words)
    s2set = set(s2words)

    vocab = wordmodel.vocab
    
    if len(s1set & s2set) == 0:
        return 0.0
    for word in s1set.copy():
        if (word not in vocab):
            s1words.remove(word)
    for word in s2set.copy():
        if (word not in vocab):
            s2words.remove(word)
    
    return wordmodel.n_similarity(s1words, s2words)


def wmd_similarity(single_comment, single_keyword, wordmodel):
    
    cwords = single_comment.split()
    cwords = set(cwords)
    for word in cwords.copy():
        if word in stopwords.words('english'):
            cwords.remove(word)
        
    cwords = list(cwords)

    swords = single_keyword.split()
    swords = set(swords)
    for word in swords.copy():
        if word in stopwords.words('english'):
            swords.remove(word)

    swords = list(swords)
    
    return wordmodel.wmdistance(cwords, swords)

def categorizer(keywords):
    
    #driver function,
    #returns model output mapped on the input corpora as a dict object
    
    stats = open('stats.txt', 'w', encoding='utf-8')

    st = time.time()
    
    wordmodelfile = os.path.join(BASE_DIR, 'Venter/ML_model/Civis/MAX.bin')
    wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True, limit=200000)

    wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary=True, limit=200000)
    et = time.time()
    s = 'Word embedding loaded in %f secs.' % (et-st)
    print(s)
    stats.write(s + '\n')

    #filepaths
    #responsePath = os.path('./comments/')
    responsePath= os.path.join(BASE_DIR, 'Venter/ML_model/Civis/data/keyword data/')
    responseDomains = os.listdir(responsePath)
    #responseDomains.sort()
    
    #dictionary for populating the json output
    results = {}
    for responseDomain in zip(responseDomains):
        #instantiating the key for the domain
        print("-----------------------inside CATEGORIZER() of keyword model at4---------------------")
        print("ResponseDomain before is: ",responseDomain)
        print("type of BEFORE: ", type(responseDomain))
        responseDomain=str(responseDomain)
        domain=responseDomain[2:-7]
        domain=domain.lower()
        responseDomain=responseDomain[2:-3]
        #domain = responseDomain[:-4]
        print("=============================================================")
        
        print("ResponseDomain after is: ",responseDomain)
        print("type of AFTER: ", type(responseDomain))
        print("Domain is: ",domain)
        print("=============================================================")
        results[domain] = {}

        print('Categorizing %s domain...' % domain)

        temp = open(os.path.join(responsePath, responseDomain), 'r', encoding='utf-8-sig')
        responses = temp.readlines()
        rows=0
        for response in responses:
            #response = list(filter(None, response.lower().split('.'))) 
            num=0
            # if '\n' in response:
            #     num+=1
            # rows+=(len(response)-num)
            if response=='\n':
                num+=1
            rows+=(len(response)-num)
            
        categories=keywords[domain]
        columns = len(categories)

        #categories = category
        #saving the scores in a similarity matrix
        #initializing the matrix with -1 to catch dump/false entries
        st = time.time()
        similarity_matrix = [[-1 for c in range(columns)] for r in range(rows)]
        et = time.time()
        s = 'Similarity matrix initialized in %f secs.' % (et-st)
        print(s)
        stats.write(s + '\n')

        row = 0
        st = time.time()
        for response in responses:
            #response = list(filter(None, response.lower().split('.'))) 
            print("Row: ",row)
            # for single_response in response:
            #     # print("Current sentence is: ",single_response)
            #     if len(single_response) == 1:
            #         continue
            #     #print(single_response)
            #     if single_response=='\n':
            #         continue
            #     else:
            #         column = 0
            #         for category in categories:
            #             # print("Current category is: ",category)
            #             similarity_matrix[row][column] = wmd_similarity(single_response, category, wordmodel)
            #             column += 1
            if response=='\n':
                    continue
            else:
                column = 0
                for category in categories:
                    # print("Current category is: ",category)
                    similarity_matrix[row][column] = wmd_similarity(response, category, wordmodel)
                    column += 1
            row += 1
        et = time.time()
        s = 'Similarity matrix populated in %f secs. ' % (et-st)
        print(s)
        stats.write(s + '\n')

        print('Initializing json output...')
        for catName in categories:
            results[domain][catName] = []

        print('Populating category files...')
        for score_row, response in zip(similarity_matrix, responses):
            #max_sim_index = len(categories)-1
            #response = list(filter(None, response.lower().split('.'))) 
            # for single_response in response:
            #     if single_response!='\n':
            #         # print("Current score row: \n",np.array(score_row))
            #         min_sim_index=len(categories)-1
            #     #if np.array(score_row).sum() > 0:
            #         min_sim_index = np.array(score_row).argmin()
            #         temp = {}
            #         temp['response'] = single_response
            #         temp['score'] = float((np.array(score_row).min()))
            # # else:
            #         #temp = response
            #         results[domain][categories[min_sim_index]].append(temp)
            if response!='\n':
                    # print("Current score row: \n",np.array(score_row))
                min_sim_index=len(categories)-1
                #if np.array(score_row).sum() > 0:
                min_sim_index = np.array(score_row).argmin()
                temp = {}
                temp['response'] = single_response
                temp['score'] = int((np.array(score_row).min()))
            # else:
                    #temp = response
                results[domain][categories[min_sim_index]].append(temp)
        print('Completed.\n')

        #sorting domain wise categorised responses based on scores
        for domain in results:
            for category in results[domain]:                                                                                                                                 
                temp = results[domain][category]
                if len(temp)==0 or category=='Novel':
                    continue
                #print(temp)
                results[domain][category] = sorted(temp, key=lambda k: k['score'], reverse=True)
        #newlist = sorted(list_to_be_sorted, key=lambda k: k['name']) --> to sort list of dictionaries

        print('***********************************************************') 

        with open('anushri_keyword_2_json_data.json', 'w') as temp:
            json.dump(results, temp)
    
    return results
