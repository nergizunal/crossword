# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 15:18:35 2021

@author: NergizUnal
"""

import random, re, time, string
from copy import copy as duplicate

"""  H -> only if there is a intersection word and direction is horizontal
    V -> only if there is a intersection word and direction is vertical
    B -> Blocked
    - -> available, no condition
    O -> intersectable letter
"""
class Crossword(object):
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.waiting_word_list = []
        self.putted_word_list = []
    
    def initialize_grid(self):
        self.grid = []
        for i in range(self.rows):
            r = []
            for j in range(self.cols):
                r.append('')   
            self.grid.append(r)
            
    def initialize_shadow_grid(self):
        self.shadow_grid = []
        for i in range(self.rows):
            r = []
            for j in range(self.cols):
                r.append('-')
            self.shadow_grid.append(r)
        
            
    def update_shadow_grid(self, last_added_word):
        if(last_added_word.dir == 1):
            for i in range(last_added_word.length):
                self.newMark(last_added_word.row,last_added_word.col + i, 'O')
                self.newMark(last_added_word.row + 1 , last_added_word.col + i, 'V')
                self.newMark(last_added_word.row - 1, last_added_word.col + i, 'V')
            self.newMark(last_added_word.row, last_added_word.col - 1, 'B')
            self.newMark(last_added_word.row, last_added_word.col + last_added_word.length, 'B')
          
        else:
            for i in range(last_added_word.length):
                self.newMark(last_added_word.row + i,last_added_word.col , 'O')
                self.newMark(last_added_word.row + i , last_added_word.col + 1, 'H')
                self.newMark(last_added_word.row + i , last_added_word.col - 1, 'H')
            self.newMark(last_added_word.row -1 , last_added_word.col, 'B')
            self.newMark(last_added_word.row + last_added_word.length , last_added_word.col, 'B')
            
        for i in range(len(self.shadow_grid)):
           for j in range(len(self.shadow_grid[i])):
               if(self.shadow_grid[i][j] == 'O'):
                    if (self.shadow_grid[i - 1][j] == 'B' or self.shadow_grid[i + 1][j] == 'B'):
                       if(self.shadow_grid[i][j-1] == 'B' or self.shadow_grid[i][j+1] == 'B'):
                           self.newMark(i,j,'B')
   
    def newMark(self,x ,y, new):
        var = self.shadow_grid[x][y]
    
        if (var == 'B' or new == 'B') or ((var == 'V' and new == 'H')or(var == 'H' and new == 'V') or (var == 'O' and new == 'O')): #if it is already blocked it cannot be changed with any other mark
             self.shadow_grid[x][y] = 'B'
             return
        elif(var == 'O'):
            if(new == 'B'):
                self.shadow_grid[x][y] = 'X'
            else: 
                return
        else:
            self.shadow_grid[x][y] = new
            return
        
            
    def possible_intersection_pairs(self, word):
        for i in range(len(self.shadow_grid)):
            for j in range(len(self.shadow_grid[i])):
                if self.shadow_grid[i][j] == 'O' and word.contains(self.grid[i][j]):
                    if(self.canBePlaced(word, i - 3, j, -1*(1))):
                        return i,j,word
                    
    def canBePlaced(self, word, x, y, dir):
            return False       
        
    def tryToPut(self, word, x ,y , dir):
             
        self.waiting_word_list.remove(word)
        word.row = x
        word.col = y
        word.dir = dir
        self.putted_word_list.append(word)
        self.update_shadow_grid(self, word)
        return
                
    def tryToExtendGrid(self, rowAdd,colAdd):
        return
    
    
        


class Word(object):
    def __init__(self, word=None):
        self.word = re.sub(r'\s', '', word.lower())
        self.length = len(self.word)
        
        
        
    
  
class WaitingWord(Word):
    def __init__(self, word = None):
        super().__init__(self, word)
        self.score = 0
      
        
class PuttedWord(Word):
    def __init__(self, word=None):
        super.__init__(self, word)
        self.row = None
        self.col = None
        self.dir = None
        self.list = []*self.length
    
   
        
        
class Cell(object):
    def __init__(self,letter, x, y):
        self.letter = letter
        self.dir = None
        self.mark = 'A'
        self.x = x
        self.y = y
    
    def updateLetter(letter):
        self.letter = letter
        
    def updateMark(newMark):
        self.mark = newMark
        
        

    
        
        
        
a = Crossword(10, 10)  
w = Word("nergiz")
w.col = 3
w.row = 1
w.dir = -1
w3 = Word("nergiz")
w3.col = 5
w3.row = 1
w3.dir = -1
w2 = Word("nergiz")
w2.col = 2
w2.row = 2
w2.dir = 1
a.initialize_shadow_grid()
a.update_shadow_grid(w)
a.update_shadow_grid(w2)
a.update_shadow_grid(w3)

for r in a.shadow_grid:
    for c in r:
        print(c,end = " ")
    print()