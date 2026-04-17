# Gridiron Wager - A practice sports betting enviornment

[GitHub Repository Link](https://github.com/Tjhewett/Senior-Capstone/tree/master).\
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).\
The Backend is in Python Flask.\
The data is stored using MySQL.

## How to Run the React code

In the project directory (gridiron-wager), you can run:

```bash
  npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The code contains components that swap in and out of a single html page when choosing different Routes.

imports: React, useEffect, useState, useRef, useMemo ReactDOM, Link, Route, Routes, BrowserRouter, Navigate, Bootstrap.

to install imports, run npm install ...

## How to Run the Flask code 

Make sure that you have Python 3.12.0 & sql3 installed. Code can be found in the BackEnd Folder.

Open the directory in VS code or another IDE and run main.py.

This must be run alongside the React App so the endpoints on the backend can be met.

imports: Flask, jsonify, request, requests, BeautifulSoup, SQLAlchem, CORS, Bcrypt, JWTManager, os, Blueprint, create_access_token, pytest, jwt_required, get_jwt_identity, pymysql.cursors.

to install imports, run pip install ...

## Final Implementation

Users can view stats on the stat page and create an account on the sign-up page. Users can place bets on the NFL draft, week 1 NFL games, and the 2025 Super Bowl champion. Users can play a mini-game to increase thier in-game currency.

Stats are fetched from the database in MySQL and accounts are posted to the database when an account hasn't been created. Bets are saved and can be viewed under the account page. Currency gets updated when bets have been evaluated as a win. 

Impemented Features:
- User Profiles: 100%
- Different Betting styles: 100%
- Bet Tracking: 100%
- Mini-game: 100%
- Stats tab: 100%
- In-Game currency: 100% 

Current screens:
- Sign-in/Sign-up screen
- Betting screen
- Statistics screen
- Mini-game screen
- Account screen 
- Home screen






