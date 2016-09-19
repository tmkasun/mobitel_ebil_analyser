# Mobitel e-bill Analyser
This project is intend to analyse mobitel(SLT) ebills and extract meaningful data and represent them in meaningful way to its users
The basic structure of the application is 

* Read the ebill HTML file which was converted from [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX)
* Extract call information by iterating over lines of call data
* Arrange the data as per date calls data
* Insert them in to prefered DB through data access objects, I have implemented DAO for mongoDB, you may implement your preferred DAO using provided abstract class definition

![home](https://cloud.githubusercontent.com/assets/3313885/18623285/05ec74ca-7e59-11e6-9031-585f92bb9229.png)

# TODO:

* Implement front end visualizer application using Django to visualize the data
* Include calls basic statistical data such as most called number, most costliest call during that month, most called network ect.
* Add either one of the following material design libraries [material-ui](https://github.com/callemall/material-ui) > [materialize](https://github.com/Dogfalo/materialize) > [BS-material-design](https://github.com/FezVrasta/bootstrap-material-design) > [django-material](https://github.com/viewflow/django-material)

# Basic Usage

Download ebills and put them inside data directory, and use the *converter.sh* script to convert them to _.html_ file
run *data_extractor.py* by giving path to _<path_to_ebill>.html_ file

``` bash
python data_extractor.py <path_to_ebill>.html
```

# Disclaimer

This application is only developed for informative purpose of the individuals, No passwords nor username are required to use this application, all the relevant e-bills are required to download by user.

## Why Mobitel and who are they?

Well it is a mobile service provider in srilanka and i'm using their service for call , sms and data. That's it!
