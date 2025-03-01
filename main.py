import os
import sqlite3
from datetime import datetime
from flask import Flask, g, request, redirect, url_for, render_template, jsonify, session, render_template_string
import json
import requests
import datetime
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt
import io, base64


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key for production use

DATABASE = 'databases.db'

def get_db():
    db = getattr(g, '_databases', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row 
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_databases', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database with a table for storing quiz responses."""
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location TEXT,
                        latitude TEXT,
                        longitude TEXT,
                        roof_area REAL,
                        electricity_consumption TEXT,
                        electricity_rate TEXT,
                        storage_option TEXT,
                        budget TEXT,
                        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_databases', None)
    if db is not None:
        db.close()

# Homepage
@app.route('/')
def home():
    return render_template('homepage.html')

# Quiz1: Intro Page (no data to store)
@app.route('/quiz1')
def quiz1():
    return render_template('quiz11.html')

# Quiz2: Location page (uses geolocation via JS)
@app.route('/quiz2', methods=['GET', 'POST'])
def quiz2():
    if request.method == 'POST':
        # Save the location (fetched from JS and passed via a hidden input)
        session['location'] = request.form.get('location', '')
        print(f"Location: {session['location']}")  # Debug print
        session['latitude'] = request.form.get('latitude', '')
        session['longitude'] = request.form.get('longitude', '')
        print("Latitude:", session.get('latitude'))
        print("Longitude:", session.get('longitude'))

        # Save data to the database
        db = get_db()
        db.execute(
            '''INSERT INTO responses 
               (location, latitude, longitude, electricity_consumption, electricity_rate, storage_option, budget, submitted_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (session.get('location', ''),
             session.get('latitude', ''),
             session.get('longitude', ''),
             session.get('electricity_consumption', ''),
             session.get('electricity_rate', ''),
             session.get('storage_option', ''),
             session.get('budget', ''),
             datetime.datetime.now().isoformat())
        )
        db.commit()

        return redirect(url_for('quiz3'))
    return render_template('quiz22.html')

# Quiz3: Roof area
@app.route('/quiz3', methods=['GET', 'POST'])
def quiz3():
    if request.method == 'POST':
        session['roof_area'] = request.form.get('roof_area', '')
        print(f"Roof Area from form: {request.form.get('roof_area')}")

        db = get_db()
        db.execute(
            'UPDATE responses SET roof_area = ? WHERE id = (SELECT MAX(id) FROM responses)',
            [session['roof_area']]
        )
        db.commit()

        print(f"Roof Area: {session['roof_area']}") 
        return redirect(url_for('quiz5'))
    return render_template('quiz33.html')

# Quiz5: Electricity Consumption
@app.route('/quiz5', methods=['GET', 'POST'])
def quiz5():
    if request.method == 'POST':
        session['electricity_consumption'] = request.form.get('electricity_consumption', '')
        print(f"Electricity Consumption: {session['electricity_consumption']}")

        db = get_db()
        db.execute(
            'UPDATE responses SET electricity_consumption = ? WHERE id = (SELECT MAX(id) FROM responses)',
            [session['electricity_consumption']]
        )
        db.commit()

        return redirect(url_for('quiz6'))
    return render_template('quiz55.html')

# Quiz6: Electricity Rate
@app.route('/quiz6', methods=['GET', 'POST'])
def quiz6():
    if request.method == 'POST':
        session['electricity_rate'] = request.form.get('electricity_rate', '')
        print(f"Electricity Rate: {session['electricity_rate']}") 
        db = get_db()
        db.execute(
            'UPDATE responses SET electricity_rate = ? WHERE id = (SELECT MAX(id) FROM responses)',
            [session['electricity_rate']]
        )
        db.commit()

        return redirect(url_for('quiz7'))
    return render_template('quiz66.html')

# Quiz7: Storage Option (e.g., Battery or Grid offloading)
@app.route('/quiz7', methods=['GET', 'POST'])
def quiz7():
    if request.method == 'POST':
        session['storage_option'] = request.form.get('storage_option', '')
        print(f"Storage Option: {session['storage_option']}")

        db = get_db()
        db.execute(
            'UPDATE responses SET storage_option = ? WHERE id = (SELECT MAX(id) FROM responses)',
            [session['storage_option']]
        )
        db.commit()

        return redirect(url_for('quiz8'))
    return render_template('quiz77.html')

# Quiz8: Budget
@app.route('/quiz8', methods=['GET', 'POST'])
def quiz8():
    if request.method == 'POST':
        session['budget'] = request.form.get('budget', '')
        print(f"Budget: {session['budget']}")
        print("Session Data:", session) 

        db = get_db()
        db.execute(
            '''INSERT INTO responses 
               (location, roof_area, electricity_consumption, electricity_rate, storage_option, budget, submitted_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (session.get('location', ''),
             session.get('roof_area', ''),
             session.get('electricity_consumption', ''),
             session.get('electricity_rate', ''),
             session.get('storage_option', ''),
             session.get('budget', ''),
             datetime.datetime.now().isoformat())
        )
        db.commit()

        return redirect(url_for('thank_you'))
    return render_template('quiz88.html')

# Thank You page – save all data to the database and display a confirmation
@app.route('/thank_you', methods=['GET'])
def thank_you():
    # Retrieve all data from the session
    location = session.get('location', '')
    roof_area = session.get('roof_area', '')
    electricity_consumption = session.get('electricity_consumption', '')
    electricity_rate = session.get('electricity_rate', '')
    storage_option = session.get('storage_option', '')
    budget = session.get('budget', '')

    print(f"Data to be saved: {location}, {roof_area}, {electricity_consumption}, {electricity_rate}, {storage_option}, {budget}")

    # Save data to the database
    db = get_db()
    try:
        db.execute(
            '''INSERT INTO responses 
               (location, roof_area, electricity_consumption, electricity_rate, storage_option, budget, submitted_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (location, roof_area, electricity_consumption, electricity_rate, storage_option, budget, datetime.now().isoformat())
        )
        db.commit()
        print("Data saved successfully!")  # Debug print
    except Exception as e:
        print(f"Error saving data: {e}")  # Debug print
    
    # Clear the session after storing the data
    session.clear()

    # Render the loading page
    return render_template('loading.html')

# Endpoint to retrieve all stored quiz data as JSON
@app.route('/data')
def get_data():
    db = get_db()
    cur = db.execute('SELECT id, location, roof_area, electricity_consumption, electricity_rate, storage_option, budget, submitted_at FROM responses')
    entries = cur.fetchall()
    results = [
        {
            "id": row[0],
            "location": row[1],
            "roof_area": row[2],
            "electricity_consumption": row[3],
            "electricity_rate": row[4],
            "storage_option": row[5],
            "budget": row[6],
            "submitted_at": row[7]
        }
        for row in entries
    ]
    return jsonify(results)


# ---------------- NASA POWER API and Data Processing Functions ----------------

def fetch_nasa_power_data(lat, lon, start_date, end_date):
    """
    Fetches daily solar irradiance data from NASA POWER API.
    """
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        'parameters': 'ALLSKY_SFC_SW_DWN',
        'community': 'RE',
        'latitude': lat,
        'longitude': lon,
        'start': start_date,
        'end': end_date,
        'format': 'JSON'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Error fetching data from NASA POWER API")
    
    data = response.json()
    try:
        daily_data = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    except KeyError:
        raise Exception("Unexpected data format returned by NASA POWER API")
    return daily_data

def compute_daily_means(daily_data):
    """
    Computes the mean irradiance for each calendar day (MM-DD) across the period.
    (Leap day, Feb 29, is skipped.)
    """
    day_values = defaultdict(list)
    for date_str, value in daily_data.items():
        date_obj = datetime.datetime.strptime(date_str, '%Y%m%d')
        if date_obj.month == 2 and date_obj.day == 29:
            continue
        day_key = date_obj.strftime('%m-%d')
        day_values[day_key].append(value)
    daily_means = {day: statistics.mean(values) for day, values in day_values.items()}
    return daily_means

# ---------------- Graph Generation Functions ----------------

def generate_monthly_generation(installed_capacity, effective_sun_hours):
    """
    Given an installed capacity (in kW) and effective sun hours (kWh/kW/day),
    calculate the monthly generation (in kWh) using a fixed number of days per month.
    """
    # Days in each month (non-leap year)
    month_days = {
        '01': 31, '02': 28, '03': 31, '04': 30,
        '05': 31, '06': 30, '07': 31, '08': 31,
        '09': 30, '10': 31, '11': 30, '12': 31
    }
    monthly_generation = {}
    daily_generation = installed_capacity * effective_sun_hours
    for month, days in month_days.items():
        monthly_generation[month] = daily_generation * days
    return monthly_generation

def create_generation_graph(monthly_generation):
    """
    Plots the monthly generation data and returns a base64-encoded PNG image.
    """
    months = list(monthly_generation.keys())
    generation_values = [monthly_generation[m] for m in months]
    
    plt.figure(figsize=(10, 5))
    plt.plot(months, generation_values, marker='o', linestyle='-')
    plt.title("Monthly Electricity Generation (kWh)")
    plt.xlabel("Month")
    plt.ylabel("Generation (kWh)")
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    generation_graph = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return generation_graph

def create_roi_graph(annual_savings, total_cost_after_subsidy, years=20):
    """
    Plots the cumulative annual savings (ROI graph) against the investment cost.
    A horizontal line marks the net investment (after subsidy).
    """
    cumulative_savings = [annual_savings * year for year in range(1, years+1)]
    year_list = list(range(1, years+1))
    
    plt.figure(figsize=(10, 5))
    plt.plot(year_list, cumulative_savings, marker='o', linestyle='-')
    plt.axhline(y=total_cost_after_subsidy, color='r', linestyle='--', label='Investment Cost')
    plt.title("ROI Graph: Cumulative Savings Over Years")
    plt.xlabel("Years")
    plt.ylabel("Cumulative Savings (Rs.)")
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    roi_graph = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return roi_graph

# ---------------- Subsidy Calculation ----------------

def calculate_subsidy(installed_capacity):
    """
    Calculates government subsidy based on the installed capacity:
      - Up to 2 kW: Rs. 30,000 per kW
      - For capacity between 2 and 3 kW: additional Rs. 18,000 per kW
      - For systems larger than 3 kW, the subsidy is capped at Rs. 78,000.
    """
    if installed_capacity <= 2:
        subsidy = installed_capacity * 30000
    elif installed_capacity <= 3:
        subsidy = (2 * 30000) + ((installed_capacity - 2) * 18000)
    else:
        subsidy = 78000
    return subsidy

# ---------------- Flask Route for Report ----------------

@app.route('/final_report')
def final_report():
    # Retrieve data from the session
    db = get_db()
    cur = db.execute('SELECT * FROM responses ORDER BY id DESC LIMIT 1')
    user_data = cur.fetchone()
   
    if not user_data:
        print("No data found in the database.")
        return "No data found. Please complete the quiz first."
    
    print("User Data from Database:", user_data)

    # Extract required fields from the session
    lat = user_data['latitude']
    lon = user_data['longitude']
    roof_area = user_data['roof_area']               # in m²
    electricity_consumption = user_data['electricity_consumption']   # rupees (if needed)
    electricity_rate = user_data['electricity_rate'] # rupees per unit
    monthly_unit_consumption = int(electricity_consumption) /int(electricity_rate) 
    daily_unit_consumption = monthly_unit_consumption / 30.0# may be provided
    use_battery = user_data['use_battery']           # boolean: True for battery storage, False for grid offloading
    budget= user_data['budget']  

    # Calculate daily consumption (units per day)
    if not daily_unit_consumption:
        daily_consumption = monthly_unit_consumption / 30.0
    else:
        daily_consumption = daily_unit_consumption

    # ---------------- Calculate Effective Sun Hours from NASA Data ----------------
    # We use a historical period (2016-2020) to compute the average irradiance.
    try:
        start_date = "20160101"
        end_date = "20201231"
        nasa_data = fetch_nasa_power_data(lat, lon, start_date, end_date)
        nasa_daily_means = compute_daily_means(nasa_data)
        average_irradiance = statistics.mean(nasa_daily_means.values())
        # Convert average irradiance (W/m²) to daily insolation (kWh/m²/day):
        effective_sun_hours = (average_irradiance * 24) / 1000
    except Exception as e:
        # Fallback to an assumed value if NASA data cannot be fetched
        effective_sun_hours = 4.5

    # ---------------- Rooftop Area & Installed Capacity Calculations ----------------
    # Only 70% of the roof can be used for panels.
    available_area = roof_area * 0.7  # in m²
    # Assume that 1 kW of panels requires 5 m².
    area_per_kw = 5.0  # m² per kW

    # Calculate required installed capacity (kW) based on daily consumption
    # (Assuming that 1 kW installed produces effective_sun_hours kWh per day)
    required_kw = daily_consumption / effective_sun_hours
    required_panel_area = required_kw * area_per_kw

    # Check if available area is enough; if not, limit the installation
    max_installable_kw = available_area / area_per_kw
    if required_kw > max_installable_kw:
        installed_kw = max_installable_kw
    else:
        installed_kw = required_kw

    # Recalculate daily and annual generation
    daily_generation = installed_kw * effective_sun_hours  # in kWh per day
    annual_generation = daily_generation * 365             # in kWh per year

    # ---------------- Cost Calculations ----------------
    # Average cost components per kW (in Rs.)
    cost_solar_panel = 27500   # average between Rs. 25k and Rs. 30k
    cost_inverter = 17500      # average between Rs. 15k and Rs. 20k
    cost_mounting = 7500       # average between Rs. 5k and Rs. 10k
    cost_wiring = 3500         # average between Rs. 2k and Rs. 5k
    cost_installation = 7500   # average between Rs. 5k and Rs. 10k

    base_cost_per_kw = cost_solar_panel + cost_inverter + cost_mounting + cost_wiring + cost_installation

    # If the user opts for battery, add additional cost per kW installed.
    battery_cost_per_kw = 20000 if use_battery else 0

    total_cost = installed_kw * (base_cost_per_kw + battery_cost_per_kw)
    subsidy = calculate_subsidy(installed_kw)
    total_cost_after_subsidy = total_cost - subsidy

    # ---------------- Savings and Profit Calculations ----------------
    # Annual consumption (units per year)
    annual_consumption = monthly_unit_consumption * 12

    if use_battery:
        # With battery storage, all generated energy is used,
        # so savings equals the energy generated times the electricity rate.
        annual_savings = annual_generation * electricity_rate
        grid_profit = 0
    else:
        # For grid offloading: savings cover the consumption and extra generation profit.
        consumption_savings = annual_consumption * electricity_rate
        extra_units = max(0, annual_generation - annual_consumption)
        grid_profit = extra_units * 3  # Rs. 3 per extra unit sold to the grid
        annual_savings = consumption_savings + grid_profit

    # ---------------- Generate Graphs ----------------
    monthly_generation = generate_monthly_generation(installed_kw, effective_sun_hours)
    generation_graph = create_generation_graph(monthly_generation)
    roi_graph = create_roi_graph(annual_savings, total_cost_after_subsidy, years=20)

    # Calculate % of roof used for panels (based on required panel area, but not exceeding available area)
    area_used = min(required_panel_area, available_area)
    area_used_percentage = (area_used / roof_area) * 100

    # Render the final report template
    return render_template('final_report.html',
                           installed_kw=installed_kw,
                           daily_generation=daily_generation,
                           annual_generation=annual_generation,
                           required_panel_area=required_panel_area,
                           available_area=available_area,
                           area_used_percentage=area_used_percentage,
                           effective_sun_hours=effective_sun_hours,
                           total_cost=total_cost,
                           subsidy=subsidy,
                           total_cost_after_subsidy=total_cost_after_subsidy,
                           annual_savings=annual_savings,
                           grid_profit=grid_profit,
                           generation_graph=generation_graph,
                           roi_graph=roi_graph)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
