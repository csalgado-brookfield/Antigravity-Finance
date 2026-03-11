# 💰 Antigravity Finance | Personal Finance Tracker

A premium, data-science powered personal finance application built with **Django**, **Pandas**, and **Plotly**. Track your spending with a modern glassmorphism interface and automatic merchant categorization.

![Premium Dashboard](https://img.shields.io/badge/UI-Glassmorphism-purple)
![Data Analysis](https://img.shields.io/badge/Analytics-Pandas%20%2B%20Plotly-blue)
![Backend](https://img.shields.io/badge/Backend-Django%205.0-green)

---

## ✨ Features

- 📊 **MoM Comparison**: Analyze current spending vs. the previous month with dual-line charts and percentage variance.
- 🎯 **Budget Targets & Alerts**: Set monthly limits per category. Visual indicators turn **Amber** at 80% and **Red** with alerts when exceeded.
- 🏦 **Multi-Account Analysis**: Track multiple credit cards or checking accounts in one consolidated view.
- 🤖 **AI Merchant Enrichment**: Automatically cleans "messy" bank descriptions and "learns" your specific categorization habits.
- 📂 **Smart CSV Import**: Optimized Pandas parsing for high-speed transaction intake.
- 🌓 **Premium Design**: Modern translucent glassmorphism UI with a focus on visual performance.
- 🐳 **Dockerized**: Ready for instant deployment on any environment.

---

## 🚀 Quick Start (Local Setup)

If you are setting this up on a new PC, follow these steps:

### Prerequisites
- Python 3.11+
- Git

### 1. Clone the Project
```bash
git clone https://github.com/csalgado-brookfield/Antigravity-Finance.git
cd Antigravity-Finance
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python manage.py migrate
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
```

### 6. Run the App
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

---

## 🐳 Quick Start (Docker)

If you have **Docker** installed, you can skip the manual setup:

```bash
# Clone and enter directory
git clone https://github.com/csalgado-brookfield/Antigravity-Finance.git
cd Antigravity-Finance

# Launch with Docker Compose
docker-compose up --build
```
The app will be available at `http://localhost:8000`.

---

## 📂 Project Structure

- `tracker/`: Core application logic.
  - `models.py`: Transaction and Category data structures.
  - `views.py`: Data processing (Pandas) and chart generation (Plotly).
  - `templates/`: Premium glassmorphism HTML templates.
- `personal_finance/`: Django project configuration.
- `Dockerfile` & `docker-compose.yml`: Containerization settings.

---

## 📝 Usage Tips
1. **Accounts First**: Before uploading, create an "Account" (e.g. "Main CC") to keep your cross-account analysis clean.
2. **Budgets**: Set monthly limits in the **Admin Panel** to see real-time Amber/Red alerts on your dashboard.
3. **AI Training**: If a merchant name is messy or uncategorized, update it in the **Transactions** view. The system will "learn" this for all future uploads!
4. **MoM Insights**: Hover over the trend line to see specific spending differences compared to the same day last month.

---
*Created with ❤️ by the Antigravity Team.*
