const AccreditationAuthorityManager = artifacts.require(
  "AccreditationAuthorityManager"
);
const CertificationAuthorityManager = artifacts.require(
  "CertificationAuthorityManager"
);
const AccreditationAuthority = artifacts.require("AccreditationAuthority");
const CertificationAuthority = artifacts.require("CertificationAuthority");

contract("AuthorityManager", async accounts => {
  it("should add Acreditation Authority", async () => {
    let accreditationAuthority = await AccreditationAuthorityManager.deployed();

    await accreditationAuthority.insertAccreditationAuthority(
      accounts[0],
      web3.utils.asciiToHex("OPSU"),
      1234509876
    );

    /**
     *
     * @summary Check New Acreditation Authority Added
     *
     */

    let newAAAddress = await accreditationAuthority.getAccreditationAuthority.call(
      accounts[0]
    );
    let newAAInstance = await AccreditationAuthority.at(newAAAddress);

    let newAAInfo = await newAAInstance.getAuthority();

    assert.equal(web3.utils.hexToString(newAAInfo._name), "OPSU");
  });

  it("should add Certification Authority in existing Acreditation Authority", async () => {
    let accreditationAuthority = await AccreditationAuthorityManager.deployed();

    let newAAAddress = await accreditationAuthority.getAccreditationAuthority.call(
      accounts[0]
    );
    let newAAInstance = await AccreditationAuthority.at(newAAAddress);

    /**
     *
     * @summary Check Certification Authority
     *
     */

    let certificationManagerAddress = await newAAInstance.getCertificationManager.call();
    let certificationManagerInstance = await CertificationAuthorityManager.at(
      certificationManagerAddress
    );

    await certificationManagerInstance.insertCertificationAuthority(
      newAAAddress,
      accounts[0],
      web3.utils.asciiToHex("Facultad de Ingenieria ULA"),
      24374215234
    );
    let certificationAuthorityAddress = await certificationManagerInstance.getCertificationAuthority.call(
      accounts[0]
    );
    let certificationAuthorityInstance = await CertificationAuthority.at(
      certificationAuthorityAddress
    );
    let certificationAuthorityInfo = await certificationAuthorityInstance.getAuthority.call();

    assert.equal(
      web3.utils.hexToString(certificationAuthorityInfo._name),
      "Facultad de Ingenieria ULA"
    );
  });

  it("should add another Acreditation Authority", async () => {
    let accreditationAuthority = await AccreditationAuthorityManager.deployed();

    await accreditationAuthority.insertAccreditationAuthority(
      accounts[1],
      web3.utils.asciiToHex("OPSU ULA"),
      1000006
    );
  });

  it("should delete first Acreditation Authority", async () => {
    let accreditationAuthority = await AccreditationAuthorityManager.deployed();

    await accreditationAuthority.deleteAccreditationAuthority(accounts[0]);

    let count = await accreditationAuthority.getAccreditationAuthorityCount();

    assert.equal(count.toNumber(), 1);

    let get_aa = await accreditationAuthority.getAccreditationAuthority.call(
      accounts[1]
    );
    let get_aa_instance = await AccreditationAuthority.at(get_aa);
    let a = await get_aa_instance.getAuthority();

    assert.equal(web3.utils.hexToString(a._name), "OPSU ULA");
  });
  //   it("can not add repeated Acreditation Authority", async () => {
  //     let accreditationAuthority = await AccreditationAuthorityManager.deployed();

  //     try {
  //       await accreditationAuthority.insertAccreditationAuthority(
  //         accounts[0],
  //         web3.utils.asciiToHex("OPSU"),
  //         1234509876
  //       );
  //     } catch (e) {
  //       assert.equal(e.reason, "Acreditation Authority already exist");
  //     }
  //   });

  //   it("should delete Acreditation Authority", async () => {
  //     let accreditationAuthority = await AccreditationAuthorityManager.deployed();

  //     await accreditationAuthority.deleteAccreditationAuthority(accounts[0]);

  //     try {
  //       await accreditationAuthority.getAccreditationAuthority(accounts[0]);
  //     } catch (e) {
  //       assert.equal(0, 0);
  //     }
  //   });
});
