# StackOverflow-lite

![Travis](https://travis-ci.com/asheuh/StackOverflow-lite.svg?branch=develop-v2)
[![Coverage Status](https://coveralls.io/repos/github/asheuh/StackOverflow-lite/badge.svg?branch=develop-v2)](https://coveralls.io/github/asheuh/StackOverflow-lite?branch=develop-v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/465755288bc6481668ed/maintainability)](https://codeclimate.com/github/asheuh/StackOverflow-lite/maintainability)

StackOverflow-lite is a platform where people can ask questions and provide answers.

* [Heroku live demo](https://stackoverflow-lite-heroku.herokuapp.com))

#### Overview Homepage

![homepage-1](https://user-images.githubusercontent.com/22955146/43910415-7143a362-9c05-11e8-836e-39aaaac1ca76.png)

#### Required Features

- Users can create an account and log in.
- Users can post questions.
- Users can delete the questions they post.
- Users can post answers.
- Users can view the answers to questions.
- Users can accept an answer out of all the answers to his/her question as the preferred answer.
- Users can upvote or downvote an answer.
- Users can comment on an answer.
- Users can fetch all questions he/she has ever asked on the platform
- Users can search for questions on the platform
- Users can view questions with the most answers.


# Installation and Setup
Clone the repository.

```
$ git clone https://github.com/asheuh/StackOverflow-lite
```

## Navigate to the API folder

```
$ cd flaskie
```

## Create a virtual environment and activate

On linux

```
$ python -m venv venv
$ source venv/bin/activate

```

On Windows

```
$ py -3 -m venv venv
$ venv\Scripts\activate

```

## Install requirements( with pip)

```
$ pip install -r requirements.txt

```

## Running the application

After the configuration, you will run the app

Setup the application for development to make sure all the requirements are installed

```
$ python setup.py develop

```
## Create your local exports

```
$ export FLASK_APP="app.py"
$ export FLASK_DEBUG=True
$ export APP_SETTINGS="development"
$ export DATABASE_URL="Your DATABASE_URL here"

```

Run the application

```
$ flask run

```

## Url for endpoints

```
http://127.0.0.1:5000/api/v1/
http://127.0.0.1:5000/api/v2/

```
## The app is deploy to heroku with the following url

* [here is the live demo for v2 on heroku](https://stackoverflow-lite-heroku.herokuapp.com/api/v2/))

# Frontend Support

#### Sign up
- Fileds required to sign up

```
- Username
- Email address
- Password
- Conform Password

```
![signup](https://user-images.githubusercontent.com/22955146/43834826-45c57c3a-9b18-11e8-9c44-6d46e0fc614f.png)

#### Login

```
- Email address
- Password

```
![login](https://user-images.githubusercontent.com/22955146/43835943-5f443e68-9b1c-11e8-9cbf-1d4e154f722a.png)

#### Template

- You can view the UI template on [Github Pages](https://asheuh.github.io/StackOverflow-lite)
- Deployed to [Heroku, V1 of the app](https://stackoverflow-lite-heroku.herokuapp.com/api/v1/)

#### Authors

* **Brian Mboya** - *Initial work* - [asheuh](https://github.com/asheuh)

#### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

#### Acknowledgments

* Thank's for my follow bootcampers at Open Andela
* Inspiration
* The power is w3school is really awesome. N
* Don't let life craft you, craft it

