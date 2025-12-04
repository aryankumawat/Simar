"""
Example usage of ExportMap market analysis with predictive models
"""

import sys

sys.path.append("src")

from data_loader import DataLoader
from market_analyzer import MarketAnalyzer
from visualizer import MarketVisualizer
from predictive_models import GDPPredictor, MarketClassifier


def main():
    print("=== ExportMap Demo ===\n")

    # 1. Load data
    loader = DataLoader()
    data = loader.load_all_datasets()
    print()

    # 2. Analyze markets
    analyzer = MarketAnalyzer(data)
    analyzer.calculate_mos()
    recommendations = analyzer.get_market_recommendations(top_n=15)

    # 3. Display results
    print("Top 15 Markets for Children's Clothing Exports:\n")
    print(
        f"{'Rank':<6} {'Country':<25} {'MOS':<10} {'Population':<15} {'GDP/Capita':<12} {'Region'}"
    )
    print("-" * 95)

    for idx, market in enumerate(recommendations, 1):
        pop = f"{market['population']:,}" if market["population"] else "N/A"
        gdp = (
            f"${market['gdp_per_capita']:,.0f}"
            if market["gdp_per_capita"]
            else "N/A"
        )

        print(
            f"{idx:<6} {market['country']:<25} {market['mos_score']:<10.3f} {pop:<15} {gdp:<12} {market['region']}"
        )

    # 4. Train predictive models
    print("\n" + "=" * 95)
    print("PREDICTIVE MODELS")
    print("=" * 95)

    # GDP Predictor
    print("\n1. Training GDP Prediction Model...")
    gdp_predictor = GDPPredictor()
    gdp_results = gdp_predictor.train(analyzer.merged_data)

    if gdp_results:
        print(f"   R² Score: {gdp_results['r2_score']:.3f}")
        gdp_predictor.plot_results(gdp_results)

    # Market Classifier
    print("\n2. Training Market Classification Model...")
    classifier = MarketClassifier()
    class_results = classifier.train(analyzer.merged_data)

    if class_results:
        print(f"   Accuracy: {class_results['accuracy']:.3f}")
        print(f"   ROC AUC: {class_results['roc_auc']:.3f}")
        classifier.plot_results(class_results)

    # 5. Create visualizations
    print("\n3. Generating market visualizations...")
    viz = MarketVisualizer()
    viz.plot_top_markets(recommendations[:10], metric="mos_score")

    if not analyzer.merged_data.empty:
        viz.plot_regional_distribution(analyzer.merged_data)

    print("\n" + "=" * 95)
    print("✓ Analysis complete! Generated files:")
    print("  - top_markets.png")
    print("  - regional_distribution.png")
    print("  - gdp_prediction_results.png")
    print("  - market_classification_results.png")
    print("=" * 95)


if __name__ == "__main__":
    main()
