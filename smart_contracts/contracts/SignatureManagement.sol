// solium-disable linebreak-style
pragma solidity >=0.5.0 <0.7.0;

// Following CRUD standard from Hitchens Rob: https://medium.com/@robhitchens/solidity-crud-epilogue-e563e794fde

import "./ECDSA.sol";

/**
@title Signature Manager



 */
contract SignatureManager {
    struct Signature {
        address owner;
        bytes sig;
        bytes params;
        uint256 index;
    }

    mapping(uint256 => Signature) private signatures;
    uint256[] private signaturesIndex;

    event LogNewSignature(uint256 indexed, uint256);
    event LogUpdateSignature(uint256 indexed, uint256);
    event LogDeleteSignature(uint256 indexed, uint256);

    function checkSigner(
        address owner,
        uint256 nonce,
        bytes memory params,
        bytes memory sig
    ) public pure returns (bool) {
        // This recreates the params hash that was signed on the client.
        bytes32 hash = keccak256(abi.encodePacked(owner, nonce, params));
        bytes32 messageHash = ECDSA.prefixed(hash);

        address signer = ECDSA.recover(messageHash, sig);

        if (signer == owner) {
            return true;
        }

        return false;
    }

    function isSignature(uint256 nonce) public view returns (bool) {
        if (signaturesIndex.length == 0) return false;

        return (signaturesIndex[signatures[nonce].index] == nonce);
    }

    function insertSignature(
        address owner,
        uint256 nonce,
        bytes memory params,
        bytes memory sig
    ) public returns (uint256 index) {
        if (isSignature(nonce)) revert("Signature already exist");
        if (!checkSigner(owner, nonce, params, sig)) revert("Wrong signature");

        signaturesIndex.push(nonce);
        signatures[nonce].owner = owner;
        signatures[nonce].sig = sig;
        signatures[nonce].params = params;
        signatures[nonce].index = signaturesIndex.length - 1;

        emit LogNewSignature(nonce, index);
        return signaturesIndex.length - 1;
    }

    function deleteSignature(uint256 nonce) public returns (uint256 index) {
        if (!isSignature(nonce)) revert("Signature does not exist");

        uint256 rowToDelete = signatures[nonce].index;
        uint256 keyToMove = signaturesIndex[signaturesIndex.length - 1];
        signaturesIndex[rowToDelete] = keyToMove;
        signatures[keyToMove].index = rowToDelete;
        signaturesIndex.pop();

        emit LogDeleteSignature(nonce, rowToDelete);
        return rowToDelete;
    }

    function getSignature(uint256 nonce)
        public
        view
        returns (address owner, bytes memory params, bytes memory sig)
    {
        if (!isSignature(nonce)) revert("Signature does not exist");

        return (
            signatures[nonce].owner,
            signatures[nonce].params,
            signatures[nonce].sig
        );
    }

    function getAllSignatures() public view returns (uint256[] memory) {
        return signaturesIndex;
    }

    function getSignatureCount() public view returns (uint256 count) {
        return signaturesIndex.length;
    }

    function getSignatureAtIndex(uint256 index)
        public
        view
        returns (address owner, bytes memory params, bytes memory sig)
    {
        if (!isSignature(signaturesIndex[index]))
            revert("Signature does not exist");

        return (
            signatures[signaturesIndex[index]].owner,
            signatures[signaturesIndex[index]].params,
            signatures[signaturesIndex[index]].sig
        );
    }
}

/**
@title Certifier Dependency Manager



 */

contract CertifierDependencyManager {
    struct CertifierDependency {
        // mapped for `to`
        address from;
        uint256 index;
    }

    struct SignerNonce {
        // mapped for 'from'
        uint256 nonce;
        uint256 index;
    }
    //  Mapped for `to` element address
    mapping(address => CertifierDependency) certifierDependencies;
    address[] certifierDependenciesIndex;

    mapping(address => SignerNonce) signerNonce;
    address[] signerNonceIndex;

    /**
    CERTIFIER DEPENDENCIES
     */
    event LogNewCertifierDependency(address indexed, uint256);
    event LogUpdateCertifierDependency(address indexed, uint256);
    event LogDeleteCertifierDependency(address indexed, uint256);
    function isCertifierDependency(address _to) public view returns (bool) {
        if (certifierDependenciesIndex.length == 0) return false;

        return (certifierDependenciesIndex[certifierDependencies[_to].index] ==
            _to);
    }

    function insertCertifierDependency(address from, address _to)
        public
        returns (uint256 index)
    {
        if (isCertifierDependency(_to))
            revert("CertifierDependency already exist");

        certifierDependenciesIndex.push(_to);

        uint256 _index = certifierDependenciesIndex.length - 1;

        certifierDependencies[_to].from = from;
        certifierDependencies[_to].index = _index;

        emit LogNewCertifierDependency(_to, _index);
        return _index;
    }

    function deleteCertifierDependency(address to)
        public
        returns (uint256 index)
    {
        if (!isCertifierDependency(to))
            revert("CertifierDependency does not exist");

        uint256 rowToDelete = certifierDependencies[to].index;
        address keyToMove = certifierDependenciesIndex[certifierDependenciesIndex
            .length -
            1];
        certifierDependenciesIndex[rowToDelete] = keyToMove;
        certifierDependencies[keyToMove].index = rowToDelete;
        certifierDependenciesIndex.pop();

        emit LogDeleteCertifierDependency(to, rowToDelete);
        return rowToDelete;
    }

    function getCertifierDependency(address to)
        public
        view
        returns (address from, uint256 index)
    {
        if (!isCertifierDependency(to))
            revert("CertifierDependency does not exist");

        return (
            certifierDependencies[to].from,
            certifierDependencies[to].index
        );
    }

    function getAllCertifierDependencies()
        public
        view
        returns (address[] memory)
    {
        return certifierDependenciesIndex;
    }

    function getCertifierDependencyCount() public view returns (uint256 count) {
        return certifierDependenciesIndex.length;
    }

    function getCertifierDependencyAtIndex(uint256 _index)
        public
        view
        returns (address from, uint256 index)
    {
        return (
            certifierDependencies[certifierDependenciesIndex[_index]].from,
            certifierDependencies[certifierDependenciesIndex[_index]].index
        );
    }

    /**
    SIGNER NONCE
     */
    event LogNewSignerNonce(address indexed, uint256);
    event LogUpdateSignerNonce(address indexed, uint256);
    event LogDeleteSignerNonce(address indexed, uint256);
    function isSignerNonce(address _from) public view returns (bool) {
        if (signerNonceIndex.length == 0) return false;

        return (signerNonceIndex[signerNonce[_from].index] == _from);
    }

    function insertSignerNonce(address _from, uint256 nonce)
        public
        returns (uint256 index)
    {
        if (isSignerNonce(_from)) revert("SignerNonce already exist");

        signerNonceIndex.push(_from);
        signerNonce[_from].nonce = nonce;
        signerNonce[_from].index = signerNonceIndex.length - 1;

        emit LogNewSignerNonce(_from, signerNonceIndex.length - 1);
        return signerNonceIndex.length - 1;
    }

    function deleteSignerNonce(address from) public returns (uint256 index) {
        if (!isSignerNonce(from)) revert("SignerNonce does not exist");

        uint256 rowToDelete = signerNonce[from].index;
        address keyToMove = signerNonceIndex[signerNonceIndex.length - 1];
        signerNonceIndex[rowToDelete] = keyToMove;
        signerNonce[keyToMove].index = rowToDelete;
        signerNonceIndex.pop();

        emit LogDeleteSignerNonce(from, rowToDelete);
        return rowToDelete;
    }

    function getAllSignerNonce() public view returns (address[] memory) {
        return signerNonceIndex;
    }

    function getSignerNonceCount() public view returns (uint256) {
        return signerNonceIndex.length;
    }
}

/**
@title Certificate


 */

contract Certificate {
    bytes32 public title;
    bytes32 public description;
    address private recipient;
    address private subscriberCertifier;
    address private certificationAuthority;
    uint256 private index;

    SignatureManager signatures;
    CertifierDependencyManager certifierDependencies;

    constructor(
        address _recipient,
        address _subscriberCertifier,
        address _certificationAuthority,
        bytes32 _title,
        bytes32 _description
    ) public {
        recipient = _recipient;
        subscriberCertifier = _subscriberCertifier;
        certificationAuthority = _certificationAuthority;
        title = _title;
        description = _description;

        signatures = new SignatureManager();
        certifierDependencies = new CertifierDependencyManager();
    }

    function getIndex() public view returns (uint256 _index) {
        return index;
    }

    function setIndex(uint256 _index) public returns (uint256) {
        index = _index;
        return index;
    }

    function getRecipient() public view returns (address) {
        return recipient;
    }

    function getSubscriberCertifier() public view returns (address) {
        return subscriberCertifier;
    }

    function getCertificationAuthority() public view returns (address) {
        return certificationAuthority;
    }

    function getSignatures() public view returns (SignatureManager) {
        return signatures;
    }

    function getCertifierDependencies()
        public
        view
        returns (CertifierDependencyManager)
    {
        return certifierDependencies;
    }

    function getInfo() public view returns (bytes32, bytes32) {
        return (title, description);
    }
}

/**
@title Certificate Manager


 */
contract CertificateManager {
    struct CertificateStruct {
        Certificate certificate;
        uint256 index;
    }

    mapping(address => CertificateStruct) private certificates;
    address[] private certificateIndex;

    event LogNewCertificate(address indexed certificateAddress, uint256 index);
    event LogUpdateCertificate(
        address indexed certificateAddress,
        uint256 index
    );
    event LogDeleteCertificate(
        address indexed certificateAddress,
        uint256 index
    );

    /**
    @param certificateAddress Primary Key of the Certificate
    */
    function isCertificate(address certificateAddress)
        public
        view
        returns (bool isIndeed)
    {
        if (certificateIndex.length == 0) return false;

        return (certificateIndex[certificates[certificateAddress].index] ==
            certificateAddress);
    }

    function insertCertificate(address certificateAddress)
        public
        returns (uint256 index)
    {
        if (isCertificate(certificateAddress))
            revert("Certificate already exist");

        certificateIndex.push(certificateAddress);

        uint256 _index = certificateIndex.length - 1;

        certificates[certificateAddress].certificate = Certificate(
            certificateAddress
        );
        certificates[certificateAddress].index = _index;

        emit LogNewCertificate(
            certificateAddress,
            certificates[certificateAddress].index
        );

        return certificateIndex.length - 1;
    }

    function deleteCertificate(address certificateAddress)
        public
        returns (uint256 index)
    {
        if (!isCertificate(certificateAddress))
            revert("Certificate does not exist");

        uint256 rowToDelete = certificates[certificateAddress].index;
        address keyToMove = certificateIndex[certificateIndex.length - 1];

        certificateIndex[rowToDelete] = keyToMove;
        certificates[keyToMove].certificate.setIndex(rowToDelete);
        certificates[keyToMove].index = rowToDelete;

        certificateIndex.pop();

        emit LogDeleteCertificate(certificateAddress, rowToDelete);
        emit LogUpdateCertificate(keyToMove, rowToDelete);

        return rowToDelete;
    }

    function getAllCertificates() public view returns (address[] memory) {
        return certificateIndex;
    }

    function getCertificateCount() public view returns (uint256 count) {
        return certificateIndex.length;
    }

    function getCertificateAtIndex(uint256 index)
        public
        view
        returns (address certificateAddress)
    {
        return certificateIndex[index];
    }
}
