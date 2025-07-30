import pandas as pd
import numpy as np
from .preprocess import preprocess_data
from .models import get_models
from .evaluator import evaluate_models, select_best_model
from .visualizer import plot_metrics

class AutoML:
    def __init__(self, df, target, problem_type=None, test_size=0.2, cv=5, scoring='auto'):
        self.df = df
        self.target = target
        self.problem_type = problem_type
        self.test_size = test_size
        self.cv = cv
        self.scoring = scoring

    def run(self):
        X_train, X_test, y_train, y_test, problem_type = preprocess_data(
            self.df, self.target, self.problem_type
        )
        self.problem_type = problem_type

        models = get_models(problem_type)
        results = evaluate_models(models, X_train, y_train, X_test, y_test, self.cv, self.scoring, self.problem_type)
        best_model = select_best_model(results)

        print(f"\nBest Model: {best_model['name']}")
        print(f"{best_model['score_name']}: {best_model['score']:.4f}")

        plot_metrics(results, problem_type)
        return best_model

class DataCleaner:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # Drop duplicates
        df.drop_duplicates(inplace=True)

        # Drop constant columns
        nunique = df.nunique()
        df = df.loc[:, nunique > 1]

        # Convert numeric strings to numbers
        for col in df.select_dtypes(include="object").columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                pass

        # Fill missing values
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col].fillna(df[col].mean(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)

        # Standardize categorical text
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.strip().str.lower()

        if self.verbose:
            print(f"[DataCleaner] Cleaned DataFrame with shape: {df.shape}")

        return df
