Capital One Data Challenge - HMDA Data Analysis and Processing
==============================

_Analysis of HMDA data to understand home loans market in Washington DC and the surrounding area_

------------

This tool enables us to analyze HMDA data for the years 2012 to 2014 and gives us insight on how Change Financial can enter the home loans market.

## Code Organization


+ data_challenge
- data           
- notebooks         
- reports
- data_quality
- files.csv
    - analysis.html 
- src
- data_load_transform.py
- data_quality.py
- visuals.py
- .env
- README.md
- requirements.txt
- environment.yml

## Data

The data for this project was obtained from the Consumer Financial Protection Bureau

The following data are used for the analysis (as obtained from the metadata included with the source data files)

### Metadata

<table>
  <thead>
    <tr><th>Data file(s)</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>2012_to_2014_loans_data.csv</td>
      <td>Data on home loans originated within the states where Change Financial Operates.</td>
    </tr>
    <tr>
      <td>2012_to_2014_institutions_data.csv</td>
      <td>Data about the originating institutions as submitted by the institutions themselves</td>
    </tr>
  </tbody>
</table>

Here is the schema of the expanded loans data.

<table style="height: 477px;" width="315">
  <thead>
    <tr><th>Field</th><th>Type</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>As_of_Year</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Agency_Code</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Agency_Code_Description</td>
      <td>string</td>
    </tr>
    <tr>
      <td>Respondent_ID</td>
      <td>string</td>
    </tr>
    <tr>
      <td>Sequence_Number</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Loan_Amount_000</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Applicant_Income_000</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Loan_Purpose_Description</td>
      <td>string</td>
    </tr>
    <tr>
      <td>Loan_Type_Description</td>
      <td>string</td>
    </tr>
    <tr>
      <td>Lien_Status_Description</td>
      <td>string</td>
    </tr>
    <tr>
      <td>State_Code</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>State</td>
      <td>string</td>
    </tr>
    <tr>
      <td>County_Code</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>MSA_MD</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>MSA_MD_Description</td>
      <td>string</td>
    </tr>
    <tr>
      <td>Census_Tract_Number</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>FFIEC_Median_Family_Income</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Tract_to_MSA_MD_Income_Pct</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Number_of_Owner_Occupied_Units</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>County_Name</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Conforming_Limit_000</td>
      <td>integer</td>
    </tr>
    <tr>
      <td>Conventional_Status</td>
      <td>string</td>
    </tr>
    <tr>
      <td>Conforming_Status</td>
      <td>string</td>
    </tr>
    <tr>
      <td>Conventional_Conforming_Flag</td>
      <td>string</td>
    </tr>
    <tr>
      <td>Respondent_Name_TS</td>
      <td>string</td>
    </tr>
  </tbody>
</table>


## Getting Started


To get started, setup a new environment (preferably using anaconda) according to `./environment.yml` or `requirements.txt` file

Using pip environment can be setup as follows,

``` pip install -r requirements.txt```



#### Data Munging


As per the requirements for the project, data munging is done by running the data_load_transform.py module. The module will load institution and loan data, left join loans data with institutions then create a loan_bucket categorical variable then dump a json version of the expanded data into `./data/processed` directory. 

To run the data munging module, go into the `./src` subdirectory and type the following in your terminal

``` python data_load_transform.py ```

This will create a new json file in the `./data/processed` directory that contains the merged loan and institution data and additional column (loan_amount_bucket)


#### Data Quality


Data quality in this case is limited to quality reporting in this iteration of this product. Quality reporting is currently available for two columns in the expanded dataset (_Respondent_Name_TS_ and _Loan_Amount_000_)

The module checks for records with missing values for the selected variables, duplicate records and outliers (using _Median Absolute Deviation_ method)

To run the data quality module, navigate to the `./src` subdirectory and type the following in your terminal

``` python data_quality.py ```

The module will provide a summary of the quality issues for the day and export records with data quality issues in different files according to the issue type

#### Analysis


Analysis can be done by using jupyter notebook, first importing objects from `data_load_transform.py` and loading and transforming the data then importing `visuals.py` to find custom plotting functions that will use the data passed to them and plot a number of visualizations.

`./notebooks` directory has `analysis.ipynb` file with full analysis and plots. 

An html version of the analysis can be found under `./reports`

--------

