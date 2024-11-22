
# Diploma (*"Виявлення тролінгу в соціальних мережах з використанням нейролінгвістичного програмування"*)
[![Django CI](https://github.com/LuvellCode/Diploma-2.0/actions/workflows/django.yml/badge.svg)](https://github.com/LuvellCode/Diploma-2.0/actions/workflows/django.yml)

## Project Structure

```plaintext
📂 Project Root
├── 📂 catboost_info            # Auto-generated folder for CatBoost logs and models
├── 📂 comparison               # Data for comparing CatBoost, XGBoost, and LightGBM
├── 📂 dev                      # Django REST Framework API project
├── 📂 input                        # Input datasets (CSV files, ZIP archives)
├── .gitignore                          # Git ignore rules
├── 1. Feature Selection.ipynb          # Notebook for cleaning the data and selecting features
├── 2. Model Dev. Realtime Test.ipynb   # Notebook for training the CatBoost model
├── 3. Realtime.ipynb                   # Notebook for interactive usage of the trained model
├── catboost_model.cbm              # Trained CatBoost model
├── comparisons.ipynb           # Notebook for testing and comparing CatBoost, XGBoost, and LightGBM
├── model_test.pkl              # Pickled version of the trained model (used by Django Project)
├── README.md                   # This file
├── test.csv                    # Example input CSV file
└── test_data.csv               # Test dataset for evaluation
```


## System Requirements

To ensure smooth operation, your environment should meet the following requirements:

- **Python**: Install version `3.12.2` or later from [here](https://www.python.org/downloads/).
- **PiP**: Install version `24` or later from [here](https://pypi.org/project/pip/).
- **Required packages**: see `dev/requirements.txt`.


## Explanation of Folders and Files

### 📂 Comparison

This folder containsresources to compare the performance of three models:
- CatBoost (`!pip install catboost`)
- XGBoost (`!pip install xgboost`)
- LightGBM (`!pip install lightgbm`)

The notebook `comparisons.ipynb` runs tests on these models using the datasets inside `/comparison`.

-----
### 📂 Input

Contains raw datasets (tweets in CSV format) for preprocessing and training.

Sources:
1. [Russian Troll Tweets **[Kaggle]**](https://www.kaggle.com/datasets/fivethirtyeight/russian-troll-tweets)
2. [Raw Twitter Timelines w/ No Retweets **[Kaggle]**](https://www.kaggle.com/datasets/speckledpingu/RawTwitterFeeds)

---

### **Notebooks**
1. **Feature Selection (`1. Feature Selection.ipynb`):**
   - Processes the datasets from `/input/`.
   - Performs data preprocessing and feature engineering.
   - Selects optimal features for model training.

2. **Model Training (`2. Model Dev. Realtime Test.ipynb`):**
   - Trains the CatBoost model (selected as the best performer during comparison).
   - Includes a preliminary real-time model testing script.

3. **Interactive Model Core (`3. Realtime.ipynb`):**
   - Implements an interactive testing environment.
   - Loads the trained model using `joblib.load('model_test.pkl')`.
   - Allows interaction with the core to test predictions in real time.

---

### 📂 dev (*Django REST Framework API*)

The `/dev` folder contains the Django REST Framework API, which is built around:
1. The trained CatBoost model from `2. Model Dev. Realtime Test.ipynb`.
2. The core functionality developed in `3. Realtime.ipynb`.

This API allows prediction requests and serves as the main interface for the trolling detection system.


----
## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/LuvellCode/Diploma-2.0
$ cd Diploma-2.0/dev/
```

(Optional) Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv venv
$ venv\Scripts\activate
```

Then install the dependencies:

```sh
$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/swagger/`.

## Testing the API

The first thing you will see is the main Swagger API page:

![image](https://github.com/user-attachments/assets/912f3b3f-a51e-488c-aa81-5acd68e76623)

1. Click on `Predict` -> `Try it out`
2. Enter the JSON Array of Tweets for ONE account.

⚠️ **Warning**: The Recognition Core does not analyze accounts if they have `tweet.count < 10`. You MUST provide at least 10 tweets.

---
### Examples:

#### BOT Account:
```json
[
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    },
    {
        "account": "Me My Mus",
        "tweet": "Dan Bongino: \"\"Nobody trolls liberals better than Donald Trump.\"\" Exactly!  https://t.co/AigV93aC8J #asd #sdhfj #asd #asd #asd "
    }
]
```

#### User Account:
```json
[
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	},
	{
		"account": "Me My Mus",
		"tweet": "Hey guys im new here"
	}
	
]
```

### API Response

The API response will always have the following schema:
```json
{
  "is_troll": true,
  "confidence": 0.9543,
  "elapsed_time": 1.7436
}
```

