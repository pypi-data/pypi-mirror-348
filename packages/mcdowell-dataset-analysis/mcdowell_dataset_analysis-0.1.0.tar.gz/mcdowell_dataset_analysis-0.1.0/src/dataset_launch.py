import pandas as pd
import translations

class Launch:
    """
    This contains all functions required for using McDowell's launch dataset.
    """

    def __init__(self, translation=None, file_path="./datasets/launch.tsv"):
        """
        Initialize launch tsv file path and load the dataset into a pandas DataFrame.
        
        Launch.tsv column descriptions: https://planet4589.org/space/gcat/web/launch/lcols.html
        """
    
        self.file_path = file_path
        self.translation = translation or translations.Translation() # beautiful pythonic syntax!
        
        self.df = pd.read_csv(self.file_path, sep="\t", encoding="utf-8") # load tsv into dataframe
        
        self.preprocess_launch_df()

    def reload(self):
        """ 
        Undo all filters
        """
        self.__init__(translation=self.translation, file_path=self.file_path)
    
    def preprocess_launch_df(self):
        """
        Create new columns from existing columns in satcat dataframe to make it more pandas friendly.
        Lots of string manipulation to get the dates into a format that pandas can understand.
        """
        
        # Remove second row of tsv, signifies date of last update
        self.df = self.df.drop(index=0).reset_index(drop=True)
        
        # Rename column "#Launch_Tag" to "Launch_Tag"
        self.df.rename(columns={"#Launch_Tag": "Launch_Tag"}, inplace=True)
        
        # Strip Launch_Tags
        self.df["Launch_Tag"] = self.df["Launch_Tag"].astype(str).str.upper().str.strip()
        self.df["LV_Type"] = self.df["LV_Type"].astype(str).str.strip()
        
        date_cols = ["Launch_Date"]
        for col in date_cols:
            # Remove problematic characters from date columns (?, -) and handle NaN
            self.df[col] = self.df[col].str.strip().fillna("").str.replace(r"[?-]", "", regex=True).str.strip()
            # Replace double space "  " with single space " " - Sputnik 1 edge case!
            self.df[col] = self.df[col].str.replace(r"\s{2,}", " ", regex=True).str.strip()
            # Only include characters before the third space in all date columns (Remove hour/min/sec as unneeded and messes with data frame time formatting)
            self.df[col] = self.df[col].str.split(" ", n=3).str[:3].str.join(" ").str.strip()
            # Add " 1" to the end of all dates that only contain year and month (assuming this is all 8 character dates) eg. "2023 Feb" -> "2023 Feb 1"
            self.df[col] = self.df[col].where(self.df[col].str.len() != 8, self.df[col] + " 1")
            # Convert Mcdowell's Vague date format to pandas datetime format
            self.df[col] = pd.to_datetime(self.df[col], format="%Y %b %d", errors="coerce")

        self.df["Simple_Orbit"] = self.df["Category"].str.split(" ").str[1].str.strip() # Extract orbit from category eg. "Sat SSO SD 0"
        self.df["Simple_Orbit"] = self.df["Simple_Orbit"].where(self.df["Simple_Orbit"].isin(self.translation.launch_category_to_simple_orbit.keys()), float("nan")) # If raw orbit not present in dictionary keys, NaN
        self.df["Simple_Orbit"] = self.df["Simple_Orbit"].replace(self.translation.launch_category_to_simple_orbit) # Translate to simple orbit

        self.df["Launch_Vehicle_Family"] = self.df["LV_Type"].map(self.translation.lv_type_to_lv_family) # Translate LV_Type to LV_Family using the translation dictionary
        
        self.df["State"] = self.df["Launch_Site"].map(self.translation.launch_site_to_state_code) # Translate Launch_Site to State using the translation dictionary
        self.df["Country"] = self.df["State"].map(self.translation.state_code_to_state_name)
        
        self.df["Launch_Site_Parent"] = self.df["Launch_Site"].map(self.translation.launch_site_to_launch_site_parent)
        self.df["Launch_Site_Name"] = self.df["Launch_Site_Parent"].map(self.translation.launch_site_to_launch_site_name) # Translate Launch_Site to Launch_Site_Name using the translation dictionary

    def process_satcat_dependent_columns(self, satcat):
        """
        Create columns in launch_df derived from satcat data:
        - Payload_Mass: Sum of masses for all payloads in a launch
        - Canonical Orbit Parameters: [ODate, Ap, Pe, Inc, OpOrbit, Simple Orbit]
        Args:
            satcat_df: DataFrame containing the satcat class.
        """
        
        satcat_df = satcat.df.copy()
        
        payload_masses = (
            satcat_df
            .loc[satcat_df['Type'].str.startswith('P', na=False)] # Keep only payloads from satcat
            .groupby('Launch_Tag')['Mass'] # Group by launch tag and sum the masses of the payloads
            .sum()
        )
        
        # Create new column in launch_df for payload mass
        self.df['Payload_Mass'] = self.df['Launch_Tag'].map(payload_masses)
        
        #pick the first payload row for every Launch_Tag
        first_payload = (
            satcat_df
              .loc[satcat_df['Type'].str.startswith('P', na=False)]
              .drop_duplicates('Launch_Tag', keep='first')
              .set_index('Launch_Tag')
        )
        
        # Create new columns in launch_df for canonical orbit data
        for col in ['Orbit_Canonical_Date', 'Perigee', 'Apogee', 'Inc', 'OpOrbit']:
            self.df[col] = self.df['Launch_Tag'].map(first_payload[col])
