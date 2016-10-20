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


-- data_challenge
   - data           
   - notebooks         
   - reports
       - data_quality
       - files.csv(txt)
       - analysis.html 
   - src
       - data_load_transform.py
       - data_quality.py
       - visuals.py
   - .env
   - README.md
   - requirements.txt
   - environment.yml
    
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


... Analysis can be done by using jupyter notebook, first importing objects from `data_load_transform.py` and loading and transforming the data then importing `visuals.py` to find custom plotting functions that will use the data passed to them and plot a number of visualizations.

`./notebooks` directory has `analysis.ipynb` file with full analysis and plots. 
 
 - Also, an html version of the analysis can be found under `./reports`

--------

