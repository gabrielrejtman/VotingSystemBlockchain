// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }

    mapping(uint256 => Candidate) public candidates;
    uint256 public candidatesCount;

    mapping(bytes32 => bool) public hasVoted;

    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner has permission");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function addCandidate(string memory _name) public onlyOwner {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    function vote(bytes32 voterHash, uint256 candidateId) public {
        require(!hasVoted[voterHash], "Already voted");
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate");

        hasVoted[voterHash] = true;
        candidates[candidateId].voteCount++;
    }

    function getCandidate(uint256 candidateId) public view returns (string memory, uint256) {
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate");
        Candidate memory c = candidates[candidateId];
        return (c.name, c.voteCount);
    }

    function getCandidateNames() public view returns (string[] memory) {
        string[] memory names = new string[](candidatesCount);
        for (uint256 i = 0; i < candidatesCount; i++) {
            names[i] = candidates[i + 1].name; // IDs começam em 1
        }
        return names;
    }
}
