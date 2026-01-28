"""
Test suite for the Beancount skill
"""
import tempfile
import os
from pathlib import Path
import sys

# Add the skill to the path so we can import it
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from main import BeancountSkill


def test_beancount_skill_initialization():
    """Test basic initialization of the Beancount skill"""
    print("Testing Beancount skill initialization...")
    
    # Create a temporary directory and file for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "test.bean"
        
        # Create a minimal valid beancount file
        with open(temp_file, 'w') as f:
            f.write("""
; Test Beancount file
1970-01-01 custom "fava-option" "default-file" "{}"

2023-01-01 open Assets:Checking USD
2023-01-01 open Expenses:Food USD
2023-01-01 open Income:Salary USD

2023-01-15 * "Employer" "Salary payment"
  Assets:Checking  3000.00 USD
  Income:Salary   -3000.00 USD

2023-01-20 * "Grocery Store" "Weekly groceries"
  Expenses:Food  150.00 USD
  Assets:Checking  -150.00 USD
""".format(temp_file))
        
        # Initialize the skill
        config = {
            'beancount_file': str(temp_file),
            'beancount_directory': temp_dir
        }
        
        skill = BeancountSkill(config)
        print("✓ Beancount skill initialized successfully")
        
        # Test file validation
        result = skill.check_file()
        assert result['success'], f"File check failed: {result['error']}"
        print("✓ File validation passed")
        
        # Test balance query
        result = skill.get_balance()
        assert result['success'], f"Balance query failed: {result['error']}"
        print("✓ Balance query executed successfully")
        
        # Test getting specific account balance
        result = skill.get_balance("Assets:*")
        assert result['success'], f"Asset balance query failed: {result['error']}"
        print("✓ Asset balance query executed successfully")
        
        # Test adding a transaction
        postings = [
            {
                'account': 'Expenses:Entertainment',
                'amount': '-25.00',
                'currency': 'USD'
            },
            {
                'account': 'Assets:Checking',
                'amount': '25.00',
                'currency': 'USD'
            }
        ]
        
        result = skill.add_transaction(
            date="2023-01-25",
            payee="Movie Theater",
            narration="Movie tickets",
            postings=postings,
            tags=["entertainment"]
        )
        
        assert result['success'], f"Adding transaction failed: {result['error']}"
        print("✓ Transaction added successfully")
        
        # Verify the transaction was added by checking balances again
        result = skill.get_balance("Expenses:Entertainment")
        assert result['success'], f"Post-addition balance check failed: {result['error']}"
        assert "Expenses:Entertainment" in result['output'], "New expense account not reflected in balance"
        print("✓ New transaction reflected in balances")
        
        # Test generating income statement
        result = skill.generate_income_statement()
        assert result['success'], f"Income statement generation failed: {result['error']}"
        print("✓ Income statement generated successfully")
        
        # Test generating balance sheet
        result = skill.generate_balance_sheet()
        assert result['success'], f"Balance sheet generation failed: {result['error']}"
        print("✓ Balance sheet generated successfully")
        
    print("\n✓ All tests passed!")


def test_error_handling():
    """Test error handling in the Beancount skill"""
    print("\nTesting error handling...")
    
    # Test with non-existent file
    config = {
        'beancount_file': '/nonexistent/path/file.bean',
        'beancount_directory': '/nonexistent/path'
    }
    
    try:
        skill = BeancountSkill(config)
        result = skill.check_file()
        # Should fail gracefully
        assert not result['success'], "Should have failed with non-existent file"
        print("✓ Handled non-existent file appropriately")
    except Exception as e:
        print(f"✓ Handled initialization error: {str(e)}")


if __name__ == "__main__":
    print("Running Beancount skill tests...\n")
    test_beancount_skill_initialization()
    test_error_handling()
    print("\nAll tests completed!")