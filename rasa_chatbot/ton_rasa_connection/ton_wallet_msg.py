from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.utils import bytes_to_b64str
from tonsdk.crypto import mnemonic_new


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