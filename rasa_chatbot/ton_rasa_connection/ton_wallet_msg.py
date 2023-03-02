from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.utils import bytes_to_b64str
from tonsdk.crypto import mnemonic_new
from tonsdk.contract.token.nft import NFTItem
from tonsdk.contract.token.ft import JettonWallet
from tonsdk.utils import Address, to_nano

wallet_workchain = 0
wallet_version = WalletVersionEnum.v3r2
wallet_mnemonics = mnemonic_new()

_mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(
    wallet_mnemonics, wallet_version, wallet_workchain)
query = wallet.create_init_external_message()
base64_boc = bytes_to_b64str(query["message"].to_boc(False))

print("""
Mnemonic: {}

Raw address: {}

Bounceable, url safe, user friendly address: {}

Base64boc to deploy the wallet: {}
""".format(wallet_mnemonics,
           wallet.address.to_string(),
           wallet.address.to_string(True, True, True),
           base64_boc))


############# 
"""
Transfer NFT & Jettons
by creating a transfer message from an owner wallet
"""

body = NFTItem().create_transfer_body(
    Address("New Owner Address")
)
query = wallet.create_transfer_message(
    "NFT Item Address",
    to_nano(0.05, "ton"),
    0,  # owner wallet seqno
    payload=body
)
nft_boc = bytes_to_b64str(query["message"].to_boc(False))

body = JettonWallet().create_transfer_body(
    Address("Destination address"),
    to_nano(40000, "ton")  # jettons amount
)
query = wallet.create_transfer_message(
    "Jetton Wallet Address",
    to_nano(0.05, "ton"),
    0,  # owner wallet seqno
    payload=body
)
jettons_boc = bytes_to_b64str(query["message"].to_boc(False))

print("""
Base64boc to transfer the NFT item: {}

Base64boc to transfer the jettons: {}
""".format(nft_boc, jettons_boc))
