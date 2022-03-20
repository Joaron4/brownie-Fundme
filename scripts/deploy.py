from brownie import FundMe, MockV3Aggregator, config, network
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    local_blockchain_enviroments,
)


def deploy_fund_me():
    account = get_account()
    # Necesitamos el priceFeed address para el contrato -> 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e (rinkeby chainlink)
    if network.show_active() not in local_blockchain_enviroments:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
