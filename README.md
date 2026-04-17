# 🏈 Gridiron Wager – Practice Sports Betting Platform

A full-stack web application that simulates a sports betting environment, allowing users to place bets on NFL events using virtual currency, track performance, and analyze real-time statistics.

---

## 🚀 Features

* 👤 **User Authentication**

  * Account creation and secure login
  * JWT-based authentication for protected routes

* 💰 **Betting System**

  * Place bets on:

    * NFL Draft outcomes
    * Week 1 NFL games
    * Super Bowl winner
  * Track all bets through a user account dashboard

* 📊 **Statistics Dashboard**

  * View NFL player and team statistics
  * Data fetched and served through backend APIs

* 🎮 **Mini-Game**

  * Earn in-game currency through gameplay
  * Adds engagement and strategy to betting system

* 📈 **Bet Evaluation System**

  * Bets are evaluated and payouts are applied
  * User currency updates dynamically based on results

---

## 🛠️ Tech Stack

### Frontend

* **React**
* **React Router**
* **Bootstrap**
* JavaScript (ES6+)

### Backend

* **Python (Flask)**
* **SQLAlchemy**
* **JWT Authentication**
* **BeautifulSoup** (data scraping)

### Database

* **MySQL**

---

## 🧠 Key Concepts Demonstrated

* Full-stack application architecture (React + Flask)
* REST API design and integration
* Authentication using JWT
* State management across multiple views
* Database interaction and persistence
* Data scraping and processing
* Component-based UI design

---

## ⚙️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Tjhewett/practice-sportsbook-app.git
cd practice-sportsbook-app
```

---

### 2. Start the Frontend

```bash
npm install
npm start
```

Open:
👉 http://localhost:3000

---

### 3. Start the Backend

Navigate to the backend folder:

```bash
cd BackEnd
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python main.py
```

---

## ⚠️ Environment Setup

This project may require environment variables for:

* Database connection
* Secret keys (JWT)

Create a `.env` file (not included in repo):

```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

---

## 📂 Project Structure

```text
practice-sportsbook-app/
  src/              # React frontend
  BackEnd/          # Flask backend
  public/           # Static assets
```

---

## 📸 Screens

* Sign-in / Sign-up
* Betting dashboard
* Statistics page
* Mini-game
* User account dashboard
* Home page

---

## 🚧 Future Improvements

* Add real-time odds updates
* Improve UI/UX design
* Add more sports and betting types
* Implement live game tracking
* Enhance security and validation

---

## 👨‍💻 Author

Developed by Trevor Hewett as part of a senior capstone project, focused on building a full-stack application integrating real-world data, authentication, and user interaction.

---
