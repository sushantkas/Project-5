import pandas as pd
import numpy as np
import pickle

# Writing class and methods for Preprocessing   

class quality_check:
    def __init__(self, emi_pred, Prediction=True):
        col_X=['age', 'gender', 'marital_status', 'education', 'monthly_salary',
       'employment_type', 'years_of_employment', 'company_type', 'house_type',
       'monthly_rent', 'family_size', 'dependents', 'school_fees',
       'college_fees', 'travel_expenses', 'groceries_utilities',
       'other_monthly_expenses', 'existing_loans', 'current_emi_amount',
       'credit_score', 'bank_balance', 'emergency_fund', 'emi_scenario',
       'requested_amount', 'requested_tenure']
        
        columns=['age', 'gender', 'marital_status', 'education', 'monthly_salary',
       'employment_type', 'years_of_employment', 'company_type', 'house_type',
       'monthly_rent', 'family_size', 'dependents', 'school_fees',
       'college_fees', 'travel_expenses', 'groceries_utilities',
       'other_monthly_expenses', 'existing_loans', 'current_emi_amount',
       'credit_score', 'bank_balance', 'emergency_fund', 'emi_scenario',
       'requested_amount', 'requested_tenure', 'emi_eligibility',
       'max_monthly_emi']
        
        fixed_expenses=['school_fees', 'college_fees', 'current_emi_amount']
        otherexpenses_col=['travel_expenses', 'groceries_utilities','other_monthly_expenses']
        self.Prediction=Prediction
        if col_X == list(emi_pred.columns) or columns == list(emi_pred.columns):
            if self.Prediction==True:
                self.emi_pred=emi_pred[col_X]
            else: 
                self.emi_pred=emi_pred
            self.emi_pred["Total_Fixed_expenses"]=emi_pred[fixed_expenses].sum(axis=1)
            self.emi_pred["Total_Other_expenses"]=emi_pred[otherexpenses_col].sum(axis=1)
            with open("assets/encoder.pkl", "rb") as encoder:
                self.encoder = pickle.load(encoder)
            with open("assets/imputer.pkl","rb") as imputer:
                self.imputer = pickle.load(imputer)
        else:
            raise ValueError("Columns do not match the expected format.")
        pass



    def dtype_correction(self):
        emi_pred=self.emi_pred
        def type_corrector(x):
            # Skip if x is NaN
            if pd.isna(x):
                return np.nan
            # Convert safely to string and handle decimals
            try:
                return int(float(str(x).split(".")[0]))
            except ValueError:
                return np.nan
        for col in ["monthly_salary", "bank_balance", "age"]:
            emi_pred.loc[:, col] = emi_pred[col].apply(type_corrector)
            #emi_pred[col].astype(int, errors="ignore")
        emi_pred["age"] = emi_pred["age"].astype("int")
        emi_pred["monthly_salary"] = emi_pred["monthly_salary"].astype("int")
        emi_pred["bank_balance"] = emi_pred["bank_balance"].astype("float")
        self.emi_pred=emi_pred.copy()
        return self
    

    def strip_title(self):
        emi_pred=self.emi_pred.copy()
        obj_cols = ['gender', 'marital_status', 'education', 'employment_type',
       'company_type', 'house_type', 'existing_loans', 'emi_scenario']
        emi_pred.loc[:, obj_cols] = emi_pred[obj_cols].apply(
        lambda x: x.str.strip().str.title() )
        self.emi_pred=emi_pred.copy()
        return self
    
    def encode_boolean(self):
        self.emi_pred.replace({"existing_loans":{"Yes":1, "No":0}}, inplace=True)
        self.emi_pred.replace({"marital_status":{"Married":1, "Single":0}}, inplace=True)
        self.emi_pred.replace({"gender":{"M":1, "F":0, "Male":1, "Female":0}}, inplace=True)
        return self
    



    def final_processsing(self):
        self.dtype_correction()
        self.strip_title()
        self.encode_boolean()
        encoding_columns=['education', 'employment_type', 'company_type', 'house_type','emi_scenario']
        self.emi_pred[encoding_columns]=self.encoder.transform(self.emi_pred[encoding_columns])
        target_cols=['emi_eligibility', 'max_monthly_emi']
        if self.Prediction == False:
            self.emi_pred["emi_eligibility"].replace({"Not_Eligible":0, "Eligible":1, "High_Risk":2}, inplace=True)
            self.target_data = self.emi_pred[target_cols]
            self.emi_pred.drop(target_cols, axis=1, inplace=True)
        for i in list(self.emi_pred.columns):
            if i in target_cols:
                self.emi_pred.drop(i, axis=1, inplace=True)
        # imputer columns order and dataset columns order need to check
        imputer_columns_order=['age', 'gender', 'marital_status', 'education', 'monthly_salary',
       'employment_type', 'years_of_employment', 'company_type', 'house_type',
       'monthly_rent', 'family_size', 'dependents', 'school_fees',
       'college_fees', 'travel_expenses', 'groceries_utilities',
       'other_monthly_expenses', 'existing_loans', 'current_emi_amount',
       'credit_score', 'bank_balance', 'emergency_fund', 'emi_scenario',
       'requested_amount', 'requested_tenure', 'Total_Fixed_expenses',
       'Total_Other_expenses']
        self.emi_pred = self.emi_pred[imputer_columns_order]
        self.emi_pred = pd.DataFrame(self.imputer.transform(self.emi_pred), columns=self.emi_pred.columns)
        if self.Prediction == False:
            self.emi_pred[target_cols]=self.target_data
        
        
        return self

    




