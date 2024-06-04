# import pandas as pd

# # Function to format the chart title based on given inputs
# def format_chart_title(symbols, start_time, chart_schema):
#     # Extract the date from the start_time string
#     date_part = start_time.split('T')[0]  # Get the date part before 'T'
#     formatted_date = pd.to_datetime(date_part).strftime('%m/%d')  # Format date as MM/DD

#     # Assuming symbols is a list and we use the first symbol for the title
#     symbol = symbols[0] if symbols else 'Symbol'

#     # Extract the interval part from chart_schema (assuming it's the last part after '-')
#     interval = chart_schema.split('-')[-1].upper()

#     # Construct the title string
#     title = f"{symbol} - {formatted_date} - {interval}"
#     return title


import pandas as pd
import mplfinance as mpf
import numpy as np

# Function to format the chart title based on given inputs
def format_chart_title(symbols, start_time, chart_schema):
    date_part = start_time.split('T')[0]
    formatted_date = pd.to_datetime(date_part).strftime('%m/%d')
    symbol = symbols[0] if symbols else 'Symbol'
    interval = chart_schema.split('-')[-1].upper()
    title = f"{symbol} - {formatted_date} - {interval}"
    return title

# Function to create scatter plot for trades
def create_trade_scatter(trades_df, trade_type, color, marker):
    filtered_trades = trades_df.copy()
    filtered_trades.loc[filtered_trades['side'] != trade_type] = np.nan
    scatter_plot = mpf.make_addplot(filtered_trades['price'], 
                                    type='scatter', 
                                    markersize=20, 
                                    marker=marker, 
                                    color=color, 
                                    label=trade_type.lower())
    return scatter_plot

# Function to create PNL line plot
def create_pnl_plot(trades_df):
    pnl_plot = mpf.make_addplot(trades_df['total_pnl'], panel=1, type='line', ylabel='PNL in $')
    return pnl_plot