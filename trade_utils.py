import pandas as pd
import numpy as np

def prepare_dataframes(nq_df, underlying_df):
    nq_df['nq_ask'] = nq_df['ask_px_00']
    nq_df['nq_bid'] = nq_df['bid_px_00']
    combined_df = pd.concat([underlying_df, nq_df]).sort_index()
    combined_df['nq_ask'] = combined_df['nq_ask'].ffill()
    combined_df['nq_bid'] = combined_df['nq_bid'].ffill()
    return combined_df
  
def group_and_aggregate(df):
    return df.groupby(df.index.floor('S')).agg(
        underlying_total_sells=('side', lambda x: x.eq('A').sum()),
        underlying_total_buys=('side', lambda x: x.eq('B').sum()),
        nq_ask=('nq_ask', 'last'),
        nq_bid=('nq_bid', 'last')
    )

def create_trades_df(grouped_df, ohlcv_df):
    trades_df = pd.DataFrame(index=ohlcv_df.index, columns=['price', 'side', 'trade_open', 'trade_pnl'])
    buy_condition = (grouped_df['underlying_total_sells'] > grouped_df['underlying_total_buys'] * 2)
    sell_condition = (grouped_df['underlying_total_buys'] > grouped_df['underlying_total_sells'] * 2)
    trades_df.loc[sell_condition, 'price'] = grouped_df['nq_bid']
    trades_df.loc[sell_condition, 'side'] = 'S'
    trades_df.loc[buy_condition, 'price'] = grouped_df['nq_ask']
    trades_df.loc[buy_condition, 'side'] = 'B'
    return trades_df

def modify_trades(df):
    """
    Modifies the trades dataframe to ensure only one contract is open at a time.
    
    Args:
        df (pd.DataFrame): The trades dataframe with columns 'price', 'side', 'trade_open'.
    
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
                    df.loc[index, ['price', 'side', 'trade_open']] = np.nan
                else:
                    df.at[index, 'trade_open'] = False
                    previous_trade_open = False
            else:
                df.at[index, 'trade_open'] = True
                previous_trade_side = row['side']
                previous_trade_open = True
                
def calculate_pnl(trades_df):
    """
    This function computes the PnL for each trade based on ask / bid prices,
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