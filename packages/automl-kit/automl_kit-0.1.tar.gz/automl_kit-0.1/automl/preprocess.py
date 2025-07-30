import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preprocess_data(df, target, problem_type):
    X = df.drop(columns=[target])
    y = df[target]

    # Guess problem type
    if problem_type is None:
        problem_type = 'classification' if y.nunique() <= 20 else 'regression'

    # Basic preprocessing
    X = pd.get_dummies(X)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, problem_type