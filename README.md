# MemeCoin Generator 🔥🪙

This project is a GUI-based desktop application that allows users to easily **generate and deploy their own Meme Coins (ERC-20 tokens)** to the Ethereum blockchain using MetaMask, Infura, and Web3.

---

## ✨ Features

- Generate and deploy ERC-20 tokens with custom initial supply
- Simple GUI using Python's `tkinter`
- Interacts with MetaMask wallet (via `.env`)
- Uses Infura for connecting to Ethereum network
- Fully written in Python

---

## 📁 Project Structure

```
meme-coin-generator/
│
├── .env                # Environment variables (MetaMask keys, Infura URL)
├── deploy.py           # Deploys the MemeCoin ERC-20 contract
├── gui_interact.py     # GUI interface using tkinter
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/meme-coin-generator.git
   cd meme-coin-generator
   ```

2. **Set up a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # On macOS/Linux: source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔐 Environment Variables (.env)

Create a `.env` file in the root directory with the following contents:

```
PRIVATE_KEY=your_metamask_private_key
WALLET_ADDRESS=your_public_wallet_address
INFURA_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
CHAIN_ID=1  # For Mainnet. Use 5 for Goerli testnet, 11155111 for Sepolia, etc.
```

> ⚠️ **Never expose your private key in public repos!**

---

## 🚀 Running the App

Once dependencies are installed and `.env` is set:

```bash
python gui_interact.py
```

The GUI will launch. You can:

- Set the token supply
- Deploy the MemeCoin contract
- View the transaction hash and deployed contract address

---

## 🛠️ Powered By

- [Web3.py](https://web3py.readthedocs.io/)
- [Infura](https://infura.io/)
- [MetaMask](https://metamask.io/)
- [Python](https://www.python.org/) + [tkinter](https://docs.python.org/3/library/tkinter.html)