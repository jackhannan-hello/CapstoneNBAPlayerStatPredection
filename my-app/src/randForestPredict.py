import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree


def get_prediction():
    file_path = "sgaFullStats.csv"
    df = pd.read_csv(file_path)

    df = df.drop(columns=["Date", "Unnamed: 6", "G", "Age", "GS", "MP", "FG", "FGA",
                          "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB",
                          "STL", "BLK", "TOV", "PF", "GmSc", "+/-"])
    df = df.dropna()

    X = df.drop(columns=["PTS", "AST", "TRB"])
    y = df[["PTS", "AST", "TRB"]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    #X_train = scaler.fit_transform(X_train)
    #X_test = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error: {mae} for model\n\n")

    #plt.figure(figsize=(20, 10))
    #plot_tree(model.estimators_[0], feature_names=X.columns, filled=True, rounded=True, fontsize=10)
    #plt.show()

    recent = df.tail(5)
    actual_recent = recent[["PTS", "AST", "TRB"]]
    test_recent = recent.drop(columns=["PTS", "AST", "TRB"])
    recent_pred = model.predict(test_recent)


    #plt.figure(figsize=(20, 13))
    #plot_tree(model.estimators_[0], feature_names=test_recent.columns, filled=True, rounded=True, fontsize=10)
    #plt.show()

    predicted_df = pd.DataFrame(recent_pred, columns=["Predicted_PTS", "Predicted_AST", "Predicted_TRB"]).round(2)

    combined_df = pd.concat([actual_recent.reset_index(drop=True), predicted_df], axis=1)

    print("Actual stats compared to predicted stats for recent games")
    print(combined_df)

    recent_mae = mean_absolute_error(test_recent, recent_pred)
    print(f"Mean Absolute Error: {recent_mae}")

    return combined_df

if __name__ == '__main__':
    get_prediction()