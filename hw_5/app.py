from flask import Flask, request, jsonify, abort
from flask.app import HTTPException
import learning
from db import DB_model, init_db, make_engine
from sqlalchemy.orm import sessionmaker
from distutils.util import strtobool
from logs import get_logger
import threading

logger = get_logger(__name__)
engine = make_engine()
init_db()
session_factory = sessionmaker(bind=engine)

thr = threading.Thread(target=learning.async_handler,
                       args=(session_factory,),
                       daemon=True,
                       )
thr.start()

app = Flask(__name__)


@app.errorhandler(Exception)
def error_handler(exc):
    logger.debug(exc)
    if isinstance(exc, HTTPException):
        return jsonify({"error": exc.description, "error code": exc.code})
    return jsonify({"error": f"internal error"}), 500


@app.route('/')
def greet():
    return "Hello World!"


@app.route('/train', methods=["POST"])
def train():
    is_async = False
    try:
        is_async = bool(strtobool(request.args.get("async", "0")))
    except Exception as exc:
        abort(400, f"async must be boolean: {exc}")
        return

    json_data = request.get_json()
    try:
        train_data = json_data["data"]
        target = json_data["target"]
        n_folds = json_data["n_folds"]
        fit_int = json_data["fit_intercept"]
        l2_coef = json_data["l2_coef"]
    except Exception as exc:
        abort(400, f"invalid data: {exc}")
        return

    model = DB_model(given_data_param=json_data)
    if not is_async:
        model_info = learning.train_and_get_info(train_data=train_data, target=target,
                                                 l2_coef=l2_coef, n_folds=n_folds,
                                                 fit_int=fit_int)
        model.model_inf = model_info["model"]
        model.cv_results = model_info["cv_results"]
        model.ready = True
    else:
        model.model_inf = {}
        model.cv_results = {}
    session = session_factory()
    session.add(model)
    session.commit()
    model_id = model.id
    session.close()

    return jsonify(model_id=model_id)


@app.route('/model/<int:model_id>', methods=["GET"])
def get_model(model_id):
    session = session_factory()
    model = session.query(DB_model).filter_by(id=model_id).first()
    if model is None:
        abort(404, f"model {model_id} does not exist")
        return

    if model.ready is False:
        abort(404, f"model {model_id} is not ready")
        return

    return jsonify(model=model.model_inf, cv_results=model.cv_results)


@app.route('/predict', methods=["POST"])
def predict():
    try:
        json_data = request.get_json()
        train_data = json_data["data"]
        model_id = json_data["model_id"]
    except Exception as exc:
        abort(400, f"invalid data: {exc}")
        return
    session = session_factory()
    model_info = session.query(DB_model).filter_by(id=model_id).first().model_inf
    if model_info is None:
        abort(404, f"model {model_id} does not exist")
        return
    result = learning.get_prediction(model_info=model_info, raw_csv=train_data)

    return jsonify(result=result)


app.run()
