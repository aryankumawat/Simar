# ExportMap: Smart Market Finder for Global Businesses

An intelligent application helping small clothing exporters identify optimal international markets through data-driven insights and predictive analytics.

## Features

### Market Opportunity Score (MOS)
- Weighted scoring system combining:
  - **40%** GDP per capita (purchasing power)
  - **20%** Literacy rate (education level)
  - **20%** Phones per 1000 (infrastructure)
  - **20%** Birthrate (children's market potential)

### Predictive Models
- **Linear Regression**: Predict GDP per capita based on economic indicators
- **Logistic Regression**: Classify high-potential vs low-potential markets
- Feature importance analysis and model evaluation metrics

### Smart Data Matching
- Fuzzy matching algorithm to handle country name variations
- Intelligent merging of multiple data sources
- >80% confidence threshold for data quality

### Visualizations
- Top markets bar charts
- Regional distribution analysis
- GDP prediction accuracy plots
- ROC curves for classification models

## Data Sources
- World Population Dataset (234 countries)
- Countries of the World Statistics (227 countries)
- Future: UN Comtrade API, WTO Tariff Database, World Bank APIs

## Tech Stack
- **Python 3.8+**
- **pandas** & **numpy** - Data processing
- **scikit-learn** - Machine learning models
- **rapidfuzz** - Fuzzy string matching
- **matplotlib** & **seaborn** - Visualizations

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ExportMap

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
# Run basic analysis
python src/main.py
```

### Detailed Analysis with Visualizations
```bash
# Run comprehensive analysis with all models
python example_usage.py
```

### Output Files
- `top_markets.png` - Top 10 recommended markets
- `regional_distribution.png` - Market distribution by region
- `gdp_prediction_results.png` - Linear regression analysis
- `market_classification_results.png` - Logistic regression ROC curve

## Project Structure
```
ExportMap/
├── src/
│   ├── data_loader.py          # CSV loading and preprocessing
│   ├── market_analyzer.py      # MOS calculation and fuzzy matching
│   ├── predictive_models.py    # ML models (Linear & Logistic Regression)
│   ├── visualizer.py           # Chart generation
│   └── main.py                 # Main CLI application
├── combined_exportmap_dataset.csv
├── world_population.csv
├── countries of the world.csv
├── requirements.txt
├── README.md
└── INTEGRATION_NOTES.md        # Technical documentation
```

## Methodology

### Market Opportunity Score (MOS)
1. Normalize all features using MinMaxScaler (0-1 range)
2. Apply weighted formula: `MOS = 0.4*GDP + 0.2*Literacy + 0.2*Phones + 0.2*Birthrate`
3. Rank countries by MOS for recommendations

### GDP Prediction Model
- **Algorithm**: Linear Regression
- **Features**: Literacy, Phones per 1000, Birthrate, Infant Mortality
- **Evaluation**: R² score, coefficient analysis
- **Use Case**: Forecast economic growth potential

### Market Classification Model
- **Algorithm**: Logistic Regression
- **Target**: High MOS (above median) vs Low MOS
- **Evaluation**: Accuracy, ROC AUC, Confusion Matrix
- **Use Case**: Binary classification of market potential

## Example Output

```
Top Markets for Children's Clothing Exports:
================================================================================
Rank   Country                   MOS        GDP/Cap      Literacy   Region
--------------------------------------------------------------------------------
1      Norway                    0.892      $37,670      99.0%      WESTERN EUROPE
2      United States             0.856      $37,800      97.0%      NORTHERN AMERICA
3      Switzerland               0.847      $32,700      99.0%      WESTERN EUROPE
...
```

## Future Enhancements
- [ ] Real-time API integration (UN Comtrade, World Bank)
- [ ] Tariff analysis and trade agreement considerations
- [ ] Logistics performance scoring
- [ ] Interactive web dashboard
- [ ] Time-series forecasting for demand prediction
- [ ] Geographic heat maps

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License

## Contact
For questions or feedback, please open an issue on GitHub.
