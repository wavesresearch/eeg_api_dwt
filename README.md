# API-SP

An API for signal processing [V1] based on DWT bior2.2 and using random forest classifier.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Install all dependencies

```
pip install -r requirements.txt
```

Configure credentials in  [eeg_api_dwt/.env](api_signal_processing/.env)

```
DB_NAME = 'eegDB'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '3306'
```

### Installing

Once you configure the database, you must run locally

```
python manage.py makemigrations
```

And then

```
python manage.py migrate
```


## Running

To run the django project in the default port (8000)

```
python manage.py runserver
```


## Deployment

The default branch for the stable version is 'MASTER'

## Built With

* [Django](https://docs.djangoproject.com/en/2.0/) - The web framework used
* [scikit-learn](http://scikit-learn.org/stable/documentation.html) - Machine Learning in Python
* [PyWavelets](https://pywavelets.readthedocs.io/en/latest/) - Wavelet Transforms in Python

## Authors

* **Luis Alfredo Moctezuma** - *Initial work* - [luisalfredomoctezuma](https://github.com/luisalfredomoctezuma)

