# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:41:03 2020

@author: battu
"""

import threading
import time
import numpy as np

from Strategy_selection import *

def get_focus_data(matrix,focus):
    data = []
    data.append(focus)
    square = (int(focus[0]/3)*3,int(focus[1]/3)*3)
    sqr = {}
    for i in range(square[0],square[0]+3):
        for j in range(square[1],square[1]+3):
            if matrix[i][j]!=0:
                sqr[matrix[i][j]]=(i,j)
                
    
    data.append(sqr)
    
    
    row1 = matrix[square[0]]
    row2 = matrix[square[0]+1]
    row3 = matrix[square[0]+2]
    col1 = [matrix[x][square[1]] for x in range(0,9)]
    col2 = [matrix[x][square[1]+1] for x in range(0,9)]
    col3 = [matrix[x][square[1]+2] for x in range(0,9)]
    rw1 = {}
    for i in range(len(row1)):
        if row1[i]!=0:
            rw1[row1[i]]=(square[0],i)
    
    rw2 = {}
    for i in range(len(row2)):
        if row2[i]!=0:
            rw2[row2[i]]=(square[0]+1,i)
    rw3 = {}
    for i in range(len(row3)):
        if row3[i]!=0:
            rw3[row3[i]]=(square[0]+2,i)
            
            
    co1 = {}
    for i in range(len(col1)):
        if col1[i]!=0:
            co1[col1[i]]=(i,square[1])
            
            
            
    co2 = {}
    for i in range(len(col2)):
        if col2[i]!=0:
            co2[col2[i]]=(i,square[1]+1)
    co3 = {}
    for i in range(len(col3)):
        if col3[i]!=0:
            co3[col3[i]]=(i,square[1]+2)
    data.append(rw1)
    data.append(rw2)
    data.append(rw3)
    data.append(co1)
    data.append(co2)
    data.append(co3)
    empty_sqr= []
    for i in range(square[0],square[0]+3):
        for j in range(square[1],square[1]+3):
            if matrix[i][j]==0 and i!=focus[0] and j!=focus[1]:
                empty_sqr.append((i,j))
    data.append(empty_sqr)
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
    
    
    
class Basic():
    
    def __init__(self,matrix):
        
        self.matrix = matrix
        #self.lock = 0  #This decides if focus should send out an answer or just the focus point
        self.focus = (0,0)  #The current cordinate that is being focused on
        self.answer = (5,(0,0)) # The number and the cordinate it should be placed at
        self.lock = 0
        
        self.wait_time = 1
        self.focus_wait = 1/30
        self.stack = []
        self.current_place = (0,0)
        self.inserted = []
        self.solved =[]
        self.cells = []
        self.correct_solved = 0
        self.total_solved = 0
        self.total_empty = 0
        
        
        t1 = threading.Thread(target=self.think)
        t1.start()
        
        
        pass
    
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

    def solve(self):
        self.solved = [x[:] for x in self.matrix]
        
        print(self.solved)
        i = 0
        j = 0
        track = []
        for i in range(9):
            for j in range(9):
                if self.solved[i][j]==0:
                    track.append((i,j))
        current_index = 0
        numbers_track = [0 for x in range(len(track))]
        
        sol = False
        iterations = 0
        while not sol:
            
            iterations+=1
            if current_index >= len(track):
                sol = True
                break
           
            try: 
                numbers_track[current_index] +=1
            except:
                return
                numbers_track[current_index] +=1
            if numbers_track[current_index] > 9:
                numbers_track[current_index] = 0
                current_index -= 1
                continue
            self.solved[track[current_index][0]][track[current_index][1]] = numbers_track[current_index]
            result = self.solve_check(track[current_index][0],track[current_index][1])
            if result == -1:
                continue
            else:
                #print(current_index)
                current_index += 1
                continue
            
        print(self.solved)
        
        pass
    def solve_check(self,x,y):
        #check row
        
        for j in range(0,9):
            if y==j:
                continue
            if self.solved[x][j] == self.solved[x][y]:
                return -1
        #check column
        for i in range(0,9):
            if i==x:
                continue
            if self.solved[i][y] == self.solved[x][y]:
                return -1
        #check square
        c_x = int(x/3)*3
        c_y = int(y/3)*3
        for i in range(3):
            for j in range(3):
                if i+c_x == x and j+c_y==y:
                    continue
                if self.solved[i+c_x][j+c_y] == self.solved[x][y]:
                    return -1
            
        return 1
        
        
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
         
    def calc_dist(self,empty,focus):
        dist= []
        for i in empty:
            focus = i
            row = self.matrix[focus[0]]
            col = [self.matrix[x][focus[1]] for x in range(9)]
            a,b = int(focus[0]/3)*3,int(focus[1]/3)*3
            square = []
            for j in range(3):
                for k in range(3):
                    square.append(self.matrix[j+a][k+b])
            #print(square,row,col,square.count(0))
            s =  (9-square.count(0) + 9-row.count(0) +  9-col.count(0))
            ss = 9-square.count(0)
            rs = 9-row.count(0)
            cs = 9-col.count(0)
            
            dist.append(max(s,ss,rs,cs)**5)
        
        return [x/sum(dist) for x in dist]
    def pause(self):
        self.lock = 1
        return
    def resume(self):
        self.lock=0
    def think(self):
        self.solve()
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j]==0:
                    self.cells.append((i,j))
        self.total_empty = len(self.cells)
        
        time.sleep(self.wait_time)
        counter = 1
        done = False
        temp_matrix = self.matrix
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j]==0:
                    empty_cells.append((i,j))
        if len(empty_cells)==0:
            done = True
        #print(empty_cells)
        x = empty_cells[0][0]
        y = empty_cells[0][1]
        while not done:
            if self.lock !=0 :
                continue
            self.correct_solved = 0
            self.total_solved = 0
            for i in self.cells:
                if self.matrix[i[0]][i[1]] == self.solved[i[0]][i[1]]:
                    self.correct_solved +=1
            for i in self.cells:
                if self.matrix[i[0]][i[1]] != 0 :
                    self.total_solved +=1
            if len(empty_cells)==0:
                done = True
                continue
            
            #Select hardcoded
            #print(self.calc_dist(empty_cells,(x,y)))
            #choices = [x for _,x in sorted(zip(self.calc_dist(empty_cells,(x,y)),list(range(len(empty_cells)))))]
            choice = np.random.choice(list(range(len(empty_cells))),p = self.calc_dist(empty_cells,(x,y)))
            #print(choices)
            #choice = choices[0]
            
            
            new_cell = empty_cells[choice]
            self.find_focus_path(self.focus[0],self.focus[1],new_cell[0],new_cell[1])
            self.focus = new_cell
            #print(self.focus)
            dt = get_focus_data(self.matrix,self.focus)
            time.sleep(1)
            n,s,name = strategy_cycle(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6],dt[7],dt[8])
            if n==False:
                continue
            
            
            x = self.focus[0]
            y= self.focus[1]
            print(s,name,x,y)
            if name=='simple_strategies':
                time.sleep(2)
            if name=='medium_strategies':
                time.sleep(4)
            self.matrix[self.focus[0]][self.focus[1]] = s
            
            empty_cells.remove(self.focus)
            time.sleep(1)
            
            
            result = self.perform_check()
            if result == -1:
                self.find_focus_path(self.focus[0],self.focus[1],x,y)
                self.matrix[x][y] = 0
                
                empty_cells.append((x,y))
                
                print("Wrong Answer!",x,y,"Number:",s)
            continue
            
            
            print(len(empty_cells))
            
        return
            
                
        satisfied = False
        while not satisfied:
            a = self.perform_check()
            if a!=1:
                counter+=1
            satisfied = True
            
        
    def communicate(self):
        
        
        
        return self.focus,self.correct_solved,self.total_solved,self.total_empty
class Strategy():
    def __init__(self,name):
        
        self.name = name
    def return_strategy(self,matrix):
        if self.name == 'Easy':
            obj = Basic(matrix.copy())
        
        if self.name == "Medium":
            obj = Basic(matrix.copy())
            #Create the object for second strategy
            # obj =  second_strat(matrix)
            
        return obj            
            
