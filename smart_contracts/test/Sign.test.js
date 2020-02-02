const SignatureManager = artifacts.require("SignatureManager");

contract("SignatureManager", async accounts => {
  it("should Sign the Owner!", async () => {
    let signatureManager = await SignatureManager.deployed();

    const nonce = await web3.eth.getTransactionCount(accounts[0]);
    var hash = web3.utils
      .soliditySha3(
        { t: "address", v: accounts[0] },
        { t: "uint256", v: nonce },
        { t: "bytes", v: web3.utils.asciiToHex("Mi message") }
      )
      .toString("hex");
    const sign = await web3.eth.sign(hash, accounts[0]);
    const isSigner = await signatureManager.checkSigner(
      accounts[0],
      nonce,
      web3.utils.asciiToHex("Mi message"),
      sign
    );

    assert.equal(isSigner, true);
  });

  it("add Sign", async () => {
    let signatureManager = await SignatureManager.deployed();

    const nonce = await web3.eth.getTransactionCount(accounts[0]);
    var hash = web3.utils
      .soliditySha3(
        { t: "address", v: accounts[0] },
        { t: "uint256", v: nonce },
        { t: "bytes", v: web3.utils.asciiToHex("Mi message") }
      )
      .toString("hex");
    const sign = await web3.eth.sign(hash, accounts[0]);
    await signatureManager.insertSignature(
      accounts[0],
      nonce,
      web3.utils.asciiToHex("Mi message"),
      sign
    );

    const signature = await signatureManager.getSignature(nonce);
    assert.equal(signature.sig, sign);

    let checked = await signatureManager.checkSigner(
      accounts[0],
      nonce,
      web3.utils.asciiToHex("Mi message"),
      sign
    );
    assert.equal(checked, true);
  });
});
