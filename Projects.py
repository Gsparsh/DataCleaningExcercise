

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

#=====Read File
df=pd.read_csv(r'D:\Data Analysis\Sparsh\City_Service_Requests_in_2018.csv', header=0, sep=',')
file=open(r'Report.txt','w')
file.write('Report \n')
#checking for NA/NULL values
for i in df.columns:
    x=df[i].isna().all()
    z=str(['The column ',i, 'has null values:', x])
    print('The column ',i, 'has null values:', x)
    file.write(z)
    




#======var
labels=[]
numbers=[]
Add=pd.to_datetime(df['ADDDATE'])
Res=pd.to_datetime(df['RESOLUTIONDATE'])
Due=pd.to_datetime(df['SERVICEDUEDATE'])
Order=pd.to_datetime(df['SERVICEORDERDATE'])

df2=df
Lag=(Res-Due)
TFR=(Res-Order)

for i in range(len(Lag)):
    Lag[i]=Lag[i].days
for i in range(len(TFR)):
    TFR[i]=TFR[i].days

df2['TFR']=TFR
df2['Lag']=Lag
important=[]

#=====Start Report


for i in df.columns:
    x=str(['There are ',len(df[i].unique()), ' unique values in ', i])
    print('There are ',len(df[i].unique()), ' unique values in ', i)
    file.write(x)
    if(len(df[i].unique())<110):
        important.append(i)
 
print('Most Important Labels are: ')       
for i in important:
    file.write(i)

print()        
#====


#=====PIE CHART for # of request
luR=np.zeros((len(df['SERVICETYPECODEDESCRIPTION'].unique()),1))
counter=0
x=list(df['SERVICETYPECODEDESCRIPTION'])
y=df['SERVICETYPECODEDESCRIPTION'].unique()
for i in y:
    luR[counter]=x.count(i)
    counter=counter+1
sumn=0
for i in range(len(luR)):
    if(luR[i]>9000):
        labels.append(y[i])
        numbers.append(luR[i])
        sumn=sumn+int(luR[i])
        
labels.append('others')
numbers.append(len(df['SERVICETYPECODEDESCRIPTION'])-sumn)        
        
plt.pie(numbers, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.show() 
plt.savefig('SERVICES.png')
labels.clear()
numbers.clear()     

#===
orgs=df['ORGANIZATIONACRONYM'].unique()
orgImp=[]
oth=[]
imporgnum=[]
orgCNT=np.zeros((len(orgs),1))
for i in range(len(orgs)):
    orgCNT[i]=df[df['ORGANIZATIONACRONYM']==orgs[i]].count()['ORGANIZATIONACRONYM']

sumo=0        
for i in range(len(orgs)):
    if(orgCNT[i]>5000):
        orgImp.append(orgs[i])
        imporgnum.append(orgCNT[i])
        sumo=sumo+orgCNT[i]
    else:
        oth.append(orgs[i])

        
imporgnum.append((len(df['ORGANIZATIONACRONYM'])-sumo))
orgImp.append('Others')        
    
plt.pie(imporgnum, labels=orgImp,autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.show()    
plt.savefig('Organizations.png')


#============

sumlag=Lag.sum()
avgLag=sumlag/len(TFR)
sumTFR=TFR.sum()
avgTFR=sumTFR/len(TFR)

print('Average Time for Resolution:', avgTFR)
print('Average Lag Time (Diff from Due Date and Res Date)', avgLag, ' ,means that tickets were solved before due date')
x=str(['Average Time for Resolution:', avgTFR])
file.write(x)
x=str(['Average Lag Time (Diff from Due Date and Res Date)', avgLag, ' ,means that tickets were solved before due date'])
file.write(x)
#=======
#Priority Tickets
priority=df['PRIORITY'].unique()
cntPriority=np.zeros((len(priority),1))
for i in range(len(priority)):
    cntPriority[i]=df[df['PRIORITY']==priority[i]].count()['PRIORITY']
    
plt.pie(cntPriority, labels=priority,autopct='%1.1f%%')
plt.axis('equal')
plt.show()
plt.savefig('Priority.png')    
    
#=======
wards=df2['WARD'].unique()
WCNT=np.zeros((len(wards),1))
for i in range(len(wards)):
    WCNT[i]=df2[df2['WARD']==wards[i]].count()['WARD']

for i in range(len(WCNT)):
    WCNT[i]=100*(WCNT[i]/len(df2['WARD']))
    x=str(['Percent of requests for Ward', wards[i], ' is ',WCNT[i]])
    file.write(x)    
    
file.close()

