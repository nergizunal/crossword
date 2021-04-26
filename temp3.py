# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 12:54:50 2021

@author: NergizUnal
"""

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')
import re
import copy
import time
class Cell(object):
    def __init__(self,letter = None, mark = 'A',x = 0,y = 0):
        self.letter = letter
        self.mark = mark # B -> Blocked A-> Available V -> Vertical Crossable H-> Horizontal Crossable 
        self.x = x
        self.y = y
        self.possibleCrosses = {}
       
    def setLetter(self,letter,dir):
        if(self.letter != '*'):
            self.updateMark('B')
        else:
            self.updateMark(dir)
        self.letter = letter
            
    def updateMark(self, newMark):
        if(self.mark == 'A'):
            self.mark = newMark
        elif(newMark == 'B' ):
            self.mark = 'B'
        elif(not(self.mark == newMark)):
            if(self.letter =='*'):
                self.mark = newMark
    
    def reCalculateScores(self):
        for k,v in self.possibleCrosses.items():
            self.possibleCrosses[k] = v/(len(self.possibleCrosses))
           
     

class Grid(object):
    def __init__(self, row, col, words = None):
        self.row = row
        self.col = col
        self.cells= [[]]
        self.words = words
        self.minX = 500
        self.maxX = 0
        self.minY = 500
        self.maxY = 0
 
    def startCells(self): 
        self.cells = [[Cell(letter = '*',mark = 'A',x = i, y = j) 
                           for j in range(2*self.col + 13)] 
                              for i in range(2*self.row + 13)]
    
    def crossScore(self,word, cell,crossIndex):
        score = 0
        if(cell.letter != word.word[crossIndex]):
            return 0
        if(cell.mark == 'B' or cell.letter == '*'): 
            return False
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
             
            c = self.cells[cell.x][endy + 1] #after end
            if(not(c.letter == '*')):
                return False
            
            for l in range(0,word.length):
                c = self.cells[cell.x][starty + l]
                if(c.mark == 'B' or c.mark == 'V'):
                    return False
                elif(c.mark == 'H'):
                    if(word.word[l] == c.letter):
                        score +=1
                    if(not(c.letter == '*' or  word.word[l] == c.letter)):
                        return False
            rightEnlargement = endy - self.maxY
            leftEnlargement = self.minY - starty
            rightEnlargement = (abs(rightEnlargement) + rightEnlargement)/2
            leftEnlargement = (abs(leftEnlargement) + leftEnlargement)/2
            total = rightEnlargement + leftEnlargement
            score -=  total/(self.col*self.col)
            
                
            
        elif(cell.mark == 'V'): #vertical
            startx = cell.x - crossIndex
            endx = startx + word.length -1
            
            if(endx-self.minX >= self.row):
                   
                    return False
               
            
            if(self.maxX-startx >= self.row):
                 
                    return False
            
            c = self.cells[startx -1][cell.y] #before start
            if(not(c.letter == '*')):
                return False
            c = self.cells[endx + 1][cell.y] # after end
            if(c.letter != '*' ):
                return False
           
            for l in range(0,word.length):
                c = self.cells[startx + l][cell.y]
                if(c.mark == 'B' or c.mark == 'H'):
                    return False
                elif(c.mark == 'V' ):
                    if(word.word[l] == c.letter):
                        score +=1
                    if(not(c.letter == '*' or  word.word[l] == c.letter)):
                        return False
            downEnlargement = endx - self.maxX
            topEnlargement = self.minX - startx
            rightEnlargement = (abs(downEnlargement) + downEnlargement)/2
            topEnlargement = (abs(topEnlargement) + topEnlargement)/2
            total = downEnlargement + topEnlargement
            score -=  total/(self.row*self.row)
            
           
        else:
            return False
        
        cell.possibleCrosses[(word,crossIndex,cell)] = score
        return True
        
        
    def cellsCrossScores(self,words):
        intersectionsList = []
        
        for r in self.cells:
            for c in r:
                if(c.letter == '*' or c.mark == 'B'):
                    continue
                for w in words:
                    for i in range(w.length):
                        bool = self.crossScore(w,c,i)
                        
                c.reCalculateScores()   
        
        for r in self.cells:
           for c in r: 
             
             if(c.letter == '*' or c.mark == 'B'):
                    continue
             
             for k,v in c.possibleCrosses.items():
                 """print(k[0].word,k[1],c.letter,v)"""
                 p = {(k[0],k[1],c): v}
                
                 if(len(intersectionsList) == 0):
                     intersectionsList.append(p)
                 else:
                     index = len(intersectionsList)
                     for i in range(len(intersectionsList)):
                        values =  intersectionsList[i].values()
                        values = list(values)[0:len(intersectionsList)]
                        if(v > values[0]):
                            index = i
                     intersectionsList.insert(index,p)
                          
        return intersectionsList
        
            
    def flushScores(self):
        for c in self.cells:
            for r in c:
                r.possibleCrosses = {}
    
                            
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
            
        elif(cell.mark == 'H' or cell.mark == 'A' or cell.mark == 'B'):
           
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
       
           
        for i in range(1,len(self.cells) -1): #if 2 cross at that cell, block it
            for j in range(1,len(self.cells[0]) - 1):
                if(self.cells[i - 1][j].letter != '*' or self.cells[i + 1][j].letter != '*'):
                     if(self.cells[i][j-1].letter != '*' or self.cells[i][j+1].letter != '*'):
                         self.cells[i][j].updateMark('B') 
        for i in range(1,len(self.cells) -1): #eğer karşılıklı iki blocked cell varsa ve diğer yöndeki karşılıklı hücreler harf içeriyorsa blockla
            for j in range(1,len(self.cells[0]) - 1):
                if (self.cells[i][j].letter != '*'):
                    if(self.cells[i - 1][j].mark=='B' and self.cells[i + 1][j].mark=='B' 
                       and  self.cells[i][j-1].letter != '*' and self.cells[i][j+1].letter != '*'):
                        self.cells[i][j].updateMark('B')
                    elif(self.cells[i][j-1].mark=='B' and self.cells[i][j+1].mark=='B'
                          and self.cells[i-1][j].letter != '*' and self.cells[i+1][j].letter != '*'):
                        self.cells[i][j].updateMark('B')  
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
        self.intersectionScore = 0
    def calculateScore(self, list):
        temp = copy.deepcopy(list)
        for w in temp:
            for c in w.word:
                if(c in self.word):
                    self.startScore +=1
    
    def dictSize(self):
        count = 0
        for k,v in self.dict.items():
            for s in v:
                count += 1
        return count
                
class Solution(object):
    def __init__(self):
        self = self
    def sortByScoreWords(self,list):
        list.sort(key = lambda s: s.startScore, reverse = True)
    def sortByInterSection(self,list):
        list.sort(key = lambda s: s.intersectionScore, reverse = False)
    def solve(self):
        strList1 = ["dudak" , "bulvar","şerbet","derman","davet","nehir","çukur","eksen","test","açık","ense","tek","beş","rota","ok"]
        strList2 = ["işlev","güveç","hamle","çalgı","enlem","düet","edep","bile","ece","oje"]
        strList3 = ["aile","ela","arı"]
        strList4 = ["piliç", "sehpa", "bekçi", "vebal", "lakin", "kaşar", "işgal","naaş", "ilke","gür"]
        strList5 = ["başlıca", "dumanlı", "langırt","kristal","nakkaş", "panjur","sabıka", "pişkin", "yakın", "yalak","salya", "nükte", "misal","kasır","erik"]
        strList6 = ["bitme", "roket", "testi","tomar","idare","ofis","ıtır","boz"]
        words = []
        
        li = []
        row = 0
        col = 0
        x = input("Which List to generate? \n1) " + ' '.join(strList1)
                  +" \n2)" + ' '.join(strList2)  +" \n3)" + ' '.join(strList3)
                  +" \n4)" + ' '.join(strList4)+" \n5)" + ' '.join(strList5)
                  +" \n6)" + ' '.join(strList6)+ " \n7) new list" + " \n 8) quit \n" )
        x = int(x)
        while (x <=6 and x > 0):
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
                row = 10
                col = 6
                
           else:
               return False
           words = []
           for l in li:
               words.append(Word(l))
           l = words
            
           for w in words:
                i = l.index(w)
                l.remove(w)
                w.calculateScore(l)
                l.insert(i,w)
            
           grid = Grid(row,col)
           grid.startCells()
            #self.sortByScoreWords(words)
           
           w = words[0]
           grid.insertWord(w.word, grid.cells[grid.row + 6][grid.col + 6], 0)
           
           grid.maxX = grid.row + 6
           grid.minX = grid.row + 6
           """ print(grid.maxX, grid.minX)
           print(grid.maxY, grid.minY)"""
           words.remove(w)
            #self.sortByScoreWords(words)
           """w = words[1]
           grid.insertWord(w.word, grid.cells[grid.row + 6][grid.col + 8], 3)
           words.remove(w)
           grid.printGrid()
          """
           
           
           """for r in grid.cells:
               for c in r:
                   for k,v in c.possibleCrosses.items():
                       print(k[0].word, k[1], v)
                       print(len(c.possibleCrosses))"""
           #return True
           if(self.solveUtil(grid,words) == False):
                grid.printGrid()
                print("False return")
                
                
           print("True return")
           x = input("Which List to generate? \n1) " + ' '.join(strList1)
                  +" \n2)" + ' '.join(strList2)  +" \n3)" + ' '.join(strList3)
                  +" \n4)" + ' '.join(strList4)+" \n5)" + ' '.join(strList5)
                  +" \n6)" + ' '.join(strList6)+ " \n7) new list" + " \n8) quit \n" )
           x = int(x)
        return True
    
    def main(self):
            g = self.solve()
            print(g)
    def solveUtil(self, grid, words):
            ez = len(words)
            if( ez <= 1):
                grid.printGrid() 
                grid.printMarks()
                for w in words: 
                    print(w.word, end = " ")
                
                if(ez <= 0 ): #and (grid.maxY-grid.minY) <= grid.col and (grid.maxX-grid.minX) <= grid.row
                    grid.printGrid() 
                    return True
            
           
            tempGrid = copy.deepcopy(grid)
            tempWords = copy.deepcopy(words)
            tempGrid.flushScores()
            """print(tempGrid.maxX, tempGrid.minX)
            print(tempGrid.maxY, tempGrid.minY)"""
            list = tempGrid.cellsCrossScores(words)
            """for l in list:
                for i,v in l.items():
                    print(i[0].word, i[1], i[2].letter,v)"""
            for item in list:
                for k in item:
                   
                    w = tempWords[0]
                    j = 0
                    for i in range(len(tempWords)):
                        if(tempWords[i].word == k[0].word):
                            w = tempWords[i]
                            j = i
                            break
                    """print("put", k[0].word)   """ 
                    tempWords.remove(w)
                    """print("remove", w.word)"""
                    tempGrid.insertWord(k[0].word, k[2], k[1])
                    f = self.solveUtil(tempGrid,tempWords)
                    if (f == True):
                         return True
                    
                    tempWords.insert(i,w)
                    tempGrid = copy.deepcopy(grid)
                    #tempWords = copy.deepcopy(words)
            """for w in words: 
              print(w.word, end = " ")"""
            
            #print(len(words))
          
                
            return False
    def checkDictSize(self,list,grid):
        for l in list:
            grid.flushIntersections(l)
            grid.possibleIntersections(l)
        for l in list:
            if(l.dictSize() == 1):
                return True
        return False
    def calcMinDict(self,list,grid):
        temp = list[0]
        min = list[0].dictSize()
        tempScore = temp.startScore
        for l in list:
            grid.flushIntersections(l)
            grid.possibleIntersections(l)
            i = list.index(l)
            list.remove(l)
            l.calculateScore(list)
            list.insert(i,l)
            if( l.dictSize()>0 and l.startScore > tempScore): #l.dictSize() < min and
                temp = l
                    
            
        return temp
if __name__ == "__main__":
    s = Solution()
    s.main()    