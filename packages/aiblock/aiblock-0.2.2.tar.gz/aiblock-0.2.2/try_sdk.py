"""Example script demonstrating AIBlock SDK usage."""

import logging
import json
from typing import Dict, Any
from aiblock.wallet import Wallet
from aiblock.blockchain import BlockchainClient
from aiblock.config import get_config
from aiblock.interfaces import IResult, IErrorInternal, IMasterKeyEncrypted, IKeypair
from aiblock.constants import ITEM_DEFAULT
from aiblock.key_handler import decrypt_keypair

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Change to DEBUG level
logger = logging.getLogger(__name__)

def handle_result(result: IResult[Any], operation: str) -> None:
    """Handle an IResult, printing success or error information.
    
    Args:
        result: The IResult to handle
        operation: Description of the operation for logging
    """
    if result.is_err:
        logger.error(f"{operation} failed: {result.error} - {result.error_message}")
    else:
        logger.info(f"{operation} successful: {result.get_ok()}")

def main() -> None:
    """Main function demonstrating AIBlock SDK usage."""
    try:
        # Get configuration from environment variables
        config_result = get_config()
        if config_result.is_err:
            logger.error(f"Configuration error: {config_result.error_message}")
            return
            
        config = config_result.get_ok()
        config['valenceHost'] = 'https://valence.aiblock.ch'
        logger.debug(f"Using config: {config}")
        
        # Initialize wallet
        wallet = Wallet()
        seed_phrase = wallet.generate_seed_phrase()
        init_result = wallet.from_seed(seed_phrase, config)
        if init_result.is_err:
            logger.error(f"Failed to initialize wallet: {init_result.error_message}")
            return
            
        logger.info("Wallet initialized successfully")
        logger.info(f"Generated seed phrase: {seed_phrase}")
        
        # Generate a keypair
        keypair_result = wallet.generate_keypair()
        if keypair_result.is_err:
            logger.error(f"Failed to generate keypair: {keypair_result.error_message}")
            return
            
        keypair = keypair_result.get_ok()
        logger.info(f"Generated address: {keypair.address}")
        logger.info(f"Public key: {keypair.public_key.hex() if isinstance(keypair.public_key, bytes) else keypair.public_key}")
        
        # Initialize blockchain client
        blockchain = BlockchainClient(
            storage_host=config.get('storageHost'),
            mempool_host=config.get('mempoolHost')
        )
        
        # Get latest block
        handle_result(
            blockchain.get_latest_block(),
            "Get latest block"
        )
        
        # Get total supply
        handle_result(
            blockchain.get_total_supply(),
            "Get total supply"
        )
        
        # Get issued supply
        handle_result(
            blockchain.get_issued_supply(),
            "Get issued supply"
        )
        
        # Test with regular keypair
        metadata = {
            "name": "Test Item",
            "description": "A test item created with the AIBlock SDK",
            "image": "https://example.com/image.png",
            "attributes": [
                {"trait_type": "Rarity", "value": "Common"},
                {"trait_type": "Type", "value": "Test"}
            ]
        }
        
        logger.info("Testing create_item_asset with regular keypair...")
        logger.debug(f"Using metadata: {metadata}")
        logger.debug(f"Using keypair: address={keypair.address}, public_key={keypair.public_key.hex()}")
        
        # Call with individual key components
        item_result = wallet.create_item_asset(
            secret_key=keypair.secret_key,
            public_key=keypair.public_key,
            version=keypair.version,
            amount=ITEM_DEFAULT,
            default_genesis_hash=True,
            metadata=metadata
        )
        handle_result(item_result, "Create item asset (regular keypair)")

        # Test with encrypted keypair
        logger.info("Testing create_item_asset with encrypted keypair...")
        # First encrypt the keypair
        if not wallet.passphrase_key:
            logger.error("No passphrase key available for encryption")
            return

        logger.debug(f"Using passphrase key: {wallet.passphrase_key.hex()}")
        encrypt_result = wallet.encrypt_keypair(keypair, wallet.passphrase_key)
        if encrypt_result.is_err:
            logger.error(f"Failed to encrypt keypair: {encrypt_result.error_message}")
            return

        encrypted_keypair = encrypt_result.get_ok()
        logger.info("Successfully encrypted keypair")
        logger.debug(f"Encrypted keypair: {encrypted_keypair}")

        # Decrypt the keypair manually before calling
        decrypt_result = decrypt_keypair(encrypted_keypair, wallet.passphrase_key)
        if decrypt_result.is_err:
             logger.error(f"Failed to decrypt keypair before calling create_item_asset: {decrypt_result.error_message}")
             return
        decrypted_kp_for_call = decrypt_result.get_ok()
        logger.debug("Successfully decrypted keypair for API call.")

        # Now try to create item asset with decrypted key components
        item_result_encrypted = wallet.create_item_asset(
            secret_key=decrypted_kp_for_call.secret_key,
            public_key=decrypted_kp_for_call.public_key,
            version=decrypted_kp_for_call.version,
            amount=ITEM_DEFAULT,
            default_genesis_hash=True,
            metadata=metadata
        )
        handle_result(item_result_encrypted, "Create item asset (encrypted keypair)")

        # Test balance fetching
        balance_result = wallet.fetch_balance([keypair.address])
        if balance_result.is_err:
            logger.error(f"Failed to get balance: {balance_result.error_message}")
            return
            
        balance = balance_result.get_ok()
        logger.info(f"Balance: {balance}")
            
        # Example transaction
        tx_result = wallet.create_transactions(
            destination_address=keypair.address,  # Send to self for testing
            amount=100
        )
        handle_result(tx_result, "Create transaction")

        # --- 2WayPayment Example Usage ---
        logger.info("\n--- 2WayPayment Example Usage ---")
        # Prepare dummy data
        payment_address = keypair.address
        sending_asset = {"Token": 100}
        receiving_asset = {"Item": {"amount": 1}}
        all_keypairs = [keypair]
        # Encrypt the keypair for receive_address
        encrypted_keypair_result = wallet.encrypt_keypair(keypair, wallet.passphrase_key)
        if encrypted_keypair_result.is_ok:
            receive_address = encrypted_keypair_result.get_ok()
        else:
            logger.error("Failed to encrypt keypair for 2WayPayment example")
            return

        # Make 2-way payment
        result = wallet.make_2way_payment(payment_address, sending_asset, receiving_asset, all_keypairs, receive_address)
        handle_result(result, "Make 2WayPayment")
        if result.is_ok:
            druid = result.get_ok().get('druid', 'druid123')
            encrypted_tx = result.get_ok().get('encryptedTx', 'encrypted_data')
        else:
            druid = 'druid123'
            encrypted_tx = 'encrypted_data'

        # Fetch pending 2-way payments
        result = wallet.fetch_pending_2way_payments(all_keypairs, [encrypted_tx])
        handle_result(result, "Fetch Pending 2WayPayments")
        if result.is_ok:
            pending = result.get_ok().get('pending', {druid: {'details': 'pending details'}})
        else:
            pending = {druid: {'details': 'pending details'}}

        # Accept 2-way payment
        result = wallet.accept_2way_payment(druid, pending, all_keypairs)
        handle_result(result, "Accept 2WayPayment")

        # Reject 2-way payment
        result = wallet.reject_2way_payment(druid, pending, all_keypairs)
        handle_result(result, "Reject 2WayPayment")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == '__main__':
    main() 