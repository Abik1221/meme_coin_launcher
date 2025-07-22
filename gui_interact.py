import tkinter as tk
from tkinter import messagebox
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
INFURA_URL = os.getenv("INFURA_URL")
CHAIN_ID = int(os.getenv("CHAIN_ID"))

# Setup Web3 and Solidity compiler
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
assert web3.is_connected(), "Web3 is not connected"

install_solc("0.8.0")
set_solc_version("0.8.0")

# Solidity Contract
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

compiled_sol = compile_source(contract_source_code, output_values=["abi", "bin"])
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]
MemeCoin = web3.eth.contract(abi=abi, bytecode=bytecode)

# GUI Setup
app = tk.Tk()
app.title("MemeCoin Deployer")
app.geometry("400x400")

contract_address_var = tk.StringVar()
balance_label_var = tk.StringVar()


def deploy_contract():
    try:
        nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)
        tx = MemeCoin.constructor(1_000_000).build_transaction({
            'from': WALLET_ADDRESS,
            'chainId': CHAIN_ID,
            'gas': 3000000,
            'gasPrice': web3.to_wei('10', 'gwei'),
            'nonce': nonce
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        global contract_instance
        contract_instance = web3.eth.contract(address=receipt.contractAddress, abi=abi)
        contract_address_var.set(receipt.contractAddress)
        messagebox.showinfo("Success", f"Contract deployed at:\n{receipt.contractAddress}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def check_balance():
    try:
        if not contract_address_var.get():
            raise Exception("Contract not deployed yet.")
        balance = contract_instance.functions.balanceOf(WALLET_ADDRESS).call()
        balance_label_var.set(f"Your balance: {balance // (10 ** 18)} MEME")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def transfer_tokens():
    try:
        recipient = recipient_entry.get()
        amount = int(amount_entry.get()) * 10**18
        nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)

        tx = contract_instance.functions.transfer(recipient, amount).build_transaction({
            'from': WALLET_ADDRESS,
            'chainId': CHAIN_ID,
            'gas': 100000,
            'gasPrice': web3.to_wei('10', 'gwei'),
            'nonce': nonce
        })

        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)
        messagebox.showinfo("Success", f"Sent {amount // (10 ** 18)} MEME to {recipient}")
    except Exception as e:
        messagebox.showerror("Transfer Failed", str(e))


# UI Elements
tk.Button(app, text="🚀 Deploy Contract", command=deploy_contract, bg="green", fg="white").pack(pady=10)
tk.Label(app, text="Contract Address:").pack()
tk.Entry(app, textvariable=contract_address_var, width=50).pack()

tk.Button(app, text="📦 Check Balance", command=check_balance, bg="blue", fg="white").pack(pady=10)
tk.Label(app, textvariable=balance_label_var).pack()

tk.Label(app, text="Recipient Address").pack()
recipient_entry = tk.Entry(app, width=50)
recipient_entry.pack()

tk.Label(app, text="Amount (MEME)").pack()
amount_entry = tk.Entry(app, width=20)
amount_entry.pack()

tk.Button(app, text="💸 Transfer Tokens", command=transfer_tokens, bg="purple", fg="white").pack(pady=15)

app.mainloop()
