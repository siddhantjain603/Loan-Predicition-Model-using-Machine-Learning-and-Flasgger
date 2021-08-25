# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 20:27:05 2021

@author: Siddhant Jain
"""
from flask import Flask, request
import numpy as np
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger

app=Flask(__name__)
Swagger(app)

pickle_in = open("loan_prediction.pkl","rb")
classifier=pickle.load(pickle_in)

@app.route('/')
def welcome():
    return "Welcome All"

@app.route('/predict',methods=["POST"])
def predict_loan():
    
    """Let's predict whether the loan will be given or not
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: ApplicantIncome
        in: query
        type: number
        required: true
        description: Income of the applicant
      - name: CoapplicantIncome
        in: query
        type: number
        required: true
        description: Income of the co-applicant
      - name: LoanAmount
        in: query
        type: number
        required: true
        description: Loan amount in thousands
      - name: Loan_Amount_Term
        in: query
        type: number
        required: true
        description: Term of loan in months
      - name: Credit_History
        in: query
        enum: ["YES","NO"]
        required: true
        description: Select YES if you have credit history else select NO
      - name: Gender
        in: query
        enum: ["MALE","FEMALE"]
        required: true
        description: Select your gender
      - name: Married
        in: query
        enum: ["YES","NO"]
        required: true
        description: Select your martial status
      - name: Number_of_dependents
        in: query
        type: number
        required: true
        description: Enter no. of dependents
      - name: Graduate
        in: query
        enum: ["YES","NO"]
        required: true
        description: Select YES if your graduate else select NO
      - name: Self_Employed
        in: query
        enum: ["YES","NO"]
        required: true
        description: Select YES if your self employed else select NO
      - name: Area
        in: query
        enum: ["RURAL","SEMIURBAN","URBAN"]
        required: true
        description: Select your area of living
    responses:
        200:
            description: The output values
        
    """
    ApplicantIncome=request.args.get("ApplicantIncome")
    CoapplicantIncome=request.args.get("CoapplicantIncome")
    LoanAmount=request.args.get("LoanAmount")
    Loan_Amount_Term=request.args.get("Loan_Amount_Term")
    Credit_History=request.args.get("ApplicantIncome")
    Gender=request.args.get("Gender")
    Married=request.args.get("Married")
    Number_of_dependents=request.args.get("Number_of_dependents")
    Graduate=request.args.get("Graduate")
    Self_Employed=request.args.get("Self_Employed")
    Area=request.args.get("Area")
    if Number_of_dependents==0:
        Dependents_0=1
        Dependents_1=0
        Dependents_2=0
    elif Number_of_dependents==1:
        Dependents_0=0
        Dependents_1=1
        Dependents_2=0
    elif Number_of_dependents==2:
        Dependents_0=0
        Dependents_1=0
        Dependents_2=1
    else:
        Dependents_0=0
        Dependents_1=0
        Dependents_2=0
    
    creditHistory=1
    if Credit_History=="YES":
        creditHistory=1
    else:
        creditHistory=0
        
    gender=0
    if Gender=="MALE":
        gender=1
    else:
        gender=0
        
    married=0
    if Married=="YES":
        married=1
    else:
        married=0
    
    graduate=0
    if Graduate=="YES":
        graduate=1
    else:
        graduate=0
        
    employed=0
    if Self_Employed=="YES":
        employed=1
    else:
        employed=0
        
    Rural=0
    Urban=0
    if Area==1:
        Rural=1
        Urban=0
    elif Area==2:
        Rural=0
        Urban=0
    elif Area==2:
        Rural=0
        Urban=1
        
    prediction=classifier.predict([[ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,
                                    creditHistory,gender,married,Dependents_0,Dependents_1,Dependents_2,
                                    graduate,employed,Rural,Urban]])
    print(prediction)
    if prediction==0:
        return " Sorry, your loan is denied"
    else:
        return "Congrats, your loan is approved"


if __name__=="__main__":
    app.run(debug=True, use_reloader=False)
