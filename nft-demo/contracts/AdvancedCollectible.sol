// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract AdvancedCollectible is ERC721URIStorage {
    uint256 public tokenCounter;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    mapping(uint256 => Breed) public tokenIDtoBreed;
    mapping(bytes32 => address) public requestIDtoSender;

    constructor() ERC721("Doggie", "Dog") {
        tokenCounter = 0;
    }

    function createCollectible() public returns (bytes32) {
        requestIDtoSender[0] = msg.sender;
    }

    function randomArea(string memory _tokenURI) public {
        Breed breed = Breed(2);
        uint256 newTokenID = tokenCounter;
        tokenIDtoBreed[newTokenID] = breed;
        address owner = requestIDtoSender[0];
        _safeMint(owner, newTokenID);
        setTokenURI(newTokenID, _tokenURI);
        tokenCounter += 1;
    }

    function setTokenURI(uint256 tokenID, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenID));
        _setTokenURI(tokenID, _tokenURI);
    }
}
