import pandas as pd
import mplfinance as mpf
import numpy as np

def create_trade_scatter(trades_df, trade_type, color, marker):
    """
    Create a scatter plot for either buy or sell trades.

    Args:
    trades_df (DataFrame): DataFrame containing trade data.
    trade_type (str): Type of trade ('B' for buy, 'S' for sell).
    color (str): Color of the markers.
    marker (str): Shape of the markers.

    Returns:
    mplfinance.plotting.make_addplot: Scatter plot object for mplfinance.
    """
    filtered_trades = trades_df.copy()
    filtered_trades.loc[filtered_trades['side'] != trade_type] = np.nan
    label = "Buy" if trade_type == 'B' else "Sell"
    scatter_plot = mpf.make_addplot(filtered_trades['price'], 
                                    type='scatter', 
                                    markersize=20, 
                                    marker=marker, 
                                    color=color, 
                                    label=label)
    return scatter_plot

def create_pnl_plot(trades_df):
    """
    Create a profit and loss line plot.

    Args:
    trades_df (DataFrame): DataFrame containing trade data.

    Returns:
    mplfinance.plotting.make_addplot: PNL line plot object for mplfinance.
    """
    pnl_plot = mpf.make_addplot(trades_df['total_pnl'], panel=1, type='line', ylabel='PNL in $')
    return pnl_plot

def format_chart_title(symbols, start_time, chart_schema):
    """
    Format the chart title based on given inputs.

    Args:
    symbols (list): List of symbol strings.
    start_time (str): Start time in ISO format.
    chart_schema (str): Chart schema string.

    Returns:
    str: Formatted chart title.
    """
    date_part = start_time.split('T')[0]
    formatted_date = pd.to_datetime(date_part).strftime('%m/%d')
    symbol = symbols[0] if symbols else 'Symbol'
    interval = chart_schema.split('-')[-1].upper()
    title = f"{symbol} - {formatted_date} - {interval}"
    return title