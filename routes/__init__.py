from .professors import professors_blueprint
from .subjects import subjects_blueprint
from .schedules import schedules_blueprint

def register_routes(app):
    app.register_blueprint(professors_blueprint, url_prefix='/professors')
    app.register_blueprint(subjects_blueprint, url_prefix='/subjects')
    app.register_blueprint(schedules_blueprint, url_prefix='/schedules')
