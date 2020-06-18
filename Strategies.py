#!/usr/bin/env python
# coding: utf-8

# In[83]:


import numpy as np


# In[ ]:


def get_column_row_focus(focus,square,row1,row2,row3,col1,col2,col3):
    
    focus_row_index = focus[0] % 3
    focus_column_index = focus[1] % 3
    
    if focus_row_index == 0:
        focus_row = row1
    elif focus_row_index == 1:
        focus_row = row2
    elif focus_row_index == 2:
        focus_row = row3
        
    if focus_column_index == 0:
        focus_column = col1
    elif focus_column_index == 1:
        focus_column = col2
    elif focus_column_index == 2:
        focus_column = col3
        
    return focus_column, focus_row


# In[84]:


## This function recieves as input a row or a column to check if only
## a single cell is empty and its value.
def only_choice_rule_column(focus,square,row1,row2,row3,col1,col2,col3):
    cells,_ = get_column_row_focus(focus,square,row1,row2,row3,col1,col2,col3)
    numbers = list(cells.keys())
    solved = False
    solution = 0
    ## If the size of the values vector is 8, we can identify which value
    ## is missing
    if np.size(numbers)==8:
        solution += 1
        while (solved == False):
            solved = True
            for cell in numbers:
                if cell == solution:
                    solution += 1
                    solved = False
    return solved, solution


# In[ ]:


## This function recieves as input a row or a column to check if only
## a single cell is empty and its value.
def only_choice_rule_row(focus,square,row1,row2,row3,col1,col2,col3):
    _,cells = get_column_row_focus(focus,square,row1,row2,row3,col1,col2,col3)
    numbers = list(cells.keys())
    solved = False
    solution = 0
    ## If the size of the values vector is 8, we can identify which value
    ## is missing
    if np.size(numbers)==8:
        solution += 1
        while (solved == False):
            solved = True
            for cell in numbers:
                if cell == solution:
                    solution += 1
                    solved = False
    return solved, solution


# In[85]:


## This function recieves as input a row and a column to check if only
## a single cell is empty and its value.
def single_possibility_rule(focus,square,row1,row2,row3,col1,col2,col3):
    column,row = get_column_row_focus(focus,square,row1,row2,row3,col1,col2,col3)
    solved = False
    solution = 0
    
    ## We create a vector with the unique values of the row+column combination.
    values = np.append(list(row.keys()),list(column.keys()))
    values = np.unique(values)
    
    ## If the size of the values vector is 8, we can identify which value
    ## is missing in the row+column combination.
    if np.size(values)==8:
        solution += 1
        while (solved == False):
            solved = True
            for value in values:
                if value == solution:
                    solution += 1
                    solved = False
        
    return solved, solution


# In[86]:


## This function recieves as input a square to check if only
## a single cell is empty and its value.
def only_square_rule(focus,square,row1,row2,row3,col1,col2,col3):
    numbers = list(square.keys())
    solved = False
    solution = 0
    ## If the size of the values vector is 8, we can identify which value
    ## is missing
    if np.size(numbers)==8:
        solution += 1
        while (solved == False):
            solved = True
            for cell in numbers:
                if cell == solution:
                    solution += 1
                    solved = False
    return solved, solution


# In[ ]:


## This function recieves as input a row, a column and a square to check if only
## a single cell is empty and its value.
def mixed_single_possibility_rule(focus,square,row1,row2,row3,col1,col2,col3):
    solved = False
    solution = 0
    
    ## We create a vector with the unique values of the row+column combination.
    column,row = get_column_row_focus(focus,square,row1,row2,row3,col1,col2,col3)
    values = np.append(list(row.keys()),list(column.keys()))
    values = np.append(values,list(square.keys()))
    values = np.unique(values)
    
    ## If the size of the values vector is 8, we can identify which value
    ## is missing in the row+column combination.
    if np.size(values)==8:
        solution += 1
        while (solved == False):
            solved = True
            for value in values:
                if value == solution:
                    solution += 1
                    solved = False
        
    return solved, solution


# In[ ]:


## Rows and columns are all the rows and columns based on the square. We need a number (f.e. )
## Think that we need a coordinate + number system, not just the number vector,
## cause we have to do diff comprobations based on the position (row or column the cell belongs to).
def two_out_of_three_rule(focus,square,row1,row2,row3,col1,col2,col3,empty_sqr):
    solved = False
    solution = 0
    
    focus_column,focus_row = get_column_row_focus(focus,square,row1,row2,row3,col1,col2,col3)
    
    all_possible_values = list(range(1, 10))
    focus_possible_values = np.empty(0, int)    
    
    focus_no_possible_values = np.append(list(focus_row.keys()),list(focus_column.keys()))
    focus_no_possible_values = np.append(focus_no_possible_values,list(square.keys()))
    focus_no_possible_values = np.unique(focus_no_possible_values)
    
    for number in all_possible_values:
        if number not in focus_no_possible_values:
            focus_possible_values = np.append(focus_possible_values,number)
            
    for number in focus_possible_values:
        solved = True
        
        for coord in empty_sqr:
            
            empty_cell_possible_values = np.empty(0, int)
            empty_cell_column,empty_cell_row = get_column_row_focus(coord,square,row1,row2,row3,col1,col2,col3)
            empty_cell_no_possible_values = np.append(list(empty_cell_row.keys()),list(empty_cell_column.keys()))
            empty_cell_no_possible_values = np.append(empty_cell_no_possible_values,list(square.keys()))
            empty_cell_no_possible_values = np.unique(empty_cell_no_possible_values)
                            
            if number not in empty_cell_no_possible_values:
                solved = False
        
        if solved == True:
            solution = number
            break
    
    return solved, solution

