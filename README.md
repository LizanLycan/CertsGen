# CertsGen

It is a platform built in Django with Web3.py interface for a DApp that is responsible for guaranteeing the generation of digital certificates for all kinds of "value" assets.

It allows to register the authorities required to carry out a certification process: accrediting authorities, certification authorities, certifiers and recipients, so that the recipients can request the required certificates and be able to share them with the assurance that they are signed and endorsed by the respective authority.

# Installation Instructions

Git installation is required if you need to use the following command:

```bash
git clone https://github.com/LizanLycan/CertsGen.git
```

## Smart contract environment installation

### Prerequisites

1.  You will need [Metamask](https://metamask.io/) plugin for Chrome.
2.  Make sure you have [Node.js](https://nodejs.org/en/) installed (recommend Node v11.15.0)

### Installation

1.  Install [Truffle Framework](http://truffleframework.com/) and [Ganache CLI](http://truffleframework.com/ganache/) globally. If you prefer, the graphical version of Ganache works as well.

    ```bash
    npm install -g truffle
    npm install -g ganache-cli
    ```

    <strong>Note</strong>: The graphical version of Ganache seems to be more stable on Mac whereas Ganache CLI works fine on Ubuntu.

2.  Run the development blockchain.

    ```bash
    // no blocktime specified so transaction will be mined instantly
    ganache-cli -m "(phrase seed given by Metamask)"
    ```

3.  Check the balance given in Metamask plugin for the `localhost:8545` network.

4.  Install all dependencies inside environment:

    ```bash
    cd ./smart_contracts/
    npm install
    ```

5.  Migrate contracts to development Blockchain
    ```bash
    // inside smart_contracts folder
    truffle migrate --reset --compile-all --network development
    ```

## Django API REST environment

### Prerequisites

1. Install [python](https://www.python.org/downloads/).
2. Install [`pip`](https://pip.pypa.io/en/stable/installing/).
3. Make sure you have an activated [`venv`](https://docs.python.org/3/tutorial/venv.html) in the root.

### Installation

1. Run the following commands with an activated `venv`:

   ```bash
   pip install -r ./requirements.txt
   python manage.py migrate

   // For /admin page of the django application
   pyhon manage.py createsuperuser

   // Important! This guarantees communication with the newly deployed smart contracts to the test network.
   python manage.py collectstatic
   python manage.py runserver 127.0.0.1:8080
   ```

2. Its recommended run the application in port `8080`, because you can use optionally [Etherparty Explorer](https://github.com/etherparty/explorer).

3. Config Postman and see the example API calls:

   - Make sure you have installed Postman app.
   - Import the collection given in the root project `CertsGen.postman_collection.json`
   - Import the environment given in the root project `certs_gen.postman_environment.json`
