import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from itertools import combinations
from src.models.polynomial_regression import PolyRegression

def compute_performance_df(X_train_arr, y_train_arr, X_test_arr, y_test_arr, models, names):
    errors = pd.DataFrame(columns=['R-squared', 'Test MSE', 'Train MSE'], index=names)
    
    for model, name in zip(models, names):

        if len(X_train_arr.shape) == 1:
            X_train_arr = X_train_arr.reshape(-1, 1)
            X_test_arr = X_test_arr.reshape(-1, 1)

        errors.at[name, 'R-squared'] = model.score(X_test_arr, y_test_arr)
        errors.at[name, 'Test MSE'] = mean_squared_error(y_test_arr, model.predict(X_test_arr))
        errors.at[name, 'Train MSE'] = mean_squared_error(y_train_arr, model.predict(X_train_arr))

    return errors


def print_for_latex_table_perf(df, print_index=False):

    print("\hline")
    if print_index:
        print("Model & ")
    print(" & ".join(df.columns), " \\\ ")
    print("\hline")
    for row in df.iterrows():
        if print_index:
            print(f"{row[0]} & ")
        print(" & ".join([str(round(m, 2)) for m in row[1]]) + " \\\ ")
        print("\hline")

def print_coef(result_series):
    eq = ""
    for index, value in result_series.sort_values(ascending=False, key=lambda x: abs(x)).items():
        eq += (" + " if value >= 0 else " - ") +  " \ " + str(abs(round(value, 2))) + " \ * \ " + index.replace(' ', r'\_') + " \ "

    print(eq[:-3])


def fit_polynomial_for_every_subset(X_train_arr, y_train_arr, 
                                    X_test_arr, y_test_arr, degrees, attributes,
                                    n_attribs=None):

    if not n_attribs:
        n_attribs = len(attributes)
    features_range = list(range(2, n_attribs + 1))
    features_labels = list(range(len(attributes)))
    best_model = None
    best_model_score = None  
    best_attributes = None 

    results = pd.DataFrame(columns=degrees, index=features_range) 

    for p in features_range:

        for degree in degrees:

            for subset_features in combinations(features_labels, p):

                subset_features = list(subset_features)
                X_train_subset = X_train_arr[:, subset_features]
                X_test_subset = X_test_arr[:, subset_features]

                poly_model = PolyRegression(degree)
                poly_model.fit(X_train_subset, y_train_arr)
                if np.isnan(results.loc[p, degree]) or poly_model.score(X_test_subset, y_test_arr) > results.loc[p, degree]:
                    results.at[p, degree] = poly_model.score(X_test_subset,
                                                              y_test_arr)
                
                if best_model_score is None or results.loc[p, degree] > best_model_score:
                    best_model = poly_model
                    best_model_score = results.at[p, degree]
                    best_attributes = attributes[subset_features]
                    
    return results, (best_model, best_attributes)
        