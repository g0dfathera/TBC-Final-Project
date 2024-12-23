from db import app, db

# Run the app
if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    from routes import *
    app.run(host='0.0.0.0', port=5000, debug=True)
