// solium-disable linebreak-style
pragma solidity >=0.5.0 <0.7.0;
import "./UserManagement.sol";

// The Authority Management CRUD following Library Standard from Hitchens
// Rob: https://medium.com/@robhitchens/solidity-crud-epilogue-e563e794fde

/**

@author LizanLycan (Lizandro A. Zerpa N.)
@title Authority Contract
@dev Parent Contract of all Authorities

 */
contract Authority {
    address owner;
    bytes32 name;
    uint256 id;
    uint256 public index;

    constructor(address _owner, bytes32 _name, uint256 _id, uint256 _index)
        public
    {
        owner = _owner;
        name = _name;
        id = _id;
        index = _index;
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    function getAuthority()
        public
        view
        returns (bytes32 _name, uint256 _id, uint256 _index)
    {
        return (name, id, index);
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
}

/**

@author LizanLycan (Lizandro A. Zerpa N.)
@title Acreditation Authority Contract
@dev Acreditation Authority Contract that handle owns Certifications Authorities

 */

contract AccreditationAuthority is Authority {
    CertificationAuthorityManager certificationAuthorityManager;

    constructor(address _owner, bytes32 _name, uint256 _id, uint256 _index)
        public
        Authority(_owner, _name, _id, _index)
    {
        certificationAuthorityManager = new CertificationAuthorityManager();
    }

    function getCertificationManager()
        public
        view
        returns (CertificationAuthorityManager)
    {
        return certificationAuthorityManager;
    }
}

/**

@author LizanLycan (Lizandro A. Zerpa N.)
@title Certification Authority Contract
@dev Certification Authority Contract that handle owns Certifiers

 */
contract CertificationAuthority is Authority {
    /**
        Certifiers Denpendency
     */
    CertifierManager certifierManager;
    /**
        Register Office
     */
    RecipientManager recipientManager;

    address accreditationAuthority;

    constructor(
        address _accreditationAuthority,
        address _owner,
        bytes32 _name,
        uint256 _id,
        uint256 _index
    ) public Authority(_owner, _name, _id, _index) {
        accreditationAuthority = _accreditationAuthority;
        certifierManager = new CertifierManager();
        recipientManager = new RecipientManager();
    }

    function getAccreditationAuthority()
        public
        view
        returns (address _accreditationAuthority)
    {
        return accreditationAuthority;
    }

    function getCertifierManager() public view returns (CertifierManager) {
        return certifierManager;
    }

    function getRecipientManager() public view returns (RecipientManager) {
        return recipientManager;
    }
}

/**

@author LizanLycan (Lizandro A. Zerpa N.)
@title Acreditation Authority Manager Contract
@dev Acreditation Authority Manager Contract that handle CRUD for Acreditation Authority Instances

 */

contract AccreditationAuthorityManager {
    struct AccreditationAuthorityStruct {
        AccreditationAuthority accreditationAuthority;
        uint256 index;
    }

    mapping(address => AccreditationAuthorityStruct) private accreditationAuthorities;
    address[] private accreditationAuthorityIndex;

    event LogNewAccreditationAuthority(address indexed owner, uint256 index);
    event LogUpdateAccreditationAuthority(address indexed owner, uint256 index);
    event LogDeleteAccreditationAuthority(address indexed owner, uint256 index);

    function isAccreditationAuthority(address owner)
        public
        view
        returns (bool isIndeed)
    {
        if (accreditationAuthorityIndex.length == 0) return false;

        return (accreditationAuthorityIndex[accreditationAuthorities[owner]
            .index] ==
            owner);
    }

    function insertAccreditationAuthority(
        address owner,
        bytes32 name,
        uint256 id
    ) public returns (uint256 index) {
        if (isAccreditationAuthority(owner))
            revert("Acreditation Authority already exist");

        accreditationAuthorityIndex.push(owner);
        uint256 _index = (accreditationAuthorityIndex.length - 1);

        accreditationAuthorities[owner]
            .accreditationAuthority = new AccreditationAuthority(
            owner,
            name,
            id,
            _index
        );
        accreditationAuthorities[owner].index = _index;

        return accreditationAuthorityIndex.length - 1;
    }

    function deleteAccreditationAuthority(address owner)
        public
        returns (uint256 index)
    {
        if (!isAccreditationAuthority(owner))
            revert("AccreditationAuthority does not exist");

        uint256 rowToDelete = accreditationAuthorities[owner].index;
        address keyToMove = accreditationAuthorityIndex[accreditationAuthorityIndex
            .length -
            1];

        accreditationAuthorityIndex[rowToDelete] = keyToMove;
        accreditationAuthorities[keyToMove].accreditationAuthority.setIndex(
            rowToDelete
        );
        accreditationAuthorities[keyToMove].index = rowToDelete;

        accreditationAuthorityIndex.pop();

        emit LogDeleteAccreditationAuthority(owner, rowToDelete);
        emit LogUpdateAccreditationAuthority(keyToMove, rowToDelete);

        return rowToDelete;
    }

    function getAccreditationAuthority(address owner)
        public
        view
        returns (AccreditationAuthority accreditationAuthority)
    {
        if (!isAccreditationAuthority(owner))
            revert("AccreditationAuthority does not exist");

        return accreditationAuthorities[owner].accreditationAuthority;
    }

    function getAccreditationAuthorityCount()
        public
        view
        returns (uint256 count)
    {
        return accreditationAuthorityIndex.length;
    }

    function getAccreditationAuthorityAtIndex(uint256 index)
        public
        view
        returns (address owner)
    {
        return accreditationAuthorityIndex[index];
    }
}

/**

@author LizanLycan (Lizandro A. Zerpa N.)
@title Certification Authority Manager Contract
@dev Certification Authority Manager Contract that handle CRUD for Certification Authority Instances

 */
contract CertificationAuthorityManager {
    struct CertificationAuthorityStruct {
        CertificationAuthority certificationAuthority;
        uint256 index;
    }

    mapping(address => CertificationAuthorityStruct) private certificationAuthorities;
    address[] private certificationAuthorityIndex;

    event LogNewCertificationAuthority(address indexed owner, uint256 index);
    event LogUpdateCertificationAuthority(address indexed owner, uint256 index);
    event LogDeleteCertificationAuthority(address indexed owner, uint256 index);

    function isCertificationAuthority(address owner)
        public
        view
        returns (bool isIndeed)
    {
        if (certificationAuthorityIndex.length == 0) return false;

        return (certificationAuthorityIndex[certificationAuthorities[owner]
            .index] ==
            owner);
    }

    function insertCertificationAuthority(
        address accreditationAuthority,
        address owner,
        bytes32 name,
        uint256 id
    ) public returns (uint256 index) {
        if (isCertificationAuthority(owner))
            revert("Certification Authority already exist");

        certificationAuthorityIndex.push(owner);
        uint256 _index = certificationAuthorityIndex.length - 1;
        certificationAuthorities[owner]
            .certificationAuthority = new CertificationAuthority(
            accreditationAuthority,
            owner,
            name,
            id,
            _index
        );
        certificationAuthorities[owner].index = _index;

        emit LogNewCertificationAuthority(
            owner,
            certificationAuthorities[owner].certificationAuthority.getIndex()
        );

        return certificationAuthorityIndex.length - 1;
    }

    function deleteCertificationAuthority(address owner)
        public
        returns (uint256 index)
    {
        if (!isCertificationAuthority(owner))
            revert("CertificationAuthority does not exist");

        uint256 rowToDelete = certificationAuthorities[owner].index;
        address keyToMove = certificationAuthorityIndex[certificationAuthorityIndex
            .length -
            1];

        certificationAuthorityIndex[rowToDelete] = keyToMove;
        certificationAuthorities[keyToMove].certificationAuthority.setIndex(
            rowToDelete
        );
        certificationAuthorities[keyToMove].index = rowToDelete;

        certificationAuthorityIndex.pop();

        emit LogDeleteCertificationAuthority(owner, rowToDelete);
        emit LogUpdateCertificationAuthority(keyToMove, rowToDelete);

        return rowToDelete;
    }

    function getCertificationAuthority(address owner)
        public
        view
        returns (CertificationAuthority certificationAuthority)
    {
        if (!isCertificationAuthority(owner))
            revert("CertificationAuthority does not exist");

        return certificationAuthorities[owner].certificationAuthority;
    }

    function getAllCertificationAuthorities()
        public
        view
        returns (address[] memory)
    {
        return certificationAuthorityIndex;
    }

    function getCertificationAuthorityCount()
        public
        view
        returns (uint256 count)
    {
        return certificationAuthorityIndex.length;
    }

    function getCertificationAuthorityAtIndex(uint256 index)
        public
        view
        returns (address owner)
    {
        return certificationAuthorityIndex[index];
    }
}
