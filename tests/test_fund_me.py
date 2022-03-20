from scripts.helpful_scripts import get_account, local_blockchain_enviroments
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

# comando apra iniciar las pruebas -> brownie test
def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.AdsToMoneyFund(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.AdsToMoneyFund(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in local_blockchain_enviroments:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()  # random account
    with pytest.raises(
        exceptions.VirtualMachineError
    ):  # decirle que si hay un revert pasa el test
        fund_me.withdraw({"from": bad_actor})
