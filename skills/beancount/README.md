# Beancount Skill for Clawdbot

A comprehensive skill for managing Beancount accounting files through Clawdbot. This skill provides tools for adding transactions, querying balances, and generating financial reports.

## Features

- **Transaction Management**: Add new transactions to your Beancount file with proper formatting
- **Balance Queries**: Get account balances by pattern or date
- **Financial Reports**: Generate trial balances, income statements, and balance sheets
- **Price Tracking**: Add price entries for currencies and commodities
- **Data Extraction**: Extract entries from external sources
- **Direct Queries**: Execute custom Beancount queries

## Prerequisites

You need to have Beancount installed on your system:

```bash
pip install beancount
```

## Configuration

The skill can be configured with the following options:

- `beancount_file`: Path to your main Beancount file (default: `main.bean`)
- `beancount_directory`: Directory containing your Beancount files (default: current directory)

Example configuration:

```json
{
  "beancount_file": "finance/main.bean",
  "beancount_directory": "/home/user/accounting"
}
```

## Available Functions

### File Operations
- `check_file()`: Check the Beancount file for syntax errors
- `print_entries(date_range)`: Print entries from the file optionally filtered by date range

### Balance Queries
- `get_balance(account_pattern, commodity)`: Get account balances
- `get_balances_by_date(date, account_pattern)`: Get balances at a specific date

### Transaction Management
- `add_transaction(date, payee, narration, postings, tags, links)`: Add a new transaction
- `add_price(date, currency, price, base_currency)`: Add a price entry

### Report Generation
- `generate_trial_balance()`: Generate a trial balance
- `generate_income_statement()`: Generate an income statement (P&L)
- `generate_balance_sheet()`: Generate a balance sheet

### Data Queries
- `query_transactions(query)`: Execute a custom Beancount query
- `get_account_information(account)`: Get detailed information about an account
- `extract_entries(source_file, account)`: Extract entries from external sources

## Usage Examples

### Adding a Transaction

```python
result = add_transaction(
    date="2023-10-15",
    payee="Supermarket",
    narration="Grocery shopping",
    postings=[
        {"account": "Expenses:Food", "amount": "-125.30", "currency": "USD"},
        {"account": "Assets:Checking", "amount": "125.30", "currency": "USD"}
    ],
    tags=["weekly-shopping"]
)
```

### Checking Balances

```python
# Get all asset balances
balances = get_balance("Assets:*")

# Get balance for a specific account at a specific date
balance = get_balances_by_date("2023-10-01", "Assets:Checking")
```

### Generating Reports

```python
# Generate income statement
income_stmt = generate_income_statement()

# Generate balance sheet
balance_sheet = generate_balance_sheet()
```

## Transaction Format

When adding transactions, the `postings` parameter should be a list of dictionaries with the following structure:

```python
[
    {
        "account": "Account Name",      # Required
        "amount": "Amount",             # Required (negative for debits)
        "currency": "Currency Code",    # Optional
        "cost": "Cost Basis",           # Optional
        "price": "Price Annotation"     # Optional
    }
]
```

For example:
```python
postings = [
    {
        "account": "Expenses:Restaurants",
        "amount": "-45.60",
        "currency": "USD"
    },
    {
        "account": "Assets:Cash",
        "amount": "45.60",
        "currency": "USD"
    }
]
```

## Error Handling

All functions return a dictionary with the following structure:
- `success`: Boolean indicating if the operation was successful
- `output`: String containing the operation output (if successful)
- `error`: String containing error message (if failed)
- `returncode`: Return code from the underlying command (if applicable)

## Security Considerations

- Ensure your Beancount files have appropriate file permissions
- Be cautious when executing custom queries that could potentially modify data
- Regularly backup your Beancount files before making bulk changes

## Troubleshooting

- If you get "Beancount installation not found" error, ensure Beancount is installed and `bean-check` command is available in your PATH
- If you encounter encoding issues, ensure your Beancount files are saved in UTF-8 encoding
- For large files, some operations might take longer than the default timeout (30 seconds)