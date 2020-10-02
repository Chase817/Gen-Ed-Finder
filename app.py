#!/usr/bin/env python3

#
# genEdFinder.py - Finds gen eds that satisfy multiple categories
#
# 03 Nov 2018 - Written by Chase Hill
#


from flask import Flask, render_template
#from flask import Flask, flash, redirect, render_template, request, session, abort
from bs4 import BeautifulSoup
from itertools import combinations
import re
import requests
 
app = Flask(__name__)
 
@app.route("/")
def index():
    return "Enter selection in URL (Ex: 127.0.0.1/BCDEFG)"
 
@app.route("/<string:selection>/")
def genEdFinder(selection):

    # Gets all the courses found at the passed url and returns a list of their
    # names without course descriptions
    def getCourses(url):
        
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
        
        # Initialize list of courses without descriptions
        courseNoDesc = []
        
        # Searches each line for the string immediately preceding the course and
        # uses string methods and regular expressions to parse the course names
        for i in range(len(lines)):
            
            if (lines[i].strip() == '<p style="text-indent: -10px; margin-top: 0px; margin-bottom: 0px; padding: 0px; margin-left: 23px;">'):
        
                course = lines[i+1] + lines[i+3]
                
                course = course.strip()  # Strips whitespace on beginning and end
        
                course = re.sub(r"\s+", ' ', course)  # Subs all remaining
                                                      # whitespace for single
                                                      # space
                
                # Gets rid of everything but course name
                courseNoDesc.append(re.sub(r" -.*", '', course))
                
        return courseNoDesc
    
    
    urlB = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaB.aspx'
    urlC = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaC.aspx'
    urlD = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaD.aspx'
    urlE = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaE.aspx'
    urlF = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaF.aspx'
    urlG = 'https://my.sa.ucsb.edu/catalog/Current/UndergraduateEducation/AreaG.aspx'
    
    # Formats selection input from url to be used
    selection = selection.replace(" ", "")
    selection = selection.upper()
    selection = list(selection)
    
    courses = [[],[],[],[],[],[]]  # List of area course lists, B through G
    
    print("Downloading course lists...")
    
    for i in range(len(selection)):
       
        if selection[i] == 'B': courses[0] = getCourses(urlB)
        elif selection[i] == 'C': courses[1] = getCourses(urlC)
        elif selection[i] == 'D': courses[2] = getCourses(urlD)
        elif selection[i] == 'E': courses[3] = getCourses(urlE)
        elif selection[i] == 'F': courses[4] = getCourses(urlF)
        elif selection[i] == 'G': courses[5] = getCourses(urlG)
        
        # Gotta get input checking working better with the website
        else: print("An area you have selected is invalid")

    # String that lists the areas being matched
    areaString = ' & '.join(selection)
    
    # Finds all possible combinations of areas to match
    areaCombinations = []
    selectionString = ''.join(selection)
    for i in range(len(selection)):
        if i > 1:
            areaCombinations.append([x for x in combinations(selectionString,i)])
    
    # Generates list of indexes corresponding to populated courses[] elements
    # Ex: areaSelectionIndex[0] is the first element of courses[] with a
    # complete list
    areaSelectionIndex = []
    for i in range(len(courses)):
        if courses[i] != []:
            areaSelectionIndex.append(i)
            
    # Looks for perfect matches to the selection
    matches = set(courses[areaSelectionIndex[0]])
    for i in areaSelectionIndex:
        matches = matches.intersection(courses[i])
    
    # String containing all output to the website
    finalOutputString = ''
    
    # Lists perfect matches if possible
    if matches != set():
        print("Courses satisfying Area", areaString)
        matches = sorted(matches)
        matches = ', '.join(matches)
        print(matches)
        finalOutputString += "Courses satisfying Area " + areaString + ": <br/><br/>" + matches + "<br/>"
    else:
        print("No exact matches, but I found these:")
        finalOutputString += "No exact matches, but I found these:<br/><br/>"
        
    
    
    # Looks for secondary matches satisfying any combination of selected areas
    if matches == set():
        for i in areaCombinations:  # Will this ever iterate beyond areaCombinations[0]?
            for j in i:
                areaSelectionIndex = []  # List of courses[] indices 
                                         # corresponding to areas being matched
                for k in range(len(j)):
                    if j[k] == 'B': areaSelectionIndex.append(0)
                    elif j[k] == 'C': areaSelectionIndex.append(1)
                    elif j[k] == 'D': areaSelectionIndex.append(2)
                    elif j[k] == 'E': areaSelectionIndex.append(3)
                    elif j[k] == 'F': areaSelectionIndex.append(4)
                    elif j[k] == 'G': areaSelectionIndex.append(5)
                    
                matches = set(courses[areaSelectionIndex[0]])
                for i in areaSelectionIndex:
                    matches = matches.intersection(courses[i])
                    
                if matches != set():
                    areaString = ' & '.join(j)
                    matches = sorted(matches)
                    matches = ', '.join(matches)
                    print(areaString + ':',matches)
                    finalOutputString += areaString + ":<br/>" + matches + "<br/><br/>"
 
    return render_template(
        'test.html',**locals())
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
