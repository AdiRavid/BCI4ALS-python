import xgboost as xgb
import optuna
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# def objective_xgb(trial):
#     # data loading and train-test split
#     X_train, X_test, y_train, y_test = train_test_split(X, y)
#
#     # hyperparameter setting
#     n_estimators = trial.suggest_int('n_estimators', 2, 300)
#     max_depth = trial.suggest_int('max_depth', 1, 50)
#     learning_rate = trial.suggest_uniform('learning_rate', 0.0, 1.0)
#     colsample_bytree = trial.suggest_uniform('colsample_bytree', 0.0, 1.0)
#     alpha = trial.suggest_float('alpha', 0.0, 17.0)
#     booster = trial.suggest_categorical('booster', ('gbtree', 'gblinear', 'dart'))
#     tree_method = trial.suggest_categorical('tree_method', ('approx', 'auto', 'exact', 'hist'))
#     importance_type = trial.suggest_categorical('importance_type',
#                                                 ('gain', 'weight', 'cover', 'total_gain', 'total_cover'))
#     # is_weighted = trial.suggest_categorical('is_weighted', ('yes', 'no'))
#     # if is_weighted == 'yes':
#     #     model = xgb.XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate,
#     #                               colsample_bytree=colsample_bytree,
#     #                               alpha=alpha, booster=booster, tree_method=tree_method,
#     #                               importance_type=importance_type,
#     #                               scale_pos_weight=sum(label_test["LabelTest"].flatten() == 2) / sum(
#     #                                   label_test["LabelTest"].flatten() == 3))
#     # else:
#     model = xgb.XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate,
#                               colsample_bytree=colsample_bytree,
#                               alpha=alpha, booster=booster, tree_method=tree_method,
#                               importance_type=importance_type)
#
#     # model training
#     model.fit(X_train, y_train)
#     y_pred = model.predict(X_test)
#
#     # evaluation
#     report = classification_report(y_test, y_pred, output_dict=True)
#     #     recall_one = report['1']['recall']
#     #     recall_zero = report['0']['recall']
#     #     precision_one = report['1']['precision']
#     #     precision_zero = report['0']['precision']
#
#     # output: evaluation score
#     return report['accuracy'] + report['1']['recall'] + report['2']['recall'] + report['3']['recall']

def run_optuna(X,y):
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
        # is_weighted = trial.suggest_categorical('is_weighted', ('yes', 'no'))
        # if is_weighted == 'yes':
        #     model = xgb.XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate,
        #                               colsample_bytree=colsample_bytree,
        #                               alpha=alpha, booster=booster, tree_method=tree_method,
        #                               importance_type=importance_type,
        #                               scale_pos_weight=sum(label_test["LabelTest"].flatten() == 2) / sum(
        #                                   label_test["LabelTest"].flatten() == 3))
        # else:
        model = xgb.XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate,
                                  colsample_bytree=colsample_bytree,
                                  alpha=alpha, booster=booster, tree_method=tree_method,
                                  importance_type=importance_type)

        # model training
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # evaluation
        report = classification_report(y_test, y_pred, output_dict=True)
        #     recall_one = report['1']['recall']
        #     recall_zero = report['0']['recall']
        #     precision_one = report['1']['precision']
        #     precision_zero = report['0']['precision']

        # output: evaluation score
        return report['accuracy'] # + report['1.0']['recall'] + report['2.0']['recall'] + report['3.0']['recall']


    study_xgb = optuna.create_study(direction='maximize') #Set minimize for minimization and maximize for maximization.
    #To start the optimization, we create a study object and pass the objective function to method
    study_xgb.optimize(objective_xgb, n_trials=100)
    print("best params are: ",study_xgb.best_params)