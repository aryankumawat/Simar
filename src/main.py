"""
ExportMap: Smart Market Finder
Main application entry point
"""

from data_loader import DataLoader
from market_analyzer import MarketAnalyzer
from predictive_models import GDPPredictor, MarketClassifier


def main():
    print("=== ExportMap: Smart Market Finder ===\n")

    # Load data
    loader = DataLoader()
    data = loader.load_all_datasets()

    # Initialize analyzer
    analyzer = MarketAnalyzer(data)

    # Calculate Market Opportunity Score
    print("Calculating Market Opportunity Scores...\n")
    analyzer.calculate_mos()

    # Get top market recommendations
    print("Top Markets for Children's Clothing Exports:")
    print("=" * 80)
    recommendations = analyzer.get_market_recommendations(
        product_category="children_clothing", top_n=15
    )

    # Display results in table format
    print(
        f"{'Rank':<6} {'Country':<25} {'MOS':<10} {'GDP/Cap':<12} {'Literacy':<10} {'Region'}"
    )
    print("-" * 80)

    for idx, market in enumerate(recommendations, 1):
        gdp = (
            f"${market['gdp_per_capita']:,.0f}"
            if market["gdp_per_capita"]
            else "N/A"
        )
        lit = f"{market['literacy']:.1f}%" if market["literacy"] else "N/A"

        print(
            f"{idx:<6} {market['country']:<25} {market['mos_score']:<10.3f} {gdp:<12} {lit:<10} {market['region']}"
        )

    # Predictive Models
    print("\n" + "=" * 80)
    print("PREDICTIVE ANALYTICS")
    print("=" * 80)

    # 1. GDP Prediction Model
    print("\n1. GDP Prediction (Linear Regression)")
    print("-" * 80)
    gdp_predictor = GDPPredictor()
    gdp_results = gdp_predictor.train(analyzer.merged_data)

    if gdp_results:
        print(f"R² Score: {gdp_results['r2_score']:.3f}")
        print("\nFeature Coefficients:")
        for feature, coef in gdp_results["coefficients"].items():
            print(f"  {feature:<40} {coef:>10.2f}")
        print(f"  {'Intercept':<40} {gdp_results['intercept']:>10.2f}")
        gdp_predictor.plot_results(gdp_results)

    # 2. Market Classification Model
    print("\n2. High-Potential Market Classification (Logistic Regression)")
    print("-" * 80)
    classifier = MarketClassifier()
    class_results = classifier.train(analyzer.merged_data)

    if class_results:
        print(f"Accuracy: {class_results['accuracy']:.3f}")
        print(f"ROC AUC: {class_results['roc_auc']:.3f}")
        print("\nConfusion Matrix:")
        print(class_results["confusion_matrix"])
        print("\nClassification Report:")
        print(class_results["classification_report"])
        classifier.plot_results(class_results)

    print("\n" + "=" * 80)
    print("Analysis complete! Check generated PNG files for visualizations.")
    print("=" * 80)


if __name__ == "__main__":
    main()
