import unittest
from BankAccount import BankAccount

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount(123)

    def test_initial_balance(self):
        self.assertEquals(self.account.balance, 0, msg="Initial balance should be 0")

    def test_deposit(self):
        self.account.deposit(100)
        self.assertEquals(self.account.balance, 100, msg="Deposit amount should increase the balance")

    def test_withdraw_sufficient_balance(self):
        self.account.deposit(100)
        result = self.account.withdraw(50)
        self.assertTrue(result, msg="Withdrawal should return True for sufficient balance")
        self.assertEquals(self.account.balance, 50, msg="Withdrawal amount should decrease the balance")

    def test_withdraw_insufficient_balance(self):
        self.account.deposit(100)
        result = self.account.withdraw(150)
        self.assertFalse(result, msg="Withdrawal should return False for insufficient balance")
        self.assertEquals(self.account.balance, 100, msg="Withdrawal amount shouldn't change for insufficient withdraw")


if __name__ == '__main__':
    unittest.main()