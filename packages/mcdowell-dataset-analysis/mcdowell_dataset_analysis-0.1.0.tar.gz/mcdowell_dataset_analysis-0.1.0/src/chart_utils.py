import pandas as pd
import matplotlib.pyplot as plt

class ChartUtils:
    """
    This class contains utility functions for working with dataframes and generating charts.
    """
    
    def pivot_dataframe(df, index_col, column_col, value_col):
        """
        Index_col is used as the row index of the pivoted dataframe.
        Column_col specifies the values that become the new columns of the pivoted dataframe.
        Value_col specifies the values that fill the new DataFrame, at the interscetion of the index and column values.
        
        Example:
        >>> df = pd.DataFrame({
        ...     'Launch_Date': ['2020-01-01', '2020-01-01', '2020-02-01'],
        ...     'Launch_Pad': ['SLC4E', 'LC39A', 'SLC4E'],
        ...     'Apogee': [550, 600, 560]
        ... })
        >>> pivot_dataframe(df, 'Launch_Date', 'Launch_Pad', 'Apogee')
           Launch_Date  LC39A  SLC4E
        0  2020-01-01  600.0  550.0
        1  2020-02-01    NaN  560.0
        
        Raises:
            ValueError: If the pivot operation results in duplicate entries for an index-column combination.
        
        See Pandas documentation for more details:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html
        """
        pivoted = df.pivot(index=index_col, columns=column_col, values=value_col)
        pivoted = pivoted.reset_index().sort_values(by=index_col)
        return pivoted

    def bin_dataframe(df, value_col, bins, labels):
        """
        Sort groups into discrete bins (eg. intervals of payload mass) and count how many data points fall into each bin.
        
        Eg. mass bins and labels:
        bins = [0,1000,2000,3000]
        mass_labels = ['0-1T','1-2T','2-3T']
        
        Notice that labels are between the bins. The bins variable specifies the edges of the bins.
        """
        binned = pd.cut(df[value_col], bins=bins, labels=labels, include_lowest=True).value_counts()
        return binned.reindex(labels)

    def plot_scatter(df, x_col, y_cols, title, xlabel, ylabel, output_path, figsize=(10, 6)):
        """
        Generate a scatter plot for multiple y-columns against an x-column.
        """
        plt.figure(figsize=figsize)
        for col in y_cols:
            plt.scatter(df[x_col], df[col], label=col, alpha=0.7)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(title=y_cols.name if hasattr(y_cols, 'name') else 'Series')
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()
        print(f"Plot saved as '{output_path}'.")

    def plot_histogram(df, title, xlabel, ylabel, output_path, stacked=True, figsize=(10, 6)):
        """
        Generate a histogram-like plot for a DataFrame with binned data.
        """
        plt.figure(figsize=figsize)
        df.plot(kind='bar', stacked=stacked)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        
        print(f"Plot saved as '{output_path}'.")