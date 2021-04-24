# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 12:54:50 2021

@author: NergizUnal
"""

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')
import re
import copy

class Cell(object):
    def __init__(self,letter = None, mark = 'A',x = 0,y = 0):
        self.letter = letter
        self.mark = mark # B -> Blocked A-> Available V -> Vertical Crossable H-> Horizontal Crossable 
        self.x = x
        self.y = y
       
    def setLetter(self,letter,dir):
        if(self.letter != '*'):
            self.updateMark('B')
        else:
            self.updateMark(dir)
        self.letter = letter
            
    def updateMark(self, newMark):
        if(self.mark == 'A'):
            self.mark = newMark
        elif(newMark == 'B'):
            self.mark = 'B'
        elif(not(self.mark == newMark)):
            if(self.letter =='*'):
                self.mark = newMark

class Grid(object):
    def __init__(self, row, col, words = None):
        self.row = row
        self.col = col
        self.cells= [[]]
        self.words = words
        self.minX = 2000
        self.maxX = 0
        self.minY = 2000
        self.maxY = 0
 
    def startCells(self): 
        self.cells = [[Cell(letter = '*',mark = 'A',x = i, y = j) 
                           for j in range(2*self.col + 12)] 
                              for i in range(2*self.row + 12)]
    
    def canBePlaced(self,word, cell,crossIndex):
        if(cell.mark == 'H'): #horizontal
            starty = cell.y - crossIndex
            endy = starty + word.length - 1
         
            if(endy-self.minY  >= self.col):
                return False
                
            if(self.maxY-starty >= self.col):
                return False
            
            c = self.cells[cell.x][starty -1] # before start
            if(not(c.letter == '*')):
                return False
            
            c = self.cells[cell.x][starty] #start
            if(c.mark == 'B' or c.mark == 'V' ):
                return False
            elif(c.mark != 'A'):
                if(not(c.letter == word.word[0] or c.letter == '*')):
                    return False
         
                
            c = self.cells[cell.x][endy] #end
            if(c.mark == 'B' or c.mark == 'H'):
                return False
            elif(c.mark != 'A'):
                if(not(word.word[-1] == c.letter or c.letter == '*')):
                    return False 
                
            c = self.cells[cell.x][endy + 1] #after end
            if(not(c.letter == '*')):
                return False
                
            for l in range(1,word.length -1):
                c = self.cells[cell.x][starty + l]
                if(c.mark == 'B' or c.mark == 'V'):
                    
                    return False
                elif(c.mark == 'H'):
                    if(not(c.letter == '*' or word.word[l] == c.letter)):
                        
                        return False 
        elif(cell.mark == 'V'): #vertical
            startx = cell.x - crossIndex
            endx = startx + word.length -1
            if(endx > self.maxX ): 
                if(endx-self.minX >= self.row):
                    return False
               
            if(startx < self.minX ):
                if(self.maxX-startx >= self.row):
                    return False
            
            c = self.cells[startx -1][cell.y] #before start
            if(not(c.letter == '*')):
                return False
            
            c = self.cells[startx][cell.y] #start
            if(c.mark == 'B' or c.mark == 'H'): 
                return False
            elif(c.mark != 'A'):
                if(not(c.letter == word.word[0] or c.letter == '*')):
                    return False 
                
           
            c = self.cells[endx][cell.y] #end
            if(c.mark == 'B' or c.mark == 'H'):
                return False
            elif(c.mark != 'A'):
                if(not(c.letter == word.word[-1] or c.letter == '*')):
                    return False 
            c = self.cells[endx + 1][cell.y] # after end
            if(c.letter != '*' ):
                return False
            
            for l in range(1,word.length -1):
                c = self.cells[startx + l][cell.y]
                if(c.mark == 'B' or c.mark == 'H'):
                    return False
                elif(c.mark == 'V' ):
                    if(not(c.letter == '*' or  word.word[l] == c.letter)):
                        return False 
        else:
            return False
        return True
  
    def insertWord(self, nextWord, cell, crossIndex):
        if(cell.mark == 'V'):
            startx = cell.x - crossIndex
            endx = startx + len(nextWord) -1
            if(endx > self.maxX): 
                #if(endx-self.minX > self.row):
                    self.maxX = endx
            if(startx < self.minX):
                #if(self.maxX-startx > self.row):
                     self.minX = startx
            for i in range(len(nextWord)):
                c = self.cells[startx + i][cell.y]
                c.setLetter(nextWord[i],'H')
                self.cells[startx + i][cell.y + 1].updateMark('H')
                self.cells[startx + i][cell.y -1].updateMark('H')
            self.cells[startx - 1][cell.y].updateMark('B')
            self.cells[endx + 1][cell.y].updateMark('B')
        else:
            starty = cell.y - crossIndex
            endy = starty + len(nextWord) -1
            if(endy > self.maxY):
                    self.maxY = endy
            if(starty < self.minY):
                    self.minY = starty
            for i in range(len(nextWord)):
                c = self.cells[cell.x][starty + i]
                c.setLetter(nextWord[i],'V')
                self.cells[cell.x + 1][starty + i].updateMark('V')
                self.cells[cell.x - 1][starty + i].updateMark('V')
            self.cells[cell.x][starty - 1].updateMark('B')
            self.cells[cell.x][endy + 1].updateMark('B')
            
        for i in range(1,len(self.cells) -1): #if 2 cross index letter cells, block
            for j in range(1,len(self.cells[0]) - 1):
                if(self.cells[i - 1][j].letter != '*' or self.cells[i + 1][j].letter != '*'):
                     if(self.cells[i][j-1].letter != '*' or self.cells[i][j+1].letter != '*'):
                         self.cells[i][j].updateMark('B')
        for i in range(1,len(self.cells) -1): #eğer karşılıklı iki blocked cell varsa ve diğer yöndeki karşılıklı hücreler harf içeriyorsa blockla
            for j in range(1,len(self.cells[0]) - 1):
                if (self.cells[i][j].letter != '*'):
                    if(self.cells[i - 1][j].mark=='B' and self.cells[i + 1][j].mark=='B' 
                       and self.cells[i-1][j].letter != '*' and self.cells[i+1][j].letter != '*' ):
                        self.cells[i][j].updateMark('B')
                    elif(self.cells[i][j-1].mark=='B' and self.cells[i][j+1].mark=='B'
                          and self.cells[i][j-1].letter != '*' and self.cells[i][j+1].letter != '*'):
                        self.cells[i][j].updateMark('B')    
        for i in range(1,len(self.cells) -1): #eğer 4 tarafı harf ya da blocked ise blockla
            for j in range(1,len(self.cells[0]) - 1):
                c1 = self.cells[i - 1][j]
                c2 = self.cells[i + 1][j]
                c3 = self.cells[i][j-1]
                c4 = self.cells[i][j+1]
                if(c1.letter !='*' or c1.mark == 'B'):
                    if(c2.letter !='*' or c2.mark == 'B'):
                        if(c3.letter !='*' or c3.mark == 'B'):
                            if(c4.letter !='*' or c4.mark == 'B'):
                                self.cells[i][j].updateMark('B')
                           
    def possibleIntersections(self,nextWord):
        for r in self.cells:
            for c in r:
                if(c.letter == '*' or c.mark == 'B'):
                    continue
                for i in range(nextWord.length):
                    if(c.letter == nextWord.word[i]):
                        if(self.canBePlaced(nextWord,c,i)):
                            if(i in nextWord.dict.keys()):    
                                nextWord.dict[i].append(c)
                            else: 
                                nextWord.dict[i] = [c]
                            
    def flushIntersections(self,word):
        for i in range(word.length):
            for r in self.cells:
                for c in r:
                    word.dict[i] = []

    def printGrid(self):
        for r in self.cells:
            for c in r:
                if(c.letter == '*'):
                    print(" ",end = " ")
                else:
                    print(c.letter,end = " ")
            print()
    def printMarks(self):
            for r in self.cells:
                for c in r:
                    if(c.mark == 'A'):
                        print(" ",end = " ")
                    else:
                        print(c.mark,end = " ")
                print()
class Word(object):
    def __init__(self, word = None):
        self.word = re.sub(r'\s', '', word.lower())
        self.length = len(self.word)
        self.dict = {}
        self.startScore = 0
    def calculateScore(self, list):
        s = set()
        for w in list:
            for c in w.word:
                if(c in self.word):
                    s.add(c)
        self.startScore = len(s)
        self.startScore = self.startScore
class Solution(object):
    def __init__(self):
        self = self
    def sortByScoreWords(self,list):
        list.sort(key = lambda s: s.startScore, reverse = False)
    def solve(self):
        strList1 = ["bulvar","şerbet","derman","davet","dudak" ,"nehir","çukur","eksen","test","açık","ense","tek","beş","rota","ok"]
        strList2 = ["işlev","güveç","hamle","çalgı","enlem","düet","edep","bile","ece","oje"]
        strList3 = ["aile","ela","arı"]
        strList4 = ["piliç", "sehpa", "bekçi", "vebal", "lakin", "kaşar", "işgal","naaş", "ilke","gür"]
        strList5 = ["başlıca", "dumanlı", "langırt","kristal","nakkaş", "panjur","sabıka", "pişkin", "yakın", "yalak","salya", "nükte", "misal","kasır","erik"]
        strList6 = ["bitme", "roket", "testi","tomar","idare","ofis","ıtır","boz"]
        words = []
        
        li = []
        row = 0
        col = 0
        x = input("choose: ")
        x = int(x)
        if(x == 1):
            li = strList1
            row = 7
            col = 14
        elif(x ==2):
            li = strList2
            row = 6
            col = 10
        elif(x ==3):
            li = strList3
            row = 3
            col = 4
        elif(x ==4):
            li = strList4
            row = 6
            col = 11
        elif(x ==5):
            li = strList5
            row = 8
            col = 13
        elif(x ==6):
            li = strList6
            row = 6
            col = 10
        else:
            li = strList6
            row = 6
            col = 10
            
        for l in li:
            words.append(Word(l))
        l = words
        
        for w in words:
            i = l.index(w)
            l.remove(w)
            w.calculateScore(l)
            l.insert(i,w)
        #self.sortByScoreWords(words)
        grid = Grid(row,col)
        grid.startCells()
        for w in words:
            print(w.word, end = " ")
        
        y = input("start")
        w = words[0]
        print(w.word)
        grid.insertWord(w.word, grid.cells[grid.row + 6][grid.col + 6], 0)
        words.remove(w)
        
        if(self.solveUtil(grid,words,2**len(words)) == False):
            grid.printGrid()
            return False
            
            
        print("True return")
        print(grid.maxX, grid.minX)
        print(grid.maxY, grid.minY)
        grid.printGrid()
        for w in words:
            print(w.word)
        print(len(words))
        return True

    def solveUtil(self, grid, words, level, count = 0):
        ez = len(words)
        #grid.printGrid()  
        #grid.printMarks()
        if( ez <= 1):
          grid.printGrid()
          grid.printMarks()
        if( ez <= 0):
          grid.printGrid()
          return True
        
        
        tempGrid = copy.deepcopy(grid)
        tempWords = copy.deepcopy(words)
       # tempGrid = grid
        #tempWords = words
        for w in words: 
            print(w.word, end = " ")
    
        print(len(words))
        for w in words:
            tempGrid.flushIntersections(w)
            tempGrid.possibleIntersections(w)
            
            i = words.index(w)
            words.remove(w)
            
            for k,v in w.dict.items():
                for s in v:
                    count +=1
                    """if(count>level):
                        print("countttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
                        return False"""
                    grid.insertWord(w.word, s, k)
                    f = self.solveUtil(grid,words,level/2,count)
                  
                    if (f == True):
                        grid.printGrid()
                        return True
                    
                    #tempGrid = copy.deepcopy(grid) 
                    #tempGrid = grid
                    grid = copy.deepcopy(tempGrid)
            words.insert(i,w) 
        
        return False
    
    def main(self):
        g = self.solve()
        print(g)
       
     
    
    
if __name__ == "__main__":
    s = Solution()
    s.main()    