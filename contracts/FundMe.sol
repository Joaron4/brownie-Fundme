// SPDX-License-Identifier: MIT

// simpre hay qeui compilar el cto con brownie compile
pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public AdsToMoneyFund;

    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        //$_us
        uint256 minUs = 2 * 10**18; //usd-wei
        require(
            getConversionRate(msg.value) >= minUs,
            "You need to send more ETH"
        ); //falla la transacción si son menos de 2 usd
        AdsToMoneyFund[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10**10);
    }

    //261943116353000000000
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethInUs = (ethPrice * ethAmount) / 10**18; //convertir en Wei
        return ethInUs;
        //1000000000 un Gwei
        //2619431163530 18 puestos decimales
        //0,000002619431163530 USD-ETH
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 0.5 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex]; //funders = array
            AdsToMoneyFund[funder] = 0;
        }
        funders = new address[](0);
    }
}
