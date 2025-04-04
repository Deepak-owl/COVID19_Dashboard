import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import matplotlib.dates as mdates
from tkinter import Tk, Label, Button, Frame
from tkinter.ttk import Combobox
from tkcalendar import Calendar
from datetime import datetime
import mplcursors
from visualizations import show_visualizations  # Import the new file

# Load the CSV file
data = pd.read_csv('compact.csv')
data['date'] = pd.to_datetime(data['date'])

# Connect to SQLite database and save data
conn = sqlite3.connect('covid_data.db')
data.to_sql('covid_data', conn, if_exists='replace', index=False)
conn.close()

# Get unique countries and date range
countries = sorted(data['country'].unique())
min_date = data['date'].min()
max_date = data['date'].max()

# Function to format numbers
def format_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f} million"
    elif num >= 1_000:
        return f"{num / 1_000:.1f} thousand"
    else:
        return str(int(num))

# Function to plot main graph
def plot_graph():
    for widget in msg_frame.winfo_children():
        widget.destroy()

    country = country_var.get()
    start_date = cal_start.get_date()
    end_date = cal_end.get_date()

    start_date = datetime.strptime(start_date, '%m/%d/%y').strftime('%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%m/%d/%y').strftime('%Y-%m-%d')

    conn = sqlite3.connect('covid_data.db')
    query = f"SELECT * FROM covid_data WHERE country = '{country}' AND date BETWEEN '{start_date}' AND '{end_date}'"
    country_range = pd.read_sql_query(query, conn)
    country_range['date'] = pd.to_datetime(country_range['date'])
    conn.close()

    if country_range.empty:
        Label(msg_frame, text=f"No data for {country} in this range!", fg="red").pack()
    else:
        fig, ax = plt.subplots()
        cases_line, = ax.plot(country_range['date'], country_range['total_cases'], label='Total Cases', color='blue')
        deaths_line, = ax.plot(country_range['date'], country_range['total_deaths'], label='Total Deaths', color='red')
        ax.set_title(f'COVID-19 in {country} ({start_date} to {end_date})')
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')
        ax.legend()
        ax.grid(True)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)
        plt.tight_layout()

        cursor = mplcursors.cursor([cases_line, deaths_line], hover=True)
        @cursor.connect("add")
        def on_add(sel):
            x = sel.target[0]
            y = sel.target[1]
            date_str = pd.Timestamp(x).strftime('%Y-%m-%d')
            if sel.artist == cases_line:
                label = f"Date: {date_str}\nCases: {format_number(y)}"
            else:
                label = f"Date: {date_str}\nDeaths: {format_number(y)}"
            sel.annotation.set_text(label)

        plt.show()
        Label(msg_frame, text="Graph displayed successfully!", fg="green").pack()

# Function to launch extra visualizations
def launch_visualizations():
    country = country_var.get()
    start_date = cal_start.get_date()
    end_date = cal_end.get_date()
    start_date = datetime.strptime(start_date, '%m/%d/%y').strftime('%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%m/%d/%y').strftime('%Y-%m-%d')
    show_visualizations(country, start_date, end_date)

# Create the GUI window
root = Tk()
root.title("COVID-19 Dashboard")
root.geometry("400x650")
root.configure(bg="#f0f0f0")

# Country dropdown
Label(root, text="Select Country:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
country_var = Combobox(root, values=countries, height=10)
country_var.set(countries[0])
country_var.pack(pady=10)

# Start date calendar
Label(root, text="Start Date:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
cal_start = Calendar(root, selectmode="day", mindate=min_date, maxdate=max_date,
                    year=min_date.year, month=min_date.month, day=min_date.day)
cal_start.pack(pady=10)

# End date calendar
Label(root, text="End Date:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
cal_end = Calendar(root, selectmode="day", mindate=min_date, maxdate=max_date,
                  year=max_date.year, month=max_date.month, day=max_date.day)
cal_end.pack(pady=10)

# Buttons
Button(root, text="Show Main Graph", command=plot_graph, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
Button(root, text="Show More Visualizations", command=launch_visualizations, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

# Message frame
msg_frame = Frame(root, bg="#f0f0f0")
msg_frame.pack(pady=5)

# Run the GUI
root.mainloop()