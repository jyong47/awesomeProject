"""
20-MINUTE INTERVIEW SOLUTION: Stock Backtesting Framework
Focus: Speed, clarity, and completeness over perfection
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def quick_clean_and_merge(file_paths):
    """Step 2 & 3: Clean and merge datasets quickly"""

    print("🔄 Step 2&3: Cleaning and Merging Data")
    print("-" * 50)

    all_data = []

    for filepath in file_paths:
        df = pd.read_parquet(filepath)

        # Quick fixes for main quality issues:
        # 1. Standardize date format
        df['date'] = pd.to_datetime(df['date'], format='mixed')

        # 2. Remove duplicates
        df = df.drop_duplicates()

        # 3. Handle missing adj_close (use close as fallback)
        df['adj_close'] = df['adj_close'].fillna(df['close'])

        # 4. Remove rows with missing critical data
        df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])

        all_data.append(df)
        print(f"✓ Loaded {Path(filepath).name}: {len(df)} rows")

    # Merge all data
    merged_df = pd.concat(all_data, ignore_index=True)
    print(f"✓ Merged total: {len(merged_df)} rows, {merged_df['symbol'].nunique()} symbols")

    return merged_df.sort_values(['symbol', 'date'])

def calculate_factor(df, window=5):
    """Step 4: Calculate simple factor (5-day Moving Average)"""

    print(f"\n📈 Step 4: Calculating {window}-day Moving Average Factor")
    print("-" * 50)

    # Calculate MA for each symbol
    df['ma_factor'] = df.groupby('symbol')['close'].transform(
        lambda x: x.rolling(window=window, min_periods=window).mean()
    )

    # Calculate signal: 1 if price > MA (buy), 0 otherwise
    df['signal'] = (df['close'] > df['ma_factor']).astype(int)

    print(f"✓ Factor calculated for {len(df)} rows")
    print(f"✓ Buy signals generated: {df['signal'].sum()} ({df['signal'].mean()*100:.1f}%)")

    return df

def simple_backtest(df):
    """Step 5: Simple backtesting with key metrics"""

    print(f"\n💰 Step 5: Backtesting Factor Performance")
    print("-" * 50)

    results = {}

    # Calculate daily returns
    df['daily_return'] = df.groupby('symbol')['close'].pct_change()

    # Strategy returns: only when signal = 1
    df['strategy_return'] = df['daily_return'] * df['signal'].shift(1)

    # Calculate metrics per symbol
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol].copy()

        # Remove NaN returns
        symbol_data = symbol_data.dropna(subset=['strategy_return', 'daily_return'])

        if len(symbol_data) == 0:
            continue

        # Cumulative returns
        symbol_cum_return = (1 + symbol_data['strategy_return']).prod() - 1
        benchmark_cum_return = (1 + symbol_data['daily_return']).prod() - 1

        # Basic metrics
        strategy_mean = symbol_data['strategy_return'].mean() * 252  # Annualized
        strategy_std = symbol_data['strategy_return'].std() * np.sqrt(252)  # Annualized
        sharpe_ratio = strategy_mean / strategy_std if strategy_std > 0 else 0

        # Win rate
        win_rate = (symbol_data['strategy_return'] > 0).mean()

        # Max drawdown
        cumulative = (1 + symbol_data['strategy_return']).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        results[symbol] = {
            'total_return': symbol_cum_return,
            'annual_return': strategy_mean,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'benchmark_return': benchmark_cum_return,
            'num_trades': symbol_data['signal'].sum()
        }

    # Print results
    print("\n📊 Backtesting Results:")
    print(f"{'Symbol':<15} {'Return':<12} {'Sharpe':<10} {'Win Rate':<10} {'Max DD':<10}")
    print("-" * 65)

    for symbol, metrics in results.items():
        print(f"{symbol:<15} {metrics['total_return']:>10.2%} {metrics['sharpe_ratio']:>9.2f} "
              f"{metrics['win_rate']:>9.1%} {metrics['max_drawdown']:>9.2%}")

    return results

def main():
    """Complete interview solution"""

    print("🎯 STOCK BACKTESTING FRAMEWORK - 20 MINUTE SOLUTION")
    print("=" * 70)

    # File paths
    file_paths = [
        '/Users/admin4/Downloads/stock_data_part1.parquet',
        '/Users/admin4/Downloads/stock_data_part2.parquet',
        '/Users/admin4/Downloads/stock_data_part3.parquet'
    ]

    try:
        # Step 2&3: Clean and merge
        df = quick_clean_and_merge(file_paths)

        # Step 4: Calculate factor
        df = calculate_factor(df, window=5)

        # Step 5: Backtesting
        results = simple_backtest(df)

        print(f"\n✅ COMPLETE! Solution ready for tuning and optimization")
        print(f"⏱️  Ready for refinement within time constraint")

        return df, results

    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

if __name__ == "__main__":
    df, results = main()