# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 12:54:50 2021

@author: NergizUnal
"""
import string
import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')
import random, re, time, string
from copy import copy as duplicate
from enum import Enum


class Cell(object):
    def __init__(self,letter = None, mark = 'A',x = 0,y = 0):
        self.letter = letter
        self.mark = mark # B -> Blocked A-> Available V -> Vertical Crossable H-> Horizontal Crossable 
        self.x = x
        self.y = y
       
    def setLetter(self,letter,dir):
        self.updateMark(dir)
        self.letter = letter
            
    def updateMark(self, newMark):
        if(self.mark == 'A'):
            self.mark = newMark
        elif(self.mark == 'B'):
            self.mark = 'B'
        else:
            if(self.letter == '*'):
                self.mark = newMark
            else:
                self.mark = 'B'


class Grid(object):
    def __init__(self, row, col ,keys, words = None):
        self.row = row
        self.col = col
        self.cells= [[]]
        self.dict = {k: set() for k in keys}
        self.waitingWords = words
        self.puttedWords = []
        self.minX = 2000
        self.maxX = 0
        self.minY = 2000
        self.maxY = 0
        
    def startCells(self): 
        self.cells = [[Cell(letter = '*',mark = 'A',x = i, y = j) for j in range(2*self.col + 5)] for i in range(2*self.row + 5)]
    
   
    def putWord(self, word):
        return
    def canBePlaced(self,word, crossIndex,cell):
        if(cell.mark == 'H'): #horizontal
            starty = cell.y - crossIndex
            endy = starty + len(word)
            if(endy > self.maxY):
                if(endy-self.minY > self.col):
                    return False
                #self.maxY = endy
            if(starty < self.minY):
                if(self.maxY-starty > self.col):
                    return False
                #self.minY = starty
            for l in range(len(word)):
                c = self.cells[cell.x][starty + l]
                if(c.mark == 'B' or c.mark == 'V'):
                    return False
                elif(c.mark == 'H'):
                    if(not(c.letter == '*' or word[l] == c.letter)):
                        return False 
        else: #vertical
            startx = cell.x - crossIndex
            endx = startx + len(word)
            if(endx > self.maxX): 
                if(endx-self.minX > self.row):
                    return False
               # self.maxX = endx
            if(startx < self.minX):
                if(self.maxX-startx > self.row):
                    return False
               # self.minX = startx
            for l in range(len(word)):
                c = self.cells[startx + l][cell.y]
                if(c.mark == 'B' or c.mark == 'H'):
                    return False
                elif(c.mark == 'V' ):
                    if(not(c.letter == '*' or  word[l] == c.letter)):
                        return False 
        return True

   
                
                
    def updateCells(self, word):
        self.dict[keys]
        return

    
    def insertWord(self, nextWord, cell, crossIndex):
        if(cell.mark == 'H'):
            starty = cell.y - crossIndex
            endy = starty + len(nextWord)
            if(endy > self.maxY):
                if(endy-self.minY > self.col):
                    self.maxY = endy
            if(starty < self.minY):
                if(self.maxY-starty > self.col):
                    self.minY = starty
            for i in range(len(nextWord)):
                c = self.cells[cell.x][starty + i]
                c.setLetter(nextWord[i],'H')
        else:
            startx = cell.x - crossIndex
            endx = startx + len(nextWord)
            if(endx > self.maxX): 
                if(endx-self.minX > self.row):
                    self.maxX = endx
            if(startx < self.minX):
                if(self.maxX-startx > self.row):
                     self.minX = startx
            for i in range(len(nextWord)):
                c = self.cells[startx + i][cell.y]
                c.setLetter(nextWord[i],'V')
        self.updateCells()
            
        return
    def updateDict(self):
        for r in self.cells:
            for c in r:
                if(c.letter != '*'):
                    if(c.letter in self.dict):
                        self.dict[c.letter].add(c)
                    else:
                        self.dict[c.letter] = {c}
                        
    def possibleIntersections(self,nextWord):
        for i in range(len(nextWord)):
            for r in self.cells:
                for c in r:
                    if(c.letter != '*'):
                        if(c.letter == nextWord[i]):
                            if(self.canBePlaced(nextWord,c,i)):
                                if(i in nextWord.dict.keys()):    
                                    nextWord.dict[i].add(c)
                                else: 
                                    nextWord.dict[i] = {c}

        for i in range(len(nextWord)):
            if nextWord[i] in self.dict:
                for c in self.dict[nextWord[i]]:
                    if(self.canBePlaced(nextWord,c,i)):
                        nextWord.dict[i].add(c)
        

class Word(object):
    def __init__(self, word = None, cells = []):
        self.word = re.sub(r'\s', '', word.lower())
        self.length = len(self.word)
        self.cells = cells
        self.dict = {i: None for i in range (len(word))}
        
    def updateDict(self):
        return
    

keys = "" # "abcçdefgğhıijklmnoöprsştuüvyz"
g = Grid(3,4,keys)
g.startCells()


g.cells[1][1].setLetter('a', 'V')    
g.cells[1][2].setLetter('a', 'V')
g.cells[1][1].setLetter('a', 'V')
g.cells[1][1].setLetter('a', 'V')
g.cells[1][3].setLetter('a', 'V')
g.updateDict()

print(len(g.dict))
print(g.dict)


for k,v in g.dict.items():
    print(k,v)
    
print(len(g.dict['a']))
for r in g.cells:
    for c in r:
        print(c.letter,end = " ")
    print()
    
for r in g.cells:
    for c in r:
        print(c.mark,end = " ")
    print()