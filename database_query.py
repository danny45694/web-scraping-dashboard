import sqlite3
import pandas as pd

# Connect to database 
def run_query(query):
    conn = sqlite3.connect("weather.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# menu
def menu():
    print("\n========================================")
    print("WEATHER DATABASE QUERY TOOL")
    print("========================================")
    print("\n1 - View all data")
    print("2 - Filter by category")
    print("3 - Filter by temperature")
    print("4 - Search by city")
    print("5 - Show statistics")
    print("6 - Custom query")
    print("0 - Exit")
    print("========================================")

# Option 1: Show all data
def all():
    print("\nHow many rows to show?")
    num = input("Enter number (default 20): ")
    
    if num == "":
        num = "20"
    
    query = "SELECT * FROM weather LIMIT " + num
    result = run_query(query)
    print("\n--- All Weather Data ---")
    print(result)

# Option 2: Filter by category
def category():
    print("\nCategories:")
    print("- very cold")
    print("- cold")
    print("- comfortable")
    print("- hot")
    print("- very hot")
    
    cat = input("\nEnter category: ")
    
    query = "SELECT * FROM weather WHERE [temp category] = '" + cat + "'"
    result = run_query(query)
    print("\n--- Cities in " + cat + " category ---")
    print(result)

# Option 3: Filter by temperature 
def temperature():
    min_temp = input("Minimum temperature: ")
    max_temp = input("Maximum temperature: ")
    
    query = "SELECT * FROM weather WHERE [temp values] >= " + min_temp + " AND [temp values] <= " + max_temp
    result = run_query(query)
    print("\n--- Cities between " + min_temp + " and " + max_temp + " degrees ---")
    print(result)

# Option 4: Search by city
def city():
    city = input("Enter city name: ")
    
    query = "SELECT * FROM weather WHERE City LIKE '%" + city + "%'"
    result = run_query(query)
    print("\n--- Search results for " + city + " ---")
    print(result)

# Option 5: Show statistics
def stats():
    query = "SELECT [temp category], COUNT(*) as count, AVG([temp values]) as avg_temp FROM weather GROUP BY [temp category]"
    result = run_query(query)
    print("\n--- Temperature Statistics ---")
    print(result)

# Option 6: Custom query
def custom_query():
    print("\nEnter your SQL query:")
    print("Example: SELECT * FROM weather WHERE [temp values] > 80")
    
    query = input("\nQuery: ")
    result = run_query(query)
    print("\n--- Query Results ---")
    print(result)

# Main program
def main():
    print("\nWelcome to Weather Query Tool!")
    
    while True:
        menu()
        choice = input("\nPick an option: ")
        
        if choice == "0":
            print("\nGoodbye!")
            break
        elif choice == "1":
            all()
        elif choice == "2":
            category()
        elif choice == "3":
            temperature()
        elif choice == "4":
            city()
        elif choice == "5":
            stats()
        elif choice == "6":
            custom_query()
        else:
            print("\nInvalid choice. Pick 0-6.")
        
        input("\nPress Enter to continue...")

# Run the program
main()