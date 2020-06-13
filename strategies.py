# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:41:03 2020

@author: battu
"""

import threading
import time

def get_focus_data(matrix,focus):
    data = []
    data.append(focus)
    square = (int(focus[0]/3)*3,int(focus[1]/3)*3)
    data.append(square)
    row1 = matrix[square[0]]
    row2 = matrix[square[0]+1]
    row3 = matrix[square[0]+2]
    col1 = [matrix[x][square[1]] for x in range(0,9)]
    col2 = [matrix[x][square[1]+1] for x in range(0,9)]
    col3 = [matrix[x][square[1]+2] for x in range(0,9)]
    row1[:] = [x for x in row1 if x != 0]
    row2[:] = [x for x in row2 if x != 0]
    row3[:] = [x for x in row3 if x != 0]
    col1[:] = [x for x in col1 if x != 0]
    col2[:] = [x for x in col2 if x != 0]
    col3[:] = [x for x in col3 if x != 0]
    data.append(row1)
    data.append(row2)
    data.append(row3)
    data.append(col1)
    data.append(col2)
    data.append(col3)
    return data
    
    
    
'''
Template for strategy class

class strategy_a():
    
    def __init__(self,matrix):
        
        #Content for initialization
        self.matrix = matrix
        self.lock = 0  #This decides if focus should send out an answer or just the focus point
        self.focus = (0,0)  #The current cordinate that is being focused on
        self.answer = (0,(0,0)) # The number and the cordinate it should be placed at
        #-----------------------------Do any extra initialization here --------------------------------------------------
        
        
        
        
        #-----------------------------Stop Initialization --------------------------------------------------------------
        t1 = threading.Thread(target=self.think)
        t1.start()
        
        
        
    Any other functions you want for your strategies you can write here.
    def think(self):
        #This is your main thinking strategy function, here you will write logic for your code
        #Always update the focus when you are looking at a cell. This will run in a thread, so it will happen parallely
        #Always release the lock after you are ready to provide an answer (make lock=1)
        pass
    
    
    
    def focus(self): This is the important function to communicate between the environment and the model
    
        
        #This function will be called every second.
        #Two Return types.
        
        #1.) First return type are cordinates (x,y) = (row,column) in the matrix which shows where the vision of agent
        #    is(or the focus of the agent as it looks at numbers). 
        #2.) The output number and its position where you want to place it, Update the matrix locally.
        #Look at the example strategy below to get a better understanding.
        
        if self.lock == 0:
            return self.focus
        else:
            lock = 0
            t1 = threading.Thread(target=self.think)
            t1.start()
            return self.answer
    
    
    
    

'''

#Example Strategy
class backtrack():

    def __init__(self,matrix):
        
        self.matrix = matrix
        #self.lock = 0  #This decides if focus should send out an answer or just the focus point
        self.focus = (0,0)  #The current cordinate that is being focused on
        self.answer = (5,(0,0)) # The number and the cordinate it should be placed at
        
        
        self.wait_time = 1
        self.focus_wait = 1/10
        self.stack = []
        self.current_place = (0,0)
        self.inserted = []
        
        t1 = threading.Thread(target=self.think)
        t1.start()
        
        
        pass
    
    #Helper Function
    def find_focus_path(self,i,j,x,y):
        a = x - i
        b = y - j
        c_x = i
        c_y = j
        if a<0:
            a_sign = -1
        else:
            a_sign = 1
        if b<0:
            b_sign = -1
        else:
            b_sign = 1
        for i in range(abs(a)):
            c_x += a_sign
            self.focus = (c_x,c_y)
            time.sleep(self.focus_wait)
        for i in range(abs(b)):
            c_y += b_sign
            self.focus = (c_x,c_y)
            time.sleep(self.focus_wait)
        return
    
    
    def perform_check(self):
        time.sleep(self.focus_wait)
        #Check part
        check_x = self.focus[0]
        check_y = self.focus[1]
        digit = self.answer[0]
        self.find_focus_path(check_x,check_y,check_x,0)
        #Check row
        for j in range(0,9):
            self.focus = (check_x,j)
            time.sleep(self.focus_wait)
            if j == check_y:
                continue
            if self.matrix[check_x][j] == self.matrix[check_x][check_y]:
                self.find_focus_path(check_x,j,check_x,check_y)
                return -1
        self.find_focus_path(self.focus[0],self.focus[1],check_x,check_y)
        for i in range(0,9):
            self.focus = (i,check_y)
            time.sleep(self.focus_wait)
            if i == check_x:
                continue
            if self.matrix[i][check_y] == self.matrix[check_x][check_y]:
                self.find_focus_path(i,check_y,check_x,check_y)
                return -1
        self.find_focus_path(self.focus[0],self.focus[1],check_x,check_y)
        t_x = int(check_x/3)*3
        t_y = int(check_y/3)*3
        self.find_focus_path(check_x,check_y,t_x,t_y)
        for i in range(t_x,t_x+3):
            for j in range(t_y,t_y+3):
                self.focus = (i,j)
                time.sleep(self.focus_wait)
                if i==check_x and j == check_y:
                    continue
                if self.matrix[i][j] == self.matrix[check_x][check_y]:
                    self.find_focus_path(i,j,check_x,check_y)
                    return -1
        return 1
                
                 
    def think(self):
        #This is your main strategy code - My fake strategy doesnt use ACT-R.
        time.sleep(self.wait_time)
        counter = 1
        done = 0
        temp_matrix = self.matrix
        for i in range(9):
            for j in range(9):
                self.focus = (i,j)
                time.sleep(self.focus_wait)
                if self.matrix[i][j] == 0:
                    #self.answer = (counter,(i,j))
                    self.matrix[i][j] = counter
                    self.stack.append(counter)
                    self.inserted.append((i,j))
                    done=1
                    break
            if done==1:
                break
        satisfied = False
        while not satisfied:
            a = self.perform_check()
            if a!=1:
                counter+=1
            satisfied = True
            
                    
        
        
        
        
        
        
    def get_focus(self):
        
        
        return self.focus
        
    
class Strategy():
    def __init__(self,name):
        self.name = name
    def return_strategy(self,matrix):
        if self.name == 'First':
            obj = backtrack(matrix)
        
        if self.name == "Second":
            #Create the object for second strategy
            # obj =  second_strat(matrix)
            pass
        return obj            
            