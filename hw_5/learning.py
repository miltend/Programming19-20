from io import StringIO
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from db import DB_model
from logs import get_logger
import time

logger = get_logger(__name__)


def get_data(raw_csv, target):
    try:
        data = pd.read_csv(StringIO(str(raw_csv)))
        features = []
        for i in range(len(data.columns)):
            if data.columns[i] != target:
                features.append(data.columns[i])
        X = data[features]
        y = data[target]
    except Exception as exc:
        logger.debug(f"something went wrong: {exc}")
        raise ValueError(f"something went wrong: {exc}")
    return X, y, features


def train(X, y, l2_coef, n_folds, fit_intercept=True):
    try:
        l2_coef_score = {}
        for coef in l2_coef:
            reg = linear_model.Ridge(alpha=coef, fit_intercept=fit_intercept)
            scores = -cross_val_score(reg, X, y, cv=n_folds, scoring="neg_mean_squared_error")
            l2_coef_score[coef] = scores.mean()
        min_score = min(l2_coef_score.values())
        best_coef = [key for key in l2_coef_score if l2_coef_score[key] == min_score]
        reg = linear_model.Ridge(best_coef[0])
        reg.fit(X, y)
        intercept = reg.intercept_
        reg_coef = reg.coef_
    except Exception as exc:
        logger.debug(f"something went wrong: {exc}")
        raise ValueError(f"something went wrong: {exc}")

    return intercept, reg_coef, l2_coef_score,


def get_model_info(features, intercept, reg_coef, l2_coef_score):
    try:
        coeffs = {}  # коэффициенты регрессии
        cv_results = []
        best_model_info = {}
        model_info = {}
        for i in range(len(features)):  # приводим коэффициенты к требуемому виду
            coeffs[features[i]] = reg_coef[i]
        for key, value in l2_coef_score.items():
            info = {"param_value": key, "mean_mse": value}
            cv_results.append(info)
        best_model_info["intercept"] = intercept
        best_model_info["coef"] = coeffs
        model_info["model"] = best_model_info
        model_info["cv_results"] = cv_results
    except Exception as exc:
        logger.debug(f"something went wrong: {exc}")
        raise ValueError(f"something went wrong: {exc}")
    return model_info


def get_prediction(model_info, raw_csv):
    try:
        X_pred = pd.read_csv(StringIO(str(raw_csv)))
        y_pred = []
        intercept = model_info["intercept"]
        coeffs = model_info["coef"]
        for row in X_pred.iterrows():
            result = [intercept]
            for coef, value in coeffs.items():
                result.append(row[1][coef] * value)
            y_pred.append(sum(result))
    except Exception as exc:
        logger.debug(f"something went wrong: {exc}")
        raise ValueError(f"something went wrong: {exc}")
    return y_pred


def train_and_get_info(train_data, target, l2_coef, n_folds, fit_int):
    try:
        X, y, features = get_data(raw_csv=train_data, target=target)
        (model_intercept, model_coef, l2_coef_score) = train(X=X, y=y, l2_coef=l2_coef,
                                                             n_folds=n_folds, fit_intercept=fit_int)
        model_info = get_model_info(features=features, intercept=model_intercept,
                                    reg_coef=model_coef, l2_coef_score=l2_coef_score)
    except Exception as exc:
        logger.debug(f"smth went wrong: {exc}")
        return

    return model_info


def async_handler(session_factory):
    try:
        logger.debug("async_init")
        session = session_factory()
        while True:
            model = session.query(DB_model).filter_by(ready=False).first()
            if model is not None:
                logger.debug(f"async processing: {model.id}")

                data = model.given_data_param
                csv = data["data"]
                target = data["target"]
                l2_coef = data["l2_coef"]
                n_folds = data["n_folds"]
                fit_int = data["fit_intercept"]

                model_inform = train_and_get_info(csv, target, l2_coef, n_folds, fit_int)
                model.model_inf = model_inform["model"]
                model.cv_results = model_inform["cv_results"]
                model.ready = True
                session.commit()

            time.sleep(0.5)
    except Exception as exc:
        logger.debug(f"something went wrong: {exc}")
        raise ValueError(f"something went wrong: {exc}")