# Capstone NBA Player Stat Prediction

This project is a web application that predicts NBA player statistics using machine learning models and statistical methods. The application provides predictions for points (PTS), assists (AST), and rebounds (TRB) based on historical data, career averages, and matchup information.

## Features

- **Prediction Methods**:
  - **Random Forest**: A machine learning algorithm that builds decision trees to make predictions.
  - **Weighted Average**: A statistical approach using weighted averages of recent performance, career stats, and matchup data.
  - **Comparison Mode**: View predictions from both methods side-by-side.

- **Player Selection**:
  - Choose a team and player to see their predicted statistics.
  - Displays player images for better visualization.

- **Accuracy Metrics**:
  - Displays overall accuracy and individual accuracy for PTS, AST, and TRB.
  - Handles edge cases like division by zero when actual values are `0`.

- **Interactive UI**:
  - User-friendly interface built with React.
  - Dynamic tables to display predictions and accuracy metrics.

## Technologies Used

### Frontend
- **React**: For building the user interface.
- **CSS**: For styling the application.

### Backend
- **Flask**: For handling API requests and serving predictions.
- **Pandas**: For data manipulation and analysis.
- **Machine Learning**:
  - Random Forest model for predictions.

### Other Tools
- **Python**: For backend logic and data processing.
- **JavaScript**: For frontend interactivity.
- **GitHub**: For version control and collaboration.

## Installation

### Prerequisites
- Node.js and npm installed on your machine.
- Python 3.x installed.
- Flask, Numpy, Pandas, SKLearn, and MatPlotLib are the required Python libraries installed.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/jackhannan-hello/CapstoneNBAPlayerStatPredection.git
   cd CapstoneNBAPlayerStatPredection

2. Install frontend dependencies:
cd my-app
npm install

3. Install backend dependencies:
pip install -r requirments.txt

4. Start the backend server:
python src/server.py

5. Start the frontend development server:
cd my-app
npm start or npm run dev

6. Open the application in your browser:
when you run it. It should give you the link or web addres to run the site

Usage:
1. Select a team and player from the dropdown menus.
2. Choose a prediction method:
    Random Forest
    Weighted Average
    Both (Comparison Mode)
3. view the predicted statistics and accuracy metrics in the tables.
4. Check the player's image and overall accuracy for better insights.


License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or feedback, feel free to reach out:

Author: Jack Hannan
GitHub: jackhannan-hello
