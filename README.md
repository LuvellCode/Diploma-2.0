# Diploma ("Виявлення тролінгу в соціальних мережах з використанням нейролінгвістичного програмування")
[![Django CI](https://github.com/LuvellCode/Diploma-2.0/actions/workflows/django.yml/badge.svg)](https://github.com/LuvellCode/Diploma-2.0/actions/workflows/django.yml)

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

## Testing

The first thing you will see is the main Swagger API page:

![image](https://github.com/user-attachments/assets/912f3b3f-a51e-488c-aa81-5acd68e76623)

Click on `Predict` -> `Try it out`

Enter the JSON Array of Tweets for ONE account.

⚠️ Warning: The Recognition Core does not analyse accounts if they have tweet.count < 10. So you MUST mock at least 10 tweets.

Examples:

BOT Account:
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

User Account:
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

## API Response

As a result, you shoold see the API response:
![image](https://github.com/user-attachments/assets/2d89b47a-02f3-4c38-b01f-262cfbedadf4)

Response JSON will always have this schema:
```json
{
  "is_troll": true,
  "confidence": 0.9543,
  "elapsed_time": 1.7436
}
```
