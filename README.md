<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div >


<h2 >NQ Script</h2>

  <p >
  A trading algorithm that looks at historical data and outputs a dataframe of trades.
    <br />
    <br />
    <a href="https://github.com/gty3/dom-replay/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/gty3/dom-replay/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

![Product Screenshot](https://raw.githubusercontent.com/gty3/dom-img/main/nq_1s_2m.png)

This project serves as an educational experiment. 




### Built With
* [![Python](https://img.shields.io/badge/Python-20232A?style=for-the-badge&logo=python&logoColor=61DAFB)](https://www.python.org/)
* [![Pandas](https://img.shields.io/badge/Pandas-42b883?style=for-the-badge&logo=pandas)](https://pandas.pydata.org/)
* [![Jupyter](https://img.shields.io/badge/Jupyter-DEA584?style=for-the-badge&logo=jupyter)](https://jupyter.org/)
* [![mplfinance](https://img.shields.io/badge/mplfinance-FF9900?style=for-the-badge&logo=)](https://github.com/matplotlib/mplfinance)


* [![SST](https://img.shields.io/badge/dtale-4A90E2?style=for-the-badge&logo=serverless-stack)](https://github.com/man-group/dtale)
* [![Databento](https://img.shields.io/badge/Databento-DEA584?style=for-the-badge&logo=custom&logoColor=white)](https://databento.com/)





<!-- GETTING STARTED -->
## Getting Started

To run the Jupyter notebook, you'll need an appropriate environment.
I'm using Visual Studio Code with the Jupyter extension. 

You will need an API key from  [Databento](https://databento.com/).

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/gty3/python_nq.git
   ```
2. Open the project with your choice of Jupyter platform.
3. Rename `env.example` to `.env` and add your DATABENTO_API_KEY

4. Go to nq_script.ipynb and select Run All.
  
    If you are using vscode you will be prompted to select a kernel.






<!-- USAGE EXAMPLES -->
## Usage

The project is divided into 4 cells. 

Cell 1 imports 3 datasets using the [get_range](https://databento.com/docs/api-reference-historical/timeseries/timeseries-get-range?historical=python&live=python) method:
- The first 2 datasets use the "tbbo" schema - "Top of Book Bid and Offer". While the order book data is necessary for logging the NQ trade prices, it is not necessary for the underlying instruments orders. However, as these datasets are merged, it enables more concise code.
- The 3rd dataset uses the "ohlcv-1s" schema to create our candlestick chart in cell 4.


Cell 2 implements the trading logic for the algorithm.
It aggregates the number of buys and sells across the 100 underlying instruments each second.
The data comes in a dataframe and the library `pandas` is used for data manipulation.
The cell defines a function `modify_trades` to handle trade modifications based on specific conditions, such as preventing multiple open trades of the same type. It then calculates buy and sell conditions based on the aggregated data of underlying instruments and the NQ contract and logs this in a dataframe. Finally, the cell calculates the profit and loss (PnL) for each trade, adjusting for trading fees, and aggregates the total PnL.

Cell 3 utilizes the `dtale` library to render an interactive view of the trades dataframe. This is a great tool to visualize the dataframe while modifying the code. 

Cell 4 creates a candlestick chart, overlaying a buy and sell dataframe, split from the previous dataframe, on a ohlc dataframe chart.

<!-- ROADMAP -->
## Roadmap

- [ ] Simulate network latency.
- [ ] Add a stop loss. 
- [ ] Add max duration to a trade.




<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.





<!-- CONTACT -->
## Contact

Geoff Young - [@_gty__](https://x.com/_gty__)

Project Link: [https://github.com/gty3/python_nq](https://github.com/gty3/python_nq)
