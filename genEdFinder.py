#!/usr/bin/env python3

#
# genEdFinder.py - Finds gen eds that satisfy multiple categories
#                           using requests and bs4
#
# 31 Oct 2018 - Written by Chase Hill
#


from bs4 import BeautifulSoup
import re
import requests


def getCourses(url):
    
    print("Running getCourses()...")
    
    # Grabs data from index.html of the course site
    r = requests.get(url)
    
    # Extracts the content into webpage
    webpage = r.content
    
    # Parses the html into a form that BeautifulSoup can operate on
    soup = BeautifulSoup(webpage, 'html.parser')
    
    # Definitely not using BS to its full potential here, but the prettify method
    # prints out the html in a tiered fashion in which I can parse the desired
    # lines easier using string methods
    page = soup.prettify()
    
    # Splits the "prettified"  page up by lines
    lines = page.split('\n')
    
    courseNoDesc = []
    
    # Searches each line for the string immediately preceding the course and
    # uses string methods to parse the rest of the line in a readable way
    for i in range(len(lines)):
        
        if (lines[i].strip() == '<p style="text-indent: -10px; margin-top: 0px; margin-bottom: 0px; padding: 0px; margin-left: 23px;">'):
    
            course = lines[i+1] + lines[i+3]
            
            course = course.strip()  # Strips whitespace on beginning and end
    
            course = re.sub(r"\s+", ' ', course)  # Subs all whitespace for single
                                                  # space
            
            courseNoDesc.append(re.sub(r" -.*", '', course))
            
    return courseNoDesc


urlB = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaB.aspx'
urlC = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaC.aspx'
urlD = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaD.aspx'
urlE = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaE.aspx'
urlF = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaF.aspx'
urlG = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaG.aspx'

selection = input("Which areas? (Comma sep) [B,C,D,E,F,G]: ")
selection = selection.split(',')

courses = []  # List of area course lists

for i in range(len(selection)):
   
    if selection[i] == 'B': courses.append(getCourses(urlB))
    elif selection[i] == 'C': courses.append(getCourses(urlC))
    elif selection[i] == 'D': courses.append(getCourses(urlD))
    elif selection[i] == 'E': courses.append(getCourses(urlE))
    elif selection[i] == 'F': courses.append(getCourses(urlF))
    elif selection[i] == 'G': courses.append(getCourses(urlG))
    else: print("An area you have selected is invalid")
    


areaString = ''

for i in range(len(selection)):
    if i == 0:
        areaString = selection[i]
    else:
        areaString += (' & ' + selection[i])

print("Courses satisfying Area", areaString)

matches = set(courses[0]).intersection(courses[1])
subsequentListIndex = 2
while subsequentListIndex < (len(selection)):
    matches = matches.intersection(courses[subsequentListIndex])
    subsequentListIndex = subsequentListIndex + 1
    
# =============================================================================
# if (len(selection) > 2) and (matches != set()):
#     print('Perfect match not found. Near matches:')
#     matches = set(courses[0]).intersection(courses[1])
#     if matches != set():
# =============================================================================

print(matches)