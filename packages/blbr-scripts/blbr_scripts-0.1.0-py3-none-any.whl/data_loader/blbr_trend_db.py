import logging
from fileinput import close

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TrendUtils:
    """
    Utility class containing helper methods used throughout the trend analysis.
    """

    @staticmethod
    def get_next_counter(references):
        """Get the next counter value for trend counting."""
        try:
            value = references[-1][3]
            counter = value if isinstance(value, int) else 0
            counter += 1
            return counter
        except (IndexError, TypeError):
            return 1

    @staticmethod
    def get_value_as_bool(references, row, col):
        """Safely extract boolean values from references."""
        try:
            value = references[row][col]
            return value if isinstance(value, bool) else ""
        except (IndexError, TypeError):
            return ""

    @staticmethod
    def get_value(references, row, col):
        """Safely extract str values from references."""
        try:
            value = references[row][col]
            return value if isinstance(value, str) else ""
        except (IndexError, TypeError):
            return ""

    @staticmethod
    def get_base_high_low(bl_br_references, df, row_number):
        """Get the baseline high and low values for comparison."""
        if row_number == 1 or not bl_br_references:
            prev_low = df.loc[row_number - 1, "LOW_PRICE"]
            prev_high = df.loc[row_number - 1, "HIGH_PRICE"]
        else:
            prev_low = bl_br_references[-1][1]
            prev_high = bl_br_references[-1][2]
        return prev_high, prev_low


def bull_bear_percentage(bear, bull, close_price):
    # Handle None or zero values to prevent division errors
    if close_price == 0 or close_price is None or bull is None or bear is None:
        return f"0.0%", f"0.0%"  # Avoid division by zero or None comparisons

    diff = 100 / close_price
    bull_percentage = (bull - close_price) * diff
    bear_percentage = (bear - close_price) * diff
    return f"{round(bull_percentage, 2)}%", f"{round(bear_percentage, 2)}%"



