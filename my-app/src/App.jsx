import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
    const [selectedValue, setSelectedValue] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [inputData, setInputData] = useState(null);
    const [showImage, setShowImage] = useState(false);

    const handleChange = async (event) => {
        setSelectedValue(event.target.value);
        setShowImage(false);

        if (event.target.value === "predict") {
            try {
                // Fetch prediction results
                const predictionResponse = await fetch("http://localhost:5000/get-prediction");
                const predictionData = await predictionResponse.json();

                // Fetch input results
                const inputResponse = await fetch("http://localhost:5000/get-input");
                const inputData = await inputResponse.json();

                if (predictionData.predictions && inputData.input_data) {
                    setPrediction(JSON.parse(predictionData.predictions)); // Convert back to array of objects
                    setInputData(JSON.parse(inputData.input_data));
                    setShowImage(true); // Show image after fetching data
                } else {
                    console.error("Error fetching predictions:", predictionData.error, inputData.error);
                }
            } catch (error) {
                console.error("Request failed:", error);
            }
        }
    };

    return (
        <div className="container">
            <h2>NBA Player Prediction</h2>
            <select value={selectedValue} onChange={handleChange} className="select-box">
                <option value="">Select an option</option>
                <option value="predict">Run Prediction</option>
            </select>

            {showImage && (
                <div>
                    <img
                        src="https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/4278073.png&w=350&h=254"
                        alt="Player"
                        className="player-image"
                    />
                </div>
            )}

            {/* Prediction Table */}
            {prediction && (
                <div className="table-container">
                    <h3>Prediction Results</h3>
                    <h3>Result from Random Forest Prediction</h3>
                    {prediction.map((row, index) => (
                        <table className="prediction-table" key={index}>
                            <thead>
                                <tr>
                                    <th>Stat</th>
                                    <th>Actual</th>
                                    <th>Predicted</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>PTS</td>
                                    <td>{row.PTS}</td>
                                    <td>{row.Predicted_PTS}</td>
                                </tr>
                                <tr>
                                    <td>AST</td>
                                    <td>{row.AST}</td>
                                    <td>{row.Predicted_AST}</td>
                                </tr>
                                <tr>
                                    <td>TRB</td>
                                    <td>{row.TRB}</td>
                                    <td>{row.Predicted_TRB}</td>
                                </tr>
                            </tbody>
                        </table>
                    ))}
                </div>
            )}

            {/* Input Data Table */}
            {inputData && (
                <div className="table-container">
                    <h3>Result from Average Prediction</h3>
                    {inputData.map((row, index) => (
                        <table className="prediction-table" key={index}>
                            <thead>
                                <tr>
                                    <th>Stat</th>
                                    <th>Actual</th>
                                    <th>Predicted</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>PTS</td>
                                    <td>{row.PTS}</td>
                                    <td>{row.Predicted_PTS}</td>
                                </tr>
                                <tr>
                                    <td>AST</td>
                                    <td>{row.AST}</td>
                                    <td>{row.Predicted_AST}</td>
                                </tr>
                                <tr>
                                    <td>TRB</td>
                                    <td>{row.TRB}</td>
                                    <td>{row.Predicted_TRB}</td>
                                </tr>
                            </tbody>
                        </table>
                    ))}
                </div>
            )}
        </div>
    )
}

export default App
