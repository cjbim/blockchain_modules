// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "./@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "./@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721, ERC721URIStorage, Ownable,ERC721Enumerable {
    using SafeMath for uint256;

    constructor(string memory _name, string memory _symbol) ERC721(_name, _symbol) {}


    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }
    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721Enumerable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
    function _beforeTokenTransfer(address from, address to, uint256 tokenId, uint256 batchSize) internal override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }
 

        
    
    function mintWithTokenURI(address to, uint256 tokenId, string memory tokenURI) public payable returns (bool) {
        _mint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
        return true;
    }
    function multimint (address[] memory dests,uint256[] memory tokenIds, string[] memory tokenURIs) public payable returns (uint256) {
        uint256 i = 0;
        while (i < dests.length) {
        mintWithTokenURI(dests[i],tokenIds[i], tokenURIs[i]);
           i += 1;
        }
        return(i);
    }
}

