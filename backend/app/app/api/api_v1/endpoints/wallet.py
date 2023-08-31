import os
import ecdsa
import hashlib
import codecs
import json

def generate_private_key():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    return private_key

def get_public_key(private_key):
    public_key = private_key.get_verifying_key().to_string()
    public_key_hex = codecs.encode(public_key, 'hex')
    return public_key_hex

def get_address(public_key_hex):
    address = hashlib.sha256(public_key_hex).hexdigest()[:40]
    return address

def sign_transaction(private_key, transaction):
    signature = private_key.sign(transaction.encode())
    return signature

# def encrypt_private_key(private_key, password):

#     encrypted_key = private_key.to_pem().decode('utf-8').encode('utf-8')

#     encrypted_key += b'\n' + password.encode()

#     return encrypted_key

def encrypt_private_key(private_key, password):
    encrypted_key = private_key.to_pem().decode('utf-8').encode('utf-8')
    encrypted_key = encrypted_key + b'\n' + password.encode()
    return encrypted_key

def decrypt_private_key(encrypted_key, password):
    pem, key_password = encrypted_key.split(b'\n', maxsplit=1)
    if key_password.decode() == password:
        private_key = ecdsa.SigningKey.from_pem(pem)
        return private_key
    else:
        return None

def store_private_key(encrypted_key):
    with open('wallet.pem', 'wb') as f:
        f.write(encrypted_key)

def load_private_key(password):
    with open('wallet.pem', 'rb') as f:
        encrypted_key = f.read()
    private_key = decrypt_private_key(encrypted_key, password)
    if private_key:
        return private_key
    else:
        return None

# generate private key
private_key = generate_private_key()


print('private_key')
print(private_key)

# get public key
public_key = get_public_key(private_key)

print(public_key)

# get address
address = get_address(public_key)

print(address)

# sign transaction
transaction = json.dumps({'to': address, 'value': 100})
signature = sign_transaction(private_key, transaction)

# encrypt private key
password = input("Enter password to encrypt private key: ")
encrypted_key = encrypt_private_key(private_key, password)

# store encrypted key
store_private_key(encrypted_key)

# load private key
private_key = load_private_key(password)