import mysql.connector
from fastapi import FastAPI, Form
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# --- CONFIGURATION ---
# 1. Add Gemini API Key
genai.configure(api_key="enter your key...")
model_ai = genai.GenerativeModel('gemini-2.5-flash')

# 2. Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=".......",
        database="fitai_db"
    )

app = FastAPI()

# 3. CORS Permission
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class LoginRequest(BaseModel):
    email: str
    password: str

# --- ROUTES ---

# 1. REGISTER

@app.post("/register")
def register_user(
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    age: int = Form(...), 
    weight: float = Form(...), 
    height: float = Form(...), 
    activity_level: int = Form(...), 
    gender: str = Form(...), 
    food_pref: str = Form(...)
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Check Existing User
    check_query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(check_query, (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return {"status": "Exist", "message": "Email already registered!"}

    # 2. Calculations
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)
    
    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    bmr = round(bmr, 2)
    
    multipliers = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725}
    tdee = round(bmr * multipliers.get(activity_level, 1.2), 2)
    
    diet_category = "Normal"
    if bmi < 18.5: diet_category = "Underweight"
    elif bmi > 24.9: diet_category = "Overweight"

    # --- 3. AI PLAN GENERATION (Safety Fix) ---

    diet_plan_text = """
    <table>
        <tr><th>Error</th></tr>
        <tr><td>Could not generate plan right now. Please try again later.</td></tr>
    </table>
    """

    prompt = f"""
    Act as a professional nutritionist. Create a strict 1-day diet plan for a {age} year old {gender}, 
    Weight: {weight}kg, Height: {height}cm, Goal: {diet_category}, Food Pref: {food_pref}.
    
    Output format: Provide ONLY an HTML Table code without ```html``` tags.
    The table must have these columns: 
    1. Meal (Breakfast, Lunch, Snack, Dinner)
    2. Food Recommendation (Specific items)
    3. Approx Calories
    
    Make it look clean. Do not add any introductory text or conclusion. Just the <table>...</table>.
    """
    
    try:
        response = model_ai.generate_content(prompt)
        # default value overwrite
        if response.text:
            diet_plan_text = response.text
    except Exception as e:
        print(f"⚠️ AI Error: {e}") 


    # 4. Database Save
    try:
        query = """INSERT INTO users 
                   (name, email, password, age, weight, height, food_pref, diet_plan_text, gender, activity_level, bmi, bmr, tdee, diet_category) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, email, password, age, weight, height, food_pref, diet_plan_text, gender, activity_level, bmi, bmr, tdee, diet_category))
        conn.commit()
        conn.close()

        return {
            "status": "Success",
            "message": "User registered!",
            "user_name": name,
            "diet_plan": diet_plan_text,
            "bmi": bmi, "bmr": bmr, "tdee": tdee, "category": diet_category
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}
# 2. LOGIN API (Email + Password Check)
@app.post("/login")
def login_user(request: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (request.email, request.password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "status": "Success",
            "user_name": user['name'],
            "diet_plan": user['diet_plan_text'],
            "bmi": user['bmi'],
            "bmr": user['bmr'],
            "tdee": user['tdee'],
            "category": user['diet_category']
        }
    else:
        # if not found
        return {"status": "Error", "message": "Invalid Email or Password!"}
    
    # --- ADMIN PANEL ROUTES ---

# 1. Get All Users
@app.get("/admin/users")
def get_all_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name, email, age, bmi, diet_category, created_at FROM users ORDER BY created_at DESC"
        cursor.execute(query)
        users = cursor.fetchall()
        conn.close()
        return {"status": "Success", "users": users}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

# 2. Delete User
@app.delete("/admin/users/{user_id}")
def delete_user(user_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        conn.close()
        return {"status": "Success", "message": "User deleted successfully!"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
    
    # --- ADMIN ANALYTICS ---

@app.get("/admin/stats")
def get_admin_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 1. Category Count (Pie Chart)
        cursor.execute("SELECT diet_category, COUNT(*) as count FROM users GROUP BY diet_category")
        categories = cursor.fetchall()
        
        # 2. Gender Count (Bar Chart)
        cursor.execute("SELECT gender, COUNT(*) as count FROM users GROUP BY gender")
        genders = cursor.fetchall()
        
        conn.close()
        return {"status": "Success", "categories": categories, "genders": genders}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
    
    # --- CHATBOT AI ROUTE  ---
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:

        prompt = f"Act as a friendly health & fitness coach. Answer this briefly: {request.message}"
        
        response = model_ai.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": "Sorry, I am having trouble connecting to the AI brain right now."}