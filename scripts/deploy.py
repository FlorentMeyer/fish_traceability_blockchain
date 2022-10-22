from brownie import PRC, accounts


def deploy_PRC():
    admin = accounts[0]
    return PRC.deploy({"from": admin})


def main():
    prc = deploy_PRC()
