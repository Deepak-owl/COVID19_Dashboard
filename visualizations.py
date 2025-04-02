import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def show_visualizations(country, start_date, end_date):
    # Connect to database
    conn = sqlite3.connect('covid_data.db')
    query = f"SELECT * FROM covid_data WHERE country = '{country}' AND date BETWEEN '{start_date}' AND '{end_date}'"
    data = pd.read_sql_query(query, conn)
    data['date'] = pd.to_datetime(data['date'])
    conn.close()

    if data.empty:
        print(f"No data for {country} in this range!")
        return

    # Plot 1: Bar chart of new cases over time
    plt.figure(figsize=(10, 5))
    plt.bar(data['date'], data['new_cases'], color='orange', label='New Cases')
    plt.title(f'New COVID-19 Cases in {country} ({start_date} to {end_date})')
    plt.xlabel('Date')
    plt.ylabel('New Cases')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Plot 2: Pie chart of vaccination stats (latest date)
    latest = data.iloc[-1]  # Last row
    fully_vaccinated = latest['people_fully_vaccinated'] if pd.notna(latest['people_fully_vaccinated']) else 0
    population = latest['population'] if pd.notna(latest['population']) else 0
    vacc_data = [fully_vaccinated, max(population - fully_vaccinated, 0)]  # Avoid negative
    vacc_labels = ['Fully Vaccinated', 'Not Fully Vaccinated']
    plt.figure(figsize=(6, 6))
    plt.pie(vacc_data, labels=vacc_labels, autopct='%1.1f%%', colors=['green', 'gray'])
    plt.title(f'Vaccination Status in {country} (Latest: {latest["date"].date()})')

    # Plot 3: Scatter plot of stringency index vs new cases
    plt.figure(figsize=(10, 5))
    plt.scatter(data['stringency_index'], data['new_cases'], c='purple', alpha=0.5)
    plt.title(f'Stringency Index vs New Cases in {country}')
    plt.xlabel('Stringency Index (0-100)')
    plt.ylabel('New Cases')
    plt.grid(True)
    plt.tight_layout()

    plt.show()

# Test it standalone with a range including vaccination data
if __name__ == "__main__":
    show_visualizations('India', '2021-01-01', '2021-12-31')