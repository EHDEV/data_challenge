Capital One Data Challenge
==============================

Analysis of HMDA data to understand home loans market in Washington DC and the surrounding area

# Change Financial - HMDA Data Analysis and Processing
------------

This tool enables us to analyze HMDA data for the years 2012 to 2014 and gives us insight on how Change Financial can enter the home loans market.

## Data

The data for this project came from the Home Mortgage Disclosure Act reporting 

### Metadata

<table>
<thead><tr>
<th>Field</th>
<th>Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>As_of_Year</td>
<td>integer</td>
<td>Year in which loan was originated and for which the data was reported. Keep in mind these are real people reporting data, and often variations can crop up in how they handle each year</td>
</tr>
<tr>
<td>Agency_Code</td>
<td>alphanumeric</td>
<td>The agency to which the Respondent_ID "responded" with its information</td>
</tr>
<tr>
<td>Agency_Code_Description</td>
<td>string</td>
<td>Expanded form of the agency code for readability.</td>
</tr>
<tr>
<td>Respondent_ID</td>
<td>string</td>
<td>When paired with the Agency_Code, provides a unique identifier for the institution that year.</td>
</tr>
<tr>
<td>Sequence_Number</td>
<td>integer</td>
<td>Provides a unique identifier corresponding to an application or loan for a given responding insitution. I.e., each application at a responding institution must be assigned its own unique sequence number in a given year.</td>
</tr>
<tr>
<td>Loan_Amount_000</td>
<td>integer</td>
<td>Amount of the loan, in $000's</td>
</tr>
<tr>
<td>Applicant_Income_000</td>
<td>integer</td>
<td>The total income used for decisioning the loan</td>
</tr>
<tr>
<td>Loan_Purpose_Description</td>
<td>string</td>
<td>The purpose of the loan is whether it was used for purchasing a home, refinancing an alread-existing loan, or used for "home improvement" purposes. ("Home Improvement" loans have been removed from this data file.)</td>
</tr>
<tr>
<td>Loan_Type_Description</td>
<td>string</td>
<td>Specifies whether the loan was "conventional," i.e., not backed by a government-sponsored program or government-insured or government-guaranteed</td>
</tr>
<tr>
<td>Lien_Status_Description</td>
<td>string</td>
<td>Lien position of the loan. If first lien position, then this loan carries the least risk if the borrower defaults because the lender has first claims to proceeds from the sale of a some. Subordinate liens carry more risk because they are paid after the lender for the first lien is paid.</td>
</tr>
<tr>
<td>State_Code</td>
<td>alphanumeric</td>
<td>Two-digit FIPS code for the state in which the home was located.</td>
</tr>
<tr>
<td>State</td>
<td>string</td>
<td>Standard 2-letter postal code for the state based on the State_Code given</td>
</tr>
<tr>
<td>County_Code</td>
<td>alphanumeric</td>
<td>Numeric code designating a county within a state in which the home was located</td>
</tr>
<tr>
<td>MSA_MD</td>
<td>alphanumeric</td>
<td>code designating a Metropolitan Statistical Area (MSA) / Metropolitan Division (MD) in which the home was located. These codes are periodically updated, and were last updated for HMDA between the 2013 and 2014 reporting years.</td>
</tr>
<tr>
<td>MSA_MD_Description</td>
<td>string</td>
<td>a human-readable format for describing MSA's. These map 1:1 with MSA_MD codes</td>
</tr>
<tr>
<td>Census_Tract_Number</td>
<td>alphanumeric</td>
<td>Identifier for the census tract in which the home was located</td>
</tr>
<tr>
<td>FFIEC_Median_Family_Income</td>
<td>alphanumeric</td>
<td>Median family income for the MSA/MD in which the census tract is located</td>
</tr>
<tr>
<td>Tract_to_MSA_MD_Income_Pct</td>
<td>alphanumeric</td>
<td>Percentage of the MSA/MD median Family income for the census tract; 2 decimal places of precsion</td>
</tr>
<tr>
<td>Number_of_Owner_Occupied_Units</td>
<td>alphanumeric</td>
<td>Number of units, in the census tract and including condominiums, in which the owner lives</td>
</tr>
<tr>
<td>County_Name</td>
<td>alphanumeric</td>
<td>Name of the county as pulled in from the <a href="http://www.fhfa.gov/DataTools/Downloads/Pages/Conforming-Loan-Limits.aspx">FHFA Conforming Loan Limits</a> as calculated under HERA. Please note that county names are only unique within a state</td>
</tr>
<tr>
<td>Conforming_Limit_000</td>
<td>numeric</td>
<td>Single Unit Conforming Loan limit for the given county.</td>
</tr>
<tr>
<td>Conventional_Status</td>
<td>string</td>
<td>Signifies whether a loan type is '1' or not.</td>
</tr>
<tr>
<td>Conforming_Status</td>
<td>string</td>
<td>'Conforming' for loans with amounts less than their county's respective conforming loan limit. "Jumbo" if the loan amount exceeds the county limit</td>
</tr>
<tr>
<td>Conventional_Conforming_Flag</td>
<td>string</td>
<td>'Y' if Conventional_Status is "Conventional" and "Conforming_Status" is "Conforming"</td>
</tr>
</tbody>
</table>

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
   
    
## Getting Started


   To get started, setup a new environment (preferably using anaconda) according to `./environment.yml` or `requirements.txt` file


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

