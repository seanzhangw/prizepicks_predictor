# README IN PROGRESS
# NBA Over/Under Predictor

This web application uses NBA data retrieved from the NBA API to train a logistic regression machine learning model. The model predicts whether the betting lines on PrizePicks will be over or under for NBA games. The backend handles data retrieval, data processing, and model training, while the frontend provides a user interface for entering bet information and viewing the predicted outcomes.

## Technologies Used

- Backend:
  - Programming Language: Python
  - Framework: Flask
  - Libraries: nba_api, scikit-learn, pandas

- Frontend:
  - Programming Languages: HTML, CSS, JavaScript
  - Framework: React
  - Libraries: Axios, Material-UI

## Backend Setup

1. Install Python (version X.X.X) and pip (if not already installed).
2. Clone this repository: `git clone https://github.com/seanzhangw/prizepicks_predictor`.
3. Navigate to the backend directory: `cd prizepicks_predictor/backend`.
4. Install the required Python dependencies: `pip install -r requirements.txt`.

## Frontend Setup

1. Navigate to the frontend directory: `cd ../frontend`.
2. Install Node.js (version X.X.X) and npm (if not already installed).
3. Install the required Node.js dependencies: `npm install`.

## Running the Application

1. Start the backend server:
   - Navigate to the backend directory: `cd backend`.
   - Run the Flask development server: `python app.py`.
   - The backend server will start running at `http://localhost:5000`.

2. Start the frontend development server:
   - Navigate to the frontend directory: `cd frontend`.
   - Run the React development server: `npm start`.
   - The frontend server will start running at `http://localhost:3000`.

3. Open your web browser and visit `http://localhost:3000` to access the web application.

<!-- ## API Endpoints

The backend provides the following API endpoints:

- `GET /api/games`: Retrieves a list of NBA games.
- `GET /api/games/{game_id}`: Retrieves details of a specific NBA game.
- `POST /api/predict`: Sends input data to the machine learning model for prediction.

Please refer to the API documentation for more details on the request and response formats. -->

## Acknowledgments

- The NBA API for providing the data used in this project.
- The scikit-learn and pandas libraries for their machine learning and data processing capabilities.
- The Flask and React communities for their excellent frameworks and libraries.