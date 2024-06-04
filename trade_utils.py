import pandas as pd
import numpy as np

def prepare_dataframes(nq_df, underlying_df):
    """
    Combine the NQ and underlying dataframes and attache NQ bid / ask to every order.

    Args:
        nq_df (pd.DataFrame): DataFrame containing NQ with columns 'ask_px_00' and 'bid_px_00'.
        underlying_df (pd.DataFrame): Orders from all the stocks in the Nasdaq 100.

    Returns:
        pd.DataFrame: Combined DataFrame with forward filled 'nq_ask' and 'nq_bid' columns.
    """
    nq_df['nq_ask'] = nq_df['ask_px_00']
    nq_df['nq_bid'] = nq_df['bid_px_00']
    combined_df = pd.concat([underlying_df, nq_df]).sort_index()
    combined_df['nq_ask'] = combined_df['nq_ask'].ffill()
    combined_df['nq_bid'] = combined_df['nq_bid'].ffill()
    return combined_df
  
def group_and_aggregate(df):
    """
    Group and aggregate the dataframe by second and calculate trading metrics, 
    total buy orders and total sell orders per second.

    Args:
        df (pd.DataFrame): Dataframe to be grouped and aggregated.

    Returns:
        pd.DataFrame: Aggregated Dataframe with total sells, total buys, and last 'nq_ask' and 'nq_bid'.
    """
    return df.groupby(df.index.floor('S')).agg(
        underlying_total_sells=('side', lambda x: x.eq('A').sum()),
        underlying_total_buys=('side', lambda x: x.eq('B').sum()),
        nq_ask=('nq_ask', 'last'),
        nq_bid=('nq_bid', 'last')
    )

def create_trades_df(grouped_df, ohlcv_df):
    """
    Create a dataframe for trades based on conditions derived from grouped data.

    Args:
        grouped_df (pd.DataFrame): Dataframe containing aggregated trade data.
        ohlcv_df (pd.DataFrame): Dataframe containing OHLCV data for the trading period.

    Returns:
        pd.DataFrame: Trades Dataframe with columns for price, side, and trade open status.
    """
    # Create a DataFrame for trades with the same index as the OHLCV dataframe to allow for plotting
    trades_df = pd.DataFrame(index=ohlcv_df.index, columns=['price', 'side', 'trade_open', 'trade_pnl'])
    # Trade condition: if total sells is greater than total buys * 2
    buy_condition = (grouped_df['underlying_total_sells'] > grouped_df['underlying_total_buys'] * 2)
    # Trade condition: if total buys is greater than total sells * 2
    sell_condition = (grouped_df['underlying_total_buys'] > grouped_df['underlying_total_sells'] * 2)
    # Log the trade in the trades dataframe, if sell, trade price will be nq_bid, and vice versa
    trades_df.loc[sell_condition, 'price'] = grouped_df['nq_bid']
    trades_df.loc[sell_condition, 'side'] = 'S'
    trades_df.loc[buy_condition, 'price'] = grouped_df['nq_ask']
    trades_df.loc[buy_condition, 'side'] = 'B'
    return trades_df

def modify_trades(df):
    """
    Modify the trades dataframe to ensure only one contract is open at a time.
    Remove consecutive trades of the same type ('S' or 'B') when a trade is already open.
    
    Args:
        df (pd.DataFrame): The trades dataframe with columns 'price', 'side', 'trade_open'.
    
    Modifies:
        df (pd.DataFrame): Trades dataframe with non-allowed trades to NaN and adjust the 'trade_open' status.
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
    Compute the PnL for each trade based on ask / bid prices,
    adjust for fees, and update trade_pnl and total_pnl accordingly.

    Args:
        trades_df (pd.DataFrame): Dataframe containing trade data with columns:
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