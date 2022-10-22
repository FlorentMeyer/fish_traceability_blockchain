// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

// Transaction History Contract
contract THC {
    struct Transaction {
        address seller;
        address buyer;
        uint16 price;
        uint256 timestamp;
    }

    Transaction[] transactions;

    constructor() {}

    // This function is called by PRC (i.e. msg.sender == PRC's address),
    // therefore the buyer's address has to be passed as argument
    function addTransaction(
        address seller,
        address buyer,
        uint16 price
    ) public {
        Transaction memory transaction;

        transaction.seller = seller;
        transaction.buyer = buyer; // Cannot be msg.sender for reason above
        transaction.price = price;
        transaction.timestamp = block.timestamp;

        transactions.push(transaction);
    }

    function getHistory() public view returns (Transaction[] memory) {
        return transactions;
    }
}