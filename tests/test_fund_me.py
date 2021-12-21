from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest
from brownie import network, accounts, exceptions


def test_fund_and_withdraw():
    # testing fund
    account = get_account()
    fund_me = deploy_fund_me()
    # just incase we need a little more cash, add an extra 100
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"form": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    # testing withdraw
    tx2 = fund_me.withdraw({"form": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
