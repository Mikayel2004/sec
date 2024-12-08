# /routes/__init_.py

from flask import Flask
from routes.professors import professors_blueprint
from routes.schedules import schedules_blueprint
from routes.subjects import subjects_blueprint

def register_routes(app: Flask):
    """Register all the blueprints."""
    app.register_blueprint(professors_blueprint, url_prefix="/api/professors")
    app.register_blueprint(schedules_blueprint, url_prefix="/api/schedules")
    app.register_blueprint(subjects_blueprint, url_prefix="/api/subjects")
