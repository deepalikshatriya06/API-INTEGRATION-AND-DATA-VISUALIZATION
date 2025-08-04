import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib.dates as mdates
import sys

# -------------------------
# USER INPUT
# -------------------------

CITY = input("Enter City Name: ").strip()

# -------------------------
# CONFIGURATION
# -------------------------

API_KEY = 'f395ec84229f304ead170b57747e3e78'  # OpenWeatherMap API key
UNITS = 'metric'
URL = f'https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units={UNITS}'

# -------------------------
# FETCHING DATA
# -------------------------

try:
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
    sys.exit()
except KeyError:
    print("Invalid response format. Check the city name or API key.")
    sys.exit()

# -------------------------
# DATA EXTRACTION
# -------------------------

dates = []
temps = []
humidity = []

for entry in data['list']:
    dt = datetime.fromtimestamp(entry['dt'])
    dates.append(dt)
    temps.append(entry['main']['temp'])
    humidity.append(entry['main']['humidity'])

# -------------------------
# DATA VISUALIZATION
# -------------------------

sns.set(style="whitegrid")
plt.figure(figsize=(14, 6))

# Temperature Plot

plt.subplot(1, 2, 1)
sns.lineplot(x=dates, y=temps, marker='o', color='orange')
plt.title(f'Temperature Forecast in {CITY}', fontsize=14)
plt.xlabel('Date-Time')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b %H:%M')) 

# Humidity Plot

plt.subplot(1, 2, 2)
sns.lineplot(x=dates, y=humidity, marker='s', color='blue')
plt.title(f'Humidity Forecast in {CITY}', fontsize=14)
plt.xlabel('Date-Time')
plt.ylabel('Humidity (%)')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b %H:%M'))  

plt.tight_layout()
plt.savefig("weather_dashboard.png", dpi=300)
plt.show()
