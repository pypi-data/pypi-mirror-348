import pytest
import pandas as pd
import numpy as np
from simple_trade.momentum import rsi, macd, stoch, cci, roc

@pytest.fixture
def sample_data():
    """Fixture to provide sample price data for testing"""
    # Create a more realistic price series with clear up and down trends
    index = pd.date_range(start='2023-01-01', periods=100, freq='D')
    
    # Create a series with more pronounced trends and volatility
    np.random.seed(42)  # For reproducibility
    
    # Base uptrend
    uptrend = np.linspace(100, 200, 40)
    # Downtrend
    downtrend = np.linspace(200, 100, 40)
    # Second uptrend
    uptrend2 = np.linspace(100, 150, 20)
    
    # Add some noise
    noise = np.random.normal(0, 3, 100)
    
    # Combine all segments with noise
    combined = np.concatenate([uptrend, downtrend, uptrend2])
    close = pd.Series(combined + noise[:len(combined)], index=index)
    
    # Create high and low with more realistic spread
    high = close + np.random.uniform(1, 5, size=len(close))
    low = close - np.random.uniform(1, 5, size=len(close))
    
    return {
        'close': close,
        'high': high,
        'low': low
    }

class TestRSI:
    """Tests for the RSI indicator"""

    def test_rsi_calculation(self, sample_data):
        """Test the basic calculation of RSI"""
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = rsi(df)
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        
        # Check RSI bounds (should be between 0 and 100)
        # Skip NaN values
        valid_result = result.dropna()
        assert valid_result.min() >= 0
        assert valid_result.max() <= 100
        
        # Check for NaN values (first 'window - 1' values will be NaN by design)
        # Default window is 14, first valid value at index 13
        assert result.iloc[:13].isna().all()
        
        # Should have some valid values after window
        assert len(valid_result) > 0

    def test_rsi_with_custom_window(self, sample_data):
        """Test RSI with a custom window parameter"""
        window = 5
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = rsi(df, parameters={'window': window}, columns=None)
        
        # Check the first 'window - 1' values are NaN
        assert result.iloc[:window-1].isna().all()
        
        # Should have some valid values after window
        assert len(result.dropna()) > 0
        
    def test_rsi_trend_detection(self, sample_data):
        """Test that RSI correctly detects trend changes"""
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = rsi(df)
        
        # Skip initial NaN values
        valid_rsi = result.dropna()
        
        # Check that there are overbought (>70) and oversold (<30) periods
        # This is more reliable than checking specific indices
        assert (valid_rsi > 70).any() or (valid_rsi < 30).any()
        
        # Calculate price changes
        price_changes = sample_data['close'].pct_change().dropna()
        
        # When prices increase consistently, RSI should increase
        # Find a period of consistent price increases
        uptrend_mask = price_changes > 0
        uptrend_periods = uptrend_mask.rolling(5).sum() >= 4  # 4 out of 5 days up
        
        # Find a period of consistent price decreases
        downtrend_mask = price_changes < 0
        downtrend_periods = downtrend_mask.rolling(5).sum() >= 4  # 4 out of 5 days down
        
        # If we have clear up/down trends, verify RSI behavior
        if uptrend_periods.any() and downtrend_periods.any():
            # Find indices where trends are detected
            uptrend_idx = uptrend_periods[uptrend_periods].index[0]
            downtrend_idx = downtrend_periods[downtrend_periods].index[0]
            
            # Get RSI values for these periods if they exist in valid_rsi
            if uptrend_idx in valid_rsi.index and downtrend_idx in valid_rsi.index:
                # In uptrend, RSI should be higher than in downtrend
                assert valid_rsi[uptrend_idx] > valid_rsi[downtrend_idx]

class TestMACD:
    """Tests for the MACD indicator"""
    
    def test_macd_calculation(self, sample_data):
        """Test basic MACD calculation"""
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = macd(df)
        
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        
        # Check column names (with default parameters)
        assert f'MACD_12_26' in result.columns
        assert 'Signal_9' in result.columns
        assert f'Hist_12_26_9' in result.columns
        
        # Verify result has same index as input
        assert result.index.equals(sample_data['close'].index)

    def test_macd_custom_params(self, sample_data):
        """Test MACD with custom window parameters"""
        window_fast = 8
        window_slow = 20
        window_signal = 7
        
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = macd(df, parameters={
                     'window_slow': window_slow, 
                     'window_fast': window_fast, 
                     'window_signal': window_signal
                     }, columns=None)
        
        # Check that column names reflect custom parameters
        assert f'MACD_{window_fast}_{window_slow}' in result.columns
        assert f'Signal_{window_signal}' in result.columns
        assert f'Hist_{window_fast}_{window_slow}_{window_signal}' in result.columns

    def test_macd_crossover(self, sample_data):
        """Test that MACD line crosses the signal line during trend changes"""
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = macd(df)
        
        # Extract MACD and Signal lines
        macd_line = result.iloc[:, 0]
        signal_line = result.iloc[:, 1]
        
        # Calculate crossovers (MACD line - Signal line changes sign)
        crossovers = np.sign(macd_line - signal_line).diff().fillna(0) != 0
        
        # There should be at least one crossover in our sample data
        assert crossovers.sum() > 0

