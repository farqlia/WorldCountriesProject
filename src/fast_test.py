from src.models.performance import fit_polynomial_for_every_subset
import numpy as np 

if __name__ == "__main__":
    attribs = ['at1', 'at2', 'at3']
    degrees = [2, 3]
    X_train, X_test = np.random.rand(40, 3), np.random.rand(20, 3)
    y_train, y_test = np.random.rand(40), np.random.rand(20)
    scores, best_model_info = fit_polynomial_for_every_subset(X_train, y_train, 
                                                              X_test, y_test, degrees, 
                                                              attribs, n_attribs=3)
    print(scores)
    best_model, best_feat = best_model_info
    print(best_model.degree)
    print(best_feat)