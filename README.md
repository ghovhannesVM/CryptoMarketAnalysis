# CryptoMarketAnalysis

This tool retrieves, cleans, and merges daily price and daily candle information for cryptocurrencies.

## Requirements

Before diving into the analysis, make sure to set up your environment with the necessary dependencies. Run the following command to install them effortlessly:

```bash
pip3 install -r requirements.txt
```

## Usage

Run the `main.py` script with the following parameters:

- `--days`: Data up to a certain number of days ago
- `--tickers`: List of crypto tickers separated by spaces

**SUPPORTED CRYPTO TICKERS:** [BTC, ETH, SOL, XRP, ADA, DAI, DOT, LTC, TRX, UNI]

**SUPPORTED NUMBER OF DAYS:** Maximum 1461 (4 years)

**SUPPORTED NUMBER OF TICKERS:** Maximum 5

As a result, there will be a 'data/' folder containing CSV files with information on the specified coins.

```bash
python3 main.py --days <number_of_days> --tickers <ticker1> <ticker2> ...
```
Replace `<number_of_days>` with your desired time frame and `<ticker1>` `<ticker2>` ... with the list of crypto tickers you wish to analyze.

Happy coding and exploring! 🚀