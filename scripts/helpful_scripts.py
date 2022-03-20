from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

forked_local_enviroments = ["mainet-fork,mainet-fork-dev"]
local_blockchain_enviroments = ["development", "ganache-local"]

decimals = 8
start_price = 2 * 10**8


def get_account():
    if (
        network.show_active() in local_blockchain_enviroments
        or network.show_active() in forked_local_enviroments
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"the active network is {network.show_active()}")
    print("deploying mocks...")
    if len(MockV3Aggregator) <= 0:  # los contratos son arrays con los ctos desplegados
        mock_aggreagator = MockV3Aggregator.deploy(
            decimals, Web3.toWei(start_price, "ether"), {"from": get_account()}
        )  # valores cto (uint8 _decimals, int256 _initialAnswer)

    print("...Mock Deployed")
