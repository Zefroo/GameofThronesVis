# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 14:41:28 2020

@author: Paul
"""
import csv
from textblob import TextBlob
from collections import Counter



def getWordCounts():
    # get number of words from file. 
    table_rows = []
    with open('gotscript.csv', encoding='utf8') as got_file:
        csv_reader = csv.reader(got_file, delimiter=',')
        next(csv_reader) # skip heading
        for row in csv_reader:
            # make a textblob to get sentiments per sentence (row[3])
            word_blob = TextBlob(row[3])
            # append the word count per sentence and sentiment polarity
            row.append(len(row[3].split()))
            row.append(word_blob.sentiment.polarity)
            table_rows.append(row)
    got_file.close()
    return table_rows 


def getNodeIds():
    """
    

    Returns
    -------
    node_dict 

    """   
    node_dict = {}
    with open('nodes.csv', encoding='utf8') as node_file:
        csv_reader = csv.reader(node_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            node_dict[row[1]] = row[0]
    return node_dict
   

def getEdges():
    edge_dict = {}
    with open('gotscript.csv', encoding='utf8') as got_file:
        csv_reader = csv.reader(got_file, delimiter=',')
        next(csv_reader) # skip heading
        previous = '' 
        for row in csv_reader:
            current = row[4]
            if current not in edge_dict.keys():
                # deal with first item not having a previous item.
                if previous != '':
                    edge_dict[current] = [previous]
                else:
                    edge_dict[current] = []
            else:
                if previous != current:
                    edge_dict[current].append(previous)
            previous = current
    got_file.close()
    # turn list into a counter for each character
    for key in edge_dict:
        edge_dict[key] = dict(Counter(edge_dict[key]))
    # get node ID's from node file
    node_dict = getNodeIds() 
    # place in a edges file
    with open('edges.csv', 'w',newline='') as edge_file:  
        csv_writer = csv.writer(edge_file)
        csv_writer.writerow(["Source", "SourceID", "Target", 
                             "TargetID", "Type", "Weight"])
        for source, targets in edge_dict.items():
            for target, weight in targets.items():
                row = [source, node_dict[source], target, node_dict[target],
                       "undirected", weight]
                csv_writer.writerow(row)
    edge_file.close()

            
#--------------------------------------
# create a new file with the new data on counts and sentiment
def updateFile(table_rows):
    with open('gotscriptnew.csv', 'w',newline='') as new_file:
        csv_writer = csv.writer(new_file)
        #create heading
        csv_writer.writerow(["lineID", "Season", "Episode Name", "Sentence", "Name", "Allegiance",
            "Series Episode Num", "Season Episode Num", "Date", "Word Count", "Sentiment"])
        for row in table_rows:
            csv_writer.writerow(row)
    new_file.close()



#--------------------------------------
def getHodors():
    """
    Count how many times Hodor said his own name
    """
    with open('gotscript.csv', encoding='utf8') as got_file:
        csv_reader = csv.reader(got_file, delimiter=',')
        next(csv_reader)
        hodors = 0
        for row in csv_reader:
            if row[4] == 'Hodor':
                hodors = hodors + len(row[3].split())
    got_file.close()
    return hodors
  
    
def main(): 
    """
    """
    rows = getWordCounts()
    updateFile(rows)
    getHodors()
    getEdges()
    

main()
    
    
