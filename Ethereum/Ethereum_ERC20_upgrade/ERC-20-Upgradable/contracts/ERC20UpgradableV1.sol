// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20BurnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/draft-ERC20PermitUpgradeable.sol";

contract BARTS is Initializable, ERC20Upgradeable, ERC20BurnableUpgradeable, PausableUpgradeable, OwnableUpgradeable, ERC20PermitUpgradeable {
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address new_owner) initializer public {
        __ERC20_init("b'arts", "b'arts");
        __ERC20Burnable_init();
        __Pausable_init();
        __Ownable_init();
        __ERC20Permit_init("b'arts");
        transferOwnership(msg.sender);
        mint(new_owner, 100000000000 * 10**decimals());
        transferOwnership(new_owner);
    }


    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function _beforeTokenTransfer(address from, address to, uint256 amount)
        internal
        whenNotPaused
        override
    {
        super._beforeTokenTransfer(from, to, amount);
    }

    function burning(uint256 amount) public onlyOwner {
        _burn(msg.sender, amount);
    }

    function transferWithPermit(address owner, address spender, address recipient, uint256 value,uint256 fee, uint256 deadline, uint8 v, bytes32 r, bytes32 s) public {
       // permit 함수 호출
        permit(owner, spender, value + fee, deadline, v, r, s);

        // 토큰 전송
        transferFrom(owner, recipient, value); 
        transferFrom(owner, msg.sender, fee);
    }

    function multisend(address[] memory dests, uint256[] memory values) public returns (uint256) {
        uint256 i = 0;
        while (i < dests.length) {
           transfer(dests[i], values[i]);
           i += 1;
        }
        return(i);
    }


}