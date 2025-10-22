Weather Dashboard Project
Summary
Web scraping project that collects weather data from timeanddate.com and displays it in an interactive dashboard. Built with Selenium, SQLite, and Dash.
Setup
Install dependencies
In bash, run command pip install -r requirements.txt
Run the programs
bash# 1. Scrape data
python web-scrape.py

# 2. Import to database
python database_import.py

# 3. Query tool (optional)
python database_query.py

# 4. Run dashboard
Change last line of program to:
        if __name__ == '__main__':
            app.run(debug=True)
Then:
python dashboard_program.py
Open browser to http://127.0.0.1:8050/
Screenshot
Show Image
Files


requirements.txt - Dependencies

Dashboard Features

Filter by temperature category
Search cities
Temperature range slider
3 visualizations: bar chart, pie chart, scatter plot

Deploy on Render
Last line of dashboard_program:
    Change last line of code to before uploading to render
    
    if __name__ == '__main__':
        app.run_server(debug=True)

Build: pip install -r requirements.txt
Start: gunicorn dashboard_program:server