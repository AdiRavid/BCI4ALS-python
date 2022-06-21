import xgboost as xgb
import optuna
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def run_optuna_xgb(X, y):
    """
    runs optuna hyper-parameter optimaizer on the given X data and y labels for the xgb classifier
    """
    def objective_xgb(trial):
        # data loading and train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # hyperparameter setting
        n_estimators = trial.suggest_int('n_estimators', 2, 300)
        max_depth = trial.suggest_int('max_depth', 1, 50)
        learning_rate = trial.suggest_uniform('learning_rate', 0.0, 1.0)
        colsample_bytree = trial.suggest_uniform('colsample_bytree', 0.0, 1.0)
        alpha = trial.suggest_float('alpha', 0.0, 17.0)
        booster = trial.suggest_categorical('booster', ('gbtree', 'gblinear', 'dart'))
        tree_method = trial.suggest_categorical('tree_method', ('approx', 'auto', 'exact', 'hist'))
        importance_type = trial.suggest_categorical('importance_type',
                                                    ('gain', 'weight', 'cover', 'total_gain', 'total_cover'))
        model = xgb.XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate,
                                  colsample_bytree=colsample_bytree,
                                  alpha=alpha, booster=booster, tree_method=tree_method,
                                  importance_type=importance_type)

        # model training
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # evaluation
        report = classification_report(y_test, y_pred, output_dict=True)

        # output: evaluation score
        return report['accuracy']

    study_xgb = optuna.create_study(
        direction='maximize')  # Set minimize for minimization and maximize for maximization.
    # To start the optimization, we create a study object and pass the objective function to method
    study_xgb.optimize(objective_xgb, n_trials=100)
    print("best params are: ", study_xgb.best_params)
    return study_xgb.best_params


def run_optuna_LR(X, y):
    """
    runs optuna hyper-parameter optimaizer on the given X data and y labels for the logistic regression classifier
    """
    def objective_LR(trial):
        # data loading and train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # hyperparameter setting
        max_iter = trial.suggest_int('max_iter', 100, 400)
        C = trial.suggest_float('C', 0.3, 2.0)
        penalty = trial.suggest_categorical('penalty', ('l1', 'l2'))
        # solver = trial.suggest_categorical('solver', ('liblinear'))

        model = LogisticRegression(max_iter=max_iter, C=C, penalty=penalty, solver='liblinear')

        # model training
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # evaluation
        report = classification_report(y_test, y_pred, output_dict=True)

        # output: evaluation score
        return report['accuracy']  # + report['1.0']['recall'] + report['2.0']['recall'] + report['3.0']['recall']

    study_LR = optuna.create_study(direction='maximize')  # Set minimize for minimization and maximize for maximization.
    # To start the optimization, we create a study object and pass the objective function to method
    study_LR.optimize(objective_LR, n_trials=100)
    print("best params are: ", study_LR.best_params)
    return study_LR.best_params


def run_optuna_RF(X, y):
    """
    runs optuna hyper-parameter optimaizer on the given X data and y labels for the random forest classifier
    """
    def objective_RF(trial):
        # data loading and train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # hyperparameter setting
        n_estimators = trial.suggest_int('n_estimators', 20, 300)
        max_depth = trial.suggest_int('max_depth', 1, 50)
        min_samples_split = trial.suggest_int('min_samples_split', 2, 10)
        min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)
        criterion = trial.suggest_categorical('criterion', ('gini', 'entropy'))
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                       min_samples_split=min_samples_split,
                                       min_samples_leaf=min_samples_leaf, criterion=criterion)

        # model training
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # evaluation
        report = classification_report(y_test, y_pred, output_dict=True)

        # output: evaluation score
        return report['accuracy']

    study_RF = optuna.create_study(direction='maximize')  # Set minimize for minimization and maximize for maximization.
    # To start the optimization, we create a study object and pass the objective function to method
    study_RF.optimize(objective_RF, n_trials=100)
    print("best params are: ", study_RF.best_params)
    return study_RF.best_params
