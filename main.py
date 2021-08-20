from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from bs4 import BeautifulSoup
import requests
import datetime
import math


class CoronaPredictor:
    def __init__(self, root):
        self.root= root
        self.root.title('Corona Predictor App | Developed By Ram | Alpha')
        self.root.geometry('1100x785+200+5')
        self.root.maxsize(1100,795)
        self.root.minsize(1100,795)
        self.root.config(bg='white')

        self.logo_icon= PhotoImage(file='doctor.png')
        self.logo_icon2= PhotoImage(file='2.png')
        self.logo_icon3= PhotoImage(file='coronavirus.png')
        
        Label(self.root, text='CoronaVirus Probability Detector', image=self.logo_icon, compound=LEFT, font=('impact', 40, 'bold'), padx=40, bg='#023548', fg='white', anchor=W).place(x=0 ,y=0, relwidth=1)
        
        # Variables
        self.feverVar=StringVar()
        self.ageVar=StringVar()
        self.bodyPainVar=StringVar()
        self.runnyNoseVar=StringVar()
        self.breathinVar=StringVar()
        # Variables

        # Taking inputs
        frame_for_taking_inputs= Frame(self.root, bd=5, relief=GROOVE)
    
        Label(frame_for_taking_inputs, text='Enter Fever Value', font=('times new roman', 18, 'bold')).place(y=10, x=38)
        Entry(frame_for_taking_inputs, bd=2, relief=GROOVE, width=20, font=('arial 15 bold'), textvariable=self.feverVar).place(x=40, y=42, width= 710)

        Label(frame_for_taking_inputs, text='Enter Age Value', font=('times new roman', 18, 'bold')).place(y=115, x=38)
        Entry(frame_for_taking_inputs, bd=2, relief=GROOVE, width=20, font=('arial 15 bold'), textvariable=self.ageVar).place(x=40, y=150, width= 710)

        Label(frame_for_taking_inputs, text='Body Pain', font=('times new roman', 18, 'bold')).place(y=220, x=38)
        bodyPain= ttk.Combobox(frame_for_taking_inputs, width=18, font=('arial 14 bold'), state='readonly',  textvariable= self.bodyPainVar)
        bodyPain['value']= ('Yes', 'No')
        bodyPain.place(x=41, y=255, width=705)

        Label(frame_for_taking_inputs, text='Runny Nose', font=('times new roman', 18, 'bold')).place(y=335, x=38)
        runnyNose= ttk.Combobox(frame_for_taking_inputs, width=18, font=('arial 14 bold'), state='readonly',  textvariable= self.runnyNoseVar)
        runnyNose['value']= ('Yes', 'No')
        runnyNose.place(x=41, y=370, width=705)

        Label(frame_for_taking_inputs, text='Breathing Difficulty', font=('times new roman', 18, 'bold')).place(y=445, x=38)
        B_Difficulty= ttk.Combobox(frame_for_taking_inputs, width=18, font=('arial 14 bold'), state='readonly',  textvariable= self.breathinVar)
        B_Difficulty['value']= ('No Difficulty', 'Little Difficulty', 'Severe Difficulty')
        B_Difficulty.place(x=41, y=480, width=705)
      
        frame_for_taking_inputs.place(x=10, y=80, height=550, width=800)
        # frame_for_taking_inputs.place(x=10, y=80, height=550, width=1085)
        # Taking inputs


        # coronaData
        
        self.x = datetime.datetime.now()
        self.month= self.x.strftime("%B")
        frame_for_displaying_current_corona_data= Frame(self.root, bd=5, relief=GROOVE)
        Label(frame_for_displaying_current_corona_data, text='Corona Status', font=('lucida', 20, 'bold')).place(x=35, y=20)
        Label(frame_for_displaying_current_corona_data, text='Corona Status', image=self.logo_icon3, compound=LEFT, font=('impact', 20, 'bold'), padx=10, bg='#023548', fg='white', anchor=W).place(x=0 ,y=0, relwidth=1)
        self.CoroDataLabel= Label(frame_for_displaying_current_corona_data, text= f'Live Updates \n({self.month})', font=('times new roman', 18, 'bold'))
        self.CoroDataLabel.place(x=25, y=100)
        frame_for_displaying_current_corona_data.place(x=815, y=80, height=550, width=280)
        # coronaData


        # buttons
        btnFrame= Frame(self.root, bd=5, relief=GROOVE)

        predictBtn=Button(btnFrame, command= self.Predict, text='Predict',  font='arial 17 bold', bd=6, width=12, bg='#607d8b', fg='lightyellow',  activebackground='#607d8b', activeforeground='orange', cursor='hand2').place(x= 220, y=5)
        refreshBtn=Button(btnFrame, command=self.RefreshData, text='Refresh Data', font='arial 17 bold', bd=6, width=12,  bg='#ff5722', fg='lightyellow', activebackground='#ff5722', activeforeground='blue', cursor='hand2').place(x=440, y=5)
        clearBtn=Button(btnFrame, command=self.clearData, text='Clear Data', font='arial 17 bold', bd=6, width=12,  bg='#07ed48', fg='lightyellow', activebackground='#07ed48', activeforeground='orange', cursor='hand2').place(x=660, y=5)

        btnFrame.place(x=10, y=630, height=78, width=1085)
        # buttons


        frame3= Frame(self.root, bd=5, relief=GROOVE)
        self.CoroPredictLabel= Label(frame3, text='Always Keep Social Distancing And Wear Mask !', font=('times new roman', 18, 'bold'), image=self.logo_icon2, compound=LEFT, padx=40, anchor=W, bg='red')
        self.CoroPredictLabel.place(x=0, y=0, relwidth=1)
        frame3.place(x=9, y=715, height=73, width=1085)

    
    # Making Functions
    def data_split(self, data, ratio):
        np.random.seed(42)
        shuffled = np.random.permutation(len(data))
        test_set_size = int(len(data) * ratio)
        test_indices = shuffled[:test_set_size]
        train_indices = shuffled[test_set_size:]
        return data.iloc[train_indices], data.iloc[test_indices]

    def Predict(self):
        # string= self.ageVar.get(), self.feverVar.get(), self.runnyNoseVar.get(), self.bodyPainVar.get(), self.breathinVar.get()
        # print(string)

        # Reading data
        df=pd.read_csv('coronaData.xlsx.csv')
        # df.head()
        # df.tail()
        # df.info()
        # df['diffBreath'].value_counts()
        # df.describe()
        
        # Train and Test Data
        train, test= self.data_split(df, 0.2)
        print(train)
        print(test)
        # quit()
        x_train = train[['fever', 'bpain', 'age','runnyNose','diffBreath']].to_numpy()
        y_train = train[['infectionProb']].to_numpy().reshape(4000, )

        x_test = test[['fever', 'bpain', 'age', 'runnyNose', 'diffBreath']].to_numpy()
        y_test = test[['infectionProb']].to_numpy().reshape(999, )
        
        clf = LogisticRegression()
        clf.fit(x_train, y_train)
        # fever	bpain	age	runnyNose	diffBreath	infectionProb
        
        if self.bodyPainVar.get() == 'Yes':
            bPain= 1
        else:
            bPain= 0

        if self.runnyNoseVar.get() == 'Yes':
            rNose= 1
        else:
            rNose= 0

        if self.breathinVar.get() == 'No': 
            dBreath= (-1)
        elif self.breathinVar.get() == 'Yes': 
            dBreath= 0
        else:
            dBreath=1

        inputFeature = [[int(self.feverVar.get()), bPain,
                        int(self.ageVar.get()), rNose, dBreath]]

        infoProb = clf.predict_proba(inputFeature)[0][1]
        infoProb2= int(infoProb)

        if infoProb2 <= 48:
            self.CoroPredictLabel.config(text=f'Corona Prediction  :  {infoProb*100}', bg='green')
        else:
            self.CoroPredictLabel.config(text=f'Corona Prediction  :  {infoProb*100}')
            


    def RefreshData(self):
        data= self.Get_corona_data()
        string= f'Cases : {data[0]}\nDeaths : {data[1]}\nRecoverd : {data[2]}'
        self.CoroDataLabel.config(text= string)

    def Get_corona_data(self):
        from bs4 import BeautifulSoup
        country_name= 'india'
        url=f'https://www.worldometers.info/coronavirus/country/{country_name}/'
        data2= self.get_url(url)
        soup=BeautifulSoup(data2,'html.parser')
        html_data=soup.findAll('div',class_='content-inner')
        ActualData=[]
        for data in html_data:
            f=data.find_all('div',id='maincounter-wrap')
            for corona_data in f:
                Numerical_value=corona_data.find('span').get_text()
                heading=corona_data.find('h1').get_text()
                ActualData.append(Numerical_value)
                print(len(ActualData), heading)
        return ActualData


    def get_url(self, url):
        data=requests.get(url)
        return data.text

    def clearData(self):
        self.CoroPredictLabel.config(text=f'Always Keep Social Distancing And Wear Mask !', bg='red')
        self.feverVar.set('')
        self.ageVar.set('')
        self.bodyPainVar.set('')
        self.runnyNoseVar.set('')
        self.breathinVar.set('')
    # Making Functions


# Creating object of FileSorting Class
root= Tk()
predictor= CoronaPredictor(root)
root.mainloop()