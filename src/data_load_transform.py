import datetime
import json
import os

import pandas as p
from dotenv import find_dotenv, load_dotenv

LOAN_SCHEMA = {'Agency_Code': 'str',
               'Agency_Code_Description': 'str',
               'Applicant_Income_000': 'str',
               'As_of_Year': 'int64',
               'Census_Tract_Number': 'str',
               'Conforming_Limit_000': 'float64',
               'Conforming_Status': 'str',
               'Conventional_Conforming_Flag': 'str',
               'Conventional_Status': 'str',
               'County_Code': 'str',
               'County_Name': 'str',
               'FFIEC_Median_Family_Income': 'float64',
               'Lien_Status_Description': 'str',
               'Loan_Amount_000': 'int64',
               'Loan_Purpose_Description': 'str',
               'Loan_Type_Description': 'str',
               'MSA_MD': 'str',
               'MSA_MD_Description': 'str',
               'Number_of_Owner_Occupied_Units': 'float64',
               'Respondent_ID': 'str',
               'Sequence_Number': 'int64',
               'State': 'str',
               'State_Code': 'int64',
               'Tract_to_MSA_MD_Income_Pct': 'float64'}
INSTITUTION_SCHEMA = {'Agency_Code': 'str',
                      'As_of_Year': 'int64',
                      'Assets_000_Panel': 'int64',
                      'Parent_City_TS': 'str',
                      'Parent_Name_TS': 'str',
                      'Parent_State_TS': 'str',
                      'Parent_ZIP_Code': 'str',
                      'Respondent_City_TS': 'str',
                      'Respondent_ID': 'str',
                      'Respondent_Name_TS': 'str',
                      'Respondent_State_TS': 'str',
                      'Respondent_ZIP_Code': 'str'}


class DataLoadTransform(object):
    def __init__(self, data_dir=None):
        """
        Construct the paths to the data sources and load the raw data into pandas DataFrames
        """
        load_dotenv(find_dotenv())
        self.data_dir = data_dir or os.path.realpath(os.environ.get('DATA_DIR'))
        loans_file = os.path.join(self.data_dir, os.environ.get('LOANS_DATA'))
        institutions_file = os.path.join(self.data_dir, os.environ.get('INSTITUTIONS_DATA'))
        self.loans = p.read_csv(loans_file)
        self.loans = p.read_csv(loans_file, dtype=LOAN_SCHEMA,
                                na_values=['NA      ', 'NA    ', 'NA   ', 'NA', 'NA ', 'NA ', 'NaN', 'NAN', ''],
                                error_bad_lines=False, skipinitialspace=True)
        self.institutions = p.read_csv(institutions_file, dtype=INSTITUTION_SCHEMA,
                                       na_values=['NA      ', 'NA    ', 'NA   ', 'NA', 'NA ', 'NA ', 'NaN', 'NAN', ''],
                                       error_bad_lines=False, skipinitialspace=True)

    @staticmethod
    def make_query(kw):
        """
        Constructs a DataFrme query from the kw dictionary
        It is assumed that each key in the dictionary matches a column name in the DataFrame
        :param kw: Dictionary
        :return: string (query)
        """
        query = ''''''
        operator = ''
        parcount = sum([1 for x in kw.values() if x])
        for key, value in kw.items():
            parcount -= 1
            if value:
                operator = 'in' if type(value) == list else '=='
                value = str(value)
                query = ''' {} {} {} {} {}'''.format(query, key, operator, value, 'and' if parcount >= 1 else '')
        return query

    @staticmethod
    def group_loan_amount(x):
        """
        Buckets loan_amount_000 into reasonable groups
        similar to size grouping for clothing
        :param x:
        :return:
        """
        if x < 10:
            return 'XS (0-10,000)'
        elif x < 100:
            return 'S (10,000-100,000)'
        elif x < 500:
            return 'M (100,000-500,000)'
        elif x < 1000:
            return 'L (500,000-1000,000)'
        elif x < 5000:
            return 'XL (1000,000-5000,000)'
        else:
            return 'XXL (5,000,000+)'

    def hmda_init(self):
        """
        Merges loan and institution DataFrames and returns a left merged dataframe [by As_of_Year, Respondent_ID
        and Agency_Code] that has an additional column (Respondent_Name_TS)
        :return: pandas DataFrame
        """
        expanded_df = self.loans.merge(
            self.institutions[['As_of_Year', 'Respondent_ID', 'Agency_Code', 'Respondent_Name_TS']],
            how='left', on=['As_of_Year', 'Respondent_ID', 'Agency_Code'])
        expanded_df['Loan_Amount_Bucket'] = expanded_df.Loan_Amount_000.apply(DataLoadTransform.group_loan_amount)
        return expanded_df

    def hmda_to_json(self, data, states=None, conventional_conforming=None, **kw):
        """
        Exports the expanded data set to disk for the selected states and conventiontional_conforming values
        grouped by product segment.
        :param states: list of states
        :param conventional_conforming: Boolean True, False or None(select all without filtering)
        :param kw: key=value (key has to match name of column in the dataframe)
        :return: True if export is successful
        """
        kw.update(
            dict(State=states, Conventional_Conforming_Flag=conventional_conforming)
        )
        query = DataLoadTransform.make_query(kw)
        if query and "" < query:
            data.query(DataLoadTransform.make_query(kw), inplace=True)

        fname = "loans_by_product_segment_{}.json".format(datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
        output_path = os.path.join(self.data_dir, 'processed', fname)
        try:
            data_dict = json.loads(data.head(5).to_json(orient='records'))
            with open(output_path, 'w+', encoding='utf-8') as f:
                json.dump(data_dict, f, sort_keys=True)
        except:
            raise Exception("Export to json Unsuccessful")

        return True


if __name__ == '__main__':
    dlt = DataLoadTransform()
    df = dlt.hmda_init()
    dlt.hmda_to_json(df, As_of_Year=[2013, 2014, 2012])
