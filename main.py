from constants import PORT

from service.application import app

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
