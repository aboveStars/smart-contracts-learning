// SPDX-License-Identifier: MIT
pragma solidity ^0.8.8;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    uint256 usdEntryFee;
    AggregatorV3Interface internal eth_usd_priceFeed;

    constructor(address _priceFeedAddress) {
        usdEntryFee = 50 * (1e18);
        eth_usd_priceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function enter() public {
        // $50 minimum but in ether
        players.push(payable(msg.sender));
    }

    function getEnteranceFee() public view returns (uint256) {
        // ?
        (, int256 price, , , ) = eth_usd_priceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * (1e10);
        uint256 costToEnter = (usdEntryFee * (1e18)) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public {}

    function endLottery() public {}
}
