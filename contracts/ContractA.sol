// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ReentrancyGuard.sol";
import "./Ownable.sol";
import "../interfaces/IContractB.sol";


contract ContractA is ReentrancyGuard, Ownable{

    IContractB public contractB;

    function setAddress(address _contractBaddress) external onlyOwner {
        contractB = IContractB(_contractBaddress);
    }
    uint public variable=0;

    function setterFunction(uint _increasedNumber)  external nonReentrant onlyOwner {
        variable = variable + _increasedNumber;
    }

    function getterFunction() public view returns(uint){
        return variable;
    }

    modifier IsAdmin {
      require(contractB.isAdmin(msg.sender), "msg.sender not admin"  );
      _;
   }

}
