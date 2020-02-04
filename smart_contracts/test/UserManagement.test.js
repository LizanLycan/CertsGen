// const Certifier = artifacts.require("Certifier");

// contract("Certifier", async accounts => {
//   it("should add Certifier", async () => {
//     let certifier = await Certifier.deployed();
//     await certifier.insertUser(
//       accounts[0],
//       web3.utils.asciiToHex("Lizandro Zerpa"),
//       web3.utils.asciiToHex("lizandroal.zerpa@gmail.com"),
//       web3.utils.asciiToHex("Cedula de identidad"),
//       24374215
//     );

//     let getCertifier = await certifier.getCertifier.call(accounts[0]);

//     console.log("===> Name: ", web3.utils.hexToAscii(getCertifier.name));
//     console.log("===> ID Number: ", getCertifier.id_number.toNumber());

//     assert.equal(web3.utils.hexToString(getCertifier.name), "Lizandro Zerpa");
//   });
// });
