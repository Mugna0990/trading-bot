# Trading Bot for Phemex

This is a Python-based trading bot designed to operate on the Phemex exchange using the [CCXT]library. The bot is capable of executing automated trades based based on simple moving averages (SMA) 

## Features

- **Automated Trading**: Executes buy and sell orders based on predefined strategies.
- **Customizable Parameters**: Easily adjust position size, target profit, and stop-loss settings 
- **Risk Management**: Implements a kill switch and stop-loss mechanism to manage risk.
- **SMA Strategy**: Utilizes daily simple moving averages to determine trends and 15-minute to price targets and opens.


## Requirements

- The following Python packages:
  - `ccxt`
  - `pandas`
  - `schedule`
  - `time`
 

