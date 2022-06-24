import pytest
from brownie import (
    ContractA,
    ContractAV2,
    ContractB,
    # TransparentUpgradeableProxy,
    # ProxyAdmin,
    Contract,
    network,
    config,
    exceptions,
    accounts
)
from scripts.helpful_scripts import get_account, encode_function_data, upgrade


def test_proxy_upgrades():
    account = get_account()
    contractA = ContractA.deploy(
        {"from": account},
    )
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
    )
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        contractA.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    contractA_V2 = ContractAV2.deploy(
        {"from": account},
    )
    proxy_box = Contract.from_abi("ContractAV2", proxy.address, ContractAV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.setterFunctionBig(100, {"from": account})
    upgrade(account, proxy, contractA_V2, proxy_admin_contract=proxy_admin)
    assert proxy_box.getterFunction() == 0
    

    # Tried changing owner, but it didnt worked
    # owner = accounts.add('6e971f11a6dae43651aec77c2d9661389972fb290ba84b07bcdbc0a41cb9e52c')
    # contractA_V2.transferOwnership(accounts.add("6e971f11a6dae43651aec77c2d9661389972fb290ba84b07bcdbc0a41cb9e52c"), {"from":account})
    proxy_box.setterFunctionBig(100, {"from": account})
    assert proxy_box.getterFunction() == 100

def test_testing():
    account = get_account()

    contractB = ContractB.deploy(
        {"from": account},
    )

    admin1 = accounts.add('6e971f11a6dae43651aec77c2d9661389972fb290ba84b07bcdbc0a41cb9e52c')
    contractB.AddAdmin(admin1, {"from": account})

    contractA = ContractA.deploy(
        {"from": account},
    )

    contractB = ContractB.deploy(
        {"from": account},
    )

    assert contractA.getterFunction() == 0


    contractA.setterFunction(10, {"from": account})

    assert contractA.getterFunction() == 10

    assert contractA.owner() == account.address # admin of contractA

    # Transfering ownership of ContractA to accounts[2] from ganache-cli
    contractA.transferOwnership(accounts[2], {"from":account})

    # Ownership of ContractA changed
    assert contractA.owner() == accounts[2]

    # adding 81
    contractA.setterFunction(81, {"from": accounts[2]})

    assert contractA.getterFunction() == 91


