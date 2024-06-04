import pandas as pd

# def calculate_pnl(trades_df):
#     """
#     Calculate the profit and loss for trades stored in a DataFrame.
    
#     Args:
#     trades_df (pd.DataFrame): DataFrame containing trade data with columns 'price', 'side', 'trade_open'.
    
#     Modifies the dataframe in-place by setting non-allowed trades to NaN and adjusting the 'trade_open' status.
#     """
#     fees_per_side = 1.38
    
#     for idx, trade in trades_df.iterrows():
#         if not trade['trade_open']:
#             # Find the previous non-NaN price
#             previous_non_nan_price = trades_df.loc[:idx, 'price'].dropna().iloc[-2]
#             # Calculate trade_pnl based on the side of the trade
#             if trade['side'] == 'S':
#                 trades_df.at[idx, 'trade_pnl'] = trade['price'] - previous_non_nan_price
#             elif trade['side'] == 'B':
#                 trades_df.at[idx, 'trade_pnl'] = previous_non_nan_price - trade['price']
#     trades_df['trade_pnl'] = trades_df['trade_pnl'].fillna(0) * 20
#     trade_count = trades_df['price'].notna().cumsum()
#     trades_df['total_pnl'] = trades_df['trade_pnl'].cumsum() - (fees_per_side * trade_count)
    
    
def calculate_pnl(trades_df):
    """
    Calculate the profit and loss (PnL) for trades stored in a DataFrame.

    This function computes the PnL for each trade based on its opening and closing prices,
    adjusts for fees, and updates the DataFrame in-place.

    Args:
        trades_df (pd.DataFrame): DataFrame containing trade data with columns:
            'price' (float): The price of the trade.
            'side' (str): 'B' for buy or 'S' for sell.
            'trade_open' (bool): True if the trade is open, False otherwise.

    Modifies:
        trades_df (pd.DataFrame): Adds 'trade_pnl' and 'total_pnl' columns to input DataFrame.
    """
    fees_per_side = 1.38
    trades_df['trade_pnl'] = 0

    for idx, trade in trades_df.iterrows():
        if not trade['trade_open']:
            previous_price = trades_df.loc[:idx, 'price'].dropna().iloc[-2]
            pnl = trade['price'] - previous_price if trade['side'] == 'S' else previous_price - trade['price']
            trades_df.at[idx, 'trade_pnl'] = pnl

    trades_df['trade_pnl'] *= 20
    trade_count = trades_df['price'].notna().cumsum()
    trades_df['total_pnl'] = trades_df['trade_pnl'].cumsum() - (fees_per_side * trade_count)