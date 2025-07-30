from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import cross_val_score
import numpy as np

def evaluate_models(models, X_train, y_train, X_test, y_test, cv, scoring, problem_type):
    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Choose score based on problem type
        if scoring == 'auto':
            if problem_type == 'classification':
                score = accuracy_score(y_test, y_pred)
                score_name = 'Accuracy'
            elif problem_type == 'regression':
                score = np.sqrt(mean_squared_error(y_test, y_pred))
                score_name = 'RMSE'
            else:
                raise ValueError(f"Unknown problem type: {problem_type}")
        elif scoring == 'rmse':
            score = mean_squared_error(y_test, y_pred, squared=False)
            score_name = 'RMSE'
        elif scoring == 'accuracy':
            score = accuracy_score(y_test, y_pred)
            score_name = 'Accuracy'
        else:
            score = cross_val_score(model, X_train, y_train, cv=cv, scoring=scoring).mean()
            score_name = scoring

        results.append({
            'name': name,
            'model': model,
            'score': score,
            'score_name': score_name
        })
    return results

def select_best_model(results):
    return max(results, key=lambda x: -x['score'] if x['score_name'] != 'RMSE' else -x['score'])
