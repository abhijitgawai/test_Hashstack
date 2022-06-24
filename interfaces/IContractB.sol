// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IContractB {
    function isAdmin(address _admin)  external view returns (bool);
}
