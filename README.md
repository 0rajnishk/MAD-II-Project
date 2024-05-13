# The Music App (Mad II Project)

The Music App is a modern music streaming application developed as part of the Modern Application Development II (Mad II) also known as Appdev 2 course. It allows users to listen to music, read lyrics, and even contribute as creators by uploading song lyrics and albums.

[Watch the presentation video](https://drive.google.com/drive/folders/1V0dc_jH9a1kC8haGDKPMDuKxT9YER_XQ?usp=sharing)

## Prerequisites

To run the Music App, you'll need:

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
    pip install -r requirements.txt
    ```

3. Set up and start the Flask server:

    ```bash
    python3 app.py
    ```

4. Start the Celery worker:

    ```bash
    celery -A backend.celery worker --loglevel=info
    ```
4. Start the Celery beat:

    ```bash
    celery -A backend.celery beat --loglevel=info
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

3. Start the development server:

    ```bash
    npm run dev
    ```

## Usage

Users can enjoy listening to music and reading lyrics. Creators can contribute by uploading song lyrics, albums, etc.

## Configuration

Creators need to sign up as users first and then can access the creator features from the user dashboard.

## Contributing

Feel free to contribute to the project on GitHub: [0rajnishk](https://github.com/0rajnishk)

## License

This project is licensed under the [MIT License](LICENSE.md).

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

## Screenshots

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)


