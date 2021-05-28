from constants import HOST, PORT

from service.application import app

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
