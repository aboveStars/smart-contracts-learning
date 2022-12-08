// SPDX-License-Identifier: MIT
pragma solidity ^0.8.8;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public recentWinner;
    uint256 usdEntryFee;
    AggregatorV3Interface internal eth_usd_priceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;
    uint256 public randomness;

    uint256 public fee;
    bytes32 public keyhash;

    //event RequestedRandomness(bytes32 requestId);

    // We actullay put 2 constructer ın here First is ours, second is from VRFConsumer...
    //With its rights VRF also needes parameters. So we give it. (-->First --> Second)
    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (1e18);
        eth_usd_priceFeed = AggregatorV3Interface(_priceFeedAddress);

        lottery_state = LOTTERY_STATE.CLOSED; // for algorithm

        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // if lottery is open
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "No Active Lottery Found to Enter"
        );

        // $50 minimum but in ether
        require(msg.value >= getEntranceFee());

        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = eth_usd_priceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * (1e10);
        uint256 costToEnter = (usdEntryFee * (1e18)) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            " Already a lottery is open "
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // Dirty and vulnerable Random Mechanism UNSAFE ! BECASUE ALL THINGS IN BOTTOM IS PREDICTABLE
        /*
        uint256 winnerIndex = uint256(
            keccak256(
                abi.encodePacked(
                    nonce,
                    msg.sender,
                    block.difficulty,
                    block.timestamp
                )
            )
        ) % players.length;
        */

        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;

        // REAL RANDOMNESS !!!

        bytes32 requestId = requestRandomness(keyhash, fee);
        //emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Lottery isn't Finished"
        );
        require(_randomness > 0, "random not found !");

        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];

        recentWinner.transfer(address(this).balance); // payment

        //reset
        players = new address payable[](0); // Zero stands for size of new array.

        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
