import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import pandas as pd
import pickle

#load the trained model
model=tf.keras.models.load_model('model.h5')

#load the encoders and scaler

with open('scaler.pkl','rb') as f:
    scaler=pickle.load(f)

with open('onehot_encoder_geo.pkl','rb') as f:
    label_encoder_geo=pickle.load(f)

with open('label_encoder_gender.pkl','rb') as f:
    label_encoder_gender=pickle.load(f)


##streamlit app

st.title('Customer Churn Prediction')

#user input
geography=st.selectbox('Geography',label_encoder_geo.categories_[0])
gender=st.selectbox('Gender',label_encoder_gender.classes_)
age=st.slider('Age',18,92)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure',0,10)
num_of_products=st.slider('Number of Products',1,4)
has_cr_card=st.selectbox('Has credit Card',[0,1])
is_active_member=st.selectbox('Is Active Member',[0,1])

#prepare the input
input_data=pd.DataFrame({
    'CreditScore':[credit_score],
    'Gender':[label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_member],
    'EstimatedSalary':[estimated_salary]
})

#onehot encoding of geography
geo_encoded=label_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded,columns=label_encoder_geo.get_feature_names_out(['Geography']))

#combine
input_data=pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)

#sacling the i/p data
input_scaled=scaler.transform(input_data)

#predict churn
prediction=model.predict(input_scaled)
prediction_proba=prediction[0][0]

st.write(f'Churn Probability: {prediction_proba:.2f}')

if prediction_proba > 0.5:
    st.write("The customer is likely to churn")
else:
    st.write("The customer is not likely to churn")