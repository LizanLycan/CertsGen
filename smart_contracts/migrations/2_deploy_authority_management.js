let AccreditationAuthorityManager = artifacts.require(
  "AccreditationAuthorityManager"
);

module.exports = (deployer, helper, accounts) => {
  deployer.then(async () => {
    try {
      await deployer.deploy(AccreditationAuthorityManager);
    } catch (error) {
      console.error(error);
    }
  });
};
