// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./SimpleStorage.sol";

// we can directly INHERIT other contracts to use its functions. --> IS + [NEEDED CONTRACT]
contract StorageFactory is SimpleStorage{

    SimpleStorage[] public simpleStorageArray; // to follow crated contracts

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage); // to follow crated contracts
    }

    function sfStore(uint256 _contractIndex, uint256 _number) public {
        // ABI
        // Address 
        // These are needed for interacting with contracts.

        SimpleStorage(address(simpleStorageArray[_contractIndex])).store(_number);

        /* THIS CODE CAN BE REFACTORED AS ABOVE
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_contractIndex]));
        simpleStorage.store(_number);
        */

    }

    function sfGet(uint256 _contractIndex) public view returns (uint256) {

        return SimpleStorage(address(simpleStorageArray[_contractIndex])).retrieve();

        /* THIS CODE CAN BE REFACTORED AS ABOVE
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_contractIndex]));
        return simpleStorage.retrieve();
        */
    }
}
