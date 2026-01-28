# How to Set Up and Use the Beancount Skill for Clawdbot

## Overview
This guide explains how to install, configure, and use the Beancount skill for Clawdbot to manage your personal finances using the Beancount double-entry accounting system.

## Step 1: Install Beancount

The Beancount skill requires the Beancount Python package and its command-line tools. You can install it using the provided script:

```bash
cd skills/beancount
./install.sh
```

Alternatively, install manually:

```bash
pip install beancount
```

After installation, verify that the command-line tools are available:

```bash
bean-check --version
```

If the command is not found, you may need to add the Python scripts directory to your PATH (typically `~/.local/bin`).

## Step 2: Prepare Your Beancount File

Before using the skill, you need a Beancount file with your accounts defined. Create a file like `main.bean` with your account structure:

```
; Main Beancount file
1970-01-01 custom "fava-option" "default-file" "main.bean"

; Account definitions
1900-01-01 open Assets:Checking USD
1900-01-01 open Assets:Savings USD
1900-01-01 open Expenses:Food USD
1900-01-01 open Expenses:Transport USD
1900-01-01 open Income:Salary USD
1900-01-01 open Liabilities:CreditCard USD

; Opening balances
2023-01-01 * "Opening balance"
  Assets:Checking              5000.00 USD
  Equity:OpeningBalance       -5000.00 USD
```

## Step 3: Configure the Skill

Add the Beancount skill to your Clawdbot configuration with the path to your Beancount file:

```json
{
  "skills": {
    "beancount": {
      "enabled": true,
      "config": {
        "beancount_file": "/path/to/your/main.bean",
        "beancount_directory": "/path/to/your/accounting/directory"
      }
    }
  }
}
```

## Step 4: Using the Skill

Once configured, you can use various functions to manage your finances:

### Adding Transactions
To add a new transaction:

```python
add_transaction(
    date="2023-10-15",
    payee="Supermarket",
    narration="Weekly groceries",
    postings=[
        {"account": "Expenses:Food", "amount": "-125.30", "currency": "USD"},
        {"account": "Assets:Checking", "amount": "125.30", "currency": "USD"}
    ],
    tags=["groceries"]
)
```

### Checking Balances
Get balances for all accounts:
```python
get_balance()
```

Get balances for specific accounts:
```python
get_balance("Assets:*")  # All asset accounts
get_balance("Expenses:Food")  # Food expenses
```

Get balances at a specific date:
```python
get_balances_by_date("2023-10-01", "Assets:Checking")
```

### Generating Reports
Generate an income statement:
```python
generate_income_statement()
```

Generate a balance sheet:
```python
generate_balance_sheet()
```

Generate a trial balance:
```python
generate_trial_balance()
```

### Validating Your File
Check for syntax errors:
```python
check_file()
```

## Step 5: Testing the Skill

You can test the skill functionality using the example script:

```bash
cd skills/beancount
python3 example_usage.py
```

This will create a sample Beancount file and demonstrate various skill functions.

## Best Practices

1. **Backup Regularly**: Always backup your Beancount files before making bulk changes
2. **Validate Often**: Use `check_file()` regularly to catch syntax errors early
3. **Use Tags**: Include meaningful tags and links in transactions for better organization
4. **Consistent Naming**: Use consistent account naming conventions
5. **Regular Reconciliation**: Regularly reconcile your accounts with bank statements

## Troubleshooting

- **Command Not Found**: If you see "bean-check command not found", ensure Beancount is properly installed and the command-line tools are in your PATH
- **Permission Errors**: Make sure Clawdbot has read/write permissions to your Beancount files
- **Syntax Errors**: Use `check_file()` to identify and fix syntax errors in your Beancount file
- **Encoding Issues**: Save your Beancount files in UTF-8 encoding to avoid character-related problems

## Security Considerations

- Protect your Beancount files as they contain financial information
- Review all transactions before committing them to your books
- Regularly audit your financial data for accuracy
- Consider encrypting your Beancount files if storing on untrusted systems

## Advanced Usage

For advanced users, you can execute custom Beancount queries:

```python
query_transactions("SELECT * FROM transactions WHERE date > 2023-01-01")
```

This allows for complex reporting and analysis beyond the standard functions.