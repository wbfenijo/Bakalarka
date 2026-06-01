import numpy as np
import pandas as pd
from scipy.stats import shapiro
import matplotlib.pyplot as plt
import scipy.stats as stats


ALPHA = 0.05
ROSES_METHOD = "ZS6"   # uprav podla toho, ktory prompt je ROSES


def test_normality(values, name):
    values = np.array(values, dtype=float)
    values = values[~np.isnan(values)]

    print(f"\n=== Normality test: {name} ===")
    print(f"n = {len(values)}")

    if len(values) < 3:
        print("Not enough values for Shapiro-Wilk test.")
        return None, None

    stat, p = shapiro(values)

    print(f"Shapiro statistic = {stat:.4f}")
    print(f"p-value = {p:.6f}")

    print("H0: data come from a normal distribution")
    print("H1: data do not come from a normal distribution")

    if p > ALPHA:
        print(f"Decision: fail to reject H0 at alpha={ALPHA}")
        print("Conclusion: normality was not rejected.")
    else:
        print(f"Decision: reject H0 at alpha={ALPHA}")
        print("Conclusion: data are not normally distributed.")

    return stat, p


def plot_normality(values, name):
    values = np.array(values, dtype=float)
    values = values[~np.isnan(values)]

    plt.figure(figsize=(6, 4))
    plt.hist(values, bins=15)
    plt.title(f"Histogram - {name}")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 6))
    stats.probplot(values, dist="norm", plot=plt)
    plt.title(f"Q-Q plot - {name}")
    plt.tight_layout()
    plt.show()


def normality_checks(df, best_model):
    # 1. RAG
    rag_scores = df[df["method"] == "RAG"]["score"]
    test_normality(rag_scores, "RAG")
    plot_normality(rag_scores, "RAG")

    # 2. ROSES
    roses_scores = df[df["method"] == ROSES_METHOD]["score"]
    test_normality(roses_scores, f"ROSES ({ROSES_METHOD})")
    plot_normality(roses_scores, f"ROSES ({ROSES_METHOD})")

    # 3. Best model
    best_model_scores = df[df["model"] == best_model]["score"]
    test_normality(best_model_scores, f"Best model ({best_model})")
    plot_normality(best_model_scores, f"Best model ({best_model})")

    # 4. All zero-shot prompts together
    zs_scores = df[df["method"] != "RAG"]["score"]
    test_normality(zs_scores, "All zero-shot prompts")
    plot_normality(zs_scores, "All zero-shot prompts")

    # 5. Each ZS prompt separately
    for method in sorted(df["method"].unique()):
        if method == "RAG":
            continue

        scores = df[df["method"] == method]["score"]
        test_normality(scores, method)