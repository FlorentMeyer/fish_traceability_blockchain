// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "./thc.sol";

// Product Registration Contract
contract PRC {
    struct Location {
        int32 longitude;
        int32 latitude;
    }

    struct Fish {
        // Fishing conditions
        address fisherman;
        Location fishingLocation;
        uint256 fishingTimestamp;
        // Morphology of the fish
        string species;
        int16 length;
        int16 weight;
        // For ownership tracking
        address thc;
    }

    address admin; // The deployer of the PRC contract

    mapping(string => Fish) fishes; // NFCTag => Fish
    mapping(address => bool) public isFisherman;

    modifier onlyAdmin() {
        require(msg.sender == admin);
        _;
    }

    modifier onlyFisherman() {
        require(isFisherman[msg.sender] == true);
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function getAdmin() public view returns (address _admin) {
        _admin = admin;
    }

    function addFisherman(address fisherman) public onlyAdmin {
        isFisherman[fisherman] = true;
    }

    function removeFisherman(address fisherman) public onlyAdmin {
        isFisherman[fisherman] = false;
    }

    function addFish(
        string memory NFCTag,
        address fisherman,
        Location memory fishingLocation,
        string memory species,
        int16 length,
        int16 weight
    ) public onlyFisherman {
        Fish memory fish;
        THC thc = new THC();

        fish.fisherman = fisherman;
        fish.fishingLocation = fishingLocation;
        fish.fishingTimestamp = block.timestamp;
        fish.species = species;
        fish.length = length;
        fish.weight = weight;

        fish.thc = address(thc);

        fishes[NFCTag] = fish;
    }

    function getFish(string memory NFCTag)
        public
        view
        returns (Fish memory fish)
    {
        fish = fishes[NFCTag];
    }

    function getFishingInfo(string memory NFCTag)
        public
        view
        returns (
            address fisherman,
            Location memory fishingLocation,
            uint256 fishingTimestamp,
            string memory species,
            int16 length,
            int16 weight
        )
    {
        Fish memory fish = fishes[NFCTag];

        fisherman = fish.fisherman;
        fishingLocation = fish.fishingLocation;
        fishingTimestamp = fish.fishingTimestamp;
        species = fish.species;
        length = fish.length;
        weight = fish.weight;
    }

    function getFreshness(string memory NFCTag)
        public
        view
        returns (uint256 freshness)
    {
        freshness = block.timestamp - fishes[NFCTag].fishingTimestamp;
    }

    // Should be restricted to onlySuppliers
    function addTHCTransaction(
        string memory NFCTag,
        address seller,
        uint16 price
    ) public {
        THC(fishes[NFCTag].thc).addTransaction(seller, msg.sender, price);
    }

    function getFishOwnershipHistory(string memory NFCTag)
        public
        view
        returns (THC.Transaction[] memory history)
    {
        history = THC(fishes[NFCTag].thc).getHistory();
    }
}
