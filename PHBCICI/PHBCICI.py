#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:29:33 2018
FYI: This project was done using Python 3.6.*
The Solution we are trying to solve can be found on the .pdf file

@author: Anani Assoutovi
"""

# You first must download the modules/lybraries used below otherwise you will have compiler errors.
import sqlite3 as sq, csv, numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics
#from sklearn import svm
import Model as md

## Creating and connecting to the Database
db = sq.connect('species.db')
cursor = db.cursor()

### Creating the 'Boran', 'Radan', and 'Deidentify' tables with Contrainsts
queryBoran = """
CREATE TABLE IF NOT EXISTS boran (
    patient_id INTEGER NOT NULL UNIQUE,
    blood_pressure REAL,
    exercise REAL NOT NULL,
    weight REAL NOT NULL,
    glucose REAL NOT NULL,
    bmi REAL NOT NULL,
    planet_id INTEGER NOT NULL,
    PRIMARY KEY(patient_id)
)
"""
cursor.execute(queryBoran)

queryRadan = """
CREATE TABLE IF NOT EXISTS radan (
    patient_id INTEGER NOT NULL UNIQUE,
    blood_pressure REAL,
    exercise REAL NOT NULL,
    weight REAL NOT NULL,
    glucose REAL NOT NULL,
    bmi REAL NOT NULL,
    planet_id INTEGER NOT NULL,
    PRIMARY KEY(patient_id)
)
"""
cursor.execute(queryRadan)

queryDeidentify = """
CREATE TABLE IF NOT EXISTS deidentify (
    patient_id INTEGER NOT NULL UNIQUE,
    age REAL NOT NULL
    CONSTRAINT patient_id REFERENCES boran(patient_id) ON DELETE RESTRICT ON UPDATE CASCADE
    CONSTRAINT patient_id REFERENCES radan(patient_id) ON DELETE RESTRICT ON UPDATE CASCADE
)
"""
cursor.execute(queryDeidentify)
db.commit()


## Loading the files and storing them in the TABLES
## Creating a method to make the code more object oriented, So we don't stress memory out
def uploadCsvToTable(fileName, statement):
    with open('{0}'.format(fileName)) as asFile:
        species = csv.reader(asFile)
        records = [rec for rec in species]
    # We need to exclude the first row since it's not part of the observation
    cursor.executemany('{0}'.format(statement), records[1:]) 
    db.commit()


# In Sqlite, the (?.?.*.*) indicates the number of columns associated with the table
# In this case, we have 7 columns
    ## BORAN
uploadCsvToTable('boran.csv', 'INSERT INTO boran VALUES (?, ?, ?, ?, ?, ?, ?)')

    ## RADAN
uploadCsvToTable('radan.csv', 'INSERT INTO radan VALUES (?, ?, ?, ?, ?, ?, ?)')
    
    ## DEIDENTIFY has 2 columns which are critical for our analysis
uploadCsvToTable('deidentify_list_cross_ref.csv', 'INSERT INTO deidentify VALUES (?, ?)')

### Creating a method to handle the Query Statements for all tables - saves us memory (lots)

def selectQuery(table):
    query = """{0}""".format(table)
    for rec in cursor.execute(query).fetchall():
        print(rec)
     
boranQuery = """
SELECT * FROM boran
"""
selectQuery(boranQuery)

radanQuery = """
SELECT * FROM radan
"""
selectQuery(radanQuery)

query = """
SELECT * FROM deidentify
"""
selectQuery(query)


###############################################################################
#strQuery = """
#SELECT * FROM %s
#"""
#model = md.model
#model.selectQuery(strQuery+str("boran"))
#
#radanQuery = """
#SELECT * FROM radan
#"""
#selectQuery(radanQuery)
#model.selectQuery(strQuery+str("radan"))
###############################################################################


# Qn. 1 To verify that our table for boran works by restricting duplicate records, 
# we intend to update one of the table. We expect to an error here to be sure. 
# The execution fails because of a Unique constraint.


# We expect an error here since there is contrainst on the page and we are not allowed to update the table
# YOU SHOULD PROBABLY COMMENT OUT THE BELOW 5 LINES OF CODES OTHERWISE YOU WILL GET A FALSE NEGATIVE RESULT WHICH COULD HALT THE COMPILER
query = """
INSERT INTO boran (patient_id,blood_pressure,exercise,weight,glucose,bmi,planet_id) VALUES (5231, 200.65365, 52.81180065, 154.2943899, 172.2315498, 1.755604441, 1)
"""
cursor.execute(query)
db.commit()


# Qn. 2 Creating a method so we can inject the table into it, and do a select 
# statement to retieve 'patient_id', 'blood_pressure', 'age', and right joining 
# it with 'patient_id' from 'deidentify' table.

