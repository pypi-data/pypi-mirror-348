import csv
import sys

class Translation:
    """
    This class contains all functions required for translating columns into more pandas or user friendly formats.
    
    This is a class because some translation dictionaries like lv_translation require a file to be read in.
    """
    
    # Define static translation dictionaries that don't require reading a tsv
    opOrbit_to_simple_orbit = {
        "ATM": "SO",      # Atmospheric
        "SO": "SO",        # Suborbital
        "TA": "SO",        # Trans-Atmospheric
        "LLEO/E": "LEO",   # Lower LEO/Equatorial
        "LLEO/I": "LEO",   # Lower LEO/Intermediate
        "LLEO/P": "SSO",   # Lower LEO/Polar
        "LLEO/S": "SSO",   # Lower LEO/Sun-Sync
        "LLEO/R": "LEO",   # Lower LEO/Retrograde
        "LEO/E": "LEO",    # Upper LEO/Equatorial
        "LEO/I": "LEO",    # Upper LEO/Intermediate
        "LEO/P": "SSO",    # Upper LEO/Polar
        "LEO/S": "SSO",    # Upper LEO/Sun-Sync
        "LEO/R": "LEO",    # Upper LEO/Retrograde
        "MEO": "MEO",      # Medium Earth Orbit
        "HEO": "HEO",      # Highly Elliptical Orbit
        "HEO/M": "HEO",    # Molniya
        "GTO": "GTO",      # Geotransfer
        "GEO/S": "GEO",    # Stationary
        "GEO/I": "GEO",    # Inclined GEO
        "GEO/T": "GEO",    # Synchronous
        "GEO/D": "GEO",    # Drift GEO
        "GEO/SI": "GEO",   # Inclined GEO (same as GEO/I)
        "GEO/ID": "GEO",   # Inclined Drift
        "GEO/NS": "GEO",   # Near-sync
        "VHEO": "HEO",    # Very High Earth Orbit
        "DSO": "BEO",      # Deep Space Orbit
        "CLO": "BEO",      # Cislunar/Translunar
        "EEO": "BEO",      # Earth Escape
        "HCO": "BEO",      # Heliocentric
        "PCO": "BEO",      # Planetocentric
        "SSE": "BEO"       # Solar System Escape
    }
    
    # Note:
    # There might be some edge cases where a satcat simple orbit is SSO
    # while launch simple orbit is LEO.
    # Eg. satcat raw orbit "LEO/P" while launch raw orbit "LEO"
    launch_category_to_simple_orbit = {
        "DSO": "BEO",    # Deep space orbit
        "EEO": "BEO",    # Earth escape orbit
        "GEO": "GEO",    # Direct geosync insertion
        "GTO": "GTO",    # Geosync transfer orbit
        "HEO": "HEO",    # Highly elliptical orbit
        "ISS": "LEO",    # International Space Station
        "LEO": "LEO",    # Low Earth Orbit
        "LSS": "LEO",    # LEO space station other than ISS
        "MEO": "MEO",    # Medium Earth Orbit
        "MOL": "HEO",    # Molniya orbit
        "MTO": "MEO",    # MEO transfer orbit
        "SSO": "SSO",    # Sun-sync orbit
        "STO": "GTO",    # Supersync transfer orbit
        "XO": "BEO"      # Extraterrestrial launch
    }
    
    payload_category_to_simple_payload_category = {
        "AST": "Observation",
        "IMG": "Observation",
        "IMGR": "Observation",
        "MET": "Observation",
        "METRO": "Observation",
        "COM": "Communications",
        "NAV": "Communications",
        "BIO": "Science",
        "GEOD": "Science",
        "MGRAV": "Science",
        "SCI": "Science",
        "EW": "Military",
        "SIG": "Military",
        "TARG": "Military",
        "WEAPON": "Military",
        "TECH": "Tech Demo",
        "CAL": "Other",
        "EDU": "Other",
        "INF": "Other",
        "MISC": "Other",
        "RB": "Other",
        "RV": "Other",
        "PLAN": "Other",
        "SS": "Other"
    }
    
    def __init__(self):
        self.generate_lv_type_to_lv_family()
        self.generate_launch_site_to_state_code()
        self.generate_org_to_state_code()
        self.generate_state_code_to_state_name()
        self.generate_launch_site_to_launch_site_parent()
        self.generate_launch_site_to_launch_site_name()

    def generate_lv_type_to_lv_family(self, filePath = "./datasets/lv.tsv"):
        """
        Generate a dictionary that translate LV_Type to LV_Family.
        This requires lv.tsv file
        Launch Vehicle Families Text File: https://planet4589.org/space/gcat/web/lvs/family/index.html
        """
        
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            reader.__next__() # Skip the index row
            reader.__next__() # Skip the header row
            self.lv_type_to_lv_family = {row[0].strip(): row[1].strip() for row in reader}
            
    def generate_launch_site_to_state_code(self, filePath = "./datasets/sites.tsv"):
        """
        Generate a dictionary that translate Launch_Site to State_Code.
        This requires launch_site.tsv file
        Launch Sites Text File: https://planet4589.org/space/gcat/data/tables/sites.html
        """
        
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            reader.__next__() # Skip the index row
            reader.__next__() # Skip the header row
            self.launch_site_to_state_code = {row[0].strip(): row[4].strip() for row in reader}
            
    def generate_org_to_state_code(self, filePath = "./datasets/orgs.tsv"):
        """
        Generate a dictionary that translate Launch_Site to State_Code.
        This requires orgs.tsv file
        Launch Sites Text File: https://planet4589.org/space/gcat/data/tables/orgs.html
        """
        
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            reader.__next__() # Skip the index row
            reader.__next__() # Skip the header row
            self.org_to_state_code = {row[0].strip(): row[2].strip() for row in reader}
            
    def generate_state_code_to_state_name(self, filePath = "./datasets/orgs.tsv"):
        """
        Generate a dictionary that translate State_Code to State_Name.
        This requires orgs.tsv file
        Launch Sites Text File: https://planet4589.org/space/gcat/data/tables/orgs.html
        """
        
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            reader.__next__() # Skip the index row
            reader.__next__() # Skip the header row
            self.state_code_to_state_name = {row[0].strip(): row[7].strip() for row in reader}
    
    def generate_launch_site_to_launch_site_parent(self, filePath = "./datasets/sites.tsv"):
        """
        Generate a dictionary that translate Launch_Site to Launch_Site_Parent.
        This requires launch_site.tsv file
        Launch Sites Text File: https://planet4589.org/space/gcat/data/tables/sites.html
        """
        
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            reader.__next__() # Skip the index row
            reader.__next__() # Skip the header row
            self.launch_site_to_launch_site_parent = {row[0].strip(): row[7].replace("-","").strip() for row in reader}
    
    def generate_launch_site_to_launch_site_name(self, filePath = "./datasets/sites.tsv"):
        """
        Generate a dictionary that translate Launch_Site to Launch_Site_Name.
        This requires launch_site.tsv file
        Launch Sites Text File: https://planet4589.org/space/gcat/data/tables/sites.html
        """
        
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            reader.__next__() # Skip the index row
            reader.__next__() # Skip the header row
            # If short name is "-", use default name instead
            self.launch_site_to_launch_site_name = {
                row[0].strip(): row[14].strip() if row[14].strip() != "-" else row[8].strip()
                for row in reader if len(row) > 14
            }