class TestStoch:
    """Tests for the Stochastic Oscillator"""
    
    def test_stoch_calculation(self, sample_data):
        """Test basic Stochastic calculation"""
        # Create DataFrame with High, Low, Close columns
        df = pd.DataFrame({
            'High': sample_data['high'],
            'Low': sample_data['low'],
            'Close': sample_data['close']
        })
        result = stoch(df, parameters=None, columns=None)
        
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        
        # Check column names (with default parameters: k_period=14, d_period=3, smooth_k=3)
        k_col = 'STOCH_K_14_3_3'
        d_col = 'STOCH_D_14_3_3'
        assert k_col in result.columns
        assert d_col in result.columns
        
        # Check bounds (Stochastic should be between 0 and 100)
        assert result[k_col].min() >= 0
        assert result[k_col].max() <= 100
        assert result[d_col].min() >= 0
        assert result[d_col].max() <= 100
        
        # Check that index matches input
        assert result.index.equals(sample_data['close'].index)

    def test_stoch_custom_params(self, sample_data):
        """Test Stochastic with custom parameters"""
        k_period = 7
        d_period = 2
        smooth_k = 2
        
        # Create DataFrame with High, Low, Close columns
        df = pd.DataFrame({
            'High': sample_data['high'],
            'Low': sample_data['low'],
            'Close': sample_data['close']
        })
        result = stoch(df, parameters={'k_period': k_period, 'd_period': d_period, 'smooth_k': smooth_k}, columns=None)
        
        # Create column names with the custom parameters
        k_col = f'STOCH_K_{k_period}_{d_period}_{smooth_k}'
        d_col = f'STOCH_D_{k_period}_{d_period}_{smooth_k}'
        
        # First k_period values should be NaN for K
        assert result[k_col].iloc[:k_period].isna().all()
        
        # K should be valid after k_period + smooth_k - 1 periods
        valid_from_k = k_period + smooth_k - 1
        assert not result[k_col].iloc[valid_from_k:].isna().any()
        
        # D should be valid after k_period + smooth_k + d_period - 2 periods
        valid_from_d = k_period + smooth_k + d_period - 2
        assert not result[d_col].iloc[valid_from_d:].isna().any()

class TestCCI:
    """Tests for the Commodity Channel Index"""
    
    def test_cci_calculation(self, sample_data):
        """Test basic CCI calculation"""
        # Create DataFrame with High, Low, Close columns
        df = pd.DataFrame({
            'High': sample_data['high'],
            'Low': sample_data['low'],
            'Close': sample_data['close']
        })
        result = cci(df)
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        
        # Check that index matches input
        assert result.index.equals(sample_data['close'].index)
        
        # First 'window - 1' values should be NaN (default window is 20)
        assert result.iloc[:19].isna().all()
        
        # Should have some valid values (not all NaNs)
        valid_result = result.dropna()
        assert len(valid_result) > 0

    def test_cci_custom_params(self, sample_data):
        """Test CCI with custom parameters"""
        window = 10
        constant = 0.02
        
        # Create DataFrame with High, Low, Close columns
        df = pd.DataFrame({
            'High': sample_data['high'],
            'Low': sample_data['low'],
            'Close': sample_data['close']
        })
        result = cci(df, parameters={'window': window, 'constant': constant}, columns=None)
        
        # First 'window - 1' values should be NaN
        assert result.iloc[:window-1].isna().all()
        
        # Should have some valid values (not all NaNs)
        valid_result = result.dropna()
        assert len(valid_result) > 0
        
    def test_cci_trend_detection(self, sample_data):
        """Test CCI trend detection properties"""
        # Create DataFrame with High, Low, Close columns
        df = pd.DataFrame({
            'High': sample_data['high'],
            'Low': sample_data['low'],
            'Close': sample_data['close']
        })
        result = cci(df)
        
        # Skip NaN values
        valid_cci = result.dropna()
        
        # There should be both positive and negative CCI values in our sample
        assert (valid_cci > 0).any()
        assert (valid_cci < 0).any()
        
        # Calculate price changes
        price_changes = sample_data['close'].pct_change()
        
        # When prices trend upward, CCI should generally be positive
        # When prices trend downward, CCI should generally be negative
        # This correlation should exist but doesn't need to be perfect
        corr = valid_cci.corr(price_changes.loc[valid_cci.index])
        assert corr > 0  # Positive correlation between price changes and CCI

class TestROC:
    """Tests for the Rate of Change indicator"""
    
    def test_roc_calculation(self, sample_data):
        """Test basic ROC calculation"""
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = roc(df)
        
        assert isinstance(result, pd.Series)
        assert not result.empty
        
        # Check that index matches input
        assert result.index.equals(sample_data['close'].index)
        
        # First 'window' values should be NaN (default window is 12)
        assert result.iloc[:12].isna().all()
        
        # Values after window should be valid
        assert not result.iloc[12:].isna().any()

    def test_roc_custom_window(self, sample_data):
        """Test ROC with custom window parameter"""
        window = 5
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = roc(df, parameters={'window': window}, columns=None)
        
        # First 'window' values should be NaN
        assert result.iloc[:window].isna().all()
        
        # Values after window should be valid
        assert not result.iloc[window:].isna().any()
        
    def test_roc_trend_detection(self, sample_data):
        """Test ROC trend detection properties"""
        # Create DataFrame with Close column
        df = pd.DataFrame({'Close': sample_data['close']})
        result = roc(df)
        
        # Skip NaN values
        valid_roc = result.dropna()
        
        # Should have both positive and negative values
        assert (valid_roc > 0).any()
        assert (valid_roc < 0).any()
        
        # ROC should correlate with price changes
        # When price increases, ROC should be positive
        # When price decreases, ROC should be negative
        price_changes = sample_data['close'].pct_change(12)  # Match ROC window
        
        # Skip NaN values after shifting
        valid_changes = price_changes.loc[valid_roc.index].dropna()
        valid_roc_subset = valid_roc.loc[valid_changes.index]
        
        # Compare signs of ROC and price changes
        # They should generally match (both positive or both negative)
        sign_match = np.sign(valid_roc_subset) == np.sign(valid_changes)
        # At least 70% of the signs should match
        assert sign_match.mean() > 0.7
