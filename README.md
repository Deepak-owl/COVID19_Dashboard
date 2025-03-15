# COVID-19 Dashboard
An interactive dashboard to visualize COVID-19 cases and deaths by country.

## Setup
1. Clone this repository: git clone https://github.com/Deepak-owl/COVID19_Dashboard.git
2. Install dependencies: pip install pandas matplotlib sqlite3 tkcalendar mplcursors
3. Download the dataset (`compact.csv`) from [Our World in Data](https://ourworldindata.org/covid-deaths) and place it in the project folder.
4. Run the dashboard: python dashboard.py


## Features
- Scrollable country dropdown
- Calendar date pickers with range limits
- Hover over graph for readable case/death counts (e.g., "1.5 million")