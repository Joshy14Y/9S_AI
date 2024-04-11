import axios from 'axios';

/**
 * Transcribes the audio file provided in the request.
 * @param {File} audioFile - The audio file to transcribe.
 * @returns {Promise<string|null>} Transcription of the audio file, or null if an error occurs.
 */
export const transcribeAudio = async (audioFile) => {
    try {
        const formData = new FormData();
        formData.append('audio', audioFile);

        const response = await axios.post('http://localhost:5000/transcribe_audio', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        const transcription = response.data.transcription;
        console.log('Transcription:', transcription);
        return transcription;
    } catch (error) {
        console.error('Error transcribing audio:', error);
        return null;
    }
};

/**
 * Recognizes emotions in the provided image.
 * @param {File} imageFile - The image file to analyze.
 * @returns {Promise<object|null>} Detected emotions in the image, or null if an error occurs.
 */
export const recognizeEmotion = async (imageFile) => {
    try {
        const formData = new FormData();
        formData.append('file', imageFile);

        const response = await axios.post('http://localhost:5000/recognize_emotion', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        console.log('Image transcription:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error transcribing image:', error);
        return null;
    }
};

/**
 * Fetches S&P prediction for a given date.
 * @param {string} inputDate - The date for which prediction is requested.
 * @returns {Promise<number|null>} Predicted value of S&P index, or null if an error occurs.
 */
export const fetchSandPPrediction = async (inputDate) => {
    try {
        const response = await axios.get('http://localhost:5000/s&p_prediction', {
            params: {
                input_date: inputDate
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching S&P prediction:', error);
        return null;
    }
};

/**
 * Fetches Ethereum prediction for a given date.
 * @param {string} inputDate - The date for which prediction is requested.
 * @returns {Promise<number|null>} Predicted value of Ethereum cryptocurrency, or null if an error occurs.
 */
export const fetchEthereumPrediction = async (inputDate) => {
    try {
        const response = await axios.get('http://localhost:5000/ethereum_prediction', {
            params: {
                input_date: inputDate
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Ethereum prediction:', error);
        return null;
    }
};

/**
 * Fetches Bitcoin prediction for a given date.
 * @param {string} inputDate - The date for which prediction is requested.
 * @returns {Promise<number|null>} Predicted value of Bitcoin cryptocurrency, or null if an error occurs.
 */
export const fetchBitcoinPrediction = async (inputDate) => {
    try {
        const response = await axios.get('http://localhost:5000/bitcoin_prediction', {
            params: {
                input_date: inputDate
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Bitcoin prediction:', error);
        return null;
    }
};

/**
 * Fetches Avocado prediction for a given date.
 * @param {string} inputDate - The date for which prediction is requested.
 * @returns {Promise<number|null>} Predicted price of avocados, or null if an error occurs.
 */
export const fetchAvocadoPrediction = async (inputDate) => {
    try {
        const response = await axios.get('http://localhost:5000/avocado_prediction', {
            params: {
                input_date: inputDate
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Avocado prediction:', error);
        return null;
    }
};

/**
 * Fetches Wine prediction based on specified attributes.
 * @param {number} volatileAcidity - The volatile acidity of the wine.
 * @param {number} density - The density of the wine.
 * @param {number} alcohol - The alcohol content of the wine.
 * @returns {Promise<string|null>} Predicted quality of wine ('Good', 'Bad', or 'Regular'), or null if an error occurs.
 */
export const fetchWinePrediction = async (volatileAcidity, density, alcohol) => {
    try {
        const response = await axios.get('http://localhost:5000/wine_prediction', {
            params: {
                volatile_acidity: volatileAcidity,
                density: density,
                alcohol: alcohol
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Wine prediction:', error);
        return null;
    }
};

/**
 * Fetches Stroke prediction based on health parameters.
 * @param {number} age - The age of the person.
 * @param {number} hypertension - Whether the person has hypertension (1 for true, 0 for false).
 * @param {number} heartDisease - Whether the person has heart disease (1 for true, 0 for false).
 * @param {number} avgGlucoseLevel - The average glucose level of the person.
 * @returns {Promise<boolean|null>} True if the likelihood of stroke is high, false otherwise, or null if an error occurs.
 */
export const fetchStrokePrediction = async (age, hypertension, heartDisease, avgGlucoseLevel) => {
    try {
        const response = await axios.get('http://localhost:5000/stroke_prediction', {
            params: {
                age: age,
                hypertension: hypertension,
                heart_disease: heartDisease,
                avg_glucose_level: avgGlucoseLevel
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Stroke prediction:', error);
        return null;
    }
};

/**
 * Fetches Pokemon prediction based on specified attributes.
 * @param {number} baseEggSteps - The base egg steps of the Pokémon.
 * @param {number} percentageMale - The percentage of male Pokémon in the dataset.
 * @returns {Promise<boolean|null>} True if the Pokémon is predicted to be legendary, false otherwise, or null if an error occurs.
 */
export const fetchPokemonPrediction = async (baseEggSteps, percentageMale) => {
    try {
        const response = await axios.get('http://localhost:5000/pokemon_prediction', {
            params: {
                base_egg_steps: baseEggSteps,
                percentage_male: percentageMale
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Pokemon prediction:', error);
        return null;
    }
};

/**
 * Fetches Heart Failure prediction based on health parameters.
 * @param {number} ejectionFraction - The ejection fraction.
 * @param {number} time - The time.
 * @returns {Promise<boolean|null>} True if the likelihood of heart failure is high, false otherwise, or null if an error occurs.
 */
export const fetchHeartFailurePrediction = async (ejectionFraction, time) => {
    try {
        const response = await axios.get('http://localhost:5000/heart_failure_prediction', {
            params: {
                ejection_fraction: ejectionFraction,
                time: time
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Heart Failure prediction:', error);
        return null;
    }
};

/**
 * Fetches Drug prediction based on patient parameters.
 * @param {number} age - The age of the patient.
 * @param {number} sex - The sex of the patient (1 for male, 0 for female).
 * @param {number} bp - The blood pressure of the patient.
 * @param {number} cholesterol - The cholesterol level of the patient.
 * @param {number} naToK - The sodium-to-potassium ratio of the patient.
 * @returns {Promise<string|null>} Recommended drug for the patient, or null if an error occurs.
 */
export const fetchDrugPrediction = async (age, sex, bp, cholesterol, naToK) => {
    try {
        const response = await axios.get('http://localhost:5000/drug_prediction', {
            params: {
                age: age,
                sex: sex,
                bp: bp,
                cholesterol: cholesterol,
                na_to_k: naToK
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Drug prediction:', error);
        return null;
    }
};

/**
 * Fetches Breast Cancer prediction based on tumor attributes.
 * @param {number} concavePointsWorst - The concave points worst.
 * @param {number} perimeterWorst - The perimeter worst.
 * @returns {Promise<boolean|null>} True if the likelihood of breast cancer is high, false otherwise, or null if an error occurs.
 */
export const fetchBreastCancerPrediction = async (concavePointsWorst, perimeterWorst) => {
    try {
        const response = await axios.get('http://localhost:5000/breast_cancer_prediction', {
            params: {
                concave_points_worst: concavePointsWorst,
                perimeter_worst: perimeterWorst
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error('Error fetching Breast Cancer prediction:', error);
        return null;
    }
};