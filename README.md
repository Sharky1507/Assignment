# VIP Customer Identification

This project identifies VIP customers based on their purchase behavior and membership status. It processes two datasets (`purchases.csv` and `members.csv`) to find customers who:

1. Made total purchases over $250 across all transactions.
2. Are Gold members.

## Files in the Repository

- **app2.py**: Python script to identify VIP customers.
- **purchases.csv**: Assignment dataset containing purchase transactions.
- **members.csv**: Assignment dataset containing membership details.
- **vip_customers.csv**: Output file containing identified VIP customers.
- **sql.txt**: Contains the SQL query for identifying VIP customers.

## How to Run the Python Script

### Prerequisites

1. Install Python (version 3.7 or higher).
2. Install the required Python libraries:
   ```bash
   pip install pandas
   ```

### Steps

1. Run the script using the following command:
   ```bash
   python app2.py --purchases purchases.csv --members members.csv --output vip_customers.csv
   ```

### Optional Arguments

- `--purchases`: Path to the purchases CSV file (default: `purchases.csv`).
- `--members`: Path to the members CSV file (default: `members.csv`).
- `--output`: Path to the output file (default: `vip_customers.csv`).
- `--format`: Output file format, either `csv` or `json` (default: `csv`).

### Example

To save the output as a JSON file:
```bash
python app2.py --purchases purchases.csv --members members.csv --output vip_customers.json --format json
```

## How to Use the SQL Query

1. Open the `sql.txt` file to view the SQL query.
2. Execute the query in your SQL database system after importing the `purchases` and `members` tables.

## Output

The script generates an output file (e.g., `vip_customers.csv`) containing the following columns:
- `customer_id`: ID of the VIP customer.
- `total_spent`: Total amount spent by the customer.
- `membership_level`: Membership level of the customer.
