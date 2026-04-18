"""
Analyze parquet files to understand data structure and quality issues.
"""
import pandas as pd
import numpy as np
from pathlib import Path

def analyze_parquet_file(filepath):
    """
    Analyze a single parquet file and return comprehensive information.

    Args:
        filepath: Path to the parquet file

    Returns:
        Dictionary with analysis results
    """
    print(f"\n{'='*70}")
    print(f"Analyzing: {Path(filepath).name}")
    print(f"{'='*70}")

    try:
        df = pd.read_parquet(filepath)

        # Basic info
        print(f"\n📊 Basic Info:")
        print(f"   Rows: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

        # Column information
        print(f"\n📋 Columns:")
        for col in df.columns:
            dtype = df[col].dtype
            non_null = df[col].notna().sum()
            print(f"   {col:20s} {str(dtype):10s} (non-null: {non_null:,}/{len(df):,})")

        # Data types
        print(f"\n🔢 Data Types:")
        print(df.dtypes)

        # First few rows
        print(f"\n👁️  First 5 rows:")
        print(df.head())

        # Statistical summary
        print(f"\n📈 Statistical Summary:")
        print(df.describe())

        # Missing values analysis
        print(f"\n❌ Missing Values Analysis:")
        missing = df.isnull().sum()
        if missing.sum() > 0:
            for col in df.columns:
                if missing[col] > 0:
                    pct = (missing[col] / len(df)) * 100
                    print(f"   {col:20s}: {missing[col]:,} ({pct:.2f}%)")
        else:
            print("   No missing values found")

        # Duplicate rows
        duplicates = df.duplicated().sum()
        print(f"\n🔍 Duplicate Rows: {duplicates:,}")

        # Time range (if timestamp column exists)
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        if timestamp_cols:
            for col in timestamp_cols:
                if pd.api.types.is_datetime64_any_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
                    try:
                        df[col] = pd.to_datetime(df[col])
                        print(f"\n📅 Time Range ({col}):")
                        print(f"   Start: {df[col].min()}")
                        print(f"   End: {df[col].max()}")
                        print(f"   Duration: {df[col].max() - df[col].min()}")

                        # Check for duplicate timestamps
                        dup_times = df[col].duplicated().sum()
                        if dup_times > 0:
                            print(f"   ⚠️  Duplicate timestamps: {dup_times:,}")
                    except Exception as e:
                        print(f"   Could not parse {col} as datetime: {e}")

        # Potential outliers (using IQR method)
        print(f"\n📊 Potential Outliers (IQR method):")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col not in ['volume']:  # Skip volume for now as it's naturally variable
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                if outliers > 0:
                    print(f"   {col:20s}: {outliers:,} potential outliers")

        return {
            'filepath': filepath,
            'rows': len(df),
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': missing.to_dict(),
            'duplicates': duplicates,
            'df': df
        }

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def main():
    """Analyze all three parquet files."""
    files = [
        '/Users/admin4/Downloads/stock_data_part1.parquet',
        '/Users/admin4/Downloads/stock_data_part2.parquet',
        '/Users/admin4/Downloads/stock_data_part3.parquet'
    ]

    print("🔍 STOCK DATA ANALYSIS")
    print("="*70)
    print("Analyzing 3 parquet files for structure, quality issues, and content")
    print("="*70)

    results = []
    for filepath in files:
        if Path(filepath).exists():
            result = analyze_parquet_file(filepath)
            if result:
                results.append(result)
        else:
            print(f"\n❌ File not found: {filepath}")

    # Summary comparison
    if results:
        print(f"\n{'='*70}")
        print("📋 SUMMARY COMPARISON")
        print(f"{'='*70}")

        print(f"\nFile Comparison:")
        print(f"{'File':<30} {'Rows':<10} {'Columns':<10} {'Missing':<10}")
        print("-" * 60)
        for result in results:
            filename = Path(result['filepath']).name
            missing_total = sum(result['missing_values'].values())
            print(f"{filename:<30} {result['rows']:<10,} {len(result['columns']):<10} {missing_total:<10,}")

        print(f"\n📊 Data Quality Issues Found:")
        all_issues = []
        for result in results:
            filename = Path(result['filepath']).name

            # Missing values
            missing_cols = [col for col, count in result['missing_values'].items() if count > 0]
            if missing_cols:
                all_issues.append(f"{filename}: Missing values in {', '.join(missing_cols)}")

            # Duplicates
            if result['duplicates'] > 0:
                all_issues.append(f"{filename}: {result['duplicates']} duplicate rows")

        if all_issues:
            for issue in all_issues:
                print(f"   ⚠️  {issue}")
        else:
            print("   ✓ No major quality issues detected")

if __name__ == "__main__":
    main()