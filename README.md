# 💰 Antigravity Finance | Personal Finance Tracker

A premium, data-science powered personal finance application built with **Django**, **Pandas**, and **Plotly**. Track your spending with a modern glassmorphism interface and automatic merchant categorization.

![Premium Dashboard](https://img.shields.io/badge/UI-Glassmorphism-purple)
![Data Analysis](https://img.shields.io/badge/Analytics-Pandas%20%2B%20Plotly-blue)
![Backend](https://img.shields.io/badge/Backend-Django%205.0-green)

---

## ✨ Features

- 📊 **Interactive Dashboard**: Visualize spending trends and category breakdowns with Plotly charts.
- 📂 **Smart CSV Import**: Upload credit card statements; Pandas handles the parsing.
- 🤖 **Auto-Categorization**: Merchant keywords are automatically mapped to categories (Food, Transport, Utilities, etc.).
- 🛠 **Transaction Management**: Edit and override categories manually.
- 🌓 **Premium Design**: Modern dark-mode UI with translucent glass effect cards.
- 🐳 **Dockerized**: Easy deployment with Docker and Docker Compose.

---

## 🚀 Quick Start (Local Setup)

If you are setting this up on a new PC, follow these steps:

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the Project
```bash
git clone https://github.com/your-username/antigravity-finance.git
cd antigravity-finance
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
git clone https://github.com/your-username/antigravity-finance.git
cd antigravity-finance

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
1. **Sample Data**: Use the included `sample_statement.csv` to quickly test the dashboard visualizations.
2. **Admin Panel**: For bulk category management, visit `http://127.0.0.1:8000/admin/`.

---
*Created with ❤️ by the Antigravity Team.*
