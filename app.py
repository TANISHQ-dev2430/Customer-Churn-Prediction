import streamlit as st
import numpy as np 
import tensorflow as tf
import sklearn.preprocessing import StandardScaler ,LabelEncoder , OneHotEncoder
import pandas as pd 
import pickle

##load the model 
model = tf.keras.model.load_model('model.h5')

##load the encoder and scaler 
with open('onehot_encoder_geo.pkl','rb') as file: 
    label_encoder_geo = pickle.load(file)
with open('label_encoder_gender.pkl','rb') as file: 
    label_encoder_gender = pickle.load(file)
with open('scaler.pkl','rb') as file: 
    scaler = pickle.load(file)

##streamlit app 
st.tittle('Customer Churn Prediction')

geography = st.selectbox('Geography',onehot_encoder_geo.categories[0])
gender = st.selectbox('Gender',label_encoder_gender.classes_)
age = st.slider('Age',18,92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure',0,10)
num_of_products = st.slider('Number of products',1,4)
has_cr_card = st.selectbox('Has Credit Card'[0,1])
is_active_number = st.selectbox('Is Active Member',[0,1])

#prepare the input data 
input_data = pd.DataFrame({
    'Gender':[label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Balance':[balance],
    'Credit Score':[credit_score],
    'Estimated Salary':[estimated_salary],
    'Tenure':[tenure],
    'Number of Products':[num_of_products],
    'Has Credit Card':[has_cr_card],
    'Is Active Member':[is_active_number]
})

#one hot encode geography
geo_encoded = label_encoder_geo.transform([geography]).toarray()
geo_df = pd.DataFrame(geo_encoded,columns=label_encoder_geo.get_feature_names_out(['Geography']))

#combine all input data
final_input = pd.concat([input_data,geo_df],axis=1)

#scale the input data
final_input_scaled = scaler.transform(final_input)

#prediction churn 
prediction = model.predict(final_input_scaled)
churn_probability = prediction[0][0]

if churn_probability >= 0.5:
    st.write(f'The customer is likely to churn with a probability of {churn_probability:.2f}')
else:
    st.write(f'The customer is unlikely to churn with a probability of {churn_probability:.2f}')