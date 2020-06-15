#!/usr/bin/env python
# coding: utf-8

# In[57]:


import numpy as np
import math

perception_boundary = 5


# In[58]:


def noise(s):
    rand = np.random.uniform(0.301,0.699)
    return 2 * s * rand


# In[59]:


## This fuction will model the perception of a cell by a human,
## based on the distance to the focus where the eye is looking to.
## The inputs are the focus coordinates, and a cell (with a value or empty, and 
## the coordinates).
def has_number(coord,focus):
        distance = math.sqrt((coord[0]-focus[0])**2+(coord[1]-focus[1])**2) ## Distance from the cell to the focus
        ## If the cell is inside our perception boundary, we detect the number
        if noise(distance) <= perception_boundary:
            return 1
        ## If the cell is outside the boundary, the number is ommited for the strategy selection
        else:
            return 0


# In[60]:


def perceived_numbers(element,focus):
    sum_numbers = 0
    for _,coord in element.items():
        sum_numbers += has_number(coord,focus)
    return sum_numbers

