# The Music App 

Short description of my project.

## Prerequisites

- Python 3.10
- Node.js
- Redis

## Installation

### Backend (Flask)

1. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install Python dependencies:

    ```bash
    pip install -r r.txt
    ```

3. Set up and start Flask server:

    ```bash
    python3 app.py
    ```

4. Start Celery worker:

    ```bash
    celery -A backend.celery worker --loglevel=info
    ```

### Frontend (Vue.js)

1. Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

2. Install Node.js dependencies:

    ```bash
    npm install
    ```

3. Start development server:

    ```bash
    npm run dev
    ```

## Usage

Listen to great music, read lyrics. If you are a creator, upload song lyrics, album, etc.

## Configuration

If you are a creator, first sign up as a user and then from the user dashboard, you will get a link to become a creator.

## Contributing

GitHub: [0rajnishk](https://github.com/0rajnishk)

## License

This project is licensed under the [License Name] - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Flask
- Node.js
- Vue.js
- Python
- Celery
- Redis
- JWT
- Flask Session
- Flask Restful API
- And others.


video: https://drive.google.com/drive/folders/1V0dc_jH9a1kC8haGDKPMDuKxT9YER_XQ?usp=sharing