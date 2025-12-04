"""
Data visualization module for market insights
"""

import matplotlib.pyplot as plt
import seaborn as sns

class MarketVisualizer:
    def __init__(self):
        sns.set_style("whitegrid")
        self.colors = sns.color_palette("husl", 10)
    
    def plot_top_markets(self, recommendations, metric="mos_score"):
        """Create bar chart of top markets"""
        countries = [r["country"] for r in recommendations]
        scores = [r.get(metric, r.get("score", 0)) for r in recommendations]

        plt.figure(figsize=(12, 6))
        plt.barh(countries, scores, color=self.colors)
        plt.xlabel(f'{metric.replace("_", " ").title()}')
        plt.ylabel("Country")
        plt.title("Top Export Markets")
        plt.tight_layout()
        plt.savefig("top_markets.png", dpi=300, bbox_inches="tight")
        plt.close()
        print("✓ Saved visualization: top_markets.png")
    
    def plot_regional_distribution(self, data):
        """Create pie chart of regional opportunities"""
        if 'Region' not in data.columns:
            return
        
        region_counts = data['Region'].value_counts()
        
        plt.figure(figsize=(10, 8))
        plt.pie(region_counts.values, labels=region_counts.index, autopct='%1.1f%%')
        plt.title('Market Distribution by Region')
        plt.tight_layout()
        plt.savefig('regional_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Saved visualization: regional_distribution.png")
