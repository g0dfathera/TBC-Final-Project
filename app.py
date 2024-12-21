from db import app

# Run the app
if __name__ == "__main__":

    from routes import *
    app.run(debug=True)
