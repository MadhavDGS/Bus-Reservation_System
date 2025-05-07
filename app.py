from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Indian cities with their states
INDIAN_CITIES = {
    'Hyderabad': 'Telangana',
    'Bangalore': 'Karnataka',
    'Chennai': 'Tamil Nadu',
    'Mumbai': 'Maharashtra',
    'Delhi': 'Delhi',
    'Kolkata': 'West Bengal',
    'Pune': 'Maharashtra',
    'Jaipur': 'Rajasthan',
    'Ahmedabad': 'Gujarat',
    'Lucknow': 'Uttar Pradesh',
    'Bhopal': 'Madhya Pradesh',
    'Chandigarh': 'Punjab',
    'Kochi': 'Kerala',
    'Bhubaneswar': 'Odisha',
    'Guwahati': 'Assam',
    'Patna': 'Bihar',
    'Ranchi': 'Jharkhand',
    'Dehradun': 'Uttarakhand',
    'Shimla': 'Himachal Pradesh',
    'Srinagar': 'Jammu & Kashmir'
}

# Popular routes with duration and base price
POPULAR_ROUTES = [
    {
        'from': 'Hyderabad',
        'to': 'Bangalore',
        'duration': '8 hours',
        'price': 1200
    },
    {
        'from': 'Mumbai',
        'to': 'Pune',
        'duration': '3.5 hours',
        'price': 500
    },
    {
        'from': 'Delhi',
        'to': 'Jaipur',
        'duration': '6 hours',
        'price': 900
    },
    {
        'from': 'Chennai',
        'to': 'Bangalore',
        'duration': '6 hours',
        'price': 800
    }
]

# Sample customer reviews
CUSTOMER_REVIEWS = [
    {
        'name': 'Rithika',
        'rating': 5,
        'comment': 'Excellent service! The bus was clean and comfortable. Driver was very professional.'
    },
    {
        'name': 'Priya Patel',
        'rating': 4,
        'comment': 'Good experience overall. The bus was on time and the journey was smooth.'
    },
    {
        'name': 'Amit Kumar',
        'rating': 5,
        'comment': 'Best bus service I have used. Very comfortable seats and great amenities.'
    }
]

# Bus types with amenities
BUS_TYPES = {
    'AC Sleeper': {
        'amenities': ['AC', 'Sleeper Berths', 'Water Bottle', 'Blanket', 'Curtains', 'Reading Light'],
        'price_multiplier': 1.5
    },
    'Non-AC Sleeper': {
        'amenities': ['Sleeper Berths', 'Water Bottle', 'Curtains', 'Reading Light'],
        'price_multiplier': 1.2
    },
    'AC Seater': {
        'amenities': ['AC', 'Reclining Seats', 'Water Bottle', 'Reading Light'],
        'price_multiplier': 1.3
    },
    'Non-AC Seater': {
        'amenities': ['Reclining Seats', 'Water Bottle'],
        'price_multiplier': 1.0
    }
}

# Dummy data for buses with enhanced features
buses = [
    {
        'id': 1,
        'name': 'Deluxe Express',
        'type': 'AC Sleeper',
        'from': 'Hyderabad',
        'to': 'Bangalore',
        'departure_time': '06:00',
        'arrival_time': '14:00',
        'price': 1200,
        'seats': 40,
        'available_seats': 40,
        'amenities': BUS_TYPES['AC Sleeper']['amenities'],
        'operator': 'Orange Tours',
        'rating': 4.5,
        'reviews': 128,
        'boarding_points': ['Secunderabad', 'Gachibowli', 'Hitech City'],
        'dropping_points': ['Electronic City', 'Majestic', 'Silk Board']
    },
    {
        'id': 2,
        'name': 'Sleeper Plus',
        'type': 'Non-AC Sleeper',
        'from': 'Bangalore',
        'to': 'Chennai',
        'departure_time': '08:30',
        'arrival_time': '14:30',
        'price': 800,
        'seats': 35,
        'available_seats': 35,
        'amenities': BUS_TYPES['Non-AC Sleeper']['amenities'],
        'operator': 'Green Line',
        'rating': 4.2,
        'reviews': 95,
        'boarding_points': ['Majestic', 'Silk Board', 'Electronic City'],
        'dropping_points': ['T Nagar', 'Anna Nagar', 'Tambaram']
    },
    {
        'id': 3,
        'name': 'Royal Travels',
        'from': 'Mumbai',
        'to': 'Pune',
        'departure_time': '07:00',
        'arrival_time': '10:30',
        'price': 500,
        'seats': 45,
        'available_seats': 45
    },
    {
        'id': 4,
        'name': 'Comfort Line',
        'from': 'Delhi',
        'to': 'Jaipur',
        'departure_time': '09:00',
        'arrival_time': '15:00',
        'price': 900,
        'seats': 38,
        'available_seats': 38
    },
    {
        'id': 5,
        'name': 'Express Deluxe',
        'from': 'Kolkata',
        'to': 'Bhubaneswar',
        'departure_time': '10:30',
        'arrival_time': '18:00',
        'price': 1100,
        'seats': 42,
        'available_seats': 42
    },
    {
        'id': 6,
        'name': 'Premium Travels',
        'from': 'Hyderabad',
        'to': 'Chennai',
        'departure_time': '11:00',
        'arrival_time': '19:00',
        'price': 1300,
        'seats': 36,
        'available_seats': 36
    },
    {
        'id': 7,
        'name': 'City Connect',
        'from': 'Bangalore',
        'to': 'Mysore',
        'departure_time': '08:00',
        'arrival_time': '11:00',
        'price': 400,
        'seats': 40,
        'available_seats': 40
    },
    {
        'id': 8,
        'name': 'Night Rider',
        'from': 'Mumbai',
        'to': 'Goa',
        'departure_time': '22:00',
        'arrival_time': '06:00',
        'price': 1500,
        'seats': 32,
        'available_seats': 32
    },
    {
        'id': 9,
        'name': 'Morning Express',
        'from': 'Delhi',
        'to': 'Agra',
        'departure_time': '05:30',
        'arrival_time': '09:00',
        'price': 600,
        'seats': 45,
        'available_seats': 45
    },
    {
        'id': 10,
        'name': 'Coastal Cruiser',
        'from': 'Chennai',
        'to': 'Pondicherry',
        'departure_time': '07:30',
        'arrival_time': '11:30',
        'price': 700,
        'seats': 38,
        'available_seats': 38
    },
    {
        'id': 11,
        'name': 'Hill View',
        'from': 'Bangalore',
        'to': 'Ooty',
        'departure_time': '06:30',
        'arrival_time': '14:00',
        'price': 1400,
        'seats': 35,
        'available_seats': 35
    },
    {
        'id': 12,
        'name': 'Tech Connect',
        'from': 'Hyderabad',
        'to': 'Pune',
        'departure_time': '09:30',
        'arrival_time': '20:00',
        'price': 1600,
        'seats': 40,
        'available_seats': 40
    }
]

