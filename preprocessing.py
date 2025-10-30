import pandas as pd
import numpy as np

# Writing class and methods for Preprocessing   

class quality_check:
    def __init__(self, emi_pred):
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
        
        if col_X == list(emi_pred.columns) or columns == list(emi_pred.columns):
            self.emi_pred=emi_pred[col_X]
        else:
            raise ValueError("Columns do not match the expected format.")
        pass



    def dtype_correction(self):
        def type_corrector(x):
            # Skip if x is NaN
            if pd.isna(x):
                return np.nan
            # Convert safely to string and handle decimals
            try:
                return int(float(str(x).split(".")[0]))
            except ValueError:
                return np.nan
        self.emi_pred["monthly_salary"] = self.emi_pred["monthly_salary"].apply(type_corrector)
        self.emi_pred["bank_balance"] = self.emi_pred["bank_balance"].apply(type_corrector)
        self.emi_pred["age"] = self.emi_pred["age"].apply(type_corrector)
        return self
    

    def strip_title(self):
        obj_cols = ['age', 'gender', 'marital_status', 'education', 'employment_type',
       'company_type', 'house_type', 'existing_loans', 'emi_scenario']
        self.emi_pred[obj_cols] = self.emi_pred[obj_cols].apply(lambda x: x.str.strip().str.title())
        return self
    
    def encode_boolean(self):
        self.emi_pred.replace({"existing_loans":{"Yes":1, "No":0}}, inplace=True)
        self.emi_pred.replace({"marital_status":{"Married":1, "Single":0}}, inplace=True)
        self.emi_pred.replace({"gender":{"M":1, "F":0, "Male":1, "Female":0}}, inplace=True)
        return self