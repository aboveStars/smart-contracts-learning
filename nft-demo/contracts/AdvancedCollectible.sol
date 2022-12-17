// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract AdvancedCollectible is ERC721URIStorage {
    uint256 public tokenCounter;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD,
        RIZE
    }
    mapping(uint256 => Breed) public tokenIDtoBreed;

    // mapping(bytes32 => address) public requestIDtoSender;

    constructor() ERC721("Doggie", "Dog") {
        tokenCounter = 0;
    }

    function createCollectible() public {
        Breed breed = Breed(3);
        uint256 newTokenID = tokenCounter;

        tokenIDtoBreed[newTokenID] = breed;

        address owner = msg.sender;
        _safeMint(owner, newTokenID); // making web-page ...
        tokenCounter += 1;
    }

    function setTokenURI(uint256 tokenID, string memory _tokenURI) public {
        // fills web-page
        require(_isApprovedOrOwner(_msgSender(), tokenID));
        _setTokenURI(tokenID, _tokenURI);
    }
}
