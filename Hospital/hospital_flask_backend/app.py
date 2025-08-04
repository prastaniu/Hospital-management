from flask import Flask
from flask_cors import CORS
from extensions import mysql, init_db    

app = Flask(__name__)
CORS(app)

init_db(app)  

def register_blueprints(app):
    from routes.doctors import doctors_bp
    from routes.patients import patients_bp
    from routes.appointments import appointments_bp
    from routes.treatments import treatments_bp
    from routes.billing import billing_bp

    app.register_blueprint(doctors_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(treatments_bp)
    app.register_blueprint(billing_bp)

register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
