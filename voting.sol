// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Voting {
    struct Candidate {
        string name;
        uint votes;
    }

    mapping(uint => Candidate) public Candidates;
    uint public totalCandidates;

    mapping(string => bool) public cpfAlreadyVoted;

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier ownerOnly() {
        require(msg.sender == owner, "Only the owner can do this.");
        _;
    }

    function addCandidate(string memory _name) public ownerOnly {
        Candidates[totalCandidates] = Candidate(_name, 0);
        totalCandidates++;
    }

    function vote(uint _idCandidate, string memory _cpf) public {
        require(_idCandidate < totalCandidates, "Invalid candidate.");
        require(!cpfAlreadyVoted[_cpf], "CPF already voted.");

        Candidates[_idCandidate].votes++;
        cpfAlreadyVoted[_cpf] = true;
    }

    function get_votes(uint _idCandidate) public view returns (uint) {
        require(_idCandidate < totalCandidates, "Invalid candidate.");
        return Candidates[_idCandidate].votes;
    }

    function list_candidates() public view returns (Candidate[] memory) {
        Candidate[] memory candidate_list = new Candidate[](totalCandidates);
        for (uint i = 0; i < totalCandidates; i++) {
            candidate_list[i] = Candidates[i];
        }
        return candidate_list;
    }
}