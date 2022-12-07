// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; // needed source for Price Feeds

contract FundMe{

    address ETH_USD_ID = 0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e;
    address USD_ETH_ID = 0x614715d2Af89E6EC99A233818275142cE88d1Cfd;

    mapping(address => uint256) public addressToAmountFunded;

    address public owner;

    address[] funders;

    function fund() public payable  {
        // $50 checking:
        uint256 minAmount = 50 * (10**18);
        require(getConversionRate(msg.value) >= minAmount);

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    constructor() { // this code block exetuces immediately... after deploying
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner  {
        // Just owner to this contract
        // require(msg.sender == owner); THIS LINE OPTIMIZED WITH MODIFIER
        payable(msg.sender).transfer(address(this).balance);

        // resetting procedure starts

        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) 
        {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0); 

        // resetting procedure stops
    }

    function getVerison() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(ETH_USD_ID); 
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(ETH_USD_ID);
        (,int256 answer,,,)  = priceFeed.latestRoundData(); // this has 8 decimal. but we should make it 18 DIGIT.
        uint256 result = uint256(answer) * (10**10);
        return uint256(result);
    }

    function getConversionRate(uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice(); // 18 digit
        uint256 conversationResult = (ethAmount * ethPrice); // 18 digit (wei)
        uint256 conversationResultReadable = conversationResult/(10**18); // non-18 digit version
        return conversationResultReadable;
    }
}

// PRICE NOTES:

/*
 Directly Taking ETH/USD rate is = 109368000000
 Last 8 number in here is decimal part. So actual number is in above:
 1093,6800..00
 So we should do: 109368000000/10**8
*/

/*
 When donating all types(ether,gwei,wei) converted to wei.
 So when to compare, it is useful to consider this.
*/