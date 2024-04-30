import axios from "axios";

export const handleEndPointToCall = async (endpoint, formData) => {
    switch (endpoint) {
        case "snp":
            return await fetchSandPPrediction(formData);
        case "ethereum":
            return await fetchEthereumPrediction(formData);
        case "bitcoin":
            return await fetchBitcoinPrediction(formData);
        case "avocado":
            return await fetchAvocadoPrediction(formData);
        case "wine":
            return await fetchWinePrediction(formData);
        case "stroke":
            return await fetchStrokePrediction(formData);
        case "pokemon":
            return await fetchPokemonPrediction(formData);
        case "failure":
            return await fetchHeartFailurePrediction(formData);
        case "drug":
            return await fetchDrugPrediction(formData);
        case "cancer":
            return await fetchBreastCancerPrediction(formData);
        default:
            return;
    }
}

/**
 * Transcribes the audio file provided in the request.
 * @param {File} audioFile - The audio file to transcribe.
 * @returns {Promise<string|null>} Transcription of the audio file, or null if an error occurs.
 */
export const transcribeAudio = async (audioFile) => {
    try {
        const formData = new FormData();
        formData.append("audio", audioFile);

        const response = await axios.post("http://localhost:5000/transcribe_audio", formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });

        const transcription = response.data.transcription;
        return transcription;
    } catch (error) {
        console.error("Error transcribing audio:", error);
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
        formData.append("file", imageFile);

        const response = await axios.post("http://localhost:5000/recognize_emotion", formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });

        console.log("Image transcription:", response.data);
        return response.data;
    } catch (error) {
        console.error("Error transcribing image:", error);
        return null;
    }
};

/**
 * Fetches S&P prediction for a given date.
 * @param {string} inputDate - The date for which prediction is requested.
 * @returns {Promise<number|null>} Predicted value of S&P index, or null if an error occurs.
 */
const fetchSandPPrediction = async (formData) => {
    const { date } = formData;
    try {
        const response = await axios.get("http://localhost:5000/s&p_prediction", {
            params: {
                input_date: date.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching S&P prediction:", error);
        return null;
    }
};

/**
 * Fetches Ethereum prediction for a given date.
 * @param {string} inputDate - The date for which prediction is requested.
 * @returns {Promise<number|null>} Predicted value of Ethereum cryptocurrency, or null if an error occurs.
 */
const fetchEthereumPrediction = async (formData) => {
    const { date } = formData;
    try {
        const response = await axios.get("http://localhost:5000/ethereum_prediction", {
            params: {
                input_date: date.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Ethereum prediction:", error);
        return null;
    }
};

/**
 * Fetches Bitcoin prediction for a given date.
 * @param {string} inputDate - The date for which prediction is requested.
 * @returns {Promise<number|null>} Predicted value of Bitcoin cryptocurrency, or null if an error occurs.
 */
const fetchBitcoinPrediction = async (formData) => {
    const { date } = formData;
    try {
        const response = await axios.get("http://localhost:5000/bitcoin_prediction", {
            params: {
                input_date: date.value
            }
        });
        console.log(response.data.prediction);
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Bitcoin prediction:", error);
        return null;
    }
};

/**
 * Fetches Avocado prediction for a given date.
 * @param {string} inputDate - The date for which prediction is requested.
 * @returns {Promise<number|null>} Predicted price of avocados, or null if an error occurs.
 */
const fetchAvocadoPrediction = async (formData) => {
    const { date } = formData;
    try {
        const response = await axios.get("http://localhost:5000/avocado_prediction", {
            params: {
                input_date: date.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Avocado prediction:", error);
        return null;
    }
};

/**
 * Fetches Wine prediction based on specified attributes.
 * @param {number} volatileAcidity - The volatile acidity of the wine.
 * @param {number} density - The density of the wine.
 * @param {number} alcohol - The alcohol content of the wine.
 * @returns {Promise<string|null>} Predicted quality of wine ("Good", "Bad", or "Regular"), or null if an error occurs.
 */
const fetchWinePrediction = async (formData) => {
    const { volatileAcidity, density, alcohol } = formData;
    try {
        const response = await axios.get("http://localhost:5000/wine_prediction", {
            params: {
                volatile_acidity: volatileAcidity.value,
                density: density.value,
                alcohol: alcohol.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Wine prediction:", error);
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
const fetchStrokePrediction = async (formData) => {
    const { age, hypertension, heartDisease, avgGlucoseLevel } = formData;
    try {
        const response = await axios.get("http://localhost:5000/stroke_prediction", {
            params: {
                age: age.value,
                hypertension: hypertension.value,
                heart_disease: heartDisease.value,
                avg_glucose_level: avgGlucoseLevel.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Stroke prediction:", error);
        return null;
    }
};

/**
 * Fetches Pokemon prediction based on specified attributes.
 * @param {number} baseEggSteps - The base egg steps of the Pokémon.
 * @param {number} percentageMale - The percentage of male Pokémon in the dataset.
 * @returns {Promise<boolean|null>} True if the Pokémon is predicted to be legendary, false otherwise, or null if an error occurs.
 */
const fetchPokemonPrediction = async (formData) => {
    const { baseEggSteps, percentageMale } = formData;
    try {
        const response = await axios.get("http://localhost:5000/pokemon_prediction", {
            params: {
                base_egg_steps: baseEggSteps.value,
                percentage_male: percentageMale.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Pokemon prediction:", error);
        return null;
    }
};

/**
 * Fetches Heart Failure prediction based on health parameters.
 * @param {number} ejectionFraction - The ejection fraction.
 * @param {number} time - The time.
 * @returns {Promise<boolean|null>} True if the likelihood of heart failure is high, false otherwise, or null if an error occurs.
 */
const fetchHeartFailurePrediction = async (formData) => {
    const { ejectionFraction, time } = formData;
    try {
        const response = await axios.get("http://localhost:5000/heart_failure_prediction", {
            params: {
                ejection_fraction: ejectionFraction.value,
                time: time.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Heart Failure prediction:", error);
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
const fetchDrugPrediction = async (formData) => {
    const { age, sex, bp, cholesterol, naToK } = formData;
    try {
        const response = await axios.get("http://localhost:5000/drug_prediction", {
            params: {
                age: age.value,
                sex: sex.value,
                bp: bp.value,
                cholesterol: cholesterol.value,
                na_to_k: naToK.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Drug prediction:", error);
        return null;
    }
};

/**
 * Fetches Breast Cancer prediction based on tumor attributes.
 * @param {number} concavePointsWorst - The concave points worst.
 * @param {number} perimeterWorst - The perimeter worst.
 * @returns {Promise<boolean|null>} True if the likelihood of breast cancer is high, false otherwise, or null if an error occurs.
 */
const fetchBreastCancerPrediction = async (formData) => {
    const { concavePointsWorst, perimeterWorst } = formData;
    try {
        const response = await axios.get("http://localhost:5000/breast_cancer_prediction", {
            params: {
                concave_points_worst: concavePointsWorst.value,
                perimeter_worst: perimeterWorst.value
            }
        });
        return response.data.prediction;
    } catch (error) {
        console.error("Error fetching Breast Cancer prediction:", error);
        return null;
    }
};