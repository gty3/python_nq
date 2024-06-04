import pandas as pd
import numpy as np

def modify_trades(df):
    """
    Modifies the trades dataframe to ensure only one contract is open at a time.
    
    Parameters:
    - df (pd.DataFrame): The trades dataframe with columns 'price', 'side', 'trade_open', 'pnl'.
    
    The function iterates through each trade in the dataframe.
    - Trades of the same type ('S' or 'B') cannot open consecutively without closing the previous one.
    - A trade of a different type can close the previous trade.
    
    Modifies the dataframe in-place by setting non-allowed trades to NaN and adjusting the 'trade_open' status.
    """
    previous_trade_side = None
    previous_trade_open = False
    for index, row in df.iterrows():
        if pd.notna(row['price']):
            if previous_trade_open:
                if row['side'] == previous_trade_side:
                    df.loc[index, ['price', 'side', 'trade_open', 'pnl']] = np.nan
                else:
                    df.at[index, 'trade_open'] = False
                    previous_trade_open = False
            else:
                df.at[index, 'trade_open'] = True
                previous_trade_side = row['side']
                previous_trade_open = True