import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_fitness_model():
    # 1. CSV File route
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'fitness_data.csv')
    if not os.path.exists(csv_path):
        print("❌ Error: 'fitness_data.csv' nahi mili! Pehle generate_dataset.py run karein.")
        return

    # 2. Data Load
    df = pd.read_csv(csv_path)

    le_gender = LabelEncoder()
    le_food = LabelEncoder()
    
    df['gender'] = le_gender.fit_transform(df['gender'])
    df['food_pref'] = le_food.fit_transform(df['food_pref'])
    
    # 4. Features (X) aur Target (y) select
    X = df[['age', 'gender', 'height', 'weight', 'activity_level', 'food_pref']]
    y = df['category']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 6. Random Forest Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, 'fitness_model.pkl')
    joblib.dump(le_gender, 'gender_encoder.pkl')
    joblib.dump(le_food, 'food_encoder.pkl')
    
    accuracy = model.score(X_test, y_test)
    print(f"🎯 Model training complete!")
    print(f"✅ Accuracy: {accuracy * 100:.2f}%")
    print("📁 Model files (.pkl) 'backend' folder mein save ho gayi hain.")

if __name__ == "__main__":
    train_fitness_model()