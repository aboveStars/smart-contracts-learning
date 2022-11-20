// SPDX-License-Identifier: MIT
// yukardaki zorunlu...

pragma solidity ^0.6.0;

contract SimpleStorage{

    // This will get initialized from 0 !
    uint256 favoriteNumber; 

    // Struct Create
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    
    // Create a Person from Struct
    /*
    People public person = People({
        favoriteNumber : 2,
        name : "Patrick"
    });
    */

    // Making Person Array
    People[] public people;
    // making MAPPING (mapping is used for like Dictionary)
    mapping(string => uint256) public nameToFavoritenumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view, pure: these are JUST state viewers and can not make transactions. AND NOT CHANGE STATE OF CHAIN, so.
    // also public varibales have built-in state viewers.
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    // Making Function of adding person
    // when declaring string in fuctions like in bottom, we MUST use "MEMORY" or "STORAGE"...
    // .. because strings are just array.

    function addPerson(string memory _name, uint _favoriteNumber ) public {
        people.push(People(_favoriteNumber, _name)); // array stuff
        nameToFavoritenumber[_name] = _favoriteNumber; // mapping stuff
    }


    /* TYPES OF DATAS
    uint256 favoriteNumber = 5;
    bool favoriteBool = true;
    string favoriteString = "String";
    int256 favoriteInt = -5
    address favoriteAddress = 0x54D2C9AB8C19CCA0bA9A5F161B65AE7032179E6B;
    bytes32 favoriteBytes = "cat"
    */
}