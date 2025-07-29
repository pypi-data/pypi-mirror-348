import pandas as pd
from dataset_launch import Launch
from dataset_satcat import Satcat
from dataframe_filters import Filters
from translations import Translation
from chart_utils import ChartUtils

# Expose Launch and Satcat directly in this module's namespace
__all__ = ['Launch', 'Satcat', 'Filters', 'McdowellDataset', 'Translation', 'ChartUtils']

class McdowellDataset:
    """
    This class serves as a wrapper for the Launch and Satcat classes, providing a unified interface for analysis.
    """
    
    def __init__(self):
        self.translation = Translation()
        
        self.launch = Launch(self.translation)
        self.satcat = Satcat(self.translation)
        
        self.launch.process_satcat_dependent_columns(self.satcat)
        self.satcat.process_launch_dependent_columns(self.launch)
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
    
    def reload(self):
        self.launch.reload()
        self.satcat.reload()