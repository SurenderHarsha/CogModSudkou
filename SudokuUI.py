# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:19:40 2020

@author: battu
"""

import pygame as p
import pandas as pd
import numpy as np
import time
from strategiesClass import *


selected_strategy = ""
easy_files = "Easy_Sudokus.csv"
medium_files = "Medium_Sudokus.csv"
file_to_load = ""

pause_check = False
resume_check = False


white = (255, 255, 255) 
black = (0,0,0)
red = (255,0,0)
blue  = (0,0,255)
green = (0,255,0)
yellow = (0,255,255)
grey=(200,200,200)
selected_location = []


(width, height) = (720, 720)
fps = 120



#Helper Functions
def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()






p.init()
p.display.set_caption('SudokuSolver!')
screen = p.display.set_mode((width, height))
p.display.flip()
Page1 = True
Page2 = False
MainGame = False
matrix_created = False
agent_created = False
Rollback = True


matrix = []
for i in range(9):
    matrix.append([0 for j in range(9)])



clock = p.time.Clock()

class Matrix():
    def __init__(self,matrix):
        self.matrix = matrix
        self.draw_start = (135,135)
        self.matrix_drew = False
        
    def matrix_drawn(self):
        global selected_location
        self.matrix_drew = True
        selected_location = [x[:] for x in self.matrix]
        for i in range(9):
            for j in range(9):
                if selected_location[i][j]!=0:
                    #print("Marking")
                    selected_location[i][j]=1
    def load_file(self):
        global file_to_load
        #print(file_to_load)
        df = pd.read_csv(file_to_load)
        l = df.loc[np.random.choice(list(range(df.shape[0])))][1:].to_list()
        k = 0
        for i in range(9):
            for j in range(9):
                self.matrix[i][j] = l[k]
                k+=1
        
    def draw_matrix(self):
        global selected_location
        i = 0
        j = 0
        p.draw.rect(screen,grey,(self.draw_start[0],self.draw_start[1],450,450))
        largeText = p.font.Font('freesansbold.ttf',20)
        while i<9:
            j=0
            
            while j<9:
                
                p.draw.rect(screen,black,(self.draw_start[0]+(j)*50,self.draw_start[1]+ (i)*50,50,50),1)
                if j%3==0 and j!=0:
                    p.draw.line(screen,red,(self.draw_start[0]+(j)*50,self.draw_start[1]+ (i)*50),(self.draw_start[0]+(j)*50,self.draw_start[1]+ (i)*50+50),3)
                if i%3==0 and i!=0:
                    p.draw.line(screen,red,(self.draw_start[0]+(j)*50,self.draw_start[1]+ (i)*50),(self.draw_start[0]+(j)*50+50,self.draw_start[1]+ (i)*50),3)
                #pass
                j+=1
            i+=1
            
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    continue
                
                if self.matrix_drew:
                    if selected_location[i][j] == 1:
                        TextSurf, TextRect = text_objects(str(self.matrix[i][j]), largeText,black)
                    else:
                        TextSurf, TextRect = text_objects(str(self.matrix[i][j]), largeText,blue)
                else:
                    TextSurf, TextRect = text_objects(str(self.matrix[i][j]), largeText,black)
                TextRect.center = (self.draw_start[0]+(j)*50+25,self.draw_start[1]+ (i)*50+25)
                screen.blit(TextSurf, TextRect)
    def refresh(self):
        for i in range(9):
            for j in range(9):
                self.matrix[i][j]=0
                
    def draw_score(self,c,ts,te):
        largeText = p.font.Font('freesansbold.ttf',20)
        TextSurf, TextRect = text_objects("Correct", largeText,blue)
        TextRect.center = (640,100)
        
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(":"+str(c), largeText,red)
        TextRect.center = (700,100)
        screen.blit(TextSurf, TextRect)
        
        
        TextSurf, TextRect = text_objects("Solved", largeText,blue)
        TextRect.center = (640,200)
        
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(":"+str(ts), largeText,red)
        TextRect.center = (700,200)
        screen.blit(TextSurf, TextRect)
        
        TextSurf, TextRect = text_objects("Total", largeText,blue)
        TextRect.center = (640,300)
        
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(":"+str(te), largeText,red)
        TextRect.center = (700,300)
        screen.blit(TextSurf, TextRect)
        
        return
    def draw_focus(self,i,j):
        p.draw.rect(screen,green,(self.draw_start[0]+(j)*50+3,self.draw_start[1]+ (i)*50+3,44,44),2)
        
        #Getting Column focus
        p.draw.rect(screen,blue,(self.draw_start[0]+(j)*50-6,self.draw_start[1]-6,62,462),2)
        #Getting Row Focus
        p.draw.rect(screen,blue,(self.draw_start[0]-6,self.draw_start[1]+(i)*50-6,462,62),2)
        
        #Current square
        start_i = int(i/3)*3
        start_j = int(j/3)*3
        #print(start_i,start_j)
        
        p.draw.rect(screen,yellow,(self.draw_start[0]+(start_j)*50-3,self.draw_start[0]+(start_i)*50-3,156,156),2)
        
        
        #p.draw.rect(screen,green,(self.draw_start[0]+(j)*50+3-50,self.draw_start[1]+(i)*50+3-50,44+100,44+100),2)
    def take_input(self,mouse):
        if mouse[0]>self.draw_start[0] and mouse[0] < self.draw_start[0]+450 and mouse[1] > self.draw_start[1] and mouse[1]< self.draw_start[1]+450:
            x = mouse[0] - self.draw_start[0]
            y = mouse[1] - self.draw_start[0]
            x = int(x/50)
            y = int(y/50)
            i =y
            j =x
            p.draw.rect(screen,green,(self.draw_start[0]+(j)*50+3,self.draw_start[1]+ (i)*50+3,44,44),2)
            events = p.event.get()
            for event in events:
                if event.type == p.KEYDOWN:
                    keys=p.key.get_pressed()
                    if keys[p.K_1]:
                        self.matrix[i][j] = 1
                    if keys[p.K_2]:
                        self.matrix[i][j] = 2
                    if keys[p.K_3]:
                        self.matrix[i][j] = 3
                    if keys[p.K_4]:
                        self.matrix[i][j] = 4
                    if keys[p.K_5]:
                        self.matrix[i][j] = 5
                    if keys[p.K_6]:
                        self.matrix[i][j] = 6
                    if keys[p.K_7]:
                        self.matrix[i][j] = 7
                    if keys[p.K_8]:
                        self.matrix[i][j] = 8
                    if keys[p.K_9]:
                        self.matrix[i][j] = 9
                    if keys[p.K_0]:
                        self.matrix[i][j] = 0
                        
m = Matrix(matrix)
class Menu_Button():
    def __init__(self,name,pos):
        self.name = name
        self.pos = pos
        
        
        
    def draw(self,mouse):
        
        p.draw.rect(screen, white,(self.pos[0],self.pos[1],150,50))
        largeText = p.font.Font('freesansbold.ttf',20)
        TextSurf, TextRect = text_objects(self.name, largeText,red)
        TextRect.center = (self.pos[0]+int(150/2),self.pos[1]+int(50/2))
        screen.blit(TextSurf, TextRect)
        if (mouse[0] > self.pos[0]) and mouse[0] < self.pos[0]+150 and mouse[1] > self.pos[1] and mouse[1] < self.pos[1]+50:
            p.draw.rect(screen, blue, (self.pos[0]+3, self.pos[1]+3, 144, 44), 2)
            a = p.mouse.get_pressed()
            if a[0] == 1:
                print(self.name)
                self.click()
        pass
    def click(self):
        global Page1,Page2,MainGame,selected_strategy,m,matrix_created,Rollback,pause_check,resume_check
        if self.name == "Start":
            time.sleep(0.5)
            Page1 = False
            Page2 = True
            MainGame = False
            return
        
        if self.name == "Exit":
            Page1 = False
            Page2 = False
            MainGame = False
            return
        if self.name == "Refresh":
            time.sleep(0.5)
            m.refresh()
            return
        if self.name == "Solve!":
            time.sleep(0.5)
            matrix_created = True
            return
        if self.name == "Load":
            time.sleep(0.5)
            m.load_file()
            return
        if self.name == "Menu":
            time.sleep(0.5)
            
            Rollback = True
            Page1 = True
            Page2 = False
            #MainGame = False
            #matrix_created = False
            #agent_created = False
            return
        if self.name == "Pause":
            time.sleep(0.5)
            pause_check = True
            return
        if self.name == "Resume":
            time.sleep(0.5)
            resume_check = True
            return
        #For strategy selection, allows many strategies
        time.sleep(0.5)
        selected_strategy = self.name
        Page2 = False
        MainGame = True
        return
        
        


def run_ui():
    global Page1,Page2,MainGame,selected_strat,m,agent_created,matrix_created,file_to_load,easy_files,medium_files,Rollback,pause_check,resume_check
    start_b = Menu_Button("Start",(275,300))
    exit_b = Menu_Button("Exit",(275,400))
    strat1 = Menu_Button("Easy",(275,300))
    strat2 = Menu_Button("Medium",(275,400))
    solve = Menu_Button("Solve!",(275,600))
    refresh = Menu_Button("Refresh",(275,660))
    load = Menu_Button("Load",(500,650))
    Pause = Menu_Button("Pause",(200,660))
    Resume = Menu_Button("Resume",(400,660))
    Main_Menu = Menu_Button("Menu",(100,50))
    
    while Page1:
        mouse = p.mouse.get_pos()
        clock.tick(fps)
        title = p.image.load('sudokuLogo.png') 
        screen.fill(black)
        start_b.draw(mouse)
        exit_b.draw(mouse)
        screen.blit(title,(175,100))
        
        p.display.flip()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.display.quit()
                p.quit()
                
    while Page2:
        mouse = p.mouse.get_pos()
        clock.tick(fps)
        selection = p.image.load('select.png') 
        screen.fill(black)
        screen.blit(selection,(150,100))
        strat1.draw(mouse)
        strat2.draw(mouse)
        p.display.flip()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.display.quit()
                p.quit()
                
    if selected_strategy == "Easy":
        print("easy selected")
        file_to_load = easy_files
    else:
        file_to_load = medium_files
        
    
                  
    agent = Strategy(selected_strategy)
    #print(file_to_load)
    once = True
    input_s = p.image.load('inputS.png')
    while MainGame:
        mouse = p.mouse.get_pos()
        clock.tick(fps)
        screen.fill(black)
        m.draw_matrix()
        
        if matrix_created == False and agent_created==False:
            screen.blit(input_s,(100,50))
            load.draw(mouse)
            solve.draw(mouse)
            refresh.draw(mouse)
            m.take_input(mouse)
            
        if matrix_created==True and agent_created==False:
            #print(m.matrix)
            m.matrix_drawn()
            #print(m.matrix)
            agent = agent.return_strategy(m.matrix)
            agent_created = True
            
        if matrix_created == True and agent_created == True:
            if pause_check:
                agent.pause()
                pause_check = False
            if resume_check:
                agent.resume()
                resume_check = False
            if Rollback:
                matrix_created=False
                agent_created=False
                MainGame=False
                return
                #print(agent.matrix)
                #print(m.matrix)
                once = False
            Pause.draw(mouse)
            Resume.draw(mouse)
            Main_Menu.draw(mouse)
            m.matrix = agent.matrix
            out,c,ts,te = agent.communicate()
            m.draw_focus(out[0],out[1])
            m.draw_score(c,ts,te)
            
        p.display.flip()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.display.quit()
                p.quit()
    
    
    
    #agent = agent.return_strategy()
                
                
    
    p.display.quit()
    p.quit()

while Rollback:
    print("Entered")
    Rollback = False
    run_ui()
    matrix = []
    for i in range(9):
        matrix.append([0 for j in range(9)])
    m = Matrix(matrix)
    