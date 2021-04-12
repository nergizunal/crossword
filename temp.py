# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 15:18:35 2021

@author: NergizUnal
"""

import random, re, time, string
from copy import copy as duplicate


class Crossword(object):
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.current_word_list = []
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
            for i in range(last_added_word.length-1):
                self.newMark(last_added_word.row,last_added_word.col + i, 'L')
                self.newMark(last_added_word.row + 1 , last_added_word.col + i, 'H')
                self.newMark(last_added_word.row - 1, last_added_word.col + i, 'H')
            self.newMark(last_added_word.row, last_added_word.col - 1, 'B')
            self.newMark(last_added_word.row, last_added_word.col + last_added_word.length -1, 'B')
          
        else:
            for i in range(last_added_word.length-1):
                self.newMark(last_added_word.row + i,last_added_word.col , 'L')
                self.newMark(last_added_word.row + i , last_added_word.col + 1, 'V')
                self.newMark(last_added_word.row + i , last_added_word.col - 1, 'V')
            self.newMark(last_added_word.row -1 , last_added_word.col, 'B')
            self.newMark(last_added_word.row + last_added_word.length -1 , last_added_word.col, 'B')
           
   
    def newMark(self,x ,y, new):
        var = self.shadow_grid[x][y]
        if (var == 'B' or var == 'L'):
            return
        elif((var == 'V' and new == 'H')or(var == 'H' and new == 'V')):
            self.shadow_grid[x][y] = 'B'
        else:
            self.shadow_grid[x][y] = new
    def possible_intersections(self, word):
        for i in self.shadow_grid.length:
            for j in self.shadow_grid[i].length:
                if self.shadow_grid[i][j] == 'L' and self.grid[i][j] == word[0]:
                    return
                    

class Word(object):
    def __init__(self, word=None):
        self.word = re.sub(r'\s', '', word.lower())
        self.length = len(self.word)
        self.row = None
        self.col = None
        self.dir = None
a = Crossword(10, 10)  
w = Word("nergiz")
w.col = 3
w.row = 2
w.dir = -1
w2 = Word("nergiz")
w2.col = 2
w2.row = 2
w2.dir = 1
a.initialize_shadow_grid()
a.update_shadow_grid(w)
a.update_shadow_grid(w2)
for r in a.shadow_grid:
    for c in r:
        print(c,end = " ")
    print()