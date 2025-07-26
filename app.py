from flask import Flask
from config import Config
from extensions import db, login_manager, migrate, socketio

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")

    # Import routes only AFTER initializing app
    from routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

# Initialize app
app = create_app()

# Import User after extensions are initialized
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    socketio.run(app, debug=True)
