# airline-system

## Overview
This project is an Air Flight Ticket System built using Flask and SQLAlchemy. It allows users to buy tickets, view available flights, explore transit flight options, and perform range searches based on days, price, and destination.

## Features
- User authentication and authorization
- Ticket purchasing functionality
- Viewing available flights with transit options
- Range search by days, price, and destination
- Simple and intuitive UI using plain templates

## Tech Stack
- Flask: Web framework for Python
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) for Python
- SQLite: Lightweight relational database

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/air-flight-ticket-system.git
   cd air-flight-ticket-system

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade


4. Run the application:
   ```bash
   flask run

5. Access the application in your browser: http://localhost:5000

## Usage

1. Create an account or log in if you already have one.
2. Explore available flights and transit options.
3. Purchase tickets for your desired flights.
4. Use the range search feature to filter flights based on days, price, and destination.


