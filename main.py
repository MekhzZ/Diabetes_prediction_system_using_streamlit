import streamlit as st
import pickle
import numpy as np
import pandas as pd

#including class since it is custom made and is needed for functioning of saved model

class SVM_Classifier():

  # initializing parameters

  def __init__(self, learning_rate, no_of_iterations, lambda_param): # self is for instance
    self.learning_rate = learning_rate
    self.no_of_iterations = no_of_iterations
    self.lambda_param = lambda_param

  # fit function

  def fit(self, X, Y):

    # m -> no of data points , n -> no of features
    self.m, self.n = X.shape

    # initializing weights and bias value with zeros

    self.w = np.zeros(self.n) # since its value is in array
    self.b = 0 # since b value is real number
    self.X = X
    self.Y = Y

    # starting gradient descent algorithm for optimization
    for i in range(self.no_of_iterations):
      self.update_weights()



  def update_weights(self):

    # label encoding
    y_label = np.where(self.Y <= 0, -1, 1) # since our dataset label is in binary 0,1 but model understand -1,1 for classification

    # gradient descent formula
    for index, x_i in enumerate(self.X):
      condition = y_label[index] * (np.dot(x_i, self.w) - self.b) >= 1 #formula from top note
      if (condition == True):
        dw = 2 * self.lambda_param * self.w # since dw = 2*lambda*w
        db = 0
      else:
        dw = 2 * self.lambda_param * self.w - np.dot(x_i, y_label[index]) # dw = 2*lambda*w - Xi * Yi
        db = y_label[index]

      self.w = self.w - self.learning_rate * dw # w = w - learning_rate * dw
      self.b = self.b - self.learning_rate * db # b = b - learning_rate * db


  def predict(self, X):
    output = np.dot(X, self.w) - self.b # y = w*x - b
    predicted_labels = np.sign(output) # since model classify by 1 or -1
    y = np.where(predicted_labels <= -1, 0, 1) # rearranging the output as output label
    return y


scaler = pickle.load(open('scaler.pkl','rb'))

model = pickle.load(open('diabetes_trained_model.pkl','rb'))


# Function for making predictions
def predict_diabetes(input_features):
    input_features = np.asarray(input_features).reshape(1, -1)
    input_features = scaler.transform(input_features)
    prediction = model.predict(input_features)
    return prediction[0]

# Streamlit UI

# set page config
st.set_page_config(page_title="Diabetes Prediction System",
                   layout="centered",
                   page_icon="📈")


st.title("📈 Diabetes Prediction System")

st.write("- MekhzZ")

st.write()

df = pd.read_csv("diabetes.csv")

st.write("you can take a random data from below to predict")

st.write(df.head(2))

col1,col2 = st.columns(2)

with col1 :
  pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0)
  blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=70)
  insulin = st.number_input("Insulin", min_value=0, max_value=900, value=80)
  diabetes_pedigree_function = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.5)


with col2 :
  glucose = st.number_input("Glucose", min_value=0, max_value=300, value=120)
  skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20)
  bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0)
  age = st.number_input("Age", min_value=0, max_value=120, value=30)

if st.button("Predict"):
    # Prepare input features for prediction
    input_features = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]
    result = predict_diabetes(input_features)
    
    # Display the result
    if result == 1:
        st.error("The person is likely to have diabetes.")
    else:
        st.success("The person is unlikely to have diabetes.")

