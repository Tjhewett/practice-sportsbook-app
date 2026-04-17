# Main File that runs the server. Run this file to start the server. 

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

