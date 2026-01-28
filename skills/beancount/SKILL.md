# Beancount Accounting Skill

## Overview
The Beancount skill enables Clawdbot to manage Beancount accounting files, allowing users to track finances, add transactions, query balances, and generate financial reports.

## Capabilities
- Add transactions to Beancount files
- Query account balances
- Generate financial reports (trial balance, income statement, balance sheet)
- Track prices for currencies and commodities
- Extract data from external sources
- Execute custom Beancount queries

## Requirements
- Python package: `beancount`
- Access to Beancount command-line tools (`bean-check`, `bean-balance`, `bean-query`, etc.)

## Installation
Make sure Beancount is installed on the system where Clawdbot runs:
```bash
pip install beancount
```

## Configuration
The skill uses the following configuration options:

```json
{
  "beancount_file": "main.bean",
  "beancount_directory": ".",
  "enabled": true
}
```

## Functions
- `initialize(config)`: Initialize the skill with configuration
- `check_file()`: Check beancount file for syntax errors
- `get_balance(account_pattern, commodity)`: Get account balances
- `get_balances_by_date(date, account_pattern)`: Get balances at specific date
- `add_transaction(date, payee, narration, postings, tags, links)`: Add a transaction
- `add_price(date, currency, price, base_currency)`: Add a price entry
- `generate_trial_balance()`: Generate trial balance report
- `generate_income_statement()`: Generate income statement
- `generate_balance_sheet()`: Generate balance sheet
- `query_transactions(query)`: Execute custom query
- `extract_entries(source_file, account)`: Extract from external sources
- `print_entries(date_range)`: Print entries with optional date filtering
- `get_account_information(account)`: Get detailed account info

## Usage Examples

### Adding a Transaction
```
add_transaction(
    date="2023-10-15",
    payee="Local Store",
    narration="Weekly groceries",
    postings=[
        {"account": "Expenses:Food", "amount": "-85.40", "currency": "USD"},
        {"account": "Assets:Checking", "amount": "85.40", "currency": "USD"}
    ]
)
```

### Getting Balances
```
get_balance("Assets:*")  # All asset accounts
get_balances_by_date("2023-10-01", "Assets:Checking")  # Specific date
```

### Generating Reports
```
generate_income_statement()  # Profit & loss
generate_balance_sheet()     # Assets, liabilities, equity
```

## Security
- Ensure proper file permissions on Beancount files
- Validate all inputs to prevent injection attacks in queries
- Run with minimal required privileges