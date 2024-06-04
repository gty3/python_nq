import pandas as pd

# Function to format the chart title based on given inputs
def format_chart_title(symbols, start_time, chart_schema):
    # Extract the date from the start_time string
    date_part = start_time.split('T')[0]  # Get the date part before 'T'
    formatted_date = pd.to_datetime(date_part).strftime('%m/%d')  # Format date as MM/DD

    # Assuming symbols is a list and we use the first symbol for the title
    symbol = symbols[0] if symbols else 'Symbol'

    # Extract the interval part from chart_schema (assuming it's the last part after '-')
    interval = chart_schema.split('-')[-1].upper()

    # Construct the title string
    title = f"{symbol} - {formatted_date} - {interval}"
    return title