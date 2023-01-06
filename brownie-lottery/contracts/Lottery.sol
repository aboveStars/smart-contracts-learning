// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/KeeperCompatibleInterface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";

error EntranceFeeNotEnough();
error LotteryPrizeCanNotBeSent();
error NoPlayersFoundGivenAddress();
error ExitingPlayerFundFailure();

contract Lottery is KeeperCompatibleInterface, VRFConsumerBaseV2 {
    uint256 private i_interval;
    uint256 private s_firstTimeStamp;
    uint256 private i_fee;
    address payable[] private s_players;

    VRFCoordinatorV2Interface private immutable i_vrfCoor;
    bytes32 private immutable i_gasLane;
    uint64 private immutable i_subId;
    uint32 private immutable i_callBack;


    event upkeepPerformed();
    event NOT_ENOUGH_ENTRANCE_FEE(address indexed _poorAddress);
    event PRIZE_COULD_NOT_BE_SENT(address indexed _luckilyButCanNotSendPrize);
    event WINNER_SELECTED(address indexed _winnerAddress);

    constructor(
        uint256 _interval,
        uint256 _fee,
        address _vrfAddress,
        bytes32 _gasLane,
        uint64 _subId,
        uint32 _callBackGasLimit
    ) VRFConsumerBaseV2(_vrfAddress) {
        i_interval = _interval;
        i_fee = _fee;

        i_vrfCoor = VRFCoordinatorV2Interface(_vrfAddress);
        i_gasLane = _gasLane;
        i_subId = _subId;
        i_callBack = _callBackGasLimit;

        s_firstTimeStamp = block.timestamp;
    }

    function checkUpkeep(
        bytes memory
    ) external view override returns (bool upkeepNeeded, bytes memory) {
        bool interval_test = (block.timestamp - s_firstTimeStamp) > i_interval;
        bool playerLengthTest = s_players.length > 0;

        upkeepNeeded = interval_test && playerLengthTest;
    }

    function performUpkeep(bytes calldata) external override {
        i_vrfCoor.requestRandomWords(i_gasLane, i_subId, 3, i_callBack, 1);
        emit upkeepPerformed();
    }

    function fulfillRandomWords(uint256, uint256[] memory randomWords) internal override{
        s_firstTimeStamp = block.timestamp;
        uint256 luckiliyIndex = randomWords[0] % s_players.length;
        address payable recentWinner = s_players[luckiliyIndex]; // this area will be randomized...

        (bool success, ) = recentWinner.call{value: address(this).balance}("");
        if (!success) {
            emit PRIZE_COULD_NOT_BE_SENT(recentWinner);
            revert LotteryPrizeCanNotBeSent();
        }

        emit WINNER_SELECTED(recentWinner);
        s_players = new address payable[](0);     
    }

    function enterToLottery() public payable {
        if (msg.value < (i_fee)) {
            emit NOT_ENOUGH_ENTRANCE_FEE((msg.sender));
            revert EntranceFeeNotEnough();
        }
        s_players.push(payable(msg.sender));
    }

    function getDelta() public view returns (uint256) {
        return (block.timestamp - s_firstTimeStamp);
    }

    function getPlayers(uint256 index_of_needed_player) public view returns (address payable) {
        return (s_players[index_of_needed_player]);
    }

    function areKeepersPerform() public view returns (bool performNeeded) {
        bool interval_test = (block.timestamp - s_firstTimeStamp) > i_interval;
        bool playerLengthTest = s_players.length > 0;

        performNeeded = interval_test && playerLengthTest;
    }
}
