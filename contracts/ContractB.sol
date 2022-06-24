// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ReentrancyGuard.sol";
import "./Ownable.sol";
import "../interfaces/IContractB.sol";

contract ContractB is Ownable, IContractB {

    mapping (address => bool) public Admins;

    function AddAdmin(address _admin) external onlyOwner{ // Here onlyOwner is superAdmin
        Admins[_admin]=true;
    }

    function RemoveAdmin(address _admin) external onlyOwner{
        require(Admins[_admin]==true, "He was not previously admin");
        Admins[_admin]=false;
    }

    function transferAdminRole(address _admin) external onlyOwner{ // this removes msg.sender admin acess, and give to _admin
        require(Admins[msg.sender]==true, "He was not previously admin");
        Admins[msg.sender]=false;
        Admins[_admin]=true;
    }
    function isAdmin(address _admin) external view override returns (bool){
        return Admins[_admin];
    }
}
