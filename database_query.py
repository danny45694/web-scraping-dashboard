import sqlite3
import pandas as pd

# Show menu
def show_menu():
    print("\n========================================")
    print("WEATHER QUERY TOOL")
    print("========================================")
    print("1 - View all data")
    print("2 - Filter by category")
    print("3 - Filter by temperature")
    print("4 - Search city")
    print("5 - Show stats")
    print("6 - Filter by date/time")
    print("7 - Advanced queries")
    print("8 - Custom query")
    print("0 - Exit")
    print("========================================")

# Option 1 - View all data
def view_all():
    # Ask user how many rows
    num = input("How many rows? (press Enter for 20): ")
    if num == "":
        num = "20"
    
    # Connect to database
    conn = sqlite3.connect("weather.db")
    
    # Make the query
    query = "SELECT * FROM weather LIMIT " + num
    
    # Run the query
    result = pd.read_sql_query(query, conn)
    
    # Close database
    conn.close()
    
    # Check if empty
    if len(result) == 0:
        print("No data!")
    else:
        print("\n--- Data ---")
        print(result)

# Option 2 - Filter by category
def filter_category():
    # Show categories
    print("\nCategories:")
    print("  very cold")
    print("  cold")
    print("  comfortable")
    print("  hot")
    print("  very hot")
    
    # Get user input
    cat = input("\nPick one: ")
    
    # Check if empty
    if cat == "":
        print("Nothing entered!")
        return
    
    # Connect to database
    conn = sqlite3.connect("weather.db")
    
    # Make the query
    query = "SELECT * FROM weather WHERE TempCategory = '" + cat + "'"
    
    # Run the query
    result = pd.read_sql_query(query, conn)
    
    # Close database
    conn.close()
    
    # Check if empty
    if len(result) == 0:
        print("No cities in that category!")
    else:
        print("\n--- Results ---")
        print(result)

# Option 3 - Filter by temperature
def filter_temperature():
    # Get min temperature
    min_temp = input("Min temp: ")
    
    # Get max temperature
    max_temp = input("Max temp: ")
    
    # Check if empty
    if min_temp == "":
        print("Need min temp!")
        return
    if max_temp == "":
        print("Need max temp!")
        return
    
    # Connect to database
    conn = sqlite3.connect("weather.db")
    
    # Make the query
    query = "SELECT * FROM weather WHERE TempValues >= " + min_temp
    query = query + " AND TempValues <= " + max_temp
    
    # Run the query
    result = pd.read_sql_query(query, conn)
    
    # Close database
    conn.close()
    
    # Check if empty
    if len(result) == 0:
        print("No cities found!")
    else:
        print("\n--- Results ---")
        print(result)

# Option 4 - Search city
def search_city():
    # Get city name
    city = input("City name: ")
    
    # Check if empty
    if city == "":
        print("Nothing entered!")
        return
    
    # Connect to database
    conn = sqlite3.connect("weather.db")
    
    # Make the query
    query = "SELECT * FROM weather WHERE City LIKE '%" + city + "%'"
    
    # Run the query
    result = pd.read_sql_query(query, conn)
    
    # Close database
    conn.close()
    
    # Check if empty
    if len(result) == 0:
        print("City not found!")
    else:
        print("\n--- Results ---")
        print(result)

# Option 5 - Show stats
def show_stats():
    # Connect to database
    conn = sqlite3.connect("weather.db")
    
    # Make the query
    query = "SELECT TempCategory, COUNT(*) as count FROM weather GROUP BY TempCategory"
    
    # Run the query
    result = pd.read_sql_query(query, conn)
    
    # Close database
    conn.close()
    
    # Check if empty
    if len(result) == 0:
        print("No data!")
    else:
        print("\n--- Stats ---")
        print(result)
    
    # Show average too
    conn = sqlite3.connect("weather.db")
    query2 = "SELECT AVG(TempValues) as average FROM weather"
    result2 = pd.read_sql_query(query2, conn)
    conn.close()
    
    print("\nAverage temperature:", result2.iloc[0]['average'])

# Option 6 - Filter by date/time
def filter_datetime():
    # Show examples
    print("Search date/time")
    print("Examples: 'Mon', 'pm', 'Jan'")
    
    # Get user input
    datetime = input("\nEnter text: ")
    
    # Check if empty
    if datetime == "":
        print("Nothing entered!")
        return
    
    # Connect to database
    conn = sqlite3.connect("weather.db")
    
    # Make the query
    query = "SELECT * FROM weather WHERE DateAndTime LIKE '%" + datetime + "%'"
    
    # Run the query
    result = pd.read_sql_query(query, conn)
    
    # Close database
    conn.close()
    
    # Check if empty
    if len(result) == 0:
        print("Nothing found!")
    else:
        print("\n--- Results ---")
        print(result)

# Option 7 - Advanced queries
def advanced_queries():
    # First query - cities above average
    print("\n--- Cities above average temp ---")
    
    # Connect to database
    conn = sqlite3.connect("weather.db")
    
    # Make the query
    query1 = "SELECT City, TemperatureText, TempValues FROM weather WHERE TempValues > (SELECT AVG(TempValues) FROM weather)"
    
    # Run the query
    result1 = pd.read_sql_query(query1, conn)
    
    # Close database
    conn.close()
    
    # Check if empty
    if len(result1) == 0:
        print("No results!")
    else:
        print(result1)
    
    # Second query - group by category
    print("\n--- Cities by category ---")
    
    # Connect to database again
    conn = sqlite3.connect("weather.db")
    
    # Make the query
    query2 = "SELECT TempCategory, COUNT(*) as total FROM weather GROUP BY TempCategory"
    
    # Run the query
    result2 = pd.read_sql_query(query2, conn)
    
    # Close database
    conn.close()
    
    # Check if empty
    if len(result2) == 0:
        print("No results!")
    else:
        print(result2)

# Option 8 - Custom query
def custom_query():
    # Show help
    print("\nTable: weather")
    print("Columns: City, DateAndTime, TemperatureText, TempValues, TempCategory")
    print("\nExample: SELECT * FROM weather WHERE TempValues > 80")
    
    # Get user query
    query = input("\nYour query: ")
    
    # Check if empty
    if query == "":
        print("No query!")
        return
    
    # Connect to database
    conn = sqlite3.connect("weather.db")
    
    # Try to run the query
    try:
        result = pd.read_sql_query(query, conn)
        conn.close()
        
        # Check if empty
        if len(result) == 0:
            print("No results!")
        else:
            print("\n--- Results ---")
            print(result)
    except:
        print("Query error!")
        conn.close()

# Main program starts here
print("\nWeather Query Tool")
print("Starting...")

# Keep looping until user exits
while True:
    # Show the menu
    show_menu()
    
    # Get user choice
    choice = input("\nPick: ")
    
    # Check what they picked
    if choice == "0":
        print("\nBye!")
        break
    
    if choice == "1":
        view_all()
    
    if choice == "2":
        filter_category()
    
    if choice == "3":
        filter_temperature()
    
    if choice == "4":
        search_city()
    
    if choice == "5":
        show_stats()
    
    if choice == "6":
        filter_datetime()
    
    if choice == "7":
        advanced_queries()
    
    if choice == "8":
        custom_query()
    
    if choice != "0" and choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5" and choice != "6" and choice != "7" and choice != "8":
        print("\nPick 0-8.")
    
    # Wait for user
    input("\nPress Enter...")

print("Program ended.")