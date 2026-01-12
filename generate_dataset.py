import pandas as pd
import numpy as np

def generate_accurate_data(n=5000):
    np.random.seed(42)
    data = []
    
    for _ in range(n):
        age = np.random.randint(18, 70)
        gender = np.random.choice(['Male', 'Female'])
        height = np.random.randint(150, 200)
        weight = np.random.randint(45, 120)
        activity_level = np.random.randint(1, 5) # 1: Sedentary to 4: Very Active
        food_pref = np.random.choice(['Veg', 'Non-Veg', 'Vegan'])
        
        # Medical Logic for BMI
        bmi = weight / ((height/100)**2)
        
        if bmi < 18.5: category = "Underweight"
        elif 18.5 <= bmi < 25: category = "Normal"
        elif 25 <= bmi < 30: category = "Overweight"
        else: category = "Obese"
        
        data.append([age, gender, height, weight, activity_level, food_pref, round(bmi, 2), category])
        
    df = pd.DataFrame(data, columns=['age', 'gender', 'height', 'weight', 'activity_level', 'food_pref', 'bmi', 'category'])
    df.to_csv('fitness_data.csv', index=False)
    print("✅ 'fitness_data.csv' with 5000 rows is ready!")

generate_accurate_data(5000)