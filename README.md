# ⚡ Smart Grid Electric Load Forecasting Using Deep Learning

##  Project Overview
This project focuses on forecasting electric load in a smart grid environment using deep learning techniques. By learning patterns from historical electricity consumption data, the model predicts future power demand, helping improve grid reliability, energy planning, and operational efficiency.

##  Objectives
- Predict future electricity load accurately  
- Analyze historical power consumption patterns  
- Apply deep learning models for time-series forecasting  
- Support smart grid energy management and demand planning  

##  Technologies Used
- Python  
- Deep Learning (FNN & LSTM)  
- Pandas  
- NumPy  
- Matplotlib  
- Jupyter Notebook  

##  Dataset
- **Source:** Kaggle – Hourly Load Consumption Data  
- **Link:** https://www.kaggle.com/datasets/emperorgraphics/hourly-load-consumption-data  
- Historical hourly electricity consumption data  
- Time-series structured dataset  
- Preprocessed for training and testing  

##  Exploratory Data Analysis (EDA)
The following visual analyses were performed to understand electricity consumption patterns and demand behavior:

### 1️ Electric Load Trend Over Time (7-Day Rolling Average)
Shows long-term trends and seasonal variations in electricity demand.

![7-Day Rolling Average Load](https://github.com/OmPatil2806/Smart-Grid-Electric-Load-Forecasting-Using-Deep-Learning/blob/main/Load_Trend.png)

### 2️ Average Load by Hour of Day
Highlights daily electricity usage patterns and peak demand hours.

![Average Load by Hour](https://github.com/OmPatil2806/Smart-Grid-Electric-Load-Forecasting-Using-Deep-Learning/blob/main/Avg_Load_Hr.png)

### 3️ Load Distribution: Weekday vs Weekend
Compares electricity consumption between weekdays and weekends.

![Weekday vs Weekend Load](https://github.com/OmPatil2806/Smart-Grid-Electric-Load-Forecasting-Using-Deep-Learning/blob/main/Load_distribution.png)

### 4️ Average Load by Temperature Range
Demonstrates how temperature variations impact electricity demand.

![Average Load by Temperature](https://github.com/OmPatil2806/Smart-Grid-Electric-Load-Forecasting-Using-Deep-Learning/blob/main/load_Temperature.png)

##  Model Description
- **Feedforward Neural Network (FNN):** Used as a baseline model to learn non-linear relationships in electricity demand.
- **LSTM (Long Short-Term Memory):** Captures temporal dependencies in time-series data, improving forecasting accuracy.

##  Model Architecture (LSTM – Sequential Model)

| Layer (Type)         | Output Shape      | Parameters |
|----------------------|-------------------|------------|
| LSTM (lstm_10)       | (None, 24, 128)   | 71,168     |
| Dropout (dropout_10) | (None, 24, 128)   | 0          |
| LSTM (lstm_11)       | (None, 24, 64)    | 49,408     |
| Dropout (dropout_11) | (None, 24, 64)    | 0          |
| LSTM (lstm_12)       | (None, 32)        | 12,416     |
| Dropout (dropout_12) | (None, 32)        | 0          |
| Dense (dense_4)      | (None, 1)         | 33         |

##  Project Workflow
1. Data collection and preprocessing  
2. Exploratory Data Analysis (EDA)  
3. Feature scaling and sequence creation  
4. FNN and LSTM model development  
5. Model training and evaluation  
6. Load forecasting and visualization  

##  Model Performance
- Trained on historical hourly load data  
- Evaluated using MAE and MSE metrics  
- LSTM outperforms  by modeling long-term temporal patterns  

## 🚀 Results
The model demonstrates strong forecasting performance by closely matching predicted load values with actual consumption.

###  Actual vs Predicted Load
![Actual vs Predicted Load](https://github.com/OmPatil2806/Smart-Grid-Electric-Load-Forecasting-Using-Deep-Learning/blob/main/Prediciton_Test.png)

##  Future Enhancements
- Hyperparameter tuning  
- Integration of weather and calendar features  
- Real-time load forecasting  
- Deployment using Streamlit or Flask  

## 👤 Author
**Om Patil**  
🔗 LinkedIn: https://www.linkedin.com/in/om-patil-039863369/
