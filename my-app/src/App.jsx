import { useState, useEffect  } from 'react'
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import './App.css'

// NBA Teams data with their players
const NBA_TEAMS = {
    "All Teams": ["Select a player"],
    "Boston Celtics": ["Jayson Tatum", "Jaylen Brown", "Al Horford", "Payton Pritchard"],
    "New York Knicks": ["Josh Hart", "Jalen Brunson"],
    "Phoenix Suns": ["Devin Booker", "Kevin Durant"],
    "Oklahoma City Thunder": ["Shai Gilgeous-Alexander"],
    "Los Angeles Lakers": ["LeBron James", "Austin Reaves"],
    "Golden State Warriors": ["Stephen Curry", "Draymond Green", "Andrew Wiggins"],
    "Denver Nuggets": ["Jamal Murray", "Russell Westbrook"],
    "Miami Heat": ["Bam Adebayo", "Tyler Herro"],
    "Minnesota Timberwolves": ["Rudy Gobert"],
    // Add more teams as needed
  };

// Player image mapping
const PLAYER_IMAGES = {
    'Jayson Tatum': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4065648.png&w=350&h=254',
    'Jaylen Brown': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3917376.png&w=350&h=254',
    'Al Horford': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3213.png&w=350&h=254',
    'Payton Pritchard': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4066835.png&w=350&h=254',
    'Josh Hart': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3062679.png&w=350&h=254',
    'Jalen Brunson': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3934672.png&w=350&h=254',
    'Devin Booker': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3136193.png&w=350&h=254',
    'Kevin Durant': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3202.png&w=350&h=254',
    'Shai Gilgeous-Alexander': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4278073.png&w=350&h=254',
    'LeBron James': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/1966.png&w=350&h=254',
    'Austin Reaves': 'https://cdn.nba.com/headshots/nba/latest/1040x760/1630559.png',
    'Stephen Curry': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3975.png&w=350&h=254',
    'Draymond Green': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/6589.png&w=350&h=254',
    'Andrew Wiggins': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3059319.png&w=350&h=254',
    'Jamal Murray': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3936299.png&w=350&h=254',
    'Russell Westbrook': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3468.png&w=350&h=254',
    'Bam Adebayo': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4066261.png&w=350&h=254',
    'Tyler Herro': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4395725.png&w=350&h=254',
    'Rudy Gobert': 'https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3032976.png&w=350&h=254',
  };

// Player API key mapping
const PLAYER_KEYS = {
    'Shai Gilgeous-Alexander': 'sga',
    'Jayson Tatum': 'jayson_tatum',
    'Josh Hart': 'josh_hart',
    'Devin Booker': 'devin_booker'
};

// Description of prediction methods
const PREDICTION_METHODS = {
    'both': {
      name: 'Both Methods',
      description: 'Show predictions from both Random Forest and Average-based methods'
    },
    'random_forest': {
      name: 'Random Forest',
      description: 'Advanced machine learning algorithm that builds decision trees to make predictions'
    },
    'average': {
      name: 'Weighted Average',
      description: 'Statistical approach using weighted averages of recent performance, career stats, and matchup data'
    }
  };

function calculateAccuracy(data) {
    if (!data || data.length === 0) return { overall: 0, stats: {} };

    const stats = ["PTS", "AST", "TRB"];
    let totalAccuracy = 0;
    const accuracyMetrics = {};

    stats.forEach((stat) => {
        const actual = data[0][stat]; // Assuming the first row contains the actual values
        const predicted = data[0][`Predicted_${stat}`];

        if (actual === 0) {
            accuracyMetrics[stat] = 0; // Avoid division by zero
        } else {
            const percentageError = Math.abs((actual - predicted) / actual) * 100;
            const accuracy = Math.max(0, 100 - percentageError);
            accuracyMetrics[stat] = accuracy.toFixed(2); // Round to 2 decimal places
            totalAccuracy += accuracy;
        }
    });

    const overallAccuracy = (totalAccuracy / stats.length).toFixed(2); // Average accuracy
    return { overall: overallAccuracy, stats: accuracyMetrics };
}

