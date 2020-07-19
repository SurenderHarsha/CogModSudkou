#!/usr/bin/env python
# coding: utf-8

# In[37]:


from model import Model
from dmchunk import Chunk
import numpy as np
from Strategies import * 
from Sudoku_perception import * 


# In[38]:


m = Model()
perseverance = 50 ## The maximum number of repetitions for the same strategy.


# In[39]:


### The chunks reserved for the kind of strategies that we will try to use. The simple ones are the straighforward
### ones, where not complex operations are needed, just checking rows/columns or squares. The medium ones require combining
### comprobations or more complex operations. The complexity rate will be used to divide the max_repetitions for this rate,
### in order to make more likely to keep and strategie of its easier than a complex one.
strategies_list = ('simple_strategies','medium_strategies')

simple_strategies_list = (only_choice_rule_column,only_choice_rule_row,single_possibility_rule,
                          only_square_rule,mixed_single_possibility_rule)
medium_strategies_list = (two_out_of_three_rule)


chunk_simple = Chunk(name = 'simple_strategies', slots = {"repetitions": 0,"times_tried":1,"complexity_rate":1})
chunk_medium = Chunk(name = 'medium_strategies', slots = {"repetitions": 0,"times_tried":0,"complexity_rate":5})


# In[40]:


## Continue using the same strategy and add a repetition to the memory.
def keep_strategy(chunk):
    m.time += 0.005
    chunk.slots["repetitions"] += 1


# In[41]:


## If the model thinks that it should change o strategy, or if the model solved a cell (put a correct number)
## it will chose a new one

def change_strategy(chunk, number_solved = False):
    
    if (number_solved == True):
        m.time += 0.005
        m.add_encounter(chunk)
    
    selected_strategy = strategies_list[np.random.randint(0,2)] 
    
    m.time += 0.005
    if selected_strategy == 'simple_strategies':
        new_strategy = chunk_simple
    elif selected_strategy == 'medium_strategies':
        new_strategy = chunk_medium
        
    new_strategy.slots["times_tried"] += 1
    new_strategy.slots["repetitions"] = 0
    
    return new_strategy


# In[42]:


## This fuction receives the current strategy used (the chunk storaged in the DM)
## and perform a random calculation of fatigue to check if they should keep trying the
## same strategie or if it should change to a new one (it could occur if he solve a cell).
## The output is the strategy that should be use next (the chunk for the DM) and the name of it (to use
## it with the logical part of the program).
def next_step(chunk,number_solved = False):
    
    repetition_sensation = chunk.slots["repetitions"] + np.random.randint(1,5)
    
    if (repetition_sensation >= perseverance / chunk.slots["complexity_rate"]):
        chunk = change_strategy(chunk)
    elif number_solved == True:
        chunk = change_strategy(chunk,True)
    else:
        keep_strategy(chunk)
        
    m.time += 0.005
    m.add_encounter(chunk)

    return chunk, chunk.name


# In[43]:


## Objects needed for the program to work
chunk = chunk_simple ## We define the first strategy, the initial one.
number_solved = False ## This will be calculated with the logic of the program.

## The function that will be used for the main program
def strategy_cycle(focus,square,r1,r2,r3,c1,c2,c3,empty_sqr):
        global chunk,number_solved
        chunk,strategy_name = next_step(chunk,number_solved)
        solution = 0
        
        focus_column,focus_row = get_column_row_focus(focus,square,r1,r2,r3,c1,c2,c3)
            
        if strategy_name == 'simple_strategies':

            perceived_ocrr = perceived_numbers(focus_row,focus)
            perceived_ocrc = perceived_numbers(focus_column,focus)
            perceived_osr = perceived_numbers(square,focus)
            perceived_spr = (perceived_ocrr + perceived_ocrc)/2
            perceived_mspr = (perceived_ocrr + perceived_ocrc + perceived_osr)/3
            
            rankings = (perceived_ocrr,perceived_ocrc,perceived_osr,perceived_spr,perceived_mspr)
            sorted_ranking = sorted(rankings)[::-1]
            
            for strat in sorted_ranking:
                strategy_name_index = rankings.index(strat)
                strategy_n = simple_strategies_list[strategy_name_index]
                number_solved,solution = strategy_n(focus,square,r1,r2,r3,c1,c2,c3)
                if number_solved == True:
                    break
            
        if strategy_name == 'medium_strategies':
            number_solved,solution = two_out_of_three_rule(focus,square,r1,r2,r3,c1,c2,c3,empty_sqr)
        #print(strategy_name)
        return number_solved,solution,strategy_name

