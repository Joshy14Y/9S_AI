import os
import pickle
import sklearn
import pandas as pd


class ModelLoader:
    def __init__(self):
        """
        Initializes the ModelLoader class.

        This class is responsible for loading machine learning models from
        pickle files and providing methods for making predictions using those models.
        """
        self.models = self.load_models()

    @staticmethod
    def load_models():
        directory_path = r"..\..\9S_AI\models"
        """
        Loads machine learning models from pickle files.

        This method loads machine learning models from pickle files located in
        a specified directory. The models are stored in a dictionary where the
        keys are the model names and the values are the loaded models.

        Returns:
        - loaded_models (dict): Dictionary containing loaded machine learning models.
        """
        directory_path = r"..\..\AI_Project_P1\models"
        loaded_models = {}
        for filename in os.listdir(directory_path):
            if filename.endswith('.pkl'):
                model_name = filename.split('.')[0]
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'rb') as file:
                    loaded_model = pickle.load(file)
                    loaded_models[model_name] = loaded_model
        return loaded_models

    def process_SARIMAX(self, model, input_date):
        """
        Makes predictions using the SARIMAX model.

        This method makes predictions using the SARIMAX model for a specified date.
        It retrieves the model corresponding to the provided model name and uses it
        to predict the value for the given date.

        Parameters:
        - model (str): Name of the SARIMAX model to use for prediction.
        - input_date (str): Date for which the prediction is to be made.

        Returns:
        - predicted_value: Predicted value for the specified date.
        """
        try:
            # Convert the input date to a datetime object
            input_datetime = pd.to_datetime(input_date)

            # Make predictions for the specified date
            pred = self.models[model].get_prediction(start=input_datetime, end=input_datetime, dynamic=False)

            # Extract the predicted value for the specified date
            predicted_value = pred.predicted_mean[input_datetime]

            return predicted_value
        except Exception as e:
            print(f"Error predicting with model '{model}': {e}")
            return None

    def wine_prediction(self, volatile_acidity, density, alcohol):
        """
        Makes predictions using the wine model.

        This method makes predictions using the wine model based on the input
        volatile acidity, density, and alcohol values.

        Parameters:
        - volatile_acidity (float): Volatile acidity of the wine.
        - density (float): Density of the wine.
        - alcohol (float): Alcohol content of the wine.

        Returns:
        - original_label (str): Predicted label for the wine quality.
        """
        try:
            # Create a DataFrame with the input data
            input_data = pd.DataFrame({
                'volatile acidity': [volatile_acidity],
                'density': [density],
                'alcohol': [alcohol],
            })

            # Make predictions using the trained model
            prediction_encoded = self.models['wine'].predict(input_data)

            # Define mapping dictionary to map encoded values to original labels
            label_mapping = {0: 'Bad', 1: 'Good', 2: 'Regular'}

            # Get the original label corresponding to the predicted encoded value
            original_label = label_mapping[prediction_encoded[0]]

            return original_label
        except Exception as e:
            print(f"Error predicting with model 'wine': {e}")
            return None

    def stroke_prediction(self, age, hypertension, heart_disease, avg_glucose_level):
        """
        Makes predictions using the stroke model.

        This method makes predictions using the stroke model based on the input
        age, hypertension, heart disease, and average glucose level values.

        Parameters:
        - age (int): Age of the patient.
        - hypertension (int): Presence of hypertension (1 for True, 0 for False).
        - heart_disease (int): Presence of heart disease (1 for True, 0 for False).
        - avg_glucose_level (float): Average glucose level of the patient.

        Returns:
        - prediction (bool): Predicted likelihood of stroke (True for high, False for low).
        """
        try:
            # Create a DataFrame with the input data
            input_data = pd.DataFrame({
                'age': [age],
                'hypertension': [hypertension],
                'heart_disease': [heart_disease],
                'avg_glucose_level': [avg_glucose_level]
            })

            # Make predictions using the trained model
            prediction = self.models['stroke'].predict(input_data)

            # Return True if prediction is equal to 1, otherwise return False
            return bool(prediction[0])  # Convert 1 or 0 to True or False

        except Exception as e:
            print(f"Error predicting with model 'stroke': {e}")
            return None

    def pokemon_prediction(self, base_egg_steps, percentage_male):
        """
        Makes predictions using the Pokémon model.

        This method makes predictions using the Pokémon model based on the input
        base egg steps and percentage male values.

        Parameters:
        - base_egg_steps (int): Base egg steps for the Pokémon.
        - percentage_male (float): Percentage of male Pokémon.

        Returns:
        - prediction (bool): Predicted likelihood of being legendary (True for legendary, False for not legendary).
        """
        try:
            # Create a DataFrame with the input data
            input_data = pd.DataFrame({
                'base_egg_steps': [base_egg_steps],
                'percentage_male': [percentage_male],
            })

            # Make predictions using the trained model
            prediction = self.models['pokemon'].predict(input_data)

            # Return True if prediction is equal to 1, otherwise return False
            return bool(prediction[0])  # Convert 1 or 0 to True or False

        except Exception as e:
            print(f"Error predicting with model 'pokemon': {e}")
            return None

    def heart_failure_prediction(self, ejection_fraction, time):
        """
        Makes predictions using the heart failure model.

        This method makes predictions using the heart failure model based on the input
        ejection fraction and time values.

        Parameters:
        - ejection_fraction (int): Ejection fraction of the patient.
        - time (int): Time of follow-up (in days).

        Returns:
        - prediction (bool): Predicted likelihood of heart failure (True for high, False for low).
        """
        try:
            # Create a DataFrame with the input data
            input_data = pd.DataFrame({
                'ejection_fraction': [ejection_fraction],
                'time': [time],
            })

            # Make predictions using the trained model
            prediction = self.models['heart_failure'].predict(input_data)

            # Return True if prediction is equal to 1, otherwise return False
            return bool(prediction[0])  # Convert 1 or 0 to True or False

        except Exception as e:
            print(f"Error predicting with model 'heart_failure': {e}")
            return None

    def drug_prediction(self, age, sex, bp, cholesterol, na_to_k):
        """
        Makes predictions using the drug model.

        This method makes predictions using the drug model based on the input
        age, sex, blood pressure, cholesterol, and sodium-to-potassium ratio.

        Parameters:
        - age (int): Age of the patient.
        - sex (int): Sex of the patient (1 for male, 0 for female).
        - bp (int): Blood pressure level.
        - cholesterol (int): Cholesterol level.
        - na_to_k (float): Sodium-to-potassium ratio.

        Returns:
        - prediction: Predicted drug type for the patient.
        """
        try:
            # Create a DataFrame with the input data
            input_data = pd.DataFrame({
                'Age': [age],
                'Sex': [sex],
                'BP': [bp],
                'Cholesterol': [cholesterol],
                'Na_to_K': [na_to_k]
            })

            # Make predictions using the trained model
            prediction = self.models['drug'].predict(input_data)

            return prediction[0]
        except Exception as e:
            print(f"Error predicting with model 'drug': {e}")
            return None

    def breast_cancer_prediction(self, concave_points_worst, perimeter_worst):
        """
        Makes predictions using the breast cancer model.

        This method makes predictions using the breast cancer model based on the input
        concave points worst and perimeter worst values.

        Parameters:
        - concave_points_worst (float): Worst concave points of the tumor.
        - perimeter_worst (float): Worst perimeter of the tumor.

        Returns:
        - prediction (bool): Predicted likelihood of breast cancer (True for high, False for low).
        """
        try:
            # Create a DataFrame with the input data
            input_data = pd.DataFrame({
                'concave points_worst': [concave_points_worst],
                'perimeter_worst': [perimeter_worst],
            })

            # Make predictions using the trained model
            prediction = self.models['breast_cancer'].predict(input_data)

            # Return True if prediction is equal to 1, otherwise return False
            return bool(prediction[0])  # Convert 1 or 0 to True or False

        except Exception as e:
            print(f"Error predicting with model 'breast_cancer': {e}")
            return None

