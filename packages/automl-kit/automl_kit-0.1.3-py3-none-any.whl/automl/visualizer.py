import matplotlib.pyplot as plt

def plot_metrics(results, problem_type):
    names = [r['name'] for r in results]
    scores = [r['score'] for r in results]
    plt.figure(figsize=(8, 5))
    plt.barh(names, scores, color='skyblue')
    plt.xlabel('Score')
    plt.title('Model Performance Comparison')
    plt.tight_layout()
    plt.show()