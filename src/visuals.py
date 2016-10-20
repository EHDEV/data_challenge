import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm


def plot_asofyear(data, group_col, kind='area', top_ten=True):
    """
    Plots Market size by Year and the passed parameter group_col
    :param data:
    :param group_col:
    :param kind:
    :param top_ten:
    :return: None
    """
    agg_group_year = data[['Loan_Amount_000', group_col, 'As_of_Year']] \
        .groupby([group_col, 'As_of_Year']) \
        .agg({"Loan_Amount_000": {'Total_Amount_(000,000)': 'sum', 'Median_(000,000)': 'median',
                                  'Loans_Volume_(000)': 'count'}}) \
        .reset_index().sort_values(by=['As_of_Year', group_col])

    agg_group_year.columns = [''.join(col).strip().replace('Loan_Amount_000', '') for col in
                              agg_group_year.columns.values]

    # Top 10 by loan volume
    tops = data[['Loan_Amount_000', group_col]].groupby(group_col).count().reset_index()
    tops = tops.sort_values(by='Loan_Amount_000', ascending=False) \
               .iloc[:min(10, agg_group_year.shape[0]) if top_ten else None]
    tops = list(tops[group_col].unique())

    # Calculating Percentage change year to year
    cols = ['Loans_Volume_(000)', 'Median_(000,000)', 'Total_Amount_(000,000)']

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.reshape(4)
    sns.set_style("whitegrid")
    cmap = cm.get_cmap('Dark2', 11)
    for i in range(len(cols)):
        tmp = agg_group_year.sort_values(by='Loans_Volume_(000)', ascending=False)

        # Reducing the number of digits for better display of the y-ticks in plot
        tmp[cols[i]] /= 1000
        tmp = tmp.sort_values(by=['As_of_Year', group_col])[['As_of_Year', cols[i], group_col]] \
            .pivot('As_of_Year', group_col, cols[i])
        tmp.index = [str(x) for x in tmp.index]
        tmp = tmp[tops]

        # Calculating the percentage of each group in Volume of Loans
        tmp_perc = tmp.apply(lambda c: np.round(c / c.sum() * 100, 2), axis=1)

        # Plotting on a (2,2) panel
        axes[i].set_title(cols[i])
        fig.tight_layout(pad=3)
        tmp.plot(kind=kind, stacked=True, legend=None, ax=axes[i], cmap=cmap)
        handles, labels = axes[0].get_legend_handles_labels()
        lg = axes[1].legend(handles, labels, bbox_to_anchor=(1.3, 1), loc=0, fontsize=10)
        for lo in lg.legendHandles:
            lo.set_linewidth(10)
    fig.suptitle("Loan Amount Stats Aggregated by {}".format(group_col), fontsize=14, verticalalignment='top')
    axx = axes[-1]

    tmp_perc.plot.barh(stacked=True, ax=axx, legend=None, cmap=cmap)
    axx.xaxis.set_visible(False)
    #     axx.yaxis.set_visible(False)

    # Plotting a table with the percentage values
    tp_tup = [tmp_perc[c] for c in tmp_perc.columns]
    try:
        tb = plt.table(cellText=tp_tup,
                       colWidths=[0.3] * len(tmp_perc.columns),
                       rowLabels=' ' + tmp_perc.columns + ' (%)', colLabels=tmp_perc.index,
                       cellLoc='center', rowLoc='center', fontsize=9)

        tb.set_fontsize(12)
    except IndexError:
        pass


def plot_loan_purpose(data, secondary_group_by, primary_group_by='Loan_Purpose_Description', top=True, year=None,
                      title='', ylab='', xlab='', data_col="Loans Volume", kind='bar'):
    """
    Plots Loan Volume broken down by Loan Purpose and passed parameter group_col

    :param year:
    :param data:
    :param primary_group_by:
    :param secondary_group_by:
    :param top:
    :param title:
    :param ylab:
    :param xlab:
    :param data_col:
    :param kind:
    :return:
    """

    # Aggregating loans by the primary and secondary group by columns
    if year:
        data = data[data.As_of_Year == year]

    aggregated = data[['Loan_Amount_000', primary_group_by, secondary_group_by]] \
        .groupby([primary_group_by, secondary_group_by]) \
        .agg({"Loan_Amount_000": {'Total(000)': 'sum', 'Average(000)': 'mean', 'Median(000)': 'median',
                                  data_col: 'count'}}).reset_index()

    # Getting the names of the top 10 States/Counties/Metropolitan Divisions/etc by loan volume
    tops = data[['Loan_Amount_000', secondary_group_by]].groupby(secondary_group_by).count().reset_index()
    tops = tops.sort_values(by='Loan_Amount_000', ascending=False) \
               .iloc[:min(20, tops.shape[0]) if top else None]
    tops = list(tops[secondary_group_by].unique())
    aggregated.columns = [''.join(col).strip().replace('Loan_Amount_000', '') for col in aggregated.columns.values]
    aggregated = aggregated.sort_values(by=[data_col, secondary_group_by, primary_group_by], ascending=False)
    aggregated.index = [str(x) for x in aggregated.index]

    # Subsetting only rows with matching secondary group by values as in tops
    aggregated = aggregated[aggregated[secondary_group_by].isin(tops)]

    # Plotting the graph
    sns.set(style="whitegrid")
    g = sns.factorplot(x=secondary_group_by, y=data_col, hue=primary_group_by, data=aggregated,
                       kind=kind, size=8, palette="muted", legend_out=False)

    g.set_xticklabels(labels=aggregated[secondary_group_by].unique(), rotation=90, fontsize=8)

    g.set_yticklabels(fontsize=8)
    g.despine(left=True)
    g.set_ylabels(ylab)
    g.set_xlabels(xlab)
    g.set(title=title)
    plt.tight_layout(pad=5)
