const ECDSA = artifacts.require("ECDSA");
const SignatureManager = artifacts.require("SignatureManager");

module.exports = function(deployer) {
  deployer.deploy(ECDSA);
  deployer.link(ECDSA, SignatureManager);
  deployer.deploy(SignatureManager);
};