# Dummy data for bookings
bookings = []

# Dummy data for user reviews
reviews = []

@app.route('/')
def home():
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', 
                         buses=buses[:6],  # Show only 6 featured buses
                         cities=INDIAN_CITIES,
                         popular_routes=POPULAR_ROUTES,
                         customer_reviews=CUSTOMER_REVIEWS,
                         today_date=today)

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        from_city = request.form.get('from')
        to_city = request.form.get('to')
        date = request.form.get('date')
        bus_type = request.form.get('bus_type')
    else:
        from_city = request.args.get('from')
        to_city = request.args.get('to')
        date = datetime.now().strftime('%Y-%m-%d')
        bus_type = None
    
    # Filter buses based on search criteria
    filtered_buses = [bus for bus in buses if bus['from'].lower() == from_city.lower() and bus['to'].lower() == to_city.lower()]
    
    if bus_type:
        filtered_buses = [bus for bus in filtered_buses if bus['type'] == bus_type]
    
    # Sort buses by price (low to high)
    filtered_buses.sort(key=lambda x: x['price'])
    
    return render_template('search_results.html', 
                         buses=filtered_buses, 
                         date=date, 
                         bus_types=BUS_TYPES,
                         from_city=from_city,
                         to_city=to_city)

@app.route('/book/<int:bus_id>', methods=['GET', 'POST'])
def book(bus_id):
    bus = next((bus for bus in buses if bus['id'] == bus_id), None)
    
    if not bus:
        flash('Bus not found!')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        seats = int(request.form.get('seats'))
        boarding_point = request.form.get('boarding_point')
        dropping_point = request.form.get('dropping_point')
        
        if seats > bus['available_seats']:
            flash('Not enough seats available!')
            return redirect(url_for('book', bus_id=bus_id))
        
        # Create booking
        booking = {
            'id': len(bookings) + 1,
            'bus_id': bus_id,
            'name': name,
            'email': email,
            'phone': phone,
            'seats': seats,
            'boarding_point': boarding_point,
            'dropping_point': dropping_point,
            'total_price': seats * bus['price'],
            'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Confirmed'
        }
        
        bookings.append(booking)
        
        # Update available seats
        bus['available_seats'] -= seats
        
        return render_template('confirmation.html', booking=booking, bus=bus)
    
    return render_template('booking.html', bus=bus)

@app.route('/my_bookings')
def my_bookings():
    return render_template('my_bookings.html', bookings=bookings, buses=buses)

@app.route('/bus_details/<int:bus_id>')
def bus_details(bus_id):
    bus = next((bus for bus in buses if bus['id'] == bus_id), None)
    if not bus:
        flash('Bus not found!')
        return redirect(url_for('home'))
    
    # Get reviews for this bus
    bus_reviews = [review for review in reviews if review['bus_id'] == bus_id]
    
    return render_template('bus_details.html', bus=bus, reviews=bus_reviews)

@app.route('/add_review/<int:bus_id>', methods=['POST'])
def add_review(bus_id):
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')
    name = request.form.get('name')
    
    review = {
        'id': len(reviews) + 1,
        'bus_id': bus_id,
        'name': name,
        'rating': rating,
        'comment': comment,
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    reviews.append(review)
    
    # Update bus rating
    bus = next((bus for bus in buses if bus['id'] == bus_id), None)
    if bus:
        bus['reviews'] += 1
        bus['rating'] = (bus['rating'] * (bus['reviews'] - 1) + rating) / bus['reviews']
    
    flash('Thank you for your review!')
    return redirect(url_for('bus_details', bus_id=bus_id))

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    booking = next((booking for booking in bookings if booking['id'] == booking_id), None)
    if booking:
        booking['status'] = 'Cancelled'
        # Return seats to available count
        bus = next((bus for bus in buses if bus['id'] == booking['bus_id']), None)
        if bus:
            bus['available_seats'] += booking['seats']
        flash('Booking cancelled successfully!')
    else:
        flash('Booking not found!')
    return redirect(url_for('my_bookings'))

if __name__ == '__main__':
    app.run(debug=True) 