# ⚡ IntelliFit - AI Powered Health & Fitness Companion

**IntelliFit** is a smart web application designed to help users achieve their fitness goals using the power of Artificial Intelligence. It generates personalized diet plans, tracks health metrics (BMI, BMR, TDEE), and provides an interactive AI Chatbot for 24/7 health guidance.

---

## 🚀 Key Features

* **🥗 AI Diet Planner:** Generates custom daily meal plans using Google Gemini AI based on user's height, weight, and goals.
* **🤖 AI Health Chatbot:** A built-in floating chatbot to answer queries about nutrition, workouts, and wellness.
* **📊 Smart Dashboard:** Interactive visualizations (Charts & Graphs) for nutrient breakdown (Protein, Carbs, Fats).
* **⚖️ Advanced Health Metrics:**
    * **BMI Meter:** Visual needle gauge to show Body Mass Index.
    * **BMR & TDEE:** Auto-calculation of daily calorie needs.
* **🧘‍♀️ Video Yoga Guide:** Recommends specific yoga poses (with video tutorials) based on whether the user is Underweight, Normal, or Overweight.
* **💧 Water & Step Tracker:** Interactive tools to track daily hydration and step goals.
* **🔒 Secure Authentication:** User Registration and Login system with MySQL database.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3 (Modern UI), JavaScript (Chart.js for graphs).
* **Backend:** Python (FastAPI Framework).
* **Database:** MySQL Workbench.
* **AI Integration:** Google Gemini API (Generative AI).
* **Tools:** VS Code, Git/GitHub.

---

## ⚙️ How to Run Locally

Follow these steps to run the project on your machine:

### 1. Prerequisites
* Python installed.
* MySQL Workbench installed.
* Git installed.

### 2. Clone the Repository
```bash
  git clone [https://github.com/YourUsername/IntelliFit-Health-AI.git](https://github.com/YourUsername/IntelliFit-Health-AI.git)
cd IntelliFit-Health-AI

3. Install Dependencies
pip install -r requirements.txt

4. Setup Database (MySQL Workbench)

Open MySQL Workbench.
Create a new schema (database) named intellifit.
Go to Server > Data Import.
Select "Import from Self-Contained File" and choose the intellifit.sql file (provided in this folder).
Click Start Import.

5. Run the Server

Open the terminal in the backend folder and run:
uvicorn main:app --reload

6. Launch the App
Open your browser and go to: http://127.0.0.1:5500/frontend/index.html (or open via file explorer).

👤 Author
Shiwangi Maurya
BCA Student
Aspiring Software Developer
LinkedIn :https://www.linkedin.com/in/shiwangi-maurya-75302328b

Made with ❤️ and Python.