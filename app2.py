import pandas as pd
import argparse
import os
import sys

def load_data(purchases_path, members_path):
    """
    Load purchases and members data from CSV files
    """
    try:
        purchases_df = pd.read_csv(purchases_path)
        members_df = pd.read_csv(members_path)
        
        print(f"Successfully loaded {len(purchases_df)} purchase records")
        print(f"Successfully loaded {len(members_df)} member records")
        
        return purchases_df, members_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def identify_vip_customers(purchases_df, members_df):
    """
    Identify VIP customers who:
    1. Made total purchases over $250 across all transactions.
    2. Are Gold members.
    """
    try:
        total_purchases = purchases_df.groupby('customer_id')['amount'].sum().reset_index()
        total_purchases.rename(columns={'amount': 'total_spent'}, inplace=True)
        
        merged_df = pd.merge(total_purchases, members_df, on='customer_id', how='inner')
        
        vip_customers = merged_df[(merged_df['membership_level'] == 'Gold') & 
                                  (merged_df['total_spent'] > 250)]
        
        result = vip_customers[['customer_id', 'total_spent', 'membership_level']]
        
        print(f"Identified {len(result)} VIP customers")
        return result
    
    except Exception as e:
        print(f"Error identifying VIP customers: {e}")
        return None

def save_results(vip_customers, output_path, format='csv'):
    """
    Save identified VIP customers to file
    """
    if vip_customers is None or vip_customers.empty:
        print("No VIP customers to save")
        return False
    
    try:
        if format.lower() == 'csv':
            vip_customers.to_csv(output_path, index=False)
        elif format.lower() == 'json':
            vip_customers.to_json(output_path, orient='records')
        else:
            print(f"Unsupported format: {format}")
            return False
        
        print(f"Successfully saved {len(vip_customers)} VIP customer records to {output_path}")
        return True
    except Exception as e:
        print(f"Error saving results: {e}")
        return False

def main():
    """
    Main function to orchestrate the VIP customer identification
    """
    parser = argparse.ArgumentParser(description='Identify VIP customers based on purchases and membership')
    parser.add_argument('--purchases', default='purchases.csv', help='Path to purchases CSV file')
    parser.add_argument('--members', default='members.csv', help='Path to members CSV file')
    parser.add_argument('--output', default='vip_customers.csv', help='Output file path')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Output file format (csv or json)')
    
    args = parser.parse_args()
    
    print("VIP customer identification...")
    
    print("\n--- Loading Data ---")
    purchases_df, members_df = load_data(args.purchases, args.members)
    if purchases_df is None or members_df is None:
        print("Data loading failed. Exiting.")
        sys.exit(1)
    
    print("\n--- Identifying VIP Customers ---")
    vip_customers = identify_vip_customers(purchases_df, members_df)
    if vip_customers is None:
        print("VIP customer identification failed. Exiting.")
        sys.exit(1)
    
    print("\n--- Saving Results ---")
    output_path = args.output
    if not output_path.lower().endswith(f'.{args.format}'):
        base, _ = os.path.splitext(output_path)
        output_path = f"{base}.{args.format}"
    
    success = save_results(vip_customers, output_path, args.format)
    
    if success:
        print("VIP customer identification completed successfully!")
        print("\nVIP Customers:")
        print(vip_customers)
    else:
        print("\nVIP customer identification failed!")
        sys.exit(1)
    

if __name__ == "__main__":
    main()