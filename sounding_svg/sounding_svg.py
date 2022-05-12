# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:41:00 2022

@author: apickett
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May  2 16:07:51 2022

@author: apickett
"""
import shutil
import math

#designate the new sounding
def sounding_svg2(input_sounding):
    for x in input_sounding:
        
        if input_sounding < 0: 
            input_sounding1 = -1 * input_sounding
        else: input_sounding1 = input_sounding
        
        #designate the formatting (1 decimal place)
        input_sounding2 = "{:.2f}".format(input_sounding1)
        size = len(input_sounding2)
        input_sounding2 = input_sounding2[:size - 1]
        
        #split up the integer and the decimal
        integer = str('>{}<').format(input_sounding2.split('.')[0])
        decimal = str('>{}<').format(input_sounding2.split('.')[1])
        
        
        if 10 < math.modf(input_sounding1)[1] < 30:
            #create a copy of the correct template 
            shutil.copyfile('sounding_template.svg', 'sounding.svg')
            change = open('sounding.svg', "rt")
            
            #read the file
            data = change.read()
        
            #find and replace the sounding numbers
            data = data.replace('>12<', integer)
            data = data.replace('>4<', decimal)
        
            change.close()
        
            change = open("sounding" + str(x) + ".svg", "wt") 
        
            change.write(data)
            
            change.close()
            
        if  math.modf(input_sounding1)[1] >30:
            shutil.copyfile('sounding_template2.svg', 'sounding.svg')
            change = open('sounding.svg', "rt")
            data = change.read()
        
            data = data.replace('>12<', integer)
        
            change.close()
        
            change = open("sounding" + str(x) + ".svg", "wt") 
        
            change.write(data)
            
            change.close()
            
        if 0 < math.modf(input_sounding1)[1] < 10:
            #create a copy of the correct template 
            shutil.copyfile('sounding_template3.svg', 'sounding.svg')
            change = open('sounding.svg', "rt")
            
            #read the file
            data = change.read()
        
            #find and replace the sounding numbers
            data = data.replace('>0<', integer)
            data = data.replace('>4<', decimal)
        
            change.close()
        
            change = open("sounding" + str(x) + ".svg", "wt") 
        
            change.write(data)
            
            change.close()
            
        if math.modf(input_sounding)[1] > 0:
            #create a copy of the correct template 
            shutil.copyfile('sounding_template4.svg', 'sounding.svg')
            change = open('sounding.svg', "rt")
            
            #read the file
            data = change.read()
        
            #find and replace the sounding numbers
            data = data.replace('>0<', integer)
            data = data.replace('>4<', decimal)
        
            change.close()
        
            change = open("sounding" + str(x) + ".svg", "wt") 
        
            change.write(data)
            
            change.close()
        

        