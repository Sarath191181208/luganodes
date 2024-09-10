# Ethereum Deposit Tracker

## Overview

The Ethereum Deposit Tracker is a Python-based application designed to monitor and record ETH deposits on the Beacon Deposit Contract. The application leverages Web3 to interact with the Ethereum blockchain and SQLite for local data storage.

## Features

- Track ETH deposits on the Beacon Deposit Contract.
- Store deposit information in a local SQLite database.
- Utilize async tasks for efficient processing.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Sarath191181208/luganodes/
   cd luganodes
   ```

2. **Install Dependencies**

   Ensure you have `pipenv` installed. If not, you can install it via pip:

   ```bash
   pip install pipenv
   ```

   Install the required packages using the lock file:

   ```bash
   pipenv install --ignore-pipfile
   ```

3. **Configuration**

   The project requires a `.env` file for configuration. For the purposes of this assignment, the `.env` file is exposed. Ensure you place the `.env` file in the root directory of the project with the following environment variables:
   Also, ensure that the SQLite database file (`database.db`) is present in the root directory or will be created by the application.

## Usage

1. **Initialize the Database**

   The database will be initialized automatically when you run the application.

2. **Run the Application**

   To start the application, use the following command:

   ```bash
   pipenv run python app.py
   ```

   This will execute the main script which tracks deposits and saves them to the database.

## Code Overview

- `connection.py`: Contains functions to send requests to the Ethereum RPC and handle responses.
- `db.py`: Includes functions for database initialization and inserting deposit records.
- `config.py`: Holds configuration variables such as the contract address.
- `models.py`: Defines the data models used in the application.

## Acknowledgments

- Web3.py for interacting with the Ethereum blockchain.
- SQLite for lightweight database management.

```
