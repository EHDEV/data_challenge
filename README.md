Capital One Data Challenge
==============================

Analysis of HMDA data to understand home loans market in Washington DC and the surrounding area

Project Organization
------------

# Change Financial - HMDA Data Analysis and Processing

This tool enables us to analyze HMDA data for the years 2012 to 2014 and gives us insight on how Change Financial can enter the home loans market.

### Data

The data for this project came from the Home Mortgage Disclosure Act reporting 

#### Metadata



### Code Organization

├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.or

├── data_challenge
│   ├── data           
│   ├── notebooks         
│   ├── reports
│       ├── data_quality
│       ├── files.csv(txt)
│       └── analysis.html 
│   ├── src
│       ├── data_load_transform.py
│       ├── data_quality.py
│       └── visuals.py
│   ├── .env
│   ├── README.md
│   ├── requirements.txt
│   └── environment.yml
    
### Getting Started

To get started, setup a new environment (preferably using anaconda) according to `./environment.yml` or `requirements.txt` file

##### Data Munging

As per the requirements for the project, data munging is done by running the data_load_transform.py module. The module will load institution and loan data, left join loans data with institutions then create a loan_bucket categorical variable then dump a json version of the expanded data into `./data/processed` directory. 

To run the data munging module, go into the `./src` subdirectory and type the following in your terminal

``` python data_load_transform.py ```

This will create a new json file in the `./data/processed` directory that contains the merged loan and institution data and additional column (loan_amount_bucket)

##### Data Quality

Data quality in this case is limited to quality reporting in this iteration of this product. Quality reporting is currently available for two columns in the expanded dataset (_Respondent_Name_TS_ and _Loan_Amount_000_)
- The module checks for records with missing values for the selected variables, duplicate records and outliers (using _Median Absolute Deviation_ method)

To run the data quality module, navigate to the `./src` subdirectory and type the following in your terminal

``` python data_quality.py ```

The module will provide a summary of the quality issues for the day and export records with data quality issues in different files according to the issue type

##### Analysis

Analysis can be done by using jupyter notebook, first importing objects from `data_load_transform.py` and loading and transforming the data then importing `visuals.py` to find custom plotting functions that will use the data passed to them and plot a number of visualizations.

`./notebooks` directory has `analysis.ipynb` file with full analysis and plots. 
 
 - Also, an html version of the analysis can be found under `./reports`

--------

