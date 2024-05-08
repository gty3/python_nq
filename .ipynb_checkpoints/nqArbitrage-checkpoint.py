import databento as db
import pandas as pd
import mplfinance as mpf
import dtale
from decimal import Decimal
from dataclasses import dataclass, field

client = db.Historical("db-VMucgt5GiD6SD9F9FVbJn83f7XT4P")
start_time = "2024-03-18T13:44:00"
end_time = "2024-03-18T13:45:00"


class Config:
    # Alpha threshold to buy/sell, k
    ALPHA_THRESHOLD: int = 1.7

    # Symbol
    DATASET = 'GLBX.MDP3'
    UNDERLYING_DATASET = 'XNAS.ITCH'
    SYMBOLS = ['NQM4']
    UNDERLYING_SYMBOLS = [
    "MSFT", "AAPL", "NVDA", "AMZN", "META", "AVGO", "GOOGL", "COST", "GOOG", "TSLA",
    "AMD", "NFLX", "PEP", "ADBE", "LIN", "CSCO", "TMUS", "QCOM", "INTU", "INTC",
    "CMCSA", "AMAT", "TXN", "AMGN", "ISRG", "HON", "LRCX", "BKNG", "VRTX", "MU",
    "SBUX", "REGN", "ADP", "MDLZ", "ADI", "KLAC", "GILD", "PANW", "SNPS", "PDD",
    "CDNS", "ASML", "MELI", "CRWD", "CSX", "MAR", "ABNB", "PYPL", "ORLY", "CTAS",
    "PCAR", "MNST", "NXPI", "ROP", "WDAY", "LULU", "MRVL", "ADSK", "CEG", "CPRT",
    "DASH", "FTNT", "DXCM", "ROST", "MCHP", "ODFL", "FAST", "PAYX", "IDXX", "AEP",
    "CHTR", "KHC", "GEHC", "KDP", "MRNA", "CSGP", "AZN", "DDOG", "CTSH", "TTD",
    "EXC", "EA", "FANG", "VRSK", "CDW", "BKR", "CCEP", "ON", "BIIB", "TEAM",
    "ANSS", "ZS", "XEL", "GFS", "DLTR", "MDB", "TTWO", "WBD", "ILMN", "WBA", "SIRI"
    ]

    VENUE_FEES_PER_SIDE: Decimal = Decimal('0.39')
    CLEARING_FEES_PER_SIDE: Decimal = Decimal('0.05')
    FEES_PER_SIDE: Decimal = VENUE_FEES_PER_SIDE + CLEARING_FEES_PER_SIDE

    # Position limit
    POSITION_MAX: int = 10

@dataclass
class Trade:
    dataset: str
    underlying_dataset: str
    symbols: list
    underlying_symbols: list
    
    # Current position, in contract units
    position: int = 0
    # Number of long contract sides traded
    buy_qty: int = 0
    # Number of short contract sides traded
    sell_qty: int = 0
    ## Total realized buy price
    real_total_buy_px: Decimal = 0
    ## Total realized sell price
    real_total_sell_px: Decimal = 0
    # Total buy price to liquidate current position
    theo_total_buy_px: Decimal = 0
    # Total sell price to liquidate current position
    theo_total_sell_px: Decimal = 0
    
    underlying_total_sells: int = 0
    underlying_total_buys: int = 0
    

    def run(self) -> None:
        nq_instrument_id = 13743
        
        underlying_df = client.timeseries.get_range(
            dataset=self.underlying_dataset,
            symbols=self.underlying_symbols,
            schema="tbbo",
            start=start_time,
            end=end_time,
        ).to_df()
        nq_df = client.timeseries.get_range(
            dataset=self.dataset,
            symbols=self.symbols,
            schema="tbbo",
            start=start_time,
            end=end_time,
        ).to_df()  
        nq_and_underlying_df = pd.concat([underlying_df, nq_df])
        
        nq_ohlc_df = client.timeseries.get_range(
            dataset=self.dataset,
            schema="ohlcv-1s",
            symbols=self.symbols,
            start=start_time,
            end=end_time,
        ).to_df()
        
        trades_df = pd.DataFrame(columns=['price', 'side'])
        current_second = None
        
        dtale.show(nq_and_underlying_df)
        
        for index, row in nq_and_underlying_df.iterrows():
            
            # this runs twice?
            if current_second is None or current_second != index.second:
                if current_second is not None:  # Ensure this is not the first iteration
                    print(self.underlying_total_sells, self.underlying_total_buys, index.second)
                    # Process trades for the previous second here if needed
                    pass
                self.underlying_total_buys = 0
                self.underlying_total_sells = 0
                current_second = index.second
            
            # if these trades per second 
            
            if row['instrument_id'] == nq_instrument_id:
                # I need an NQ bid / ask on all entries of df
                # This needs to be a running variable not inside here
                if self.underlying_total_sells > self.underlying_total_buys:
                    trade_details = pd.DataFrame({
                        'price': [row['price']],
                        'side': [row['side']]
                    }, index=[index])
                    trades_df = pd.concat([trades_df, trade_details], ignore_index=False) 
                elif self.underlying_total_buys > self.underlying_total_sells:
                    trade_details = pd.DataFrame({
                        'price': [row['price']],
                        'side': [row['side']]
                    }, index=[index])
                    trades_df = pd.concat([trades_df, trade_details], ignore_index=False)               
                    
            elif row['side'] == 'A':
                self.underlying_total_sells += 1
            elif row['side'] == 'B':
                self.underlying_total_buys += 1
                
        return nq_ohlc_df, trades_df

def chart(nq_ohlc_df: pd.DataFrame, trades_df: any) -> None:
    if trades_df.empty:
        print("No trades to plot.")
        return    
    trade_plot = mpf.make_addplot(trades_df['price'], 
                                  type='scatter', 
                                  markersize=200, 
                                  marker='.', 
                                  color='r', 
                                  label="trade")

    mpf.plot(
        nq_ohlc_df,
        type="candle",
        # volume=True,
        title="NQ",
        ylabel="OHLCV-1S Candles",
        ylabel_lower="Volume",
        xlabel="Time",
        addplot=trade_plot
    )

trade_instance = Trade(dataset=Config.DATASET, underlying_dataset=Config.UNDERLYING_DATASET, symbols=Config.SYMBOLS, underlying_symbols=Config.UNDERLYING_SYMBOLS)
nq_ohlc_df, trades_df = trade_instance.run()
dtale.show(nq_ohlc_df)
trades_df.index = pd.to_datetime(trades_df.index).round('S')
trades_df_aggregated = trades_df.groupby(trades_df.index).price.mean().reset_index()
trades_df_aggregated = trades_df_aggregated.head(60)
trades_df_aggregated.set_index('index', inplace=True)

# print(len(trades_df_aggregated))
# print(len(nq_ohlc_df))
chart(nq_ohlc_df, trades_df_aggregated)