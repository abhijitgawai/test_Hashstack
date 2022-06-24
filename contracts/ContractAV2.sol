// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ReentrancyGuard.sol";
import "./Ownable.sol";


contract ContractAV2 is ReentrancyGuard, Ownable{
    uint public variable;

    function setterFunction(uint _increasedNumber)  external nonReentrant onlyOwner {
        variable = variable + _increasedNumber;
    }

    function getterFunction() public view returns(uint){
        return variable;
    }

    function setterFunctionBig(uint _increasedNumber)  external nonReentrant onlyOwner {
        variable = variable + _increasedNumber;
    }

}