class TrendState:
    """
    Base class for trend states. Contains common data and methods.
    """

    def __init__(self, analyzer):
        self.analyzer = analyzer  # Reference to the main TrendAnalyzer

    def process(self, df, row_number):
        """
        Process the current row based on trend state.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement process method")


class TrendNotConfirmed(TrendState):
    """
    Class handling logic when trend is not yet confirmed.
    Handles scenarios 1-4.
    """

    def process(self, df, row_number):
        """
        Process row when trend is not confirmed.
        Identifies initial Br1 or Bl1 breakout points.
        """
        close_price = df.loc[row_number, "CLOSE_PRICE"]
        base_high, base_low = TrendUtils.get_base_high_low(
            self.analyzer.bl_br_references, df, row_number
        )

        trend_type = ""
        trend_confirmed = False

        # Process if close price is below previous low
        if close_price < base_low:
            trend_type, trend_confirmed = self._handle_bearish_breakout(df, row_number, base_low)

        # Process if close price is above previous high
        if close_price > base_high:
            trend_type, trend_confirmed = self._handle_bullish_breakout(df, row_number, base_high)

        logging.info(f"\nScenario 1-4: \n\tLine: {row_number + 1}, \n\tclose_price: {close_price}, "
                     f"\n\tBase base_low: {base_low}, Base base_high: {base_high}, "
                     f"\n\ttrend_confirmed : {trend_confirmed}")

        return trend_confirmed

    def _handle_bearish_breakout(self, df, row_number, base_low):
        """Handle bearish breakout when trend is not confirmed."""
        trend_confirmed = False

        if self._has_reversal_for_non_trend_confirmed_for("Bl"):
            logging.info(f"Line: {row_number + 1}, Trend not confirmed but reversal from BL to BR")
            br_counter = 1
        else:
            br_counter = TrendUtils.get_next_counter(self.analyzer.br_references)

        trend_type = f"Br{br_counter}"
        is_reversal = TrendUtils.get_value_as_bool(self.analyzer.bl_br_references, -1, 4)
        prev_trend_type_br = TrendUtils.get_value(self.analyzer.bl_br_references, -1, 3) == 'Br'

        if br_counter >= 2:
            if is_reversal and not prev_trend_type_br:
                bull = df.at[row_number, "HIGH_PRICE"]
            else:
                bull = self.analyzer.br_references[-1][2] if self.analyzer.br_references else df.at[
                    row_number, "HIGH_PRICE"]
        else:
            bull = df.at[row_number, "HIGH_PRICE"]

        bear = df.loc[row_number, "LOW_PRICE"]

        self.analyzer.trends.append((row_number, trend_type, bull, bear))

        trend_confirmed = trend_confirmed or (br_counter >= 2)
        self.analyzer.br_references.append(
            (row_number, df.loc[row_number, "LOW_PRICE"], df.loc[row_number, "HIGH_PRICE"], br_counter)
        )
        self.analyzer.bl_br_references.append(
            (row_number, df.loc[row_number, "LOW_PRICE"], df.loc[row_number, "HIGH_PRICE"], "Br", False)
        )

        return trend_type, trend_confirmed

    def _handle_bullish_breakout(self, df, row_number, base_high):
        """Handle bullish breakout when trend is not confirmed."""
        trend_confirmed = False

        if self._has_reversal_for_non_trend_confirmed_for("Br"):
            logging.info(f"Line: {row_number + 1}, Trend not confirmed but reversal from BR to BL")
            bl_counter = 1
        else:
            bl_counter = TrendUtils.get_next_counter(self.analyzer.bl_references)

        trend_type = f"Bl{bl_counter}"
        is_reversal = TrendUtils.get_value_as_bool(self.analyzer.bl_br_references, -1, 4)
        # if prev_trend_type_bl is false, the it is false breakout
        prev_trend_type_bl = TrendUtils.get_value(self.analyzer.bl_br_references, -1, 3) == 'Bl'

        if bl_counter >= 2:
            if is_reversal and not prev_trend_type_bl:
                bear = df.at[row_number, "LOW_PRICE"]
            else:
                bear = self.analyzer.bl_references[-1][1] if self.analyzer.bl_references else df.at[
                    row_number, "LOW_PRICE"]
        else:
            bear = df.at[row_number, "LOW_PRICE"]

        bull = df.loc[row_number, "HIGH_PRICE"]

        self.analyzer.trends.append((row_number, trend_type, bull, bear))

        trend_confirmed = trend_confirmed or (bl_counter >= 2)
        self.analyzer.bl_references.append(
            (row_number, df.loc[row_number, "LOW_PRICE"], df.loc[row_number, "HIGH_PRICE"], bl_counter)
        )
        self.analyzer.bl_br_references.append(
            (row_number, df.loc[row_number, "LOW_PRICE"], df.loc[row_number, "HIGH_PRICE"], "Bl", False)
        )

        return trend_type, trend_confirmed

    def _has_reversal_for_non_trend_confirmed_for(self, reversal_trend_type):
        """Checks if there are enough data points for a reversal trend."""
        try:
            prev_record_trend = self.analyzer.bl_br_references[-1][3]
            return prev_record_trend == reversal_trend_type and not self.analyzer.first_trend_confirmed
        except IndexError:
            return False


class TrendConfirmed(TrendState):
    """
    Class handling logic when trend is confirmed.
    Handles scenarios 5-18.
    """

    def process(self, df, row_number):
        """
        Process row when trend is confirmed.
        Handles trend reversals and continuations.
        """
        close_price = df.loc[row_number, "CLOSE_PRICE"]
        low_price = df.loc[row_number, "LOW_PRICE"]
        high_price = df.loc[row_number, "HIGH_PRICE"]

        # Check if we have a trend reversal first
        reversal = self._process_trend_reversal(df, row_number, close_price, low_price, high_price)

        br_trend_confirmation = self.analyzer.bl_br_references[-1][3] == 'Br'
        bl_trend_confirmation = self.analyzer.bl_br_references[-1][3] == 'Bl'

        logging.info(f"\nScenario 5-8: \n\tLine: {row_number + 1}, \n\tclose_price: {close_price}, "
                     f"\n\tlow: {low_price}, high: {high_price}, "
                     f"\n\tbr_trend_confirmation: {br_trend_confirmation}, "
                     f"bl_trend_confirmation: {bl_trend_confirmation}, "
                     f"\n\tReversal: {reversal}")

        if reversal:
            # Return False to indicate trend is no longer confirmed
            return False

        # If no reversal, check for trend continuation
        continuation = self._process_trend_continuation(df, row_number, close_price, low_price, high_price)

        if continuation:
            logging.info(f"\nScenario 9-18: \n\tLine: {row_number + 1}, \n\tclose_price: {close_price}, "
                         f"\n\tlow: {low_price}, high: {high_price}, "
                         f"\n\tbr_trend_confirmation: {br_trend_confirmation}, "
                         f"bl_trend_confirmation: {bl_trend_confirmation}, "
                         f"\n\tContinuation: {continuation}")

        # Return True to indicate trend remains confirmed
        return True

    def _process_trend_reversal(self, df, row_number, close_price, low_price, high_price):
        """Handle trend reversals when a trend is already confirmed."""
        br_trend_confirmation = self.analyzer.bl_br_references[-1][3] == 'Br'
        bl_trend_confirmation = self.analyzer.bl_br_references[-1][3] == 'Bl'

        if br_trend_confirmation:
            if len(self.analyzer.bl_br_references) > 1 and self.analyzer.bl_br_references[-2][3] == "Bl":
                close_price_derived_high = self.analyzer.br_references[-1][2]
            else:
                close_price_derived_high = self.analyzer.br_references[-2][2] if len(
                    self.analyzer.br_references) > 1 else self.analyzer.br_references[-1][2]

            if self.analyzer.br_references and close_price > close_price_derived_high:
                bull = high_price
                bear = low_price
                self.analyzer.trends.append((row_number, "Bl1", bull, bear))
                self.analyzer.bl_references.append((row_number, low_price, high_price, 1))
                self.analyzer.bl_br_references.append((row_number, low_price, high_price, "Bl", True))
                logging.info(f"Scenario 5-8: Checking Reversal: Line: {row_number + 1}, "
                             f"br_trend_high (closing price: {close_price} "
                             f"should be greater than) :{close_price_derived_high}")
                return True

        elif bl_trend_confirmation:
            if len(self.analyzer.bl_br_references) > 1 and self.analyzer.bl_br_references[-2][3] == "Br":
                close_price_derived_low = self.analyzer.bl_references[-1][1]
            else:
                close_price_derived_low = self.analyzer.bl_references[-2][1] if len(
                    self.analyzer.bl_references) > 1 else self.analyzer.bl_references[-1][1]

            if self.analyzer.bl_references and close_price < close_price_derived_low:
                bull = high_price
                bear = low_price
                self.analyzer.trends.append((row_number, "Br1", bull, bear))
                self.analyzer.br_references.append((row_number, low_price, high_price, 1))
                self.analyzer.bl_br_references.append((row_number, low_price, high_price, "Br", True))
                logging.info(f"Scenario 5-8: Checking Reversal: Line: {row_number + 1}, "
                             f"bl_trend_low (Closing price: {close_price} "
                             f"should be less than): {close_price_derived_low}")
                return True

        return False

    def _process_trend_continuation(self, df, row_number, close_price, low_price, high_price):
        """Handle trend continuation when a trend is already confirmed."""
        br_trend_confirmation = self.analyzer.bl_br_references[-1][3] == 'Br'
        bl_trend_confirmation = self.analyzer.bl_br_references[-1][3] == 'Bl'

        if br_trend_confirmation:
            if self.analyzer.br_references and close_price < self.analyzer.br_references[-1][1]:
                counter = TrendUtils.get_next_counter(self.analyzer.br_references)

                bull = self.analyzer.br_references[-1][2]
                bear = low_price
                self.analyzer.trends.append((row_number, f"Br{counter}", bull, bear))
                self.analyzer.br_references.append((row_number, low_price, high_price, counter))
                self.analyzer.bl_br_references.append((row_number, low_price, high_price, "Br", False))
                logging.info(f"Scenario 9-18: Line: {row_number + 1}")
                return True

        elif bl_trend_confirmation:
            if self.analyzer.bl_references and close_price > self.analyzer.bl_references[-1][2]:
                next_counter = TrendUtils.get_next_counter(self.analyzer.bl_references)
                bear = self.analyzer.bl_references[-1][1]
                bull = high_price
                self.analyzer.trends.append((row_number, f"Bl{next_counter}", bull, bear))
                self.analyzer.bl_references.append((row_number, low_price, high_price, next_counter))
                self.analyzer.bl_br_references.append((row_number, low_price, high_price, "Bl", False))
                logging.info(f"Scenario 9-18: Line: {row_number + 1}")
                return True

        return False


class FinancialIndicators:
    """
    Class for calculating financial indicators like RSI.
    """

    @staticmethod
    def calculate_supertrend(df, atr_multiplier=3, atr_period=10):
        """
        Calculate Supertrend indicator columns.

        Parameters:
        df (pandas.DataFrame): DataFrame containing OHLC and ATR data
        atr_multiplier (float): Multiplier for ATR to determine bands, default is 3
        atr_period (int): Period for ATR calculation, default is 14

        Returns:
        pandas.DataFrame: DataFrame with added Supertrend columns
        """
        # Initialize new columns
        df['Basic Upperband'] = None
        df['Basic Lowerband'] = None
        df['Final Upperband'] = None
        df['Final Lowerband'] = None
        df['SUPERTREND'] = None

        # We need ATR values to start calculations
        start_idx = atr_period  # First index where ATR is available

        # Calculate Basic Upperband and Lowerband
        for i in range(start_idx, len(df)):
            if pd.notna(df.loc[i, 'ATR']):
                # Basic bands calculation
                basic_ub = ((df.loc[i, 'HIGH_PRICE'] + df.loc[i, 'LOW_PRICE']) / 2) + (
                        atr_multiplier * df.loc[i, 'ATR'])
                basic_lb = ((df.loc[i, 'HIGH_PRICE'] + df.loc[i, 'LOW_PRICE']) / 2) - (
                        atr_multiplier * df.loc[i, 'ATR'])

                df.loc[i, 'Basic Upperband'] = basic_ub
                df.loc[i, 'Basic Lowerband'] = basic_lb

        # Calculate Final Upperband and Lowerband using previous values
        # First value initialization
        if len(df) > start_idx:
            df.loc[start_idx, 'Final Upperband'] = df.loc[start_idx, 'Basic Upperband']
            df.loc[start_idx, 'Final Lowerband'] = df.loc[start_idx, 'Basic Lowerband']

            # Determine initial trend
            if df.loc[start_idx, 'CLOSE_PRICE'] <= df.loc[start_idx, 'Final Upperband']:
                df.loc[start_idx, 'SUPERTREND'] = df.loc[start_idx, 'Final Upperband']
            else:
                df.loc[start_idx, 'SUPERTREND'] = df.loc[start_idx, 'Final Lowerband']

        # Calculate for the rest of the data
        for i in range(start_idx + 1, len(df)):
            # If basic upperband < previous final upperband OR close price > previous final upperband
            if (df.loc[i, 'Basic Upperband'] < df.loc[i - 1, 'Final Upperband'] or
                    df.loc[i - 1, 'CLOSE_PRICE'] > df.loc[i - 1, 'Final Upperband']):
                df.loc[i, 'Final Upperband'] = df.loc[i, 'Basic Upperband']
            else:
                df.loc[i, 'Final Upperband'] = df.loc[i - 1, 'Final Upperband']

            # If basic lowerband > previous final lowerband OR close price < previous final lowerband
            if (df.loc[i, 'Basic Lowerband'] > df.loc[i - 1, 'Final Lowerband'] or
                    df.loc[i - 1, 'CLOSE_PRICE'] < df.loc[i - 1, 'Final Lowerband']):
                df.loc[i, 'Final Lowerband'] = df.loc[i, 'Basic Lowerband']
            else:
                df.loc[i, 'Final Lowerband'] = df.loc[i - 1, 'Final Lowerband']

            # Determine SUPERTREND value
            if df.loc[i - 1, 'SUPERTREND'] == df.loc[i - 1, 'Final Upperband']:
                # Previous trend was downward (SUPERTREND = upperband)
                if df.loc[i, 'CLOSE_PRICE'] <= df.loc[i, 'Final Upperband']:
                    # Continue downward trend
                    df.loc[i, 'SUPERTREND'] = df.loc[i, 'Final Upperband']
                else:
                    # Change to upward trend
                    df.loc[i, 'SUPERTREND'] = df.loc[i, 'Final Lowerband']
            else:
                # Previous trend was upward (SUPERTREND = lowerband)
                if df.loc[i, 'CLOSE_PRICE'] >= df.loc[i, 'Final Lowerband']:
                    # Continue upward trend
                    df.loc[i, 'SUPERTREND'] = df.loc[i, 'Final Lowerband']
                else:
                    # Change to downward trend
                    df.loc[i, 'SUPERTREND'] = df.loc[i, 'Final Upperband']

        # Round all calculated columns
        df['Basic Upperband'] = df['Basic Upperband'].round(3)
        df['Basic Lowerband'] = df['Basic Lowerband'].round(3)
        df['Final Upperband'] = df['Final Upperband'].round(3)
        df['Final Lowerband'] = df['Final Lowerband'].round(3)
        df['SUPERTREND'] = df['SUPERTREND'].round(3)

        return df

    @staticmethod
    def calculate_atr(df, period=10):
        """
        Calculate Average True Range (ATR) indicator, ignoring the first record.

        Parameters:
        df (pandas.DataFrame): DataFrame containing the True Range column "TR"
        period (int): Period for the ATR calculation, default is 10

        Returns:
        list: ATR values for each row
        """
        atr_values = [None] * len(df)
        true_value = df["TR"]

        # Compute RSI starting from the point where we have 'period' data
        for i in range(period, len(df)):
            # Slice the prior 'period' gains/losses
            window_tr = true_value[i - period + 1: i + 1]

            # Calculate average gain/loss for this window
            avg_tr = sum(window_tr) / period

            # Store the average gain/loss in the arrays
            atr_values[i] = avg_tr

        return atr_values

    @staticmethod
    def calculate_true_range(df):
        """Calculate True Range indicator."""
        tr_values = [None] * len(df)

        # First row TR is simply the High-Low range
        if len(df) > 0:
            tr_values[0] = 0

        # Calculate TR for remaining rows
        for i in range(1, len(df)):
            high = df.loc[i, "HIGH_PRICE"]
            low = df.loc[i, "LOW_PRICE"]
            prev_close = df.loc[i - 1, "CLOSE_PRICE"]

            # True Range formula
            tr = max(
                high - low,  # Current high-low range
                abs(high - prev_close),  # Current high vs previous close
                abs(low - prev_close)  # Current low vs previous close
            )

            tr_values[i] = tr

        return tr_values

    @staticmethod
    def create_gain(df):
        """Calculate gain values for RSI."""
        gain_array = ["" for _ in range(len(df))]
        for row_number in range(1, len(df)):
            close_price = df.loc[row_number, "CLOSE_PRICE"]
            prev_close = df.loc[row_number - 1, "CLOSE_PRICE"]

            gain = 0
            if close_price > prev_close:
                gain = close_price - prev_close

            gain_array[row_number] = gain
        return gain_array

    @staticmethod
    def create_loss(df):
        """Calculate loss values for RSI."""
        loss_array = ["" for _ in range(len(df))]
        for row_number in range(1, len(df)):
            close_price = df.loc[row_number, "CLOSE_PRICE"]
            prev_close = df.loc[row_number - 1, "CLOSE_PRICE"]

            loss = 0
            if close_price < prev_close:
                loss = prev_close - close_price

            loss_array[row_number] = loss
        return loss_array

    @staticmethod
    def calculate_trend_bull_bear(df, trends):
        # Apply the identified trends to the dataframe
        for row_number, trend_type, bull, bear in trends:
            df.loc[row_number, "Bull"] = bull
            df.loc[row_number, "Bear"] = bear
            close_price = df.loc[row_number, "CLOSE_PRICE"]
            bull_percentage, bear_percentage = bull_bear_percentage(bear, bull, close_price)
            df.loc[row_number, "Bull %"] = bull_percentage
            df.loc[row_number, "Bear %"] = bear_percentage

        # Logic to fill blanks with previous value of Bull / Bear
        last_bull = None
        last_bear = None
        for i in range(len(df)):
            # Check for valid bull and bear values before using them
            bull_value = df.loc[i, "Bull"]
            bear_value = df.loc[i, "Bear"]
            
            # Check if both bull and bear values are valid numbers
            if (not pd.isna(bull_value) and not pd.isna(bear_value) and 
                bull_value != 0 and bear_value != 0 and
                bull_value is not None and bear_value is not None):
                last_bull = bull_value
                last_bear = bear_value
            elif i > 0:  # Skip the first row if it has no trend
                if last_bull is not None and last_bear is not None:
                    close_price = df.loc[i, "CLOSE_PRICE"]
                    # Skip if close_price is None or NaN
                    if pd.notna(close_price) and close_price is not None:
                        bull_percentage, bear_percentage = bull_bear_percentage(last_bear, last_bull, close_price)
                        df.loc[i, "Bull"] = last_bull
                        df.loc[i, "Bear"] = last_bear
                        df.loc[i, "Bull %"] = bull_percentage
                        df.loc[i, "Bear %"] = bear_percentage
        return df

    @staticmethod
    def calculate_rsi(df, period=14, column="CLOSE_PRICE"):
        """Calculate RSI using simple moving average (rolling mean)."""
        return FinancialIndicators.calculate_rsi_sma(df, period, column)

    @staticmethod
    def calculate_rsi_sma(df, period=14, column="CLOSE_PRICE"):
        """Calculate RSI using simple moving average (rolling mean)."""
        delta = df[column].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        df["RSI"] = rsi.round(3)
        df["GAIN"] = gain.round(3)  # Add raw gain values
        df["LOSS"] = loss.round(3)  # Add raw loss values
        df["AVG_GAIN"] = avg_gain.round(3)
        df["AVG_LOSS"] = avg_loss.round(3)
        return df

    @staticmethod
    def calculate_ema(df, column="CLOSE_PRICE", period=200, smoothing=2):
        """
        Calculate Exponential Moving Average (EMA) for a specified column.

        Parameters:
        df (pandas.DataFrame): DataFrame containing price data
        column (str): Column name to calculate EMA on, default is "CLOSE_PRICE"
        period (int): EMA period, default is 200
        smoothing (int): Smoothing factor, default is 2

        Returns:
        pandas.DataFrame: DataFrame with added EMA column and indicator column
        """
        if len(df) <= period:
            return df

        ema_column = f"EMA_{period}"
        ema_ind_column = f"EMA_{period}_IND"
        df[ema_column] = None

        multiplier = smoothing / (1 + period)

        # Calculate initial SMA and set as first EMA value
        df.loc[period - 1, ema_column] = df[column].iloc[:period].mean()

        # Calculate EMA from the next index
        for i in range(period, len(df)):
            prev_ema = df.loc[i - 1, ema_column]
            current_price = df.loc[i, column]
            df.loc[i, ema_column] = (current_price - prev_ema) * multiplier + prev_ema

        # Round the EMA values
        df[ema_column] = df[ema_column].round(3)

        # Add indicator column
        df[ema_ind_column] = ""
        for i in range(len(df)):
            close_val = df.loc[i, column]
            ema_val = df.loc[i, ema_column]
            if pd.notna(close_val) and pd.notna(ema_val):
                if close_val <= ema_val:
                    df.loc[i, ema_ind_column] = "DOWN"
                else:
                    df.loc[i, ema_ind_column] = "UP"

        return df


    @staticmethod
    def calculate_average_volume(df, periods=[30, 100, 200], volume_column="TTL_TRD_QNTY"):
        """
        Calculate Average Volume for specified periods (30, 100, 200 days by default).
        
        Parameters:
        df (pandas.DataFrame): DataFrame containing volume data
        periods (list): List of periods to calculate average volume for, default is [30, 100, 200]
        volume_column (str): Column name containing volume data, default is "TTL_TRD_QNTY"
        
        Returns:
        pandas.DataFrame: DataFrame with added average volume columns
        """
        # Validate input
        if volume_column not in df.columns:
            logging.warning(f"Volume column '{volume_column}' not found in DataFrame. Available columns: {df.columns.tolist()}")
            return df
            
        # Create a copy of the volume data to avoid modifying the original
        volume_data = df[volume_column].copy()
        
        # Calculate average volume for each period
        for period in periods:
            avg_vol_column = f"AVG_VOL_{period}"
            
            # Calculate rolling average
            df[avg_vol_column] = volume_data.rolling(window=period).mean().round(0)
            
        
        return df

    @staticmethod
    def calculate_adx(df, high_column="HIGH_PRICE", low_column="LOW_PRICE", close_column="CLOSE_PRICE", window=14):
        """
        Calculate Average Directional Index (ADX) indicator.
        
        Parameters:
        df (pandas.DataFrame): DataFrame containing high, low, and close price data
        high_column (str): Column name for high prices, default is "HIGH_PRICE"
        low_column (str): Column name for low prices, default is "LOW_PRICE"
        close_column (str): Column name for close prices, default is "CLOSE_PRICE"
        window (int): Period for ADX calculation, default is 14
        
        Returns:
        pandas.DataFrame: DataFrame with added ADX, +DI, and -DI columns
        """
        # Validate input
        required_columns = [high_column, low_column, close_column]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logging.warning(f"Required columns {missing_columns} not found in DataFrame. Available columns: {df.columns.tolist()}")
            return df
            
        try:
            # Import ta library for technical analysis
            import ta.trend
            
            # Create ADX indicator
            adx_indicator = ta.trend.ADXIndicator(high=df[high_column], low=df[low_column], close=df[close_column], window=window)
            
            # Add ADX, +DI, and -DI columns to the DataFrame with CSV-friendly names
            df["ADX"] = adx_indicator.adx()
            df["PLUS_DI"] = adx_indicator.adx_pos()  # Using PLUS_DI instead of +DI
            df["MINUS_DI"] = adx_indicator.adx_neg()  # Using MINUS_DI instead of -DI
            
            # Round values for better readability
            df["ADX"] = df["ADX"].round(2)
            df["PLUS_DI"] = df["PLUS_DI"].round(2)
            df["MINUS_DI"] = df["MINUS_DI"].round(2)
            
            logging.info(f"ADX indicator calculated successfully with window={window}")
            
        except Exception as e:
            logging.error(f"Error calculating ADX indicator: {str(e)}")
            
        return df


class TrendAnalyzer:
    """
    Main class that orchestrates the trend analysis process.
    """

    def __init__(self):
        self.trend_confirmed = False
        self.first_trend_confirmed = False
        self.br_references = []  # Stores br breakdown points
        self.bl_references = []  # Stores bl breakout points
        self.bl_br_references = []  # Stores both breakout points
        self.trends = []  # Initialize trends collection

        # Initialize state handlers
        self.not_confirmed_state = TrendNotConfirmed(self)
        self.confirmed_state = TrendConfirmed(self)

        # Initial state
        self.current_state = self.not_confirmed_state

    def identify_trends(self, df):
        """
        Main method to identify trends in the provided dataframe.
        """
        for row_number in range(1, len(df)):
            if self.trend_confirmed:
                self.first_trend_confirmed = True
                self.current_state = self.confirmed_state
            else:
                self.current_state = self.not_confirmed_state

            # Process current row based on state
            if self.current_state == self.not_confirmed_state:
                self.trend_confirmed = self.current_state.process(df, row_number)
            else:  # confirmed state
                still_confirmed = self.current_state.process(df, row_number)
                if not still_confirmed:
                    self.trend_confirmed = False

        # Apply the identified trends to the dataframe
        for row_number, trend_type, bull, bear in self.trends:
            df.loc[row_number, "Trend"] = trend_type

        return df, self.trends


def process_data_frame(df):
    """
    Reads an input Excel file, applies trend identification, and writes output.
    """

    # Create analyzer and identify trends
    trend_analyzer = TrendAnalyzer()
    df, trends = trend_analyzer.identify_trends(df)

    # Calculate financial indicators
    indicators = FinancialIndicators()
    df["Gain"] = indicators.create_gain(df)
    df["Loss"] = indicators.create_loss(df)

    df["Gain"] = df["Gain"].round(3)
    df["Loss"] = df["Loss"].round(3)

    indicators.calculate_rsi(df)

    indicators.calculate_trend_bull_bear(df, trends)

    # Calculate True Range
    df["TR"] = indicators.calculate_true_range(df)
    df["TR"] = df["TR"].round(3)

    # Calculate Average True Range
    df["ATR"] = indicators.calculate_atr(df, period=10)
    df["ATR"] = df["ATR"].round(3)

    df = indicators.calculate_supertrend(df, atr_period=10, atr_multiplier=3)

    # Calculate EMA with period 20
    df = indicators.calculate_ema(df, column="CLOSE_PRICE", period=20, smoothing=2)
    df = indicators.calculate_ema(df, column="CLOSE_PRICE", period=50, smoothing=2)
    df = indicators.calculate_ema(df, column="CLOSE_PRICE", period=100, smoothing=2)
    df = indicators.calculate_ema(df, column="CLOSE_PRICE", period=200, smoothing=2)

    # Calculate Average Volume
    df = indicators.calculate_average_volume(df)

    # Calculate ADX
    df = indicators.calculate_adx(df)

    # Write to output file
    return df


if __name__ == "__main__":
    input_file_path = "data/TEST_Input.csv"
    output_file_path = "data/TEST_output.csv"
    expected_file_path = "output_analysis_expected.xlsx"
    
    # Read CSV with proper numeric conversion
    df = pd.read_csv(input_file_path, thousands=',')
    
    df = process_data_frame(df)
    df.to_csv(output_file_path, index=False)
    print(f"Processed analysis file saved to {output_file_path}")

    # Try to compare with expected output if the file exists
    try:
        # Read both Excel files into DataFrames
        df_generated = pd.read_csv(output_file_path)
        df_expected = pd.read_csv(expected_file_path)

        # Compare the two DataFrames
        comparison = df_generated.compare(df_expected)

        # Check if differences exist
        if comparison.empty:
            logging.info("The generated output matches the expected output exactly.")
        else:
            logging.info("There are differences between the generated and expected output.")
            print("Differences found between generated and expected output.")
    except FileNotFoundError:
        logging.info(f"Expected file '{expected_file_path}' not found. Skipping comparison.")
        print(f"Note: Expected file '{expected_file_path}' not found. Skipping comparison.")