if __name__ == "__main__":
    # Create an instance of the ModelLoader class
    model_loader = ModelLoader()

    # Test the wine_prediction method
    wine_prediction = model_loader.wine_prediction(0.5, 0.99, 12.3)
    print("Wine Prediction:", wine_prediction)

    # Test the stroke_prediction method
    stroke_prediction = model_loader.stroke_prediction(65, 1, 0, 90)
    print("Stroke Prediction:", stroke_prediction)

    # Test the pokemon_prediction method
    pokemon_prediction = model_loader.pokemon_prediction(10000, 60)
    print("Pokemon Prediction:", pokemon_prediction)

    # Test the heart_failure_prediction method
    heart_failure_prediction = model_loader.heart_failure_prediction(35, 200)
    print("Heart Failure Prediction:", heart_failure_prediction)

    # Test the drug_prediction method
    drug_prediction = model_loader.drug_prediction(50, 1, 120, 200, 10)
    print("Drug Prediction:", drug_prediction)

    # Test the breast_cancer_prediction method
    breast_cancer_prediction = model_loader.breast_cancer_prediction(0.05, 100)
    print("Breast Cancer Prediction:", breast_cancer_prediction)

    # Assuming 'results' is your trained model object
    # print(
    #     process_SARIMAX(loaded_models['avocado'], '2024-04-08'))  # Replace 'your_model_name' with the actual model name