def sqlArr(table):
    container =[] # This array contains selected values from boran and radan
    query = """
    SELECT a.patient_id, blood_pressure, age FROM %s a JOIN deidentify ON a.patient_id = deidentify.patient_id
    """ % table
    print("############### "+str(table.upper())+" #########################")
    for rec in cursor.execute(query).fetchall():
        container.append(rec)
    return container
    db.commit()
    
sqlArr("boran") ## gives us our joined array for Boran
sqlArr("radan")

# Selecting the 'patient_id', 'blood_pressure', and 'age' and storing them as 
# a Pandas.Dataframe() onto a variables to do analysis (Linear Regression, mean, 
# histogram...).

df_Boran = pd.DataFrame(data=sqlArr("boran"), columns=['PATIENT ID', 'BLOOD PRESSURE', 'AGE'])

# Describing the Dataframe()
df_Boran.describe()

# Getting the mean() of the whole dataframe()
df_Boran.mean()

# 2a. Finding the best linear regression fit for Boran
# Features
x_df_Boran = df_Boran[['BLOOD PRESSURE']]
y_df_Boran = df_Boran['AGE']

modelBoran = LinearRegression()
modelBoran.fit(x_df_Boran, y_df_Boran)

# Predicting the Boran Species
Y_pred_Boran = modelBoran.predict(x_df_Boran)
Y_pred_Boran

print(metrics.mean_squared_error(y_df_Boran, Y_pred_Boran))

# 3. Getting the histogram of the dataframe() - Boran
df_Boran['AGE'].hist()
df_Boran['BLOOD PRESSURE'].hist()
df_Boran['PATIENT ID'].hist()


# 3a. Getting the mean() of the 'AGE' of 'Boran'
print("\nBoran AGE mean...")
df_Boran['AGE'].mean()

# 3b. Probability of creature living past the mean life expectancy age
print("\nPATIENT ID count...")
df_Boran['PATIENT ID'].count()
print("\nBoran AGE mean by observation...")
df_Boran[df_Boran['AGE'] >= df_Boran['AGE'].mean()]

df_Boran[df_Boran['AGE'] >= df_Boran['AGE'].mean()].count()

# Using MatLibPlot to show the graphics
plt.scatter(df_Boran['AGE'], df_Boran['BLOOD PRESSURE'])
plt.xlabel("Average Number of Age with Blood Pressure")
plt.ylabel("Blood Pressure")
plt.title("Relationship between Age and Blood Pressure")
plt.show()


print("\nObversation count from Boran by ...")
15/df_Boran['PATIENT ID'].count()

## ---> Doing analysis on planet Radan <---

# Selecting the 'patient_id', 'blood_pressure', and 'age' and storing them as a 
# Pandas.Dataframe() onto a variables to do analysis (Linear Regression, mean, histogram...)
df_Radan = pd.DataFrame(data=sqlArr("radan"), columns=['PATIENT ID', 'BLOOD PRESSURE', 'AGE'])
df_Radan

# Describing the Dataframe() - Radan
df_Radan.describe()

### Getting the mean of the whole Dataframe()
df_Radan.mean()

## 2a. Finding the best linear regression fit for Radan
# Features
x_df_Radan = df_Radan[['BLOOD PRESSURE']]
y_df_Radan = df_Radan['AGE']

modelRadan = LinearRegression()
modelRadan.fit(x_df_Radan, y_df_Radan)

# Predicting the Radan Species
Y_pred_Radan = modelRadan.predict(x_df_Radan)
Y_pred_Radan

print("Printing the Mean Square Error for the Radan Dataframe()...")
print(metrics.mean_squared_error(x_df_Radan, y_df_Radan))

# 3. Getting the histogram of the dataframe() - RADAN
df_Radan['AGE'].hist()
df_Radan['BLOOD PRESSURE'].hist()

df_Radan['PATIENT ID'].hist()

# Getting the mean() of the 'AGE' of 'Radan'
df_Radan['AGE'].mean()

## 3b. Probability of creature living past the mean life expectancy age
df_Radan['PATIENT ID'].count()


df_Radan[df_Radan['AGE'] >= df_Radan['AGE'].mean()]
df_Radan[df_Radan['AGE'] >= df_Radan['AGE'].mean()].count()

probability = 13/df_Radan['PATIENT ID'].count()
probability


plt.scatter(df_Radan['AGE'], df_Radan['BLOOD PRESSURE'])
plt.xlabel("Average Number of Age with Blood Pressure")
plt.ylabel("Blood Pressure")
plt.title("Relationship between Age and Blood Pressure")
plt.show()














