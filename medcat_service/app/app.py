#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

import logging
import sys
import injector
import flask_injector

from medcat_service.nlp_processor import MedCatProcessor
from medcat_service.nlp_service import MedCatService, NlpService
from medcat_service.api import api


def setup_logging():
    """
    Configure and setup a default logging handler to print messages to stdout
    """
    log_format = '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(logging.Formatter(fmt=log_format))
    log_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()

    # only add the handler if a previous one does not exists
    handler_exists = False
    for h in root_logger.handlers:
        if isinstance(h, logging.StreamHandler) and h.level is log_handler.level:
            handler_exists = True
            break

    if not handler_exists:
        root_logger.addHandler(log_handler)


def create_app():
    """
    Creates the Flask application using the factory method
    :return: Flask application
    """
    setup_logging()

    # create flask app and register API
    app = Flask(__name__)
    app.register_blueprint(api)

    # provide the dependent modules via dependency injection
    def configure(binder):
        binder.bind(MedCatProcessor, to=MedCatProcessor, scope=injector.singleton)
        binder.bind(NlpService, to=MedCatService, scope=injector.singleton)

    flask_injector.FlaskInjector(
        app=app,
        modules=[configure])

    # remember to return the app
    return app