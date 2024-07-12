import pyodbc
import pandas as pd
import requests
from selenium import webdriver
import urllib3
import json
from datetime import datetime
import time
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
app = Flask(__name__)


server = 'krishna-capstone.database.windows.net'
database = 'KrishnaCapstone'
username = 'Krushulang'
password = '{Krishna12!}'   
driver= '{ODBC Driver 18 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

resultcnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
resultcursor = resultcnxn.cursor()

majorcnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
majorcursor = majorcnxn.cursor()

tempcnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
tempcursor = tempcnxn.cursor()

precnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
precursor = precnxn.cursor()

# INSERT INTO MajorCourse (MajorName, CampusName, CourseName, IsCore)
# VALUES ('Bachelor of Science degree with a major in Biology', 'Bothell', 'BBIO ELECTIVES 20 (20 300)', 1)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/bothload', methods=['GET'])
def bothload():
   result = '{"choose":"Please choose your major"}'
   try:
      majorcursor.execute('''
                     SELECT MajorName
                     FROM Major
                     WHERE CampusName = 'Bothell'
                     '''
      )
      for row in majorcursor:
         for elm in row:
            loader = {elm:elm}
            jsonline = json.loads(result)
            jsonline.update(loader)
            result = jsonline
            result = json.dumps(result)
            
   except Exception as e:
      print(e)
   return result


