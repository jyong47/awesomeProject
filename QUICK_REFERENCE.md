# 🚀 Interview Quick Reference

## 60-Second Explanation

"I implemented a complete stock backtesting framework with 5 key steps:

1. **Data Analysis**: Identified quality issues in 3 parquet files (9,757 rows, 10 stocks)
2. **Data Cleaning**: Fixed duplicates, standardized dates, handled missing values
3. **Factor Implementation**: 5-day Moving Average crossover strategy
4. **Backtesting**: Tested strategy with Sharpe ratio, returns, win rate, max drawdown
5. **Results**: Strategy performed well on some stocks (+72% on 601318.SH), needs tuning for others

The framework is modular and scalable - easy to add new factors or improve existing ones."

---

## Key Technical Points

### Data Quality Issues Found:
- Missing adj_close values (1-3%)
- Duplicate rows (11-26 per file)
- Date format inconsistencies (YYYY-MM-DD vs YYYY/MM/DD)

### Factor Logic:
```
IF close_price > 5_day_MA THEN BUY
ELSE HOLD/Sell
```

### Performance Metrics:
- **Sharpe Ratio**: 0.80 (best) - measures risk-adjusted return
- **Win Rate**: ~21% - percentage of profitable trades
- **Max Drawdown**: -20% to -52% - largest loss from peak

---

## Optimization Ideas (If Asked)

1. **Try different periods**: 10-day MA, 20-day MA
2. **Add filters**: Volume confirmation, volatility thresholds
3. **Risk management**: Stop-loss, position sizing
4. **Combine factors**: MA + RSI, MA + Volume
5. **Transaction costs**: Include realistic trading fees

---

## Files Created
- `interview_solution.py` - Complete working solution
- `analyze_parquet.py` - Data analysis script
- `INTERVIEW_SUMMARY.md` - Detailed results

---

**Running the solution**: `python3 interview_solution.py`