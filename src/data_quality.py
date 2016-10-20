import datetime
import os

import numpy as np
from dotenv import find_dotenv, load_dotenv

from data_load_transform import DataLoadTransform


def check_missing(data, col):
    """
    If col is string, check length else assume it is numeric and find nan rows
    :param data:
    :param col:
    :return:
    """
    if data[col].dtype in ['str', 'O']:
        nans_df = data[data[col].str.strip().str.len() <= 3][data[col].str.upper().str.contains('NA')]
        nans = nans_df.index.values
    else:
        nans = np.where(list(np.isnan(data[col])))[0]
    return list(nans)


def check_type(df, col):
    pass


def check_outlier_mad(col):
    """
    Using Median Absolute Deviation to identify outliers

    :param df:
    :param col:
    :return:
    """
    ZSCORE_THRESHOLD = 6
    if col.dtype not in [float, int]:
        raise ValueError("Array is not numeric")
    median = np.median(col)
    deviation = np.abs(col - median)
    mad = np.median(deviation)
    mod_zscore = 0.6745 * deviation / mad

    return list(np.where(mod_zscore > ZSCORE_THRESHOLD)[0])


def check_duplicate(data, name):
    """
    Checks for duplicate records in the passed DataFrame
    :param df:
    :return:
    """
    # Composite key
    key_cols = ['Agency_Code', 'Respondent_ID', 'As_of_Year'] \
        if name == 'institutions' else ['Agency_Code', 'Respondent_ID', 'As_of_Year', 'Sequence_Number']

    data_unique_count = data[key_cols].count().reset_index()

    columns = data_unique_count.columns.values
    columns[-1] = 'Row_Count'
    data_unique_count.columns = columns
    duplicate_rows = data_unique_count[data_unique_count.Row_Count > 1]
    return duplicate_rows if duplicate_rows.shape[0] > 0 else None


def dq_report(data, col, data_name):
    load_dotenv(find_dotenv())
    data_dir = os.path.realpath(os.environ.get('DQ_REPORT_DIR'))
    today = datetime.datetime.now().strftime("%Y%m%d")
    fname = "{}_data_quality_report_{}.txt".format(data_name, today)
    output_path = os.path.join(data_dir, fname)

    with open(output_path, 'w+') as file:
        file.write("Data Quality Report" + os.linesep)
        nans_list = check_missing(data, col)
        file.writelines("Records with missing {}: ".format(col))
        file.writelines(str(len(nans_list)) if np.any(nans_list) else "No missing {0} records {1}".format(
            col, os.linesep))
        duplicates_df = check_duplicate(data, data_name)
        file.writelines("Duplicate records: {}".format(
            str(duplicates_df.shape[0])) if duplicates_df is not None else "No duplicate records" + os.linesep)
        if data[col].dtype in ['str', 'O']:
            col_new = data[col].str.len()
            outliers_list = check_outlier_mad(col_new)
        else:
            outliers_list = check_outlier_mad(data[col])
        file.writelines(
            "Outlier records: {}".format(str(len(outliers_list))) if outliers_list else "No outliers in {}".format(
                col) + os.linesep)

    for j, k in zip(['missing', 'duplicate', 'outliers'], [nans_list, duplicates_df, outliers_list]):
        file_name = "{}_{}_records_{}.csv".format(data_name, j, today)
        path = os.path.join(data_dir, file_name)
        data.loc[k].to_csv(path, index=False) if type(k) == list else k.to_csv(path, index=False)


if __name__ == '__main__':
    dlt = DataLoadTransform()
    loans = dlt.loans
    institutions = dlt.institutions
    dqcols = 'Loan_Amount_000'
    dq_report(loans, dqcols, 'loans')
    dqcols = 'Respondent_Name_TS'
    dq_report(institutions, dqcols, 'institutions')
