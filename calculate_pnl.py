import pandas as pd

def calculate_pnl(trades_df):
    """
    Calculate the profit and loss for trades stored in a DataFrame.
    
    Args:
    trades_df (pd.DataFrame): DataFrame containing trade data with columns 'price', 'side', 'trade_open'.
    
    Returns:
    pd.DataFrame: Updated DataFrame with a new 'trade_pnl' column.
    """
    fees_per_side = 1.38
    
    for idx, trade in trades_df.iterrows():
        if not trade['trade_open']:
            # Find the previous non-NaN price
            previous_non_nan_price = trades_df.loc[:idx, 'price'].dropna().iloc[-2]
            # Calculate trade_pnl based on the side of the trade
            if trade['side'] == 'S':
                trades_df.at[idx, 'trade_pnl'] = trade['price'] - previous_non_nan_price
            elif trade['side'] == 'B':
                trades_df.at[idx, 'trade_pnl'] = previous_non_nan_price - trade['price']
    trades_df['trade_pnl'] = trades_df['trade_pnl'].fillna(0) * 20
    trade_count = trades_df['price'].notna().cumsum()
    trades_df['total_pnl'] = trades_df['trade_pnl'].cumsum() - (fees_per_side * trade_count)
    return trades_df