@app.route('/results', methods=['POST'])
def results():
   major = request.form.get('major')
   departments = request.form.getlist('department')
   courses = request.form.getlist('courses')
   quarter = request.form.get('quarter')
   days = request.form.getlist('days')
   inperson = request.form.get('inperson')
   online = request.form.get('online')
   education = request.form.getlist('education')
   curriculum = request.form.getlist('curriculum')
   time = request.form.get('time')
   size = request.form.get('size')
   error = 'Please Select a Major Before Continuing'
   result = {}
   newres = []
   courselist = []
   for course in courses:
      if course.split(" ")[1].isdigit():
         courselist.append(course.split(" ")[0] + " " + course.split(" ")[1])
      else:
         courselist.append(course.split(" ")[0] + course.split(" ")[1] + " " + course.split(" ")[2])
   print(courselist)
   prereqarray = []
   # try:
   precursor.execute('''
                        SELECT CourseName, Prerequisite, AltCourse1, AltCourse2, AltCourse3, AltCourse4, AltCourse5, AltCourse6, AltCourse7, AltCourse8, AltCourse9 FROM [dbo].[Prerequisite]
                        '''
   )
   z = 0
   for pre in precursor:
      prehelp = []
      for next in pre:
         if not str(next) == "None":
            prehelp.append(str(next))
      prereqarray.append(prehelp)
      z += 1
   resultcursor.execute('''
                  SELECT CourseName FROM MajorCourse
                  WHERE MajorName=? 
                  ''',
                  (major))
   for course in resultcursor:
      elm = course.CourseName
      if elm.__contains__('('):
         if elm.__contains__("ELECTIVES"):
            section = elm.split(" ")[0]
            amount = elm.split(" ")[2]
            if elm.split(" ")[3].split("(")[1] == amount:
               specific = 0
            else:
               specific = elm.split(" ")[4].split(")")[0]
            if section == "ANY":
               tempcursor.execute('''
                              SELECT Department, CourseNumber FROM Courses
                              WHERE CourseNumber>=?
                              AND CourseNumber<500 
                              AND CampusName=?
                              ''',
                              (specific, 'Bothell'))
               resu = ""   
               tracker = 0
               for gen in tempcursor:
                  for new in gen:
                     resu += str(new) + " "
                     if tracker == 1:
                        tracker = 0
                        resu = resu.strip()
                        moveOn = True
                        for course in courselist:
                           if course == resu:
                              moveOn = False
                        isGood = True
                        if resu.__contains__('BACCT'):
                           temp = resu.split(" ")[1]
                           resu = 'B ACCT' + " " + temp
                           
                        if resu.__contains__('BBUS'):
                           temp = resu.split(" ")[1]
                           resu = 'B BUS' + " " + temp
                           
                        if resu.__contains__('BBECN'):
                           temp = resu.split(" ")[1]
                           resu = 'B BECN' + " " + temp
                           
                        if resu.__contains__('BBSKL'):
                           temp = resu.split(" ")[1]
                           resu = 'B BSKL' + " " + temp
                           
                        if resu.__contains__('ACMPT'):
                           temp = resu.split(" ")[1]
                           resu = 'A CMPT' + " " + temp
                           
                        if resu.__contains__('BEDUC'):
                           temp = resu.split(" ")[1]
                           resu = 'B EDUC' + " " + temp
                           
                        if resu.__contains__('BIMD'):
                           temp = resu.split(" ")[1]
                           resu = 'B IMD' + " " + temp
                           
                        if resu.__contains__('BHLTH'):
                           temp = resu.split(" ")[1]
                           resu = 'B HLTH' + " " + temp
                           
                        if resu.__contains__('BNURS'):
                           temp = resu.split(" ")[1]
                           resu = 'B NURS' + " " + temp
                           
                        if resu.__contains__('BBIO'):
                           temp = resu.split(" ")[1]
                           resu = 'B BIO' + " " + temp
                           
                        if resu.__contains__('BCHEM'):
                           temp = resu.split(" ")[1]
                           resu = 'B CHEM' + " " + temp
                           
                        if resu.__contains__('BCLIM'):
                           temp = resu.split(" ")[1]
                           resu = 'B CLIM' + " " + temp
                           
                        if resu.__contains__('BEE'):
                           temp = resu.split(" ")[1]
                           resu = 'B EE' + " " + temp
                           
                        if resu.__contains__('BENGR'):
                           temp = resu.split(" ")[1]
                           resu = 'B ENGR' + " " + temp
                           
                        if resu.__contains__('BMATH'):
                           temp = resu.split(" ")[1]
                           resu = 'B MATH' + " " + temp
                           
                        if resu.__contains__('BME'):
                           temp = resu.split(" ")[1]
                           resu = 'B ME' + " " + temp
                           
                        if resu.__contains__('BPHYS'):
                           temp = resu.split(" ")[1]
                           resu = 'B PHYS' + " " + temp
                           
                        if resu.__contains__('BASL'):
                           temp = resu.split(" ")[1]
                           resu = 'B ASL' + " " + temp
                           
                        if resu.__contains__('BARAB'):
                           temp = resu.split(" ")[1]
                           resu = 'B ARAB' + " " + temp
                           
                        if resu.__contains__('BART'):
                           temp = resu.split(" ")[1]
                           resu = 'B ART' + " " + temp
                           
                        if resu.__contains__('BARTS'):
                           temp = resu.split(" ")[1]
                           resu = 'B ARTS' + " " + temp
                           
                        if resu.__contains__('BCHIN'):
                           temp = resu.split(" ")[1]
                           resu = 'B CHIN' + " " + temp
                           
                        if resu.__contains__('BCORE'):
                           temp = resu.split(" ")[1]
                           resu = 'B CORE' + " " + temp
                           
                        if resu.__contains__('BDATA'):
                           temp = resu.split(" ")[1]
                           resu = 'B DATA' + " " + temp
                           
                        if resu.__contains__('BLEAD'):
                           temp = resu.split(" ")[1]
                           resu = 'B LEAD' + " " + temp
                           
                        if resu.__contains__('BSPAN'):
                           temp = resu.split(" ")[1]
                           resu = 'B SPAN' + " " + temp
                           
                        if resu.__contains__('BCUSP'):
                           temp = resu.split(" ")[1]
                           resu = 'B CUSP' + " " + temp
                           
                        if resu.__contains__('BWRIT'):
                           temp = resu.split(" ")[1]
                           resu = 'B WRIT' + " " + temp
                        for pre in prereqarray:
                           if pre[0].__contains__(resu):
                              if not len(pre) > 1:
                                 continue
                              isGood = False
                              for temp in pre[1:]:
                                 for course in courselist:
                                    if course.__contains__(temp):
                                       isGood = True
                              if not isGood:
                                 break
                        if moveOn and isGood and resu != "":
                           if not resu in result:
                              result[resu] = 1
                           else:
                              result[resu] += 1
                        resu = ""
                     else:
                        tracker += 1  
               
            else:
               tempcursor.execute('''
                              SELECT Department, CourseNumber FROM Courses
                              WHERE CourseNumber>?
                              AND Department=? 
                              AND CourseNumber<500
                              AND CampusName=?
                              ''',
                              (specific, section, 'Bothell'))
               resu = ""   
               tracker = 0
               for gen in tempcursor:
                  for new in gen:
                     resu += str(new) + " "
                     if tracker == 1:
                        tracker = 0
                        resu = resu.strip()
                        moveOn = True
                        for course in courselist:
                           if course == resu:
                              moveOn = False
                        isGood = True
                        if resu.__contains__('BACCT'):
                           temp = resu.split(" ")[1]
                           resu = 'B ACCT' + " " + temp
                           
                        if resu.__contains__('BBUS'):
                           temp = resu.split(" ")[1]
                           resu = 'B BUS' + " " + temp
                           
                        if resu.__contains__('BBECN'):
                           temp = resu.split(" ")[1]
                           resu = 'B BECN' + " " + temp
                           
                        if resu.__contains__('BBSKL'):
                           temp = resu.split(" ")[1]
                           resu = 'B BSKL' + " " + temp
                           
                        if resu.__contains__('ACMPT'):
                           temp = resu.split(" ")[1]
                           resu = 'A CMPT' + " " + temp
                           
                        if resu.__contains__('BEDUC'):
                           temp = resu.split(" ")[1]
                           resu = 'B EDUC' + " " + temp
                           
                        if resu.__contains__('BIMD'):
                           temp = resu.split(" ")[1]
                           resu = 'B IMD' + " " + temp
                           
                        if resu.__contains__('BHLTH'):
                           temp = resu.split(" ")[1]
                           resu = 'B HLTH' + " " + temp
                           
                        if resu.__contains__('BNURS'):
                           temp = resu.split(" ")[1]
                           resu = 'B NURS' + " " + temp
                           
                        if resu.__contains__('BBIO'):
                           temp = resu.split(" ")[1]
                           resu = 'B BIO' + " " + temp
                           
                        if resu.__contains__('BCHEM'):
                           temp = resu.split(" ")[1]
                           resu = 'B CHEM' + " " + temp
                           
                        if resu.__contains__('BCLIM'):
                           temp = resu.split(" ")[1]
                           resu = 'B CLIM' + " " + temp
                           
                        if resu.__contains__('BEE'):
                           temp = resu.split(" ")[1]
                           resu = 'B EE' + " " + temp
                           
                        if resu.__contains__('BENGR'):
                           temp = resu.split(" ")[1]
                           resu = 'B ENGR' + " " + temp
                           
                        if resu.__contains__('BMATH'):
                           temp = resu.split(" ")[1]
                           resu = 'B MATH' + " " + temp
                           
                        if resu.__contains__('BME'):
                           temp = resu.split(" ")[1]
                           resu = 'B ME' + " " + temp
                           
                        if resu.__contains__('BPHYS'):
                           temp = resu.split(" ")[1]
                           resu = 'B PHYS' + " " + temp
                           
                        if resu.__contains__('BASL'):
                           temp = resu.split(" ")[1]
                           resu = 'B ASL' + " " + temp
                           
                        if resu.__contains__('BARAB'):
                           temp = resu.split(" ")[1]
                           resu = 'B ARAB' + " " + temp
                           
                        if resu.__contains__('BART'):
                           temp = resu.split(" ")[1]
                           resu = 'B ART' + " " + temp
                           
                        if resu.__contains__('BARTS'):
                           temp = resu.split(" ")[1]
                           resu = 'B ARTS' + " " + temp
                           
                        if resu.__contains__('BCHIN'):
                           temp = resu.split(" ")[1]
                           resu = 'B CHIN' + " " + temp
                           
                        if resu.__contains__('BCORE'):
                           temp = resu.split(" ")[1]
                           resu = 'B CORE' + " " + temp
                           
                        if resu.__contains__('BDATA'):
                           temp = resu.split(" ")[1]
                           resu = 'B DATA' + " " + temp
                           
                        if resu.__contains__('BLEAD'):
                           temp = resu.split(" ")[1]
                           resu = 'B LEAD' + " " + temp
                           
                        if resu.__contains__('BSPAN'):
                           temp = resu.split(" ")[1]
                           resu = 'B SPAN' + " " + temp
                           
                        if resu.__contains__('BCUSP'):
                           temp = resu.split(" ")[1]
                           resu = 'B CUSP' + " " + temp
                           
                        if resu.__contains__('BWRIT'):
                           temp = resu.split(" ")[1]
                           resu = 'B WRIT' + " " + temp
                        for pre in prereqarray:
                           if pre[0].__contains__(resu):
                              if not len(pre) > 1:
                                 continue
                              isGood = False
                              for temp in pre[1:]:
                                 for course in courselist:
                                    if course.__contains__(temp):
                                       isGood = True
                              if not isGood:
                                 break
                        if moveOn and isGood and resu != "":
                           if not resu in result:
                              result[resu] = 1
                           else:
                              result[resu] += 1
                        resu = ""
                     else:
                        tracker += 1  
               
         else:
            requirement = elm.split(" ")[0]  
            tempcursor.execute('''
                           SELECT Department, CourseNumber FROM Courses
                           WHERE EducationRequirement LIKE ? 
                           AND CourseNumber<500
                           AND CampusName=?
                           ''',
                           ('%'+requirement+'%', 'Bothell'))
            resu = ""   
            tracker = 0
            for gen in tempcursor:
               for new in gen:
                  resu += str(new) + " "
                  if tracker == 1:
                     tracker = 0
                     resu = resu.strip()
                     moveOn = True
                     for course in courselist:
                        if course == resu:
                           moveOn = False
                     isGood = True
                     if resu.__contains__('BACCT'):
                        temp = resu.split(" ")[1]
                        resu = 'B ACCT' + " " + temp
                        
                     if resu.__contains__('BBUS'):
                        temp = resu.split(" ")[1]
                        resu = 'B BUS' + " " + temp
                        
                     if resu.__contains__('BBECN'):
                        temp = resu.split(" ")[1]
                        resu = 'B BECN' + " " + temp
                        
                     if resu.__contains__('BBSKL'):
                        temp = resu.split(" ")[1]
                        resu = 'B BSKL' + " " + temp
                        
                     if resu.__contains__('ACMPT'):
                        temp = resu.split(" ")[1]
                        resu = 'A CMPT' + " " + temp
                        
                     if resu.__contains__('BEDUC'):
                        temp = resu.split(" ")[1]
                        resu = 'B EDUC' + " " + temp
                        
                     if resu.__contains__('BIMD'):
                        temp = resu.split(" ")[1]
                        resu = 'B IMD' + " " + temp
                        
                     if resu.__contains__('BHLTH'):
                        temp = resu.split(" ")[1]
                        resu = 'B HLTH' + " " + temp
                        
                     if resu.__contains__('BNURS'):
                        temp = resu.split(" ")[1]
                        resu = 'B NURS' + " " + temp
                        
                     if resu.__contains__('BBIO'):
                        temp = resu.split(" ")[1]
                        resu = 'B BIO' + " " + temp
                        
                     if resu.__contains__('BCHEM'):
                        temp = resu.split(" ")[1]
                        resu = 'B CHEM' + " " + temp
                        
                     if resu.__contains__('BCLIM'):
                        temp = resu.split(" ")[1]
                        resu = 'B CLIM' + " " + temp
                        
                     if resu.__contains__('BEE'):
                        temp = resu.split(" ")[1]
                        resu = 'B EE' + " " + temp
                        
                     if resu.__contains__('BENGR'):
                        temp = resu.split(" ")[1]
                        resu = 'B ENGR' + " " + temp
                        
                     if resu.__contains__('BMATH'):
                        temp = resu.split(" ")[1]
                        resu = 'B MATH' + " " + temp
                        
                     if resu.__contains__('BME'):
                        temp = resu.split(" ")[1]
                        resu = 'B ME' + " " + temp
                        
                     if resu.__contains__('BPHYS'):
                        temp = resu.split(" ")[1]
                        resu = 'B PHYS' + " " + temp
                        
                     if resu.__contains__('BASL'):
                        temp = resu.split(" ")[1]
                        resu = 'B ASL' + " " + temp
                        
                     if resu.__contains__('BARAB'):
                        temp = resu.split(" ")[1]
                        resu = 'B ARAB' + " " + temp
                        
                     if resu.__contains__('BART'):
                        temp = resu.split(" ")[1]
                        resu = 'B ART' + " " + temp
                        
                     if resu.__contains__('BARTS'):
                        temp = resu.split(" ")[1]
                        resu = 'B ARTS' + " " + temp
                        
                     if resu.__contains__('BCHIN'):
                        temp = resu.split(" ")[1]
                        resu = 'B CHIN' + " " + temp
                        
                     if resu.__contains__('BCORE'):
                        temp = resu.split(" ")[1]
                        resu = 'B CORE' + " " + temp
                        
                     if resu.__contains__('BDATA'):
                        temp = resu.split(" ")[1]
                        resu = 'B DATA' + " " + temp
                        
                     if resu.__contains__('BLEAD'):
                        temp = resu.split(" ")[1]
                        resu = 'B LEAD' + " " + temp
                        
                     if resu.__contains__('BSPAN'):
                        temp = resu.split(" ")[1]
                        resu = 'B SPAN' + " " + temp
                        
                     if resu.__contains__('BCUSP'):
                        temp = resu.split(" ")[1]
                        resu = 'B CUSP' + " " + temp
                        
                     if resu.__contains__('BWRIT'):
                        temp = resu.split(" ")[1]
                        resu = 'B WRIT' + " " + temp
                        
                     for pre in prereqarray:
                        if pre[0].__contains__(resu):
                           if not len(pre) > 1:
                              continue
                           isGood = False
                           for temp in pre[1:]:
                              for course in courselist:
                                 if course.__contains__(temp):
                                    isGood = True
                           if not isGood:
                              break
                     if moveOn and isGood and resu != "":
                        if not resu in result:
                           result[resu] = 1
                        else:
                           result[resu] += 1
                     resu = ""
                  else:
                     tracker += 1  
            
      else:
         if elm.__contains__(" OR "):
            elm = elm.split(" OR ")
            for choice in elm:
               moveOn = True
               for course in courselist:
                  if course == choice:
                     moveOn = False
               isGood = True
               # if resu.__contains__('BACCT'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B ACCT' + " " + temp
                  
               # if resu.__contains__('BBUS'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B BUS' + " " + temp
                  
               # if resu.__contains__('BBECN'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B BECN' + " " + temp
                  
               # if resu.__contains__('BBSKL'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B BSKL' + " " + temp
                  
               # if resu.__contains__('ACMPT'):
               #    temp = resu.split(" ")[1]
               #    resu = 'A CMPT' + " " + temp
                  
               # if resu.__contains__('BEDUC'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B EDUC' + " " + temp
                  
               # if resu.__contains__('BIMD'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B IMD' + " " + temp
                  
               # if resu.__contains__('BHLTH'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B HLTH' + " " + temp
                  
               # if resu.__contains__('BNURS'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B NURS' + " " + temp
                  
               # if resu.__contains__('BBIO'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B BIO' + " " + temp
                  
               # if resu.__contains__('BCHEM'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B CHEM' + " " + temp
                  
               # if resu.__contains__('BCLIM'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B CLIM' + " " + temp
                  
               # if resu.__contains__('BEE'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B EE' + " " + temp
                  
               # if resu.__contains__('BENGR'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B ENGR' + " " + temp
                  
               # if resu.__contains__('BMATH'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B MATH' + " " + temp
                  
               # if resu.__contains__('BME'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B ME' + " " + temp
                  
               # if resu.__contains__('BPHYS'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B PHYS' + " " + temp
                  
               # if resu.__contains__('BASL'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B ASL' + " " + temp
                  
               # if resu.__contains__('BARAB'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B ARAB' + " " + temp
                  
               # if resu.__contains__('BART'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B ART' + " " + temp
                  
               # if resu.__contains__('BARTS'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B ARTS' + " " + temp
                  
               # if resu.__contains__('BCHIN'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B CHIN' + " " + temp
                  
               # if resu.__contains__('BCORE'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B CORE' + " " + temp
                  
               # if resu.__contains__('BDATA'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B DATA' + " " + temp
                  
               # if resu.__contains__('BLEAD'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B LEAD' + " " + temp
                  
               # if resu.__contains__('BSPAN'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B SPAN' + " " + temp
                  
               # if resu.__contains__('BCUSP'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B CUSP' + " " + temp
                  
               # if resu.__contains__('BWRIT'):
               #    temp = resu.split(" ")[1]
               #    resu = 'B WRIT' + " " + temp
               for pre in prereqarray:
                  
                  if pre[0].__contains__(choice):
                     if not len(pre) > 1:
                        continue
                     isGood = False
                     for temp in pre[1:]:
                        for course in courselist:
                           if course.__contains__(temp):
                              isGood = True
                     if not isGood:
                        break
               if moveOn and isGood:
                  if not choice in result:
                     result[choice] = 5
                  else:
                     result[choice] += 5
         else:
            moveOn = True
            for course in courselist:
               if course == elm:
                  moveOn = False
            isGood = True
            # if resu.__contains__('BACCT'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B ACCT' + " " + temp
               
            # if resu.__contains__('BBUS'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B BUS' + " " + temp
               
            # if resu.__contains__('BBECN'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B BECN' + " " + temp
               
            # if resu.__contains__('BBSKL'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B BSKL' + " " + temp
               
            # if resu.__contains__('ACMPT'):
            #    temp = resu.split(" ")[1]
            #    resu = 'A CMPT' + " " + temp
               
            # if resu.__contains__('BEDUC'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B EDUC' + " " + temp
               
            # if resu.__contains__('BIMD'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B IMD' + " " + temp
               
            # if resu.__contains__('BHLTH'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B HLTH' + " " + temp
               
            # if resu.__contains__('BNURS'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B NURS' + " " + temp
               
            # if resu.__contains__('BBIO'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B BIO' + " " + temp
               
            # if resu.__contains__('BCHEM'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B CHEM' + " " + temp
               
            # if resu.__contains__('BCLIM'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B CLIM' + " " + temp
               
            # if resu.__contains__('BEE'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B EE' + " " + temp
               
            # if resu.__contains__('BENGR'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B ENGR' + " " + temp
               
            # if resu.__contains__('BMATH'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B MATH' + " " + temp
               
            # if resu.__contains__('BME'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B ME' + " " + temp
               
            # if resu.__contains__('BPHYS'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B PHYS' + " " + temp
               
            # if resu.__contains__('BASL'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B ASL' + " " + temp
               
            # if resu.__contains__('BARAB'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B ARAB' + " " + temp
               
            # if resu.__contains__('BART'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B ART' + " " + temp
               
            # if resu.__contains__('BARTS'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B ARTS' + " " + temp
               
            # if resu.__contains__('BCHIN'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B CHIN' + " " + temp
               
            # if resu.__contains__('BCORE'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B CORE' + " " + temp
               
            # if resu.__contains__('BDATA'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B DATA' + " " + temp
               
            # if resu.__contains__('BLEAD'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B LEAD' + " " + temp
               
            # if resu.__contains__('BSPAN'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B SPAN' + " " + temp
               
            # if resu.__contains__('BCUSP'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B CUSP' + " " + temp
               
            # if resu.__contains__('BWRIT'):
            #    temp = resu.split(" ")[1]
            #    resu = 'B WRIT' + " " + temp
            for pre in prereqarray:
               if pre[0].__contains__(elm):
                  print('before ' + elm)
                  print(pre)
                  if not len(pre) > 1:
                     print('1st')
                     continue
                  if str(pre[1]) == 'None':
                     print('2nd')
                     continue
                  print('after ' + elm)
                  isGood = False
                  for temp in pre[1:]:
                     for course in courselist:
                        if course.__contains__(temp):
                           isGood = True
                  if not isGood:
                     break
            print('3rd')
            if moveOn and isGood:
               print('4th')
               if not elm in result:
                  print('5th')
                  result[elm] = 5
               else:
                  print('6th')
                  result[elm] += 5
   print(result)
   for res in result.copy():
      if res.__contains__('BACCT'):
         temp = res.split(" ")[1]
         result['B ACCT' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BBUS'):
         temp = res.split(" ")[1]
         result['B BUS' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BBECN'):
         temp = res.split(" ")[1]
         result['B BECN' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BBSKL'):
         temp = res.split(" ")[1]
         result['B BSKL' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('ACMPT'):
         temp = res.split(" ")[1]
         result['A CMPT' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BEDUC'):
         temp = res.split(" ")[1]
         result['B EDUC' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BIMD'):
         temp = res.split(" ")[1]
         result['B IMD' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BHLTH'):
         temp = res.split(" ")[1]
         result['B HLTH' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BNURS'):
         temp = res.split(" ")[1]
         result['B NURS' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BBIO'):
         temp = res.split(" ")[1]
         result['B BIO' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BCHEM'):
         temp = res.split(" ")[1]
         result['B CHEM' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BCLIM'):
         temp = res.split(" ")[1]
         result['B CLIM' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BEE'):
         temp = res.split(" ")[1]
         result['B EE' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BENGR'):
         temp = res.split(" ")[1]
         result['B ENGR' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BMATH'):
         temp = res.split(" ")[1]
         result['B MATH' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BME'):
         temp = res.split(" ")[1]
         result['B ME' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BPHYS'):
         temp = res.split(" ")[1]
         result['B PHYS' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BASL'):
         temp = res.split(" ")[1]
         result['B ASL' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BARAB'):
         temp = res.split(" ")[1]
         result['B ARAB' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BART'):
         temp = res.split(" ")[1]
         result['B ART' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BARTS'):
         temp = res.split(" ")[1]
         result['B ARTS' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BCHIN'):
         temp = res.split(" ")[1]
         result['B CHIN' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BCORE'):
         temp = res.split(" ")[1]
         result['B CORE' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BDATA'):
         temp = res.split(" ")[1]
         result['B DATA' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BLEAD'):
         temp = res.split(" ")[1]
         result['B LEAD' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BSPAN'):
         temp = res.split(" ")[1]
         result['B SPAN' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BCUSP'):
         temp = res.split(" ")[1]
         result['B CUSP' + " " + temp] = result[res]
         del result[res]
      if res.__contains__('BWRIT'):
         temp = res.split(" ")[1]
         result['B WRIT' + " " + temp] = result[res]
         del result[res]
         
   precursor.execute('''
   SELECT Courses.CourseName, Quarter, Section, Days, InPerson, EducationRequirement, Cirriculum, Time, Size, ProfessorName, sln, Credits, Description, url FROM Courses
   JOIN CourseProfessor
   ON CourseProfessor.CourseName = Courses.CourseName
   WHERE Courses.CampusName='Bothell'
   AND Quarter=?
   ''',
   (quarter))   
   for elem in precursor:
      print(elem[0])
      for res in result.copy():
         if elem[0].__contains__(res):
            tempres = []
            count = 0
            tempres.append(elem[0])
            tempres.append(elem[1])
            tempres.append(elem[2])
            tempres.append(elem[3])
            for day in days:
               if elem[3].__contains__(day):
                  count += 2
                  print("+2")
            tempres.append(elem[4])
            if inperson == "in-person":
               if elem[4] == True:
                  count += 1
                  print("+1")
            if online == "online":
               if elem[4] == False:
                  count += 4
                  print("+4")
            tempres.append(elem[5])
            if not elem[5] == "None":
               for edu in education:
                  for el in elem[5].split(','):
                     if el.split('(')[1].split(')')[0] == edu:
                        count += 3
                        print("+3")
            tempres.append(elem[6])
            print('made here')
            for curc in curriculum:
               if elem[6] == curc:
                  count += 5
                  print("+5")
            tempres.append(elem[7])
            if not elem[7] == "Async":
               temptime = elem[7].replace(':', '')
               if time.split(',')[0] <= temptime.split('-')[0] <= time.split(',')[1] or time.split(',')[0] <= temptime.split('-')[1] <= time.split(',')[1]:
                  count += 3
                  print("+3")
            tempres.append(elem[8])
            if size.split(',')[0] <= elem[8].split(':')[1] <= size.split(',')[1]:
               count += 2
               print("+2")
            tempres.append(elem[9])
            tempres.append(elem[10])
            tempres.append(elem[11])
            if elem[12].__contains__("Co-requisite:"):
               elem[12] = elem[12].split("Co-requisite:")[0]
            tempres.append(elem[12])
            tempres.append(elem[13])
            tempres.append(result[res] + count)
            print(tempres)
            newres.append(tempres)
   # except Exception as e:
   #    print(e)
   result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
   print(result)
   newres.sort(key=lambda x:x[14], reverse=True)
   print(newres)
   if major != "choose" and len(newres) != 0:
       print('Request for results page received with major=%s' % major)
       return render_template('results.html', major = major, departments = departments, courses = courses, quarter = quarter, days = days, inperson = inperson, online = online, education = education, curriculum = curriculum, time = time, size = size
      , coursename1 = newres[0][0], section1 = newres[0][2], professor1 = newres[0][9], days1 = newres[0][3], time1 = newres[0][7], credits1 = newres[0][11], inperson1 = newres[0][4], description1 = newres[0][12], url1 = newres[0][13], sln1 = newres[0][10]
      , coursename2 = newres[1][0], section2 = newres[1][2], professor2 = newres[1][9], days2 = newres[1][3], time2 = newres[1][7], credits2 = newres[1][11], inperson2 = newres[1][4], description2 = newres[1][12], url2 = newres[1][13], sln2 = newres[1][10]
      , coursename3 = newres[2][0], section3 = newres[2][2], professor3 = newres[2][9], days3 = newres[2][3], time3 = newres[2][7], credits3 = newres[2][11], inperson3 = newres[2][4], description3 = newres[2][12], url3 = newres[2][13], sln3 = newres[2][10]
      , coursename4 = newres[3][0], section4 = newres[3][2], professor4 = newres[3][9], days4 = newres[3][3], time4 = newres[3][7], credits4 = newres[3][11], inperson4 = newres[3][4], description4 = newres[3][12], url4 = newres[3][13], sln4 = newres[3][10]
      , coursename5 = newres[4][0], section5 = newres[4][2], professor5 = newres[4][9], days5 = newres[4][3], time5 = newres[4][7], credits5 = newres[4][11], inperson5 = newres[4][4], description5 = newres[4][12], url5 = newres[4][13], sln5 = newres[4][10]
      , coursename6 = newres[5][0], section6 = newres[5][2], professor6 = newres[5][9], days6 = newres[5][3], time6 = newres[5][7], credits6 = newres[5][11], inperson6 = newres[5][4], description6 = newres[5][12], url6 = newres[5][13], sln6 = newres[5][10]
      , coursename7 = newres[6][0], section7 = newres[6][2], professor7 = newres[6][9], days7 = newres[6][3], time7 = newres[6][7], credits7 = newres[6][11], inperson7 = newres[6][4], description7 = newres[6][12], url7 = newres[6][13], sln7 = newres[6][10]
      , coursename8 = newres[7][0], section8 = newres[7][2], professor8 = newres[7][9], days8 = newres[7][3], time8 = newres[7][7], credits8 = newres[7][11], inperson8 = newres[7][4], description8 = newres[7][12], url8 = newres[7][13], sln8 = newres[7][10]
      , coursename9 = newres[8][0], section9 = newres[8][2], professor9 = newres[8][9], days9 = newres[8][3], time9 = newres[8][7], credits9 = newres[8][11], inperson9 = newres[8][4], description9 = newres[8][12], url9 = newres[8][13], sln9 = newres[8][10]
      , coursename10 = newres[9][0], section10 = newres[9][2], professor10 = newres[9][9], days10 = newres[9][3], time10 = newres[9][7], credits10 = newres[9][11], inperson10 = newres[9][4], description10 = newres[9][12], url10 = newres[9][13], sln10 = newres[9][10]
      )
   else:
       print('Request for results page received with no major -- redirecting')
       return redirect(url_for('index'))


@app.route('/courseSelection', methods=['POST'])
def selection():
   jsdata = request.data
   jsdata = jsdata.decode('utf-8')
   jsdata = jsdata.split(",")[1:]

   result = '{}'
   for dep in jsdata:
      dep = dep.replace(" ", "")
      
      try:
         cursor.execute('''
                        SELECT CourseName FROM Courses
                        WHERE Department=? 
                        ''',
                        (dep))

         for row in cursor:
            for elm in row:
               loader = {elm:elm}
               jsonline = json.loads(result)
               jsonline.update(loader)
               result = jsonline
               result = json.dumps(result)
            
      except Exception as e:
         print(e)
   return result


@app.route('/bdepartmentload', methods=['GET'])
def bdepartmentload():
   departmentResponse = requests.get("https://www.washington.edu/students/crscatb/")
   text = departmentResponse.text
   text = text.split('<h2 id="B">School of Business</h2>')[1]
   departmentResult = '{}'
   for line in text.splitlines():
      if line.__contains__("("):
         line = line.split("(")
         if len(line) == 2:
            line = line[1]
         if len(line) == 3:
            line = line[2]
         if len(line) == 4:
            line = line[3]
         line = line.split(")")[0]
         line = line.replace("&amp;", "&")
         line = line.replace("&nbsp;", " ")
         if line.isupper():
            loader = {line:line}
            jsonline = json.loads(departmentResult)
            jsonline.update(loader)
            departmentResult = jsonline
            departmentResult = json.dumps(departmentResult)
   return departmentResult


@app.route('/bcurriculumload', methods=['GET'])
def bcurriculumload():
   result = '{}'
   try:
      cursor.execute('''
                     SELECT DISTINCT Cirriculum
                     FROM Courses
                     WHERE CampusName = 'Bothell'
                     '''
      )
      for row in cursor:
         for elm in row:
            loader = {elm:elm}
            jsonline = json.loads(result)
            jsonline.update(loader)
            result = jsonline
            result = json.dumps(result)
            
   except Exception as e:
      print(e)
   return result


@app.route('/load', methods=['POST'])
def load():
   reached = False
   result = '{}'
   departmentResponse = requests.get("https://www.washington.edu/students/crscatb/")
   text = departmentResponse.text
   text = text.split('<h2 id="B">School of Business</h2>')[1]
   departmentResult = []
   for line in text.splitlines():
      if line.__contains__("("):
         line = line.split("(")
         if len(line) == 2:
            line = line[1]
         if len(line) == 3:
            line = line[2]
         if len(line) == 4:
            line = line[3]
         line = line.split(")")[0]
         line = line.replace("&amp;", "&")
         line = line.replace("&nbsp;", " ")
         if line.isupper():
            departmentResult.append(line.lower())
   print(departmentResult)
   url = "https://www.washington.edu/students/crscatb/"
   for key in departmentResult:
      key = key.replace(" ", "")
      if key == "sasia":
         key = "sasian"
      if key == "csss":
         key = 'cs%26ss'
      if key == "hsteu":
         key = "modeuro"
      if key == "urbdp":
         key = 'urbdes'
      if key == "nmes":
         key = "nearmide"
      if key == "hserv":
         key = "hlthsvcs"
      if key == "as":
         key = "aerosci"
      if key == "msci":
         key = "milsci"
      if key == "nsci":
         key = "navsci"
      if key == "socwf":
         key = "socwlbasw"
      if key == "socw":
         key = "socwk"
      if key == "honors":
         key = "hnrs"

      newResponse = requests.get(url + key + ".html")
      print(url + key + ".html")
      if key == 'stem':
         continue
      text = newResponse.text
      text = text.split("<p>Detailed course offerings (Time Schedule) are available for")[1]
      text = text.split('<div id="footer">')[0]
      text = text.split('</ul></p>')[1]
      for line in text.splitlines():
         if line.__contains__("<a name"):
            line = line.split("<p><b>")[1]
            line = line.split("(")[0]
            line = line.split(" ")
            if line[1].isdigit():
               department = line[0]
               courseNumber = line[1]
               line = line[0] + line[1]
            else:
               department = line[0] + line[1]
               courseNumber = line[2]
               line = line[0] + line[1] + line[2]
            line = line.upper()
            key = key.upper()
            if key == 'BBIO':
               reached = True
            if True:
               courseURL = "http://myplan.uw.edu/course/#/courses/" + line
               print(courseURL)
               
               # try:
               #    loadcursor.execute('''
               #          UPDATE Courses
               #          SET url = ?
               #          WHERE Department = ?
               #          AND CourseNumber = ?;
               #          ''',
               #          (courseURL, department, courseNumber))
               #    loadcnxn.commit()
               # except Exception as e:
               #    print(e)
               browser = webdriver.Firefox()
               browser.implicitly_wait(5)
               browser.get(courseURL)
               checkpage = browser.page_source
               i = 0
               nogood = False
               while not checkpage.__contains__('<dl class="row mt-3">'):
                  time.sleep(1)
                  i += 1
                  if i == 20:
                     nogood = True
                     break
                  checkpage = browser.page_source
               time.sleep(1)
               if nogood:
                  continue
               page = browser.page_source
               browser.close()
               courseName = page.split("<h1>")[1].split("(")[0]
               # print(courseName)
               # extraName = courseName.split(" ")
               # if extraName[1].isdigit():
               #    department = extraName[0]
               #    courseNumber = extraName[1]
               # else:
               #    department = extraName[0] + extraName[1]
               #    courseNumber = extraName[2]
               # print(department)
               # print(courseNumber)
               page = page.split("<h2>Course Overview</h2>")[1]
               if page.__contains__('Offered Jointly With'):
                  inc = 1
               else:
                  inc = 0
               if page.__contains__('Recommended Prep'):
                  inct = 1
               else:
                  inct = 0
               courseData = page.split("Course Sections</h2>")[0]
               courseData = courseData.split("<dd")
               # description = courseData[1].split("<p>")[1]
               # description = description.split("</p>")[0]
               # print(description)
               prearray = [[0 for m in range(10)] for l in range(10)]
               prerequisites = courseData[2+inc].split('mb-3">')[1].split("</dd>")[0]
               if prerequisites != "None":
                  if prerequisites.__contains__('<button type="button" class="btn btn-link">'):
                     prerequisites = prerequisites.split('<button type="button" class="btn btn-link">')
                     if len(prerequisites) == 2:
                        prearray[0][0] = prerequisites[1].split('</button>')[0]
                     else:
                        orswitch = False
                        commanum = 0
                        startcomma = -1
                        for i in range(0, len(prerequisites) - 2):
                           if prerequisites[i+1].split('<span')[0].__contains__(';') or prerequisites[i+1].split('<span')[0].__contains__('and'):
                              if orswitch:
                                 orswitch = False
                              else:
                                 prearray[i][0] = prerequisites[i+1].split('<')[0]
                              prearray[i+1][0] = prerequisites[i+2].split('<')[0]
                           elif prerequisites[i+1].split('<span')[0].__contains__('or'):
                              if commanum > 0:
                                 prearray[startcomma][commanum] = prerequisites[i+1].split('<')[0]
                                 prearray[startcomma][commanum+1] = prerequisites[i+2].split('<')[0]
                                 commanum = 0
                                 startcomma = -1
                                 orswitch = True
                              else:
                                 if orswitch:
                                    orswitch = False
                                 else:
                                    prearray[i][0] = prerequisites[i+1].split('<')[0]
                                 prearray[i][1] = prerequisites[i+2].split('<')[0]
                                 orswitch = True
                           else:
                              if startcomma == -1:
                                 startcomma = i
                              prearray[startcomma][commanum] = prerequisites[i+1].split('<')[0]
                              commanum += 1
                     for elem in prearray:
                        count = 0
                        number = 0
                        elements = courseName
                        for ol in elem:
                           if ol != 0:
                              number += 1
                        if number != 0:
                           SQL = "INSERT INTO [dbo].[Prerequisite] (CourseName, Prerequisite"
                           for i in range(0, number):
                              if count != 0:
                                 SQL += ",AltCourse" + str(count)
                              count += 1
                           SQL += ") VALUES (?,?"
                           count = 0
                           for ol in elem:
                              if ol != 0:
                                 elements += "," + ol
                                 if count != 0:
                                    SQL += ",?"
                                 count += 1
                           SQL += ")"
                           elements += ""
                           print(SQL)
                           print(elements)
                        
                           try:
                              cursor.execute(SQL, *elements.split(','))
                              cnxn.commit()
                           except Exception as e:
                              print(e)
                  else:
                     prerequisites = "None"
                     try:
                        cursor.execute('''
                              INSERT INTO [dbo].[Prerequisite] (CourseName, Prerequisite)
                              VALUES (?, ?);
                              ''',
                              (courseName, "None"))
                        cnxn.commit()
                     except Exception as e:
                        print(e)
               
                     
               else:
                  try:
                     cursor.execute('''
                           INSERT INTO [dbo].[Prerequisite] (CourseName, Prerequisite)
                           VALUES (?, ?);
                           ''',
                           (courseName, "None"))
                     cnxn.commit()
                  except Exception as e:
                     print(e)
               # requirements = courseData[4+inc+inct]
               # requirements = requirements.split('mb-3">')[1].split("</dd>")[0]
               # if requirements != "None":
               #    requirements = requirements.split("<p>")[1].split("</p>")[0]
               # if requirements.__contains__("&amp;"):
               #    requirements = requirements.replace("&amp;", "&")
               # print(requirements)
               # curriculum = courseData[5+inc+inct].split(">")[1].split(", <")[0]
               # if curriculum.__contains__("&amp;"):
               #    curriculum = curriculum.replace("&amp;", "&")
               # print(curriculum)
               # try:
               #    cursor.execute('''
               #          INSERT INTO [dbo].[Courses] (Department, CampusName, CourseNumber, CourseName, EducationRequirement, Cirriculum, Description)
               #          VALUES (?, ?, ?, ?, ?, ?, ?);
               #          ''',
               #          (department, 'Bothell', courseNumber, courseName, requirements, curriculum, description))
               #    cnxn.commit()
               # except Exception as e:
               #    print(e)
               # if page.__contains__("Course Sections</h2>"):
               #    profData = page.split("Course Sections</h2>")[1]
               #    profData = profData.split('<div class="card border-transparent">')
               #    profData = profData[1:]
               #    h = 0
               #    for key in profData:
               #       print("prof")
               #       # print(profData[h])
               #       quarter = key.split(">")[2].split("<")[0]
               #       print(quarter)
               #       sectionSplit = key.split("<tbody")[1:]
               #       r = 0
               #       for nkey in sectionSplit:
               #          print("newSection")
               #          nkey = nkey.split("<tr>")[1]
               #          nkey = nkey.split("<td>")
               #          section = nkey[1].split('<span class="code')[1].split("</span>")[0].split(">")[1]
               #          print(section)
               #          type = nkey[2].split('<span class="text-capitalize">')[1].split("</span>")[0]
               #          if type.__contains__('('):
               #             type = type.split('(')[0]
               #          print(type)
               #          if nkey[2].split('<span class="text-capitalize">')[1].split("</span>")[0].__contains__('('):
               #             credits = nkey[2].split("(")[1].split("<")[0]
               #          else:
               #             credits = 0
               #          print(credits)
               #          inPerson = nkey[3].split('<div class="my-2 my-sm-0">')[1].split("</div>")[0]
               #          print(inPerson)
               #          if inPerson == "In-person" or inPerson == "Hybrid":
               #             inPerson = True
               #          else:
               #             inPerson = False
               #          print(inPerson)
               #          if nkey[3].__contains__("To be arranged"):
               #             days = "To be arranged"
               #          else:
               #             days = nkey[3].split('<div class="d-inline-block me-2 me-sm-0"><span aria-label="')[1].split('"')[0]
               #          print(days)
               #          if nkey[3].__contains__("time"):
               #             classTime = nkey[3].split('<time datetime="')[1].split('"')[0] + "-" + nkey[3].split('<time datetime="')[2].split('"')[0]
               #          else:
               #             classTime = 'Async'
               #          print(classTime)
               #          if nkey[4].__contains__("div"):
               #             if nkey[4].__contains__('<li>'):
               #                professor = nkey[4].split('<li>')[1].split('</li>')[0] + ", " + nkey[4].split('<li>')[2].split('</li>')[0]
               #             else:
               #                professor = nkey[4].split('<div class="mb-1">')[1].split('<')[0]
               #          else:
               #             professor = 'TBD'
               #          print(professor)
               #          sln = nkey[5].split('</span>')[1].split("<")[0]
               #          print(sln)
               #          if not nkey[6].__contains__("suspended"):
               #             size = nkey[6].split('<small class="d-block">')[1].split(' <')[0] + ':' + nkey[6].split('</abbr> of ')[1].split('<')[0]
               #          else:
               #             size = 'suspended'
               #          print(size)
               #          try:
               #             cursor.execute('''
               #                   INSERT INTO [dbo].[CourseProfessor] (ProfessorName, CampusName, Quarter, CourseName, Section, Time, Days, InPerson, Size, Type, Credits, sln)
               #                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
               #                   ''',
               #                   (professor, 'Bothell', quarter, courseName, section, classTime, days, inPerson, size, type, credits, sln))
               #             cnxn.commit()
               #          except Exception as e:
               #             print(e)
               #       h += 1
            
      

   result = '{}'
   departmentResponse = requests.get("https://www.washington.edu/students/crscatb/")
   text = departmentResponse.text
   text = text.split('<h2 id="B">School of Business</h2>')[1]
   departmentResult = '{}'
   for line in text.splitlines():
      if line.__contains__("("):
         line = line.split("(")
         if len(line) == 2:
            line = line[1]
         if len(line) == 3:
            line = line[2]
         if len(line) == 4:
            line = line[3]
         line = line.split(")")[0]
         line = line.replace("&amp;", "&")
         line = line.replace("&nbsp;", " ")
         if line.isupper():
            loader = {line:line}
            jsonline = json.loads(departmentResult)
            jsonline.update(loader)
            departmentResult = jsonline
            departmentResult = json.dumps(departmentResult)
   print(departmentResult)
   
   result = '{}'
   departmentResponse = requests.get("https://www.washington.edu/students/crscatt/")
   text = departmentResponse.text
   text = text.split('<h2 id="B">Business Administration</h2>')[1]
   departmentResult = '{}'
   for line in text.splitlines():
      if line.__contains__("("):
         line = line.split("(")
         if len(line) == 2:
            line = line[1]
         if len(line) == 3:
            line = line[2]
         if len(line) == 4:
            line = line[3]
         line = line.split(")")[0]
         line = line.replace("&amp;", "&")
         line = line.replace("&nbsp;", " ")
         if line.isupper():
            loader = {line:line}
            jsonline = json.loads(departmentResult)
            jsonline.update(loader)
            departmentResult = jsonline
            departmentResult = json.dumps(departmentResult)
   print(departmentResult)
   return render_template('load.html')

if __name__ == '__main__':
   app.run()