function App() {
    const [selectedTeam, setSelectedTeam] = useState("All Teams");
    const [availablePlayers, setAvailablePlayers] = useState(NBA_TEAMS["All Teams"]);
    const [selectedPlayer, setSelectedPlayer] = useState("");
    const [predictionMethod, setPredictionMethod] = useState("both");
    const [prediction, setPrediction] = useState(null);
    const [inputData, setInputData] = useState(null);
    const [rfAccuracyMetrics, setRfAccuracyMetrics] = useState(null);
    const [avgAccuracyMetrics, setAvgAccuracyMetrics] = useState(null);
    const [showImage, setShowImage] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    //const [debugInfo, setDebugInfo] = useState({});

    // Helper function to safely parse JSON
    const safeJsonParse = (jsonString, defaultValue = []) => {
        try {
            return JSON.parse(jsonString);
        } catch (e) {
            console.error("Error parsing JSON:", e);
            return defaultValue;
        }
    };

    // Flatten all players into a single array for direct player selection
    const allPlayers = Object.values(NBA_TEAMS)
        .flat()
        .filter(player => player !== "Select a player");

    // Effect to update available players based on selected team
    useEffect(() => {
        if (selectedTeam === "All Teams") {
            setAvailablePlayers(allPlayers);
        } else {
            setAvailablePlayers(NBA_TEAMS[selectedTeam]);
        }
    }, [selectedTeam]);
    // Effect to reset selected player when available players change
    useEffect(() => {
        setSelectedPlayer("");
        setPrediction(null);
        setInputData(null);
        setShowImage(false);
        setRfAccuracyMetrics(null);
        setAvgAccuracyMetrics(null);
        setError(null);
    }, [availablePlayers]);

    const handleTeamChange = (event) => {
        setSelectedTeam(event.target.value);
    };

    const handlePredictionMethodChange = (method) => {
        setPredictionMethod(method);
      };

    const handlePlayerChange = async (event) => {
        const playerName = event.target.value;
        setSelectedPlayer(playerName);
        setShowImage(false);
        setError(null);
        setPrediction(null);
        setRfAccuracyMetrics(null);
        setAvgAccuracyMetrics(null);
        //setDebugInfo({});

        if (playerName) { 
            setLoading(true);
            try {
                const playerKey = PLAYER_KEYS[playerName];
                const debugData = { playerName, playerKey };

                // Determine which predictions to fetch based on selected method
                let shouldFetchRF = predictionMethod === 'both' || predictionMethod === 'random_forest';
                let shouldFetchAvg = predictionMethod === 'both' || predictionMethod === 'average';

                // Fetch Random Forest prediction if needed
                if (shouldFetchRF) {
                    const predictionUrl = `http://localhost:5000/get-prediction?player=${playerKey}`;
                    const predictionResponse = await fetch(predictionUrl);
                    const predictionText = await predictionResponse.text();
                    
                    let predictionData;
                    try {
                    predictionData = JSON.parse(predictionText);
                    if (predictionData.predictions) {
                        const predictionArray = safeJsonParse(predictionData.predictions, []);
                        setPrediction(predictionArray.length > 0 ? predictionArray : [
                        { PTS: 0, AST: 0, TRB: 0, Predicted_PTS: 0, Predicted_AST: 0, Predicted_TRB: 0 }
                        ]);
                        // Set accuracy metrics for Random Forest
                        const accuracyMetrics = calculateAccuracy(predictionArray);
                        setRfAccuracyMetrics(accuracyMetrics);
                    }                    

                    } catch (e) {
                    console.error("Error parsing Random Forest prediction:", e);
                    if (shouldFetchRF && !shouldFetchAvg) {
                        throw new Error(`Failed to parse prediction response: ${e.message}`);
                    }
                    }
                }
                // debugData.predictionStatus = predictionResponse.status;
                // debugData.predictionText = predictionText.substring(0, 100) + (predictionText.length > 100 ? '...' : '');

                // let predictionData;
                // try {
                //     predictionData = JSON.parse(predictionText);
                // } catch (e) {
                //     throw new Error(`Failed to parse prediction response: ${e.message}. Response starts with: ${predictionText.substring(0, 50)}`);
                // }

                // Fetch Average-based prediction if needed
                if (shouldFetchAvg) {
                    const inputUrl = `http://localhost:5000/get-input?player=${playerKey}`;
                    const inputResponse = await fetch(inputUrl);
                    const inputText = await inputResponse.text();
            
                    let inputData;
                    try {
                    inputData = JSON.parse(inputText);
                    if (inputData.input_data) {
                        const inputArray = safeJsonParse(inputData.input_data, []);
                        setInputData(inputArray.length > 0 ? inputArray : [
                        { PTS: 0, AST: 0, TRB: 0, Predicted_PTS: 0, Predicted_AST: 0, Predicted_TRB: 0 }
                        ]);
                        // Set accuracy metrics for Average method
                        const accuracyMetrics = calculateAccuracy(inputArray);
                        setAvgAccuracyMetrics(accuracyMetrics);
                    }


                    } catch (e) {
                    console.error("Error parsing Average prediction:", e);
                    if (shouldFetchAvg && !shouldFetchRF) {
                        throw new Error(`Failed to parse input response: ${e.message}`);
                    }
                    }
                }

                // debugData.inputStatus = inputResponse.status;
                // debugData.inputText = inputText.substring(0, 100) + (inputText.length > 100 ? '...' : '');

                // let inputData;
                // try {
                //     inputData = JSON.parse(inputText);
                // } catch (e) {
                //     throw new Error(`Failed to parse input response: ${e.message}. Response starts with: ${inputText.substring(0, 50)}`);
                // }

                //setDebugInfo(debugData);

                // Check if we got at least one valid prediction
                if ((shouldFetchRF && !prediction && !shouldFetchAvg) || 
                    (shouldFetchAvg && !inputData && !shouldFetchRF)) {
                    setError("Failed to get any valid predictions. Please try another player or method.");
                } else {
                setShowImage(true);
                }
            } catch (error) {
                setError(`Request failed: ${error.message}`);
                console.error("Request failed:", error);
            }
            finally {
                setLoading(false);
            }
        }
    };

    
    // const getAccuracyColor = (accuracy) => {
    //     if (accuracy >= 90) return 'text-green-600 font-bold';
    //     if (accuracy >= 80) return 'text-green-500';
    //     if (accuracy >= 70) return 'text-yellow-500';
    //     if (accuracy >= 60) return 'text-yellow-600';
    //     return 'text-red-500';
    //   };

    // const renderAccuracyMetrics = (metrics) => {
    //     if (!metrics || Object.keys(metrics).length === 0) {
    //         return null;
    //       }

    //     return (
    //         <div className="accuracy-container mt-4 p-4 bg-gray-100 rounded-lg shadow">
    //           <h4 className="text-lg font-semibold mb-3">Prediction Accuracy</h4>
              
    //           <div className="overall-accuracy mb-4">
    //             <div className="flex items-center justify-between">
    //               <span className="text-gray-700 font-medium">Overall Accuracy:</span>
    //               <span className={`text-xl ${getAccuracyColor(metrics.overall)}`}>
    //                 {metrics.overall}%
    //               </span>
    //             </div>
                
    //             {/* Visual accuracy bar */}
    //             <div className="w-full bg-gray-300 rounded-full h-4 mt-2">
    //               <div 
    //                 className="bg-blue-600 h-4 rounded-full" 
    //                 style={{ width: `${Math.min(100, metrics.overall)}%` }}
    //               ></div>
    //             </div>
    //           </div>
        
    //           <div className="stat-accuracies grid grid-cols-3 gap-4">
    //             {['PTS', 'AST', 'TRB'].map(stat => (
    //               <div key={stat} className="stat-accuracy text-center p-2 bg-white rounded shadow-sm">
    //                 <div className="stat-name font-medium">{stat}</div>
    //                 <div className={`stat-value text-lg ${getAccuracyColor(metrics[stat].accuracy)}`}>
    //                   {metrics[stat].accuracy}%
    //                 </div>
    //                 <div className="stat-error text-xs text-gray-500">
    //                   Error: {metrics[stat].absolute_error} ({metrics[stat].percentage_error}%)
    //                 </div>
    //               </div>
    //             ))}
    //           </div>
    //         </div>
    //       );
    // };

    return (
        <div className='wrapper'>
            <div className='split-background'></div>
            
            <a 
                href="https://github.com/jackhannan-hello/CapstoneNBAPlayerStatPredection" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="github-link"
            >
             <img 
                src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" 
                alt="GitHub" 
                className="github-icon" 
             />
             View Code for Preditions on GitHub
            </a>
            <div className="container">
                <h2 className='title'>NBA Player Prediction</h2>
                <div className='method-selection'>
                    <h3>Choose Prediction Method You Would Like To Use</h3>
                    <p className='subtitle'>Select a team and player to see predicted statistics based on player performance</p>
                    <div className='method-options'>
                        <button 
                            onClick={() => handlePredictionMethodChange('random_forest')}
                            className={`method-button method-rf ${predictionMethod === 'random_forest' ? 'method-button-active' : ''}`}
                        > 
                            Random Forest
                        </button>
                        <button s
                            onClick={() => handlePredictionMethodChange('average')}
                            className={`method-button method-avg ${predictionMethod === 'average' ? 'method-button-active' : ''}`}
                        >
                            Weighted Average
                        </button>
                        <button 
                            onClick={() => handlePredictionMethodChange('both')}
                            className={`method-button method-both ${predictionMethod === 'both' ? 'method-button-active' : ''}`}
                        >
                            Compare Both
                        </button>
                    </div>
                    <div className='method-description'>
                        {PREDICTION_METHODS[predictionMethod].description}
                    </div>
                </div>                 
                
                <h3>Select Team and Player</h3>
                <div className='select-container'>
                <select
                    value={selectedTeam}
                    onChange={handleTeamChange}
                    className="select-box"
                    disabled={loading}
                >
                    {Object.keys(NBA_TEAMS).map((team) => (
                        <option key={team} value={team}>
                            {team}
                        </option>
                    ))}
                </select>
                <select
                    value={selectedPlayer}
                    onChange={handlePlayerChange}
                    className="select-box"
                    disabled={loading}
                >
                    <option value="">Select a player</option>
                    {availablePlayers.map((player) => (
                        <option key={player} value={player}>
                            {player}
                        </option>
                    ))}
                </select>
                </div>

                {loading && <div className="loading">Loading predictions...</div>}

                {error && <div className="error-message">{error}</div>}

                {showImage && (
                    <div>
                        <img
                            src={PLAYER_IMAGES[selectedPlayer]}
                            alt={selectedPlayer}
                            className="player-image"
                        />
                    </div>
                )}

                {/* Prediction Table */}
                {prediction && rfAccuracyMetrics && (
                    <div className="table-container">                        
                        <h3>Prediction Results</h3>
                        <div className="prediction-header">
                            <h3>Result from Random Forest Prediction</h3>
                            <p>Overall Accuracy: {rfAccuracyMetrics.overall}%</p> {/* Display overall accuracy */}
                        </div>
                        {prediction.map((row, index) => (
                            <table className="prediction-table" key={index}>
                                <thead>
                                    <tr>
                                        <th>Stat</th>
                                        <th>Actual</th>
                                        <th>Predicted</th>
                                        <th>Accuracy (%)</th> {/* Add Accuracy column */}
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>PTS</td>
                                        <td>{row.PTS}</td>
                                        <td>{row.Predicted_PTS}</td>
                                        <td>{rfAccuracyMetrics.stats.PTS}%</td> {/* Display PTS accuracy */}
                                    </tr>
                                    <tr>
                                        <td>AST</td>
                                        <td>{row.AST}</td>
                                        <td>{row.Predicted_AST}</td>
                                        <td>{rfAccuracyMetrics.stats.AST}%</td> {/* Display AST accuracy */}
                                    </tr>
                                    <tr>
                                        <td>TRB</td>
                                        <td>{row.TRB}</td>
                                        <td>{row.Predicted_TRB}</td>
                                        <td>{rfAccuracyMetrics.stats.TRB}%</td> {/* Display TRB accuracy */}
                                    </tr>
                                </tbody>
                            </table>
                        ))}
                    </div>
                )}

                {/* Input Data Table */}
                {inputData && avgAccuracyMetrics && (
                    <div className="table-container">
                        <div className="prediction-header">
                            <h3>Result from Average Prediction</h3>
                            <p>Overall Accuracy: {avgAccuracyMetrics.overall}%</p> {/* Display overall accuracy */}
                        </div>
                        {inputData.map((row, index) => (
                            <table className="prediction-table" key={index}>
                                <thead>
                                    <tr>
                                        <th>Stat</th>
                                        <th>Actual</th>
                                        <th>Predicted</th>
                                        <th>Accuracy (%)</th> {/* Add Accuracy column */}
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>PTS</td>
                                        <td>{row.PTS}</td>
                                        <td>{row.Predicted_PTS}</td>
                                        <td>{avgAccuracyMetrics.stats.PTS}%</td> {/* Display PTS accuracy */}
                                    </tr>
                                    <tr>
                                        <td>AST</td>
                                        <td>{row.AST}</td>
                                        <td>{row.Predicted_AST}</td>
                                        <td>{avgAccuracyMetrics.stats.AST}%</td> {/* Display AST accuracy */}
                                    </tr>
                                    <tr>
                                        <td>TRB</td>
                                        <td>{row.TRB}</td>
                                        <td>{row.Predicted_TRB}</td>
                                        <td>{avgAccuracyMetrics.stats.TRB}%</td> {/* Display TRB accuracy */}
                                    </tr>
                                </tbody>
                            </table>
                        ))}
                    </div>
                )}
                <div className="gambling-disclaimer">
                <div className="disclaimer-title">GAMBLING DISCLAIMER</div>
                <p>
                This NBA Player Stat Prediction tool is designed for informational and entertainment purposes only. 
                The predictions provided are based on statistical models and machine learning algorithms that analyze 
                historical data. These predictions do not guarantee future performance and should not be used as the 
                sole basis for placing bets or making gambling decisions. Sports outcomes are inherently unpredictable 
                and can be affected by numerous factors beyond statistical analysis. Users should exercise responsible 
                gambling practices and seek advice from licensed gambling providers. If you or someone you know has a 
                gambling problem, please call 1-800-GAMBLER for support.
                </p>
                </div>
                    {/* Debug information - hidden by default */}
                    {/* <div className={`debugSection ${Object.keys(debugInfo).length > 0 ? 'show' : ''}`}>
                        <h4>Debug Information</h4>
                        <pre>{JSON.stringify(debugInfo, null, 2)}</pre>
                    </div> */}
                </div>
        </div>
    )
}

export default App
