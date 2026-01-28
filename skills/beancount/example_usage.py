"""
Example usage of the Beancount skill
"""
import tempfile
import os
from pathlib import Path
import sys

# Add the skill to the path so we can import it
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from main import initialize, add_transaction, get_balance, generate_income_statement, generate_balance_sheet


def create_example_beancount_file(file_path):
    """Create an example beancount file with initial accounts and transactions"""
    content = """
; Example Beancount file for Clawdbot skill demonstration
1970-01-01 custom "fava-option" "default-file" "{}"

; Define account types
1900-01-01 open Assets:Checking USD
1900-01-01 open Assets:Savings USD
1900-01-01 open Assets:Investments AAPL,MSFT,GOOG,USD
1900-01-01 open Expenses:Food USD
1900-01-01 open Expenses:Transport USD
1900-01-01 open Expenses:Entertainment USD
1900-01-01 open Expenses:Bills USD
1900-01-01 open Income:Salary USD
1900-01-01 open Income:Dividends USD
1900-01-01 open Liabilities:CreditCard USD
1900-01-01 open Equity:OpeningBalance USD

; Initial balances
2023-01-01 * "Opening balance"
  Assets:Checking              5000.00 USD
  Assets:Savings              10000.00 USD
  Equity:OpeningBalance       -15000.00 USD

; Sample transactions
2023-01-15 * "Employer" "Monthly salary"
  Assets:Checking  4000.00 USD
  Income:Salary   -4000.00 USD

2023-01-16 * "Grocery Store" "Weekly groceries"
  Expenses:Food    150.00 USD
  Assets:Checking  -150.00 USD

2023-01-18 * "Gas Station" "Fill up car"
  Expenses:Transport  60.00 USD
  Assets:Checking    -60.00 USD

2023-01-20 * "Electric Company" "Electricity bill"
  Expenses:Bills  120.00 USD
  Liabilities:CreditCard  -120.00 USD

2023-02-01 * "Credit Card Payment"
  Liabilities:CreditCard  -120.00 USD
  Assets:Checking          120.00 USD
""".format(file_path)
    
    with open(file_path, 'w') as f:
        f.write(content)


def main():
    """Demonstrate the Beancount skill functionality"""
    print("Beancount Skill Example Usage\n")
    
    # Create a temporary directory and file for our example
    with tempfile.TemporaryDirectory() as temp_dir:
        beancount_file = Path(temp_dir) / "example.bean"
        create_example_beancount_file(beancount_file)
        
        print(f"Created example beancount file: {beancount_file}")
        
        # Initialize the skill with our example file
        config = {
            'beancount_file': str(beancount_file),
            'beancount_directory': str(temp_dir)
        }
        
        print("\n1. Initializing Beancount skill...")
        initialize(config)
        print("✓ Skill initialized")
        
        # Check the file for any syntax errors
        print("\n2. Checking file validity...")
        from main import check_file
        result = check_file()
        if result['success']:
            print("✓ File is valid")
        else:
            print(f"✗ File has errors: {result['error']}")
        
        # Get current balances
        print("\n3. Current account balances:")
        result = get_balance()
        if result['success']:
            print(result['output'])
        else:
            print(f"Error getting balances: {result['error']}")
        
        # Get balances for asset accounts only
        print("\n4. Asset account balances:")
        result = get_balance("Assets:*")
        if result['success']:
            print(result['output'])
        else:
            print(f"Error getting asset balances: {result['error']}")
        
        # Add a new transaction
        print("\n5. Adding a new transaction...")
        result = add_transaction(
            date="2023-02-15",
            payee="Restaurant",
            narration="Dinner with friends",
            postings=[
                {
                    "account": "Expenses:Food",
                    "amount": "-75.50",
                    "currency": "USD"
                },
                {
                    "account": "Assets:Checking",
                    "amount": "75.50",
                    "currency": "USD"
                }
            ],
            tags=["social", "dining"]
        )
        
        if result['success']:
            print(f"✓ Transaction added: {result['output']}")
        else:
            print(f"✗ Failed to add transaction: {result['error']}")
        
        # Get updated balances after adding transaction
        print("\n6. Updated food expense balance:")
        result = get_balance("Expenses:Food")
        if result['success']:
            print(result['output'])
        else:
            print(f"Error getting food balances: {result['error']}")
        
        # Generate income statement
        print("\n7. Generating income statement...")
        result = generate_income_statement()
        if result['success']:
            print(result['output'])
        else:
            print(f"Error generating income statement: {result['error']}")
        
        # Generate balance sheet
        print("\n8. Generating balance sheet...")
        result = generate_balance_sheet()
        if result['success']:
            print(result['output'])
        else:
            print(f"Error generating balance sheet: {result['error']}")
        
        print(f"\n✓ Example completed! The transaction was added to {beancount_file}")
        print("You can view the file content with: cat", beancount_file)


if __name__ == "__main__":
    main()