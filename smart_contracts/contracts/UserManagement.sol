// solium-disable linebreak-style
pragma solidity >=0.5.0 <0.7.0;

import "./SignatureManagement.sol";
// The User Management CRUD following Library Standard from Hitchens Rob: https://medium.com/@robhitchens/solidity-crud-epilogue-e563e794fde
contract User {
    address private owner;
    bytes32 private name;
    bytes32 private email;
    bytes32 private id;
    uint256 private id_number;
    uint256 private index;

    constructor(
        address _owner,
        bytes32 _name,
        bytes32 _email,
        bytes32 _id,
        uint256 _id_number,
        uint256 _index
    ) public {
        owner = _owner;
        name = _name;
        email = _email;
        id = _id;
        id_number = _id_number;
        index = _index;
    }

    function getUser()
        public
        view
        returns (
            address _owner,
            bytes32 _name,
            bytes32 _email,
            bytes32 _id,
            uint256 _id_number,
            uint256 _index
        )
    {
        return (owner, name, email, id, id_number, index);
    }

    function getIndex() public view returns (uint256 _index) {
        return index;
    }

    function setIndex(uint256 __index) public returns (uint256 _index) {
        index = __index;
        return index;
    }

    function setName(bytes32 _name) public returns (uint256 _index) {
        name = _name;
        return index;
    }

    function setEmail(bytes32 _email) public returns (uint256 _index) {
        email = _email;
        return index;
    }

    function setId(bytes32 _id) public returns (uint256 _index) {
        id = _id;
        return index;
    }

    function setIdNumber(uint256 _id_number) public returns (uint256 _index) {
        id_number = _id_number;
        return index;
    }
}

contract Recipient is User {
    CertificateManager private certificates;
    address certificationAuthority;

    constructor(
        address _certificationAuthority,
        address _owner,
        bytes32 _name,
        bytes32 _email,
        bytes32 _id,
        uint256 _id_number,
        uint256 _index
    ) public User(_owner, _name, _email, _id, _id_number, _index) {
        certificates = new CertificateManager();
    }

    function getCertificateManager() public view returns (CertificateManager) {
        return certificates;
    }

    function getCertificationAuthority() public view returns (address) {
        return certificationAuthority;
    }
}

contract Certifier is User {
    address certificationAuthority;

    constructor(
        address _certificationAuthority,
        address _owner,
        bytes32 _name,
        bytes32 _email,
        bytes32 _id,
        uint256 _id_number,
        uint256 _index
    ) public User(_owner, _name, _email, _id, _id_number, _index) {
        certificationAuthority = _certificationAuthority;
    }

    function getCertificationAuthority() public view returns (address) {
        return certificationAuthority;
    }
}

contract RecipientManager {
    struct RecipientStruct {
        Recipient recipient;
        uint256 index;
    }

    mapping(address => RecipientStruct) private recipients;
    address[] private recipientIndex;

    event LogNewRecipient(address indexed owner, uint256 index);
    event LogUpdateRecipient(address indexed owner, uint256 index);
    event LogDeleteRecipient(address indexed owner, uint256 index);

    /**
    @param owner Primary Key of the Recipient
    */
    function isRecipient(address owner) public view returns (bool isIndeed) {
        if (recipientIndex.length == 0) return false;

        return (recipientIndex[recipients[owner].index] == owner);
    }

    function insertRecipient(
        address owner,
        bytes32 name,
        bytes32 email,
        bytes32 id,
        uint256 id_number
    ) public returns (uint256 index) {
        if (isRecipient(owner)) revert("Recipient already exist");

        recipientIndex.push(owner);

        uint256 _index = recipientIndex.length - 1;

        recipients[owner].recipient = new Recipient(
            owner,
            name,
            email,
            id,
            id_number,
            _index
        );
        recipients[owner].index = _index;

        emit LogNewRecipient(owner, recipients[owner].index);

        return recipientIndex.length - 1;
    }

    function deleteRecipient(address owner) public returns (uint256 index) {
        if (!isRecipient(owner)) revert("Recipient does not exist");

        uint256 rowToDelete = recipients[owner].index;
        address keyToMove = recipientIndex[recipientIndex.length - 1];

        recipientIndex[rowToDelete] = keyToMove;
        recipients[keyToMove].recipient.setIndex(rowToDelete);
        recipients[keyToMove].index = rowToDelete;

        recipientIndex.pop();

        emit LogDeleteRecipient(owner, rowToDelete);
        emit LogUpdateRecipient(keyToMove, rowToDelete);

        return rowToDelete;
    }

    function getRecipient(address owner)
        public
        view
        returns (Recipient recipient)
    {
        if (!isRecipient(owner)) revert("Recipient does not exist");

        return recipients[owner].recipient;
    }

    function getAllRecipient() public view returns (address[] memory) {
        return recipientIndex;
    }

    function getRecipientCount() public view returns (uint256 count) {
        return recipientIndex.length;
    }

    function getRecipientAtIndex(uint256 index)
        public
        view
        returns (address owner)
    {
        return recipientIndex[index];
    }
}

contract CertifierManager {
    struct CertifierStruct {
        Certifier certifier;
        uint256 index;
    }
    mapping(address => CertifierStruct) private certifiers;
    address[] private certifierIndex;

    event LogNewCertifier(address indexed owner, uint256 index);
    event LogUpdateCertifier(address indexed owner, uint256 index);
    event LogDeleteCertifier(address indexed owner, uint256 index);

    /**
    @param owner Primary Key of the Certifier
    */
    function isCertifier(address owner) public view returns (bool isIndeed) {
        if (certifierIndex.length == 0) return false;

        return (certifierIndex[certifiers[owner].index] == owner);
    }

    function insertCertifier(
        address certificationAuthority,
        address owner,
        bytes32 name,
        bytes32 email,
        bytes32 id,
        uint256 id_number
    ) public returns (uint256 index) {
        if (isCertifier(owner)) revert("Certifier already exist");

        certifierIndex.push(owner);

        uint256 _index = certifierIndex.length - 1;

        certifiers[owner].certifier = new Certifier(
            certificationAuthority,
            owner,
            name,
            email,
            id,
            id_number,
            _index
        );
        certifiers[owner].index = _index;

        emit LogNewCertifier(owner, certifiers[owner].index);

        return certifierIndex.length - 1;
    }

    function deleteCertifier(address owner) public returns (uint256 index) {
        if (!isCertifier(owner)) revert("Certifier does not exist");

        uint256 rowToDelete = certifiers[owner].index;
        address keyToMove = certifierIndex[certifierIndex.length - 1];

        certifierIndex[rowToDelete] = keyToMove;
        certifiers[keyToMove].certifier.setIndex(rowToDelete);
        certifiers[keyToMove].index = rowToDelete;

        certifierIndex.pop();

        emit LogDeleteCertifier(owner, rowToDelete);
        emit LogUpdateCertifier(keyToMove, rowToDelete);

        return rowToDelete;
    }

    function getCertifier(address owner)
        public
        view
        returns (Certifier certifier)
    {
        if (!isCertifier(owner)) revert("Certifier does not exist");

        return certifiers[owner].certifier;
    }

    function getAllCertifiers() public view returns (address[] memory) {
        return certifierIndex;
    }

    function getCertifierCount() public view returns (uint256 count) {
        return certifierIndex.length;
    }

    function getCertifierAtIndex(uint256 index)
        public
        view
        returns (address owner)
    {
        return certifierIndex[index];
    }
}
