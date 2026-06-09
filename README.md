# SkyFare.Aero - AI Flight Fare Prediction System

![SkyFare Logo](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)

SkyFare.Aero is a complete end-to-end Machine Learning project that predicts airline ticket prices based on various flight characteristics. The project encompasses deep exploratory data analysis, robust feature engineering, model benchmarking, and deployment into a stunning, responsive, glassmorphism-styled web application.

## 📊 Exploratory Data Analysis (EDA) Highlights

Thorough EDA was conducted to understand the underlying patterns in flight pricing:
- **Airline Dominance:** Jet Airways and IndiGo are the most frequent carriers in the dataset. Premium classes (e.g., Jet Airways Business) show expected high-fare outliers.
- **Route Popularity:** Delhi to Cochin is the most heavily trafficked route.
- **Missing Values:** Only two records contained missing values. These were dropped to ensure data integrity without losing significant training volume.
- **Fare Distribution:** Fares exhibit a right-skewed distribution, typical for pricing data where majority tickets are economical, with a long tail of premium tickets.

## ⚙️ Data Preprocessing & Feature Engineering

Based on EDA findings, the following preprocessing steps were applied to prepare the data for modeling:
- **Datetime Extraction:** Machine learning models cannot interpret raw string dates. `Journey_date`, `Dep_time`, and `Arrival_time` were decomposed into Day, Month, Hour, and Minute numerical features to capture temporal constraints.
- **Categorical Encoding:** 
  - **One-Hot Encoding (OHE)** was utilized for nominal categorical variables like `Airline`, `Source`, and `Destination` to prevent the model from assigning arbitrary numerical hierarchy to locations.
  - **Label Encoding** was applied to `Total_Stops` since it represents ordinal data (0 stops < 1 stop < 2 stops).
- **Dimensionality Reduction:** High-cardinality string columns (`Route`, `Additional_Info`) were dropped as their variance was successfully captured by engineered features.

## 🧠 Model Benchmarking & Selection

To predict continuous fare values, four baseline and ensemble models were evaluated:
1. **Linear Regression:** Used as a baseline model.
2. **Decision Tree Regressor:** Applied to capture non-linear relationships.
3. **Random Forest Regressor:** An ensemble method used to reduce the variance and overfitting observed in single Decision Trees.
4. **XGBoost:** Explored for advanced gradient boosting.

**Selection:** 
The **Random Forest Regressor** outperformed all other models (highest $R^2$ score and lowest RMSE). 
**Hyperparameter Tuning** was performed using `RandomizedSearchCV` to fine-tune the `n_estimators`, `max_depth`, and `min_samples_split`, leading to the highly accurate final serialized model (`flight_fare_model.pkl`).

## 🚀 Web Application & Deployment

The trained model was deployed into a fully functional Flask web application featuring a highly interactive UI:
- **Dashboard:** Interactive charts and key dataset metrics.
- **Predictor:** A sleek, animated interface where users input flight details and receive AI-calculated fare estimates.
- **Design System:** The UI is built with vanilla CSS focusing on modern Glassmorphism, neon glows, and micro-interactions for a premium SaaS feel.

## 🔮 Scope for Improvement & Next Steps

1. **Real-time Data Integration:** Connect to live flight APIs (like Skyscanner or Amadeus) to fetch current prices and continuously train the model on dynamic market data.
2. **Deep Learning Integration:** Experiment with deep Neural Networks (DNN) incorporating Entity Embeddings for categorical variables to capture deeper latent patterns.
3. **Cloud Deployment:** Containerize the application using Docker and deploy it to AWS/GCP for global scalability.