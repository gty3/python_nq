# import pandas as pd
# import numpy as np

# def modify_trades(df):
#     """
#     This function modifies the trades dataframe to ensure only one contract is open at a time.
#     """
#     previous_trade_side = None
#     previous_trade_open = False
    
#     # Iterate through the DataFrame rows
#     for index, row in df.iterrows():
#         # Check if the current row is a trade (price is not NaN)
#         if pd.notna(row['price']):
#             # If no trade precedes this trade, set trade_open to True
#             if previous_trade_side is None:
#                 df.at[index, 'trade_open'] = True

#             # Previous trade_open is True and current and prev trade are either "S/S" or "B/B", remove current trade
#             if previous_trade_open:
#                 # Cannot sell if a sell position is already open
#                 # If current and prev trade are both "S", remove current trade
#                 if row['side'] == 'S' and previous_trade_side == 'S':
#                     df.loc[index, ['price', 'side', 'trade_open', 'pnl']] = np.nan
#                 if row['side'] == 'B' and previous_trade_side == 'B':
#                     df.loc[index, ['price', 'side', 'trade_open', 'pnl']] = np.nan
#                 # If current and prev trade are "S/B" or "B/S", close the trade
#                 if row['side'] == 'S' and previous_trade_side == 'B':
#                     df.at[index, 'trade_open'] = False
#                     previous_trade_open = False
                    
#                 if row['side'] == 'B' and previous_trade_side == 'S':
#                     df.at[index, 'trade_open'] = False
#                     previous_trade_open = False
#             else:
#                 # Previous trade_open is False
#                 df.at[index, 'trade_open'] = True
#                 previous_trade_side = row['side']
#                 previous_trade_open = df.at[index, 'trade_open']
#         else:
#             # If not a trade, continue without changing previous trade details
#             continue

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