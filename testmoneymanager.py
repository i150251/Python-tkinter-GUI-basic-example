import unittest

from moneymanager import MoneyManager

class TestMoneyManager(unittest.TestCase):

    def setUp(self):
        # Money Manager Object and passing balance
        self.user = MoneyManager()     
        self.user.balance = 1000.0

    def test_legal_deposit_works(self):
        # Code to test that depsositing money using the account's
        self.user.deposit_funds( 3000.0 )    

    def test_illegal_deposit_raises_exception(self):
        # Code to test that depositing an illegal value 
        self.user.deposit_funds('adad')    
        

    def test_legal_entry(self):
        # code  to test that adding a new entry
        self.user.add_entry(2000,"Food")
        

    def test_illegal_entry_amount(self):
        # code to test that withdrawing an illegal amount 
        self.user.add_entry('G',"Food")

        
    def test_illegal_entry_type(self):
        # code to test that adding an illegal entry type 
        self.user.add_entry(200,"PAY RESPECT")

    def test_insufficient_funds_entry(self):
        # code  to test that you can only spend funds which are available.
        self.user.add_entry(50000,"Food")

#Running tests
unittest.main()
