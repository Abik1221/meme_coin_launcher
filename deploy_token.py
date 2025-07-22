import json
import os
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_source, install_solc

from solcx import install_solc, set_solc_version

install_solc('0.8.0')       # Ensures the version is installed
set_solc_version('0.8.0')   # Explicitly sets the version for compilation


# Load environment variables
load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
INFURA_URL = os.getenv("INFURA_URL")
CHAIN_ID = int(os.getenv("CHAIN_ID"))

# Connect to Infura
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
assert web3.is_connected(), "❌ Web3 is not connected"

# Install Solidity compiler version 0.8.0 (once)
install_solc('0.8.0')

# ERC-20 Contract in Solidity
contract_source_code = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MemeCoin {
    string public name = "MemeCoin";
    string public symbol = "MEME";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 initialSupply) {
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address to, uint256 value) public returns (bool success) {
        require(balanceOf[msg.sender] >= value, "Not enough balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
}
'''

# Compile the contract
compiled_sol = compile_source(contract_source_code, output_values=['abi', 'bin'])
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# Build contract instance
MemeCoin = web3.eth.contract(abi=abi, bytecode=bytecode)
nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)

# Build deployment transaction
initial_supply = 1_000_000
tx = MemeCoin.constructor(initial_supply).build_transaction({
    'from': WALLET_ADDRESS,
    'chainId': CHAIN_ID,
    'gas': 3000000,
    'gasPrice': web3.to_wei('10', 'gwei'),
    'nonce': nonce
})

# Sign the transaction
signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

# Send and confirm
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"⏳ Deploying contract... TX Hash: {web3.to_hex(tx_hash)}")

receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"✅ Contract deployed at: {receipt.contractAddress}")
