import pandas as pd
import argparse
import os
import sys

def extract_data(file_path):
    """
    Extract data from CSV file into a DataFrame
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {len(df)} records from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def transform_data(df):
    """
    Transform data according to requirements
    """
    if df is None or df.empty:
        return None
    
    initial_count = len(df)
    
    df = df.dropna(subset=['rating', 'review_text'])
    print(f"Removed {initial_count - len(df)} records with null rating or review_text")
    
    try:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df = df.dropna(subset=['rating'])
        df['rating'] = df['rating'].astype(int)
    except Exception as e:
        print(f"Error converting ratings to integers: {e}")
        return None
    
    valid_ratings_count = len(df)
    df = df[(df['rating'] >= 1) & (df['rating'] <= 5)]
    print(f"Removed {valid_ratings_count - len(df)} records with invalid ratings")
    
    df['sentiment'] = df['review_text'].str.contains('bad', case=False).map({True: 'Negative', False: 'Positive'})
    
    print(f"Transformation complete. Final record count: {len(df)}")
    return df

def load_data(df, output_path, format='csv'):
    """
    Load transformed data to output file
    """
    if df is None or df.empty:
        print("No data to save")
        return False
    
    try:
        if format.lower() == 'csv':
            df.to_csv(output_path, index=False)
        elif format.lower() == 'json':
            df.to_json(output_path, orient='records', lines=True)
        else:
            print(f"Unsupported format: {format}")
            return False
        
        print(f"Successfully saved {len(df)} records to {output_path}")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def main():
    """
    Main function that orchestrates the ETL pipeline
    """
    parser = argparse.ArgumentParser(description='ETL Pipeline for Product Reviews')
    parser.add_argument('--input', default='product_reviews.csv', help='Input CSV file path')
    parser.add_argument('--output', default='enriched_product_reviews.csv', help='Output file path')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Output file format (csv or json)')
    
    args = parser.parse_args()
    
    print("Starting ETL pipeline...")
    
    print("\n--- Extract phase ---")
    df = extract_data(args.input)
    if df is None:
        print("Extract phase failed. Exiting pipeline.")
        sys.exit(1)
    
    print("\n--- Transform phase ---")
    transformed_df = transform_data(df)
    if transformed_df is None:
        print("Transform phase failed. Exiting pipeline.")
        sys.exit(1)
    
    print("\n--- Load phase ---")
    
    output_path = args.output
    if not output_path.lower().endswith(f'.{args.format}'):
        base, _ = os.path.splitext(output_path)
        output_path = f"{base}.{args.format}"
    
    success = load_data(transformed_df, output_path, args.format)
    
    if success:
        print("\nETL pipeline completed successfully!")
    else:
        print("\nETL pipeline failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
