"""
Beancount Skill for Clawdbot
Manages Beancount accounting files with transaction management, balance queries, and report generation
"""
import json
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional, Union


class BeancountSkill:
    """
    A skill for managing Beancount accounting files
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the Beancount skill
        
        Args:
            config: Configuration dictionary with beancount settings
        """
        self.config = config or {}
        self.beancount_file = self.config.get('beancount_file', 'main.bean')
        self.beancount_dir = self.config.get('beancount_directory', '.')
        
        # Ensure the beancount file path is absolute
        if not Path(self.beancount_file).is_absolute():
            self.beancount_file = Path(self.beancount_dir) / self.beancount_file
            
        # Validate that beancount tools are available
        self._validate_beancount_installation()
    
    def _validate_beancount_installation(self):
        """Validate that beancount tools are installed and accessible"""
        try:
            result = subprocess.run(['bean-check', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise Exception("Beancount installation not found or bean-check command failed")
        except FileNotFoundError:
            raise Exception("Beancount tools not found. Please install beancount: pip install beancount")
        except subprocess.TimeoutExpired:
            raise Exception("Beancount version check timed out")
    
    def _run_beancount_command(self, command: List[str], input_text: str = None) -> Dict:
        """
        Run a beancount command and return the result
        
        Args:
            command: List of command arguments
            input_text: Optional input text to pass to the command
            
        Returns:
            Dictionary with 'success', 'output', 'error', and 'returncode'
        """
        full_command = ['bean-' + command[0]] + command[1:]
        
        try:
            # Run the command with the beancount file as needed
            if command[0] in ['check', 'balance', 'print', 'extract', 'query']:
                # Insert the beancount file after the command name
                full_command = [full_command[0], str(self.beancount_file)] + full_command[1:]
            
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            proc_result = subprocess.run(
                full_command,
                input=input_text,
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )
            
            return {
                'success': proc_result.returncode == 0,
                'output': proc_result.stdout.strip(),
                'error': proc_result.stderr.strip(),
                'returncode': proc_result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': 'Command timed out',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Error running command: {str(e)}',
                'returncode': -1
            }
    
    def check_file(self) -> Dict:
        """
        Check the beancount file for syntax errors
        
        Returns:
            Result of the check operation
        """
        return self._run_beancount_command(['check'])
    
    def get_balance(self, account_pattern: str = None, commodity: str = None) -> Dict:
        """
        Get account balances
        
        Args:
            account_pattern: Pattern to match accounts (e.g., 'Assets:*', 'Expenses:Dining')
            commodity: Filter by specific commodity (e.g., 'USD', 'EUR')
            
        Returns:
            Balance information
        """
        cmd = ['balance']
        if commodity:
            cmd.extend(['--account', commodity])
        if account_pattern:
            cmd.append(account_pattern)
            
        return self._run_beancount_command(cmd)
    
    def get_balances_by_date(self, date: str, account_pattern: str = None) -> Dict:
        """
        Get account balances at a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
            account_pattern: Pattern to match accounts
            
        Returns:
            Balance information at the specified date
        """
        cmd = ['balance', '--date', date]
        if account_pattern:
            cmd.append(account_pattern)
            
        return self._run_beancount_command(cmd)
    
    def add_transaction(self, date: str, payee: str, narration: str, postings: List[Dict], 
                       tags: List[str] = None, links: List[str] = None) -> Dict:
        """
        Add a new transaction to the beancount file
        
        Args:
            date: Transaction date in YYYY-MM-DD format
            payee: Payee name
            narration: Transaction description
            postings: List of posting dictionaries with 'account' and 'amount' keys
            tags: Optional list of tags
            links: Optional list of links
            
        Returns:
            Result of the append operation
        """
        # Construct the transaction entry
        transaction_lines = []
        transaction_lines.append(f'{date} * "{payee}" "{narration}"')
        
        if tags:
            tag_str = ' '.join([f'#{tag}' for tag in tags])
            transaction_lines[0] += f' {tag_str}'
            
        if links:
            link_str = ' '.join([f'^{link}' for link in links])
            transaction_lines[0] += f' {link_str}'
        
        # Add postings
        for posting in postings:
            account = posting['account']
            amount = posting['amount']
            currency = posting.get('currency', '')
            
            if currency:
                posting_line = f'  {account}  {amount} {currency}'
            else:
                posting_line = f'  {account}  {amount}'
                
            # Add cost basis if provided
            cost = posting.get('cost')
            if cost:
                posting_line += f' {{{cost}}}'
                
            # Add price annotation if provided
            price = posting.get('price')
            if price:
                posting_line += f' @{price}'
                
            transaction_lines.append(posting_line)
        
        transaction_entry = '\n'.join(transaction_lines) + '\n'
        
        # Append to the beancount file
        try:
            with open(self.beancount_file, 'a', encoding='utf-8') as f:
                f.write('\n' + transaction_entry)
            
            return {
                'success': True,
                'output': f'Transaction added successfully to {self.beancount_file}',
                'error': '',
                'returncode': 0
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Failed to append transaction to file: {str(e)}',
                'returncode': -1
            }
    
    def add_price(self, date: str, currency: str, price: str, base_currency: str) -> Dict:
        """
        Add a price entry to the beancount file
        
        Args:
            date: Price date in YYYY-MM-DD format
            currency: Currency being priced
            price: Price value
            base_currency: Base currency for the price
            
        Returns:
            Result of the append operation
        """
        price_entry = f'{date} price {currency} {price} {base_currency}\n'
        
        try:
            with open(self.beancount_file, 'a', encoding='utf-8') as f:
                f.write('\n' + price_entry)
            
            return {
                'success': True,
                'output': f'Price entry added successfully to {self.beancount_file}',
                'error': '',
                'returncode': 0
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Failed to append price entry to file: {str(e)}',
                'returncode': -1
            }
    
    def generate_trial_balance(self) -> Dict:
        """
        Generate a trial balance report
        
        Returns:
            Trial balance information
        """
        return self._run_beancount_command(['balance'])
    
    def generate_income_statement(self) -> Dict:
        """
        Generate an income statement (profit & loss)
        
        Returns:
            Income statement information
        """
        return self._run_beancount_command(['balance', 'Expenses', 'Income'])
    
    def generate_balance_sheet(self) -> Dict:
        """
        Generate a balance sheet
        
        Returns:
            Balance sheet information
        """
        return self._run_beancount_command(['balance', 'Assets', 'Liabilities', 'Equity'])
    
    def query_transactions(self, query: str) -> Dict:
        """
        Execute a beancount query using bean-query
        
        Args:
            query: SQL-like query string
            
        Returns:
            Query results
        """
        # For bean-query, we need to pass the query as stdin
        return self._run_beancount_command(['query'], input_text=query)
    
    def extract_entries(self, source_file: str, account: str = None) -> Dict:
        """
        Extract entries from an external source file
        
        Args:
            source_file: Path to the source file (like CSV, PDF, etc.)
            account: Account to filter for (optional)
            
        Returns:
            Extracted entries
        """
        cmd = ['extract']
        if account:
            cmd.extend(['--account', account])
        cmd.append(source_file)
        
        return self._run_beancount_command(cmd)
    
    def print_entries(self, date_range: str = None) -> Dict:
        """
        Print entries from the beancount file
        
        Args:
            date_range: Date range in the format YYYY-MM-DD:YYYY-MM-DD
            
        Returns:
            Printed entries
        """
        cmd = ['print']
        if date_range:
            cmd.extend(['--date', date_range])
            
        return self._run_beancount_command(cmd)
    
    def get_account_information(self, account: str) -> Dict:
        """
        Get detailed information about a specific account
        
        Args:
            account: Account name to query
            
        Returns:
            Account information
        """
        # Use bean-query to get detailed account info
        query = f'SELECT * FROM postings WHERE account = "{account}" ORDER BY date DESC LIMIT 20;'
        return self.query_transactions(query)


# Global instance to maintain state during a session
beancount_skill_instance = None


def initialize(config: Dict = None):
    """
    Initialize the Beancount skill with configuration
    
    Args:
        config: Configuration dictionary
    """
    global beancount_skill_instance
    beancount_skill_instance = BeancountSkill(config)


def check_file() -> Dict:
    """Check the beancount file for syntax errors"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.check_file()


def get_balance(account_pattern: str = None, commodity: str = None) -> Dict:
    """Get account balances"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.get_balance(account_pattern, commodity)


def get_balances_by_date(date: str, account_pattern: str = None) -> Dict:
    """Get account balances at a specific date"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.get_balances_by_date(date, account_pattern)


def add_transaction(date: str, payee: str, narration: str, postings: List[Dict], 
                   tags: List[str] = None, links: List[str] = None) -> Dict:
    """Add a new transaction to the beancount file"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.add_transaction(date, payee, narration, postings, tags, links)


def add_price(date: str, currency: str, price: str, base_currency: str) -> Dict:
    """Add a price entry to the beancount file"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.add_price(date, currency, price, base_currency)


def generate_trial_balance() -> Dict:
    """Generate a trial balance report"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.generate_trial_balance()


def generate_income_statement() -> Dict:
    """Generate an income statement (profit & loss)"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.generate_income_statement()


def generate_balance_sheet() -> Dict:
    """Generate a balance sheet"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.generate_balance_sheet()


def query_transactions(query: str) -> Dict:
    """Execute a beancount query using bean-query"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.query_transactions(query)


def extract_entries(source_file: str, account: str = None) -> Dict:
    """Extract entries from an external source file"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.extract_entries(source_file, account)


def print_entries(date_range: str = None) -> Dict:
    """Print entries from the beancount file"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.print_entries(date_range)


def get_account_information(account: str) -> Dict:
    """Get detailed information about a specific account"""
    if not beancount_skill_instance:
        return {'success': False, 'error': 'Beancount skill not initialized'}
    return beancount_skill_instance.get_account_information(account)