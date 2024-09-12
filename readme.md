# Trading Bot for Phemex

This Python-based trading bot is designed to operate on the Phemex exchange using the [CCXT] library. The bot executes automated trades based on simple moving averages (SMA) to capture market trends and optimize entry and exit points. It includes risk management tools and customizable parameters.

## Features

- **Automated Trading**: Executes buy and sell orders based on predefined strategies.
- **Risk Management**: Implements a stop-loss mechanism to protect against significant losses during market volatility.
- **Customizable Parameters**: Users can adjust position sizes, target profits, and stop-loss settings to suit their trading style and risk tolerance.
- **SMA Strategy**: Uses daily simple moving averages to detect trends and a 15-minute SMA to determine specific buy/sell price points for trade entry.

## Trading Strategy

The bot's strategy revolves around using two SMAs to detect trends and fine-tune entry points:

- **Daily SMA (Long-Term Trend)**:  
  The daily SMA (100 column) is used to determine the overall market trend. If the price is above the daily SMA, the bot will seek long (buy) opportunities. If the price is below the daily SMA, it will seek short (sell) positions. This ensures that trades are placed in the direction of the prevailing trend.

- **15-Minute SMA (Entry Price Calculation)**:  
  The 15-minute SMA (100 column) is used to determine specific price points for opening positions. Once the trend direction is established by the daily SMA, the bot calculates buy and sell prices based on the 15-minute SMA as follows:
  
  - **Buy Price (Long Positions)**:
    - `bp_1`: 0.1% above the 15-minute SMA
    - `bp_2`: 0.3% below the 15-minute SMA
  - **Sell Price (Short Positions)**:
    - `sp_1`: 0.1% below the 15-minute SMA
    - `sp_2`: 0.3% above the 15-minute SMA

  This setup allows the bot to trigger long positions slightly above or below the 15-minute SMA in an uptrend, and short positions slightly below or above the 15-minute SMA in a downtrend, providing flexibility and precision in trade entry.

### Example Workflow:

Positions are opened using *limit orders* at these price points. This strategy helps minimize trading fees by not executing *market orders*.

1. **Uptrend**:  
   If the price is trading above the daily SMA, the bot calculates potential buy prices (bp_1 and bp_2) based on the 15-minute SMA and opens a long position.
2. **Downtrend**:  
   If the price is trading below the daily SMA, the bot calculates potential sell prices (sp_1 and sp_2) based on the 15-minute SMA and opens a short position.


This trading bot is developed for educational and experimental purposes only. It is not intended for live trading or financial use. Users should not rely on it for actual trading, and the creators are not responsible for any financial losses incurred by using this software.
