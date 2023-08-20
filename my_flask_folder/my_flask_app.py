# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 12:16:58 2023

@author: Shankhadeep Purkait
"""

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
def calculate_mark(df, correct, wrong, category1):
    df=df.loc[:,['Correct Option(s)','Recorded Response']]
    df['Mark']=''
    for i in range(0,len(df)):
        if i==category1:
            break
        if df.iloc[i,0]==df.iloc[i,1]:
            df.iloc[i,2]=correct
        elif df.iloc[i,0]=="-" or df.iloc[i,1]=="-":
            df.iloc[i,2]=0
        else:
            df.iloc[i,2]=wrong
    
    for i in range(category1,len(df)):
        if df.iloc[i,0]==df.iloc[i,1]:
            df.iloc[i,2]=2
        elif df.iloc[i,0]=="-" or df.iloc[i,1]=="-":
            df.iloc[i,2]=0
        elif df.iloc[i,0]!=df.iloc[i,1]:
            if len(df.iloc[i,0])<len(df.iloc[i,1]):
                df.iloc[i,2]=0
            else:
                count=0
                x=df.iloc[i,0].split(',')
                y=df.iloc[i,1].split(',')
                for j in range(0,len(x)):
                  for k in range(0,len(y)):
                      try:
                          if x[j]==y[k]:
                              count+=1
                          else:
                              count=0
                              break
                      except IndexError:
                              pass
                cal=(2*count)/len(x)
                df.iloc[i,2]=cal
    x = df['Mark'].sum()
    df.at[len(df),'Recorded Response']='Sum:'+str(x)
    df.iloc[len(df)-1,0]="****"
    df.iloc[len(df)-1,2]="****"
    return x, df

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csv = request.files['file']
        print(csv)
        correct = float(request.form['correct'])
        wrong = float(request.form['wrong'])
        category1 = int(request.form['category1'])
        
        # You may need to adjust this part based on how you're planning to get the CSV file input
        # For simplicity, I'm assuming you'll get the CSV file from a form field named 'csv_file'
        #csv_file = request.files[csv]
        df = pd.read_csv(csv)
        
        x, df = calculate_mark(df, correct, wrong, category1)
        df.to_csv('result.csv', index=False)
        
        return render_template('result.html', mark=x, result_df=df.to_html())
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
