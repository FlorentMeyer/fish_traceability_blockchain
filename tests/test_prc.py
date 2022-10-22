from brownie import PRC, accounts, exceptions
import pytest


pytest.admin = None
pytest.fisherman = None
pytest.manufacturer = None
pytest.consumer = None
pytest.fish001 = {}
pytest.fish002 = {}
pytest.prc = None


def test_deploy():
    pytest.admin = accounts[0].address
    pytest.fisherman = accounts[1].address
    pytest.manufacturer = accounts[2].address
    pytest.consumer = accounts[3].address
    pytest.fish001 = {
        "NFCTag": "fish001",
        "fisherman": pytest.fisherman,
        # 'ContractContainer' object has no attribute 'Location'
        # => structs must be passed as tuples
        "fishingLocation": (-56388, 67900),
        "species": "Atlantic cod",
        "length": 2000,
        "weight": 1500,
    }
    pytest.fish002 = {
        "NFCTag": "fish002",
        "fisherman": pytest.fisherman,
        # 'ContractContainer' object has no attribute 'Location'
        # => structs must be passed as tuples
        "fishingLocation": (45000, -12654),
        "species": "Red salmon",
        "length": 1600,
        "weight": 1270,
    }
    pytest.prc = PRC.deploy({"from": accounts[0]})
    assert pytest.prc.getAdmin() == pytest.admin


def test_add_fisherman():
    t = pytest.prc.addFisherman(pytest.fisherman, {"from": pytest.admin})
    # t.wait(1)  # Appearently, waiting for transactions to complete isn't required
    assert pytest.prc.isFisherman(pytest.fisherman)


def test_add_fishes():
    with pytest.raises(exceptions.VirtualMachineError):  # Called by admin => fail
        pytest.prc.addFish(
            *pytest.fish001.values(),
            {"from": pytest.admin},
        )

    checkable_attributes_getter = [0, 1, 3, 4, 5]
    checkable_attributes_fixture = [1, 2, 3, 4, 5]

    def test_add_fish(fish_fixture):
        pytest.prc.addFish(
            *fish_fixture.values(),
            {"from": pytest.fisherman},
        )
        get_fish = list(
            map(
                pytest.prc.getFish(fish_fixture["NFCTag"]).__getitem__,
                checkable_attributes_getter,
            )
        )
        get_fishing_info = list(
            map(
                pytest.prc.getFishingInfo(fish_fixture["NFCTag"]).__getitem__,
                checkable_attributes_getter,
            )
        )
        fish_expected = list(
            map(list(fish_fixture.values()).__getitem__, checkable_attributes_fixture)
        )
        assert get_fish == get_fishing_info == fish_expected

    test_add_fish(pytest.fish001)
    test_add_fish(pytest.fish002)


def test_add_THC_transactions():
    transaction1 = {
        "NFCTag": pytest.fish001["NFCTag"],
        "seller": pytest.fisherman,
        "price": 900,
    }
    pytest.prc.addTHCTransaction(*transaction1.values(), {"from": pytest.manufacturer})

    transaction2 = {
        "NFCTag": pytest.fish001["NFCTag"],
        "seller": pytest.manufacturer,
        "price": 1000,
    }
    pytest.prc.addTHCTransaction(*transaction2.values(), {"from": pytest.consumer})

    checkable_attributes_getter = [0, 1, 2]  # Timestamp excluded
    get_history = [
        list(
            map(
                transaction.__getitem__,
                checkable_attributes_getter,
            )
        )
        for transaction in pytest.prc.getFishOwnershipHistory(pytest.fish001["NFCTag"])
    ]
    history_expected = [
        [transaction1["seller"], pytest.manufacturer, transaction1["price"]],
        [transaction2["seller"], pytest.consumer, transaction2["price"]],
    ]
    assert get_history == history_expected

def test_get_freshness():
    freshness = pytest.prc.getFreshness(pytest.fish001["NFCTag"])
    assert freshness > 0

def test_remove_fisherman():
    pytest.prc.removeFisherman(pytest.fisherman, {"from": pytest.admin})
    assert not pytest.prc.isFisherman(pytest.fisherman)
