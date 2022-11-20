// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; // needed source for Price Feeds

contract FundMe{

    address ETH_USD_ID = 0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e;

    mapping(address => uint256) public addressToAmountFunded;

    function fund() public payable  {
        // $1 minimum
        uint256 minimumUSD = 1 * (10**18);
        
        require(getConverationRate(msg.value)>minimumUSD, "You should spend more!");

        addressToAmountFunded[msg.sender] += msg.value;
    }

    function withdraw() public payable  {
        payable(msg.sender).transfer(address(this).balance);
    }

    function getVerison() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(ETH_USD_ID); 
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(ETH_USD_ID);
        (,int256 answer,,,)  = priceFeed.latestRoundData(); // this camos with 18 digit
        return uint256(answer * 10000000000); // multiply by 10 zeros
    }

    function getConverationRate(uint256 ethAmount) public view returns(uint256) { // THIS FUNCTION GIVES US WE NEED
        uint256 ethPrice = getPrice();
        uint256 totalAmountEtherInUSD = (ethPrice*ethAmount)/1000000000000000000; // adjusting ZEROS dividing 18 ZEROS
        return totalAmountEtherInUSD;
    }
}