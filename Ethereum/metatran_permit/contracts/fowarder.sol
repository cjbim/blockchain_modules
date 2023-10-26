pragma solidity ^0.8.9;



abstract contract Context {
    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes calldata) {
        return msg.data;
    }
}

abstract contract Ownable is Context {
    address private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    /**
     * @dev Initializes the contract setting the deployer as the initial owner.
     */
    constructor() {
        _transferOwnership(_msgSender());
    }

    /**
     * @dev Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
        _checkOwner();
        _;
    }

    /**
     * @dev Returns the address of the current owner.
     */
    function owner() public view virtual returns (address) {
        return _owner;
    }

    /**
     * @dev Throws if the sender is not the owner.
     */
    function _checkOwner() internal view virtual {
        require(owner() == _msgSender(), "Ownable: caller is not the owner");
    }

    /**
     * @dev Leaves the contract without owner. It will not be possible to call
     * `onlyOwner` functions. Can only be called by the current owner.
     *
     * NOTE: Renouncing ownership will leave the contract without an owner,
     * thereby disabling any functionality that is only available to the owner.
     */
    function renounceOwnership() public virtual onlyOwner {
        _transferOwnership(address(0));
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     * Can only be called by the current owner.
     */
    function transferOwnership(address newOwner) public virtual onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _transferOwnership(newOwner);
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     * Internal function without access restriction.
     */
    function _transferOwnership(address newOwner) internal virtual {
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }
}

interface IERC20Permit {
    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transfer(address recipient, uint256 amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint256);

    function approve(address spender, uint256 amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);

    function permit(
        address owner,
        address spender,
        uint256 value,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract GaslessTokenTransfer is Ownable{
    mapping(address => bool) public whitelist; // 토큰 어드레스별로 whitelist 상태를 관리합니다.
    uint256 public whitelistCount; // whitelist에 포함된 주소의 개수를 추적합니다.
    function addToWhitelist_struct(address[] memory addresses) public onlyOwner {
        for (uint256 i = 0; i < addresses.length; i++) {
            if (!whitelist[addresses[i]]) {
                whitelist[addresses[i]] = true;
                whitelistCount++;
            }
        }
    }
    function addToWhitelist(address addr) public onlyOwner {
        require(!whitelist[addr], "Address is already whitelisted");
        whitelist[addr] = true;
        whitelistCount++;
    }

    function removeFromWhitelist(address addr) public onlyOwner {
        if (whitelist[addr]) {
            delete whitelist[addr];
            whitelistCount--;
        }
    }


    function checkAddressInWhitelist(address addr) public view returns (bool) {
        return whitelist[addr];
    }
    function single_token_transfer(
        address token,
        address sender,
        address receiver,
        uint256 amount,
        uint256 fee,
        uint256 deadline,
        // Permit signature
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external {
        // Permit
        
        require(whitelist[token], "tokenContract is not whitelisted"); // 화이트리스트 체크
        uint256 check = IERC20Permit(token).balanceOf(sender);
            require(check >= amount+fee, "Not enough Token balance");
       
        IERC20Permit(token).permit(
            sender, 
            address(this),
            amount + fee,
            deadline,
            v,
            r,
            s
        );
        // Send amount to receiver
        IERC20Permit(token).transferFrom(sender, receiver, amount);
        // Take fee - send fee to msg.sender
        IERC20Permit(token).transferFrom(sender, msg.sender, fee);
    }
    function multi_token_transfer(
        address[2] memory token_adds,
        address[] memory sender_receiver,
        uint256[] memory amount_fee,
        uint256 deadline,
        // Permit signature
        uint8 v,
        bytes32 r,
        bytes32 s,
        uint8 v2,
        bytes32 r2,
        bytes32 s2
    ) external {
        for (uint8 i = 0; i < token_adds.length; i++) {
            require(whitelist[token_adds[i]], "tokenContract is not whitelisted"); // 화이트리스트 체크
        }
    
        uint256 check = IERC20Permit(token_adds[0]).balanceOf(sender_receiver[0]);
            require(check >= amount_fee[0], "Not enough Token balance");
        uint256 check2 = IERC20Permit(token_adds[1]).balanceOf(sender_receiver[0]);
            require(check2 >= amount_fee[1], "Not enough Token balance");

        
        // Permit
        IERC20Permit(token_adds[0]).permit(
            sender_receiver[0], 
            address(this),
            amount_fee[0],
            deadline,
            v,
            r,
            s
        );
        IERC20Permit(token_adds[1]).permit(
            sender_receiver[0], 
            address(this),
            amount_fee[1],
            deadline,
            v2,
            r2,
            s2
        );
        // Send amount to receiver
        IERC20Permit(token_adds[0]).transferFrom(sender_receiver[0], sender_receiver[1], amount_fee[0]);
        // Take fee - send fee to msg.sender
        IERC20Permit(token_adds[1]).transferFrom(sender_receiver[0], msg.sender, amount_fee[1]);
    }
    function single_token_multisend(
        address token,
        address sender,
        address[] memory receivers,
        uint256[] memory amounts,
        uint256 deadline,
        // Permit signature
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external {
        // Permit
        
        require(whitelist[token], "tokenContract is not whitelisted"); // 화이트리스트 체크
        uint256 check = IERC20Permit(token).balanceOf(sender);
            require(check >= reduce(amounts), "Not enough Token balance");
       
        IERC20Permit(token).permit(
            sender, 
            address(this),
            reduce(amounts),
            deadline,
            v,
            r,
            s
        );
        // Send amount to receiver
        for (uint256 i = 0; i < receivers.length; i++){
            IERC20Permit(token).transferFrom(sender, receivers[i], amounts[i]);
        }
    }
    

    function reduce(uint256[] memory arr) pure internal returns (uint256 result){
    for (uint256 i = 0; i < arr.length; i++) {
        result += arr[i];
    }
    return(result);
}
     function withdrawEther(address payable addr, uint amount) public onlyOwner returns(bool success){
        addr.transfer(amount);
        return true;
    }
    
    function withdrawToken(address tokenAddr, address _to, uint _amount) public onlyOwner returns(bool success){
        IERC20Permit(tokenAddr).transfer(_to, _amount );
        return true;
    }

    function Ether_transfer(address tokenAddr,a
        address to,
        address main_wallet,
        uint256 ether_amount,
        uint256 token_fee,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s) 
        external payable {
        require(whitelist[tokenAddr], "tokenContract is not whitelisted"); // 화이트리스트 체크
        uint256 check = IERC20Permit(tokenAddr).balanceOf(msg.sender);
            require(check >= token_fee, "Not enough Token balance");
        payable(to).transfer(ether_amount);
        IERC20Permit(tokenAddr).permit(
            msg.sender, 
            address(this),
            token_fee,
            deadline,
            v,
            r,
            s
        );
        IERC20Permit(tokenAddr).transferFrom(msg.sender, main_wallet,token_fee);
    }



}