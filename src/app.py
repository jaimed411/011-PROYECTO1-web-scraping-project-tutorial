# your app code here


#Step 1: Setup and installation
#pip install pandas sqlite3 requests


#Step 2: Create app.py
#print("Hello world")


#Step 3: Download the data using the request library
#Use the requests library to download the data.
import requests

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
response = requests.get(url)
html_data = response.text


#Step 4: Parse the HTML data using BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
from colorama import Fore, Style

# Instala la biblioteca html5lib si no está instalada
# pip install html5lib

soup = BeautifulSoup(html_data, 'html.parser')
table = soup.find_all('table')[0]  # Assuming the Tesla quarterly revenue table is the second table

tesla_revenue = pd.read_html(str(table), flavor='html5lib')[0]

# Rename columns
tesla_revenue.columns = ['Date', 'Revenue']

# Remove comma and dollar sign from Revenue column
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',', '').str.replace('$', '')

# Print message in blue color
print(Fore.GREEN + "Tesla Quarterly Revenue" + Style.RESET_ALL + "\n")
# Print table in white color
print(tesla_revenue)

# Reset color settings
print(Style.RESET_ALL)


#Step 5: Clean rows
# Remove rows with empty strings or NaN in the Revenue column
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'].notna() & (tesla_revenue['Revenue'] != '')]

# Print message in blue color
print(Fore.GREEN + "Tesla Quarterly Revenue Cleaned" + Style.RESET_ALL + "\n")
# Print table in white color
print(tesla_revenue)


#Step 6: Insert the data into SQLite
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue


#Step 7: Connect to SQLite
import sqlite3

# Create a connection object
conn = sqlite3.connect('Tesla.db')


#Step 8: Create a table in our database to store revenue values:
cursor = conn.cursor()

# Create table
cursor.execute("CREATE TABLE IF NOT EXISTS Revenue (Date TEXT, Revenue TEXT)")

# Commit the changes
conn.commit()


#Step 9: Retrieve the data from the database
for row in conn.execute('SELECT * FROM revenue'):
    print(row)


#Step 10: Finally, create a plot to visualize the data
import seaborn as sns
import matplotlib.pyplot as plt

# Ordenar los datos por la columna 'Date' de forma ascendente
tesla_revenue = tesla_revenue.sort_values('Date')

# Convertir la columna 'Revenue' a tipo numérico
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].astype(int)

# Crear el gráfico utilizando Seaborn
plt.figure(figsize=(10, 6))
sns.lineplot(data=tesla_revenue, x='Date', y='Revenue')

# Establecer el título y las etiquetas del gráfico
plt.title('Tesla Revenue Over Time')
plt.xlabel('Date')
plt.ylabel('Revenue')

# Mostrar el gráfico
plt.show()