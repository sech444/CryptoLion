import ecdsa
import bitcoin

def inscribe_transaction(private_key, satoshi_ordinal, inscription):
  """
  Inscribes the given inscription to the given satoshi ordinal.

  Args:
    private_key: The private key of the Bitcoin address that will be used to sign the transaction.
    satoshi_ordinal: The satoshi ordinal to be inscribed.
    inscription: The inscription to be attached to the satoshi ordinal.

  Returns:
    The serialized Bitcoin transaction.
  """

  # Create a Bitcoin transaction.
  tx = bitcoin.Transaction()

  # Add an input to the transaction.
  tx.add_input(bitcoin.OutPoint(satoshi_ordinal, 0))

  # Create a signature for the transaction.
  signature = ecdsa.sign(tx.serialize_without_witness(), private_key)

  # Add a witness to the transaction.
  tx.add_witness(bitcoin.Script([signature]))

  # Add an output to the transaction.
  tx.add_output(bitcoin.Amount(0), bitcoin.Script([inscription]))

  # Serialize the transaction.
  return tx.serialize()

if __name__ == "__main__":
  # Get the private key.
  private_key = ecdsa.SigningKey.from_secret_exponent(b"my_secret_exponent")

  # Get the satoshi ordinal to be inscribed.
  satoshi_ordinal = 1234567890

  # Get the inscription to be attached to the satoshi ordinal.
  inscription = "This is an inscription."

  # Inscribe the transaction.
  transaction = inscribe_transaction(private_key, satoshi_ordinal, inscription)

  # Print the serialized transaction.
  print(transaction)