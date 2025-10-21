# Pokémon Explorer

A simple full-stack application that displays Pokémon information using Python (Flask) for the backend, SQLite for data caching, and plain HTML/JavaScript for the frontend, with static file serving for the UI.

### Tech Stack
- Backend: Python 3 with Flask, Flask-SQLAlchemy, Flask-CORS
- Database: SQLite (for caching Pokémon data)
- Frontend: HTML, CSS, JavaScript (Vanilla JS with Fetch API)
- External API: PokéAPI[](https://pokeapi.co/)

### Setup Instructions
1. **Install Dependencies**
   - Ensure you have Python 3 installed.
   - Install required packages:

pip install flask flask-sqlalchemy flask-cors requests

2. **Prepare the Project**
- Create a folder named `static` in the project directory.
- Save the provided `index.html` file (see below) in the `static` folder.

3. **Run the Backend**
- Save the backend code in `app.py`.
- Run the Flask server:

python app.py

- The backend and frontend will be available at `http://127.0.0.1:5000`.

4. **Access the Application**
- Open your web browser and go to `http://127.0.0.1:5000`.
- No additional server is needed for the frontend, as it is served statically by Flask.

### How It Works
- The backend fetches data from PokéAPI, caches it in a SQLite database, and serves it via API endpoints:
- `GET /api/pokemon`: Returns a list of the first 20 Pokémon (name, image).
- `GET /api/pokemon/<name>`: Returns detailed information (name, image, types, height, weight, abilities).
- The frontend, served from the `/` route, displays a list of Pokémon. Clicking on one loads the detailed view, with a "Back to List" option.
- Data is cached to avoid repeated API calls, and CORS is enabled for cross-origin requests.

### Included Files
- `app.py`: Backend server with API endpoints and database logic.
- `static/index.html`: Frontend HTML file with embedded CSS and JavaScript.

### Notes
- If the `pokemon.db` file exists and is corrupted, delete it to re-fetch data from PokéAPI.
- The application assumes the `static` folder contains `index.html`. Ensure this file is present before running.
- Debug mode is enabled (`debug=True`), which provides helpful error messages during development.

### Example User Flow
1. User opens `http://127.0.0.1:5000`.
2. Sees a grid/list of the first 20 Pokémon with images.
3. Clicks on "Pikachu" to view detailed information.
4. Uses "Back to List" to return to the grid.

