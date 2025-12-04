"""
Market analysis and recommendation engine
Based on fuzzy matching and Market Opportunity Score (MOS) methodology
"""

import pandas as pd
import numpy as np
from rapidfuzz import process, fuzz
from sklearn.preprocessing import MinMaxScaler

class MarketAnalyzer:
    def __init__(self, data):
        self.data = data
        self.merged_data = self._merge_datasets()
        self.scaler = MinMaxScaler()
    
    def _fuzzy_match_country(self, name, choices):
        """Fuzzy match country names using rapidfuzz"""
        if pd.isna(name):
            return None
        match, score, _ = process.extractOne(name, choices, scorer=fuzz.WRatio)
        return match if score > 80 else None
    
    def _merge_datasets(self):
        """Merge datasets using fuzzy matching for country names"""
        if not self.data:
            return None
        
        pop = self.data.get('population', pd.DataFrame())
        cw = self.data.get('countries', pd.DataFrame())
        
        if pop.empty or cw.empty:
            return pop if not pop.empty else cw
        
        # Clean country names
        cw['Country'] = cw['Country'].str.strip()
        pop['Country/Territory'] = pop['Country/Territory'].str.strip()
        
        # Fuzzy match countries
        cw['match_country'] = cw['Country'].apply(
            lambda x: self._fuzzy_match_country(x, pop['Country/Territory'].tolist())
        )
        
        # Merge on matched names
        merged = pd.merge(
            pop, cw,
            left_on='Country/Territory',
            right_on='match_country',
            how='inner'
        )
        
        merged = merged.drop(columns=['match_country'])
        return merged
    
    def calculate_mos(self):
        """
        Calculate Market Opportunity Score (MOS) using weighted features
        MOS = 0.4*GDP + 0.2*Literacy + 0.2*Phones + 0.2*Birthrate
        """
        if self.merged_data is None or self.merged_data.empty:
            return
        
        df = self.merged_data
        mos_features = ['GDP ($ per capita)', 'Literacy (%)', 'Phones (per 1000)', 'Birthrate']
        
        # Check if all features exist
        missing = [f for f in mos_features if f not in df.columns]
        if missing:
            print(f"Warning: Missing MOS features: {missing}")
            return
        
        # Scale features to 0-1 range
        scaled_cols = [f + '_scaled' for f in mos_features]
        df[scaled_cols] = self.scaler.fit_transform(df[mos_features])
        
        # Calculate weighted MOS
        df['MOS'] = (
            0.4 * df['GDP ($ per capita)_scaled'] +
            0.2 * df['Literacy (%)_scaled'] +
            0.2 * df['Phones (per 1000)_scaled'] +
            0.2 * df['Birthrate_scaled']
        )
        
        self.merged_data = df.sort_values('MOS', ascending=False)
    
    def get_market_recommendations(self, product_category="children_clothing", top_n=10):
        """
        Generate market recommendations using MOS (Market Opportunity Score)
        """
        if self.merged_data is None or self.merged_data.empty:
            return []
        
        # Calculate MOS if not already done
        if 'MOS' not in self.merged_data.columns:
            self.calculate_mos()
        
        df = self.merged_data
        
        # Get top markets by MOS
        top_markets = df.nlargest(top_n, 'MOS') if 'MOS' in df.columns else df.head(top_n)
        
        recommendations = []
        for _, row in top_markets.iterrows():
            recommendations.append({
                'country': row.get('Country/Territory', 'Unknown'),
                'mos_score': row.get('MOS', 0),
                'population': row.get('2022 Population', 0),
                'gdp_per_capita': row.get('GDP ($ per capita)', 0),
                'literacy': row.get('Literacy (%)', 0),
                'birthrate': row.get('Birthrate', 0),
                'region': row.get('Region', 'Unknown'),
                'continent': row.get('Continent', 'Unknown')
            })
        
        return recommendations
