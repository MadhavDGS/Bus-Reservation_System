# Saketh Bus Reservation System

A simple bus reservation system built with Python and Flask. This system allows users to search for buses, book tickets, and view their bookings.

## Features

- Search buses by route and date
- View available buses and their details
- Book tickets with passenger information
- View booking confirmations
- View all bookings in one place

## Setup Instructions

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit:
```
http://localhost:5000
```

## Usage

1. On the home page, enter your journey details (From, To, and Date)
2. Click "Search Buses" to view available buses
3. Select a bus and click "Book Now"
4. Fill in your details and confirm the booking
5. View your booking confirmation
6. Access all your bookings from the "My Bookings" page

## Note

This is a demo application with dummy data. In a production environment, you would need to:
- Implement a proper database
- Add user authentication
- Add payment processing
- Implement proper security measures
- Add admin features for bus management

## Technologies Used

- Python
- Flask
- Bootstrap 5
- HTML/CSS
- JavaScript # Bus-Reservation_System
