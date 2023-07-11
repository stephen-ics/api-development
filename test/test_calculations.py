import pytest
from app.calculations import add, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (5, 2, 7),
    (2, 52, 54)
])
def test_add(num1, num2, expected):
    print("goo")
    assert add(num1, num2) == expected

def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    bank_account.deposite(30)
    assert bank_account.balance == 80   

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 5) == 55
