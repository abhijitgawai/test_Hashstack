#!/usr/bin/python3
from brownie import (
    ContractAV2,
    ContractA,
    ContractB
    # TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    network,
    Contract,
)
from scripts.helpful_scripts import get_account, upgrade, encode_function_data

def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")

    contractA = ContractA.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # Optional, deploy the ProxyAdmin and use that as the admin contract
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
    )

    box_encoded_initializer_function = encode_function_data()
    
    proxy = TransparentUpgradeableProxy.deploy(
        contractA.address,
        # account.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )

    contractA_v2 = ContractAV2.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # proxy = TransparentUpgradeableProxy[-1]
    proxy_admin = ProxyAdmin[-1]
    upgrade(account, proxy, contractA_v2, proxy_admin_contract=proxy_admin)
    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("ContractAV2", proxy.address, ContractAV2.abi)
    print(f"Starting value {proxy_box.getterFunction()}")
    proxy_box.decrement(10, {"from": account})
    print(f"Ending value {proxy_box.getterFunction()}")
