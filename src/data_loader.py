"""
Data loading and preprocessing module
"""

import pandas as pd
from pathlib import Path

class DataLoader:
    def __init__(self, data_dir="./"):
        self.data_dir = Path(data_dir)
    
    def load_all_datasets(self):
        """Load all available datasets"""
        print("Loading datasets...")
        
        data = {}
        
        # Load population data
        try:
            data['population'] = pd.read_csv(self.data_dir / 'world_population.csv')
            print(f"✓ Loaded population data: {len(data['population'])} countries")
        except Exception as e:
            print(f"✗ Error loading population data: {e}")
        
        # Load country statistics
        try:
            data["countries"] = pd.read_csv(self.data_dir / "countries of the world.csv")
            data["countries"] = self.clean_all_numeric_columns(data["countries"])
            print(f"✓ Loaded country data: {len(data['countries'])} countries")
        except Exception as e:
            print(f"✗ Error loading country data: {e}")
        
        # Load combined export data
        try:
            data['exports'] = pd.read_csv(self.data_dir / 'combined_exportmap_dataset.csv')
            print(f"✓ Loaded export data: {len(data['exports'])} records")
        except Exception as e:
            print(f"✗ Error loading export data: {e}")
        
        return data
    
    def clean_numeric_column(self, df, column):
        """Clean numeric columns with comma decimal separators"""
        if column in df.columns:
            df[column] = (
                df[column].astype(str).str.replace(",", ".").astype(float, errors="ignore")
            )
        return df

    def clean_all_numeric_columns(self, df):
        """Clean all numeric columns that might have comma separators"""
        numeric_cols = [
            "GDP ($ per capita)",
            "Literacy (%)",
            "Phones (per 1000)",
            "Birthrate",
            "Deathrate",
            "Infant mortality (per 1000 births)",
            "Pop. Density (per sq. mi.)",
            "Net migration",
            "Arable (%)",
            "Crops (%)",
            "Other (%)",
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(",", "."), errors="coerce"
                )
        return df
