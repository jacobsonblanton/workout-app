# Creating this Python file to run the web app

from workout_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) # automatically makes changes to the web server