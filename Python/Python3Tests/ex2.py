from BankAccount import BankAccount
import pytest

@pytest.fixture
def account():
    return BankAccount(123)

def test_initial_balance(account):
    assert account.balance == 0, "Initial balance should be 0"

def test_deposit(account):
    account.deposit(100)
    assert account.balance == 100, "deposit amount should increase the balance"

def test_withdraw_sufficient_balance(account):
    account.deposit(100)
    result = account.withdraw(50)
    assert result is True, "Withdrawal should return True for sufficient balance"
    assert account.balance == 50, "Withdrawal amount should decrease the balance"

def test_withdraw_insufficient_balance(account):
    account.deposit(100)
    result = account.withdraw(150)
    assert result is False, "Withdrawal should return False for insufficient balance"
    assert account.balance == 100, "Withdrawal amount shouldn't change for insufficient withdraw"



if __name__ == '__main__':
    pytest.main()