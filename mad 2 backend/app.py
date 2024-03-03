from backend import app
from flask_cors import CORS

CORS(app)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)