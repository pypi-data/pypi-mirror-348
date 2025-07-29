import paho.mqtt.client as mqtt
from web3 import Web3
from web3.contract import Contract as Web3Contract

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from decimal import Decimal
from datetime import datetime
from eth_account.messages import encode_defunct
from enum import Enum
from typing import Optional, Dict, Any, List
from events import Events
import json
import ssl
import time
import os
import threading


class DPSN_ERROR_CODES(Enum):
    CONNECTION_ERROR = 400
    UNAUTHORIZED = 401
    PUBLISH_ERROR = 402
    INITIALIZATION_FAILED = 403
    CLIENT_NOT_INITIALIZED = 404
    CLIENT_NOT_CONNECTED = 405
    SUBSCRIBE_ERROR = 406
    SUBSCRIBE_NO_GRANT = 407
    SUBSCRIBE_SETUP_ERROR = 408
    DISCONNECT_ERROR = 409
    BLOCKCHAIN_CONFIG_ERROR = 410
    INVALID_PRIVATE_KEY = 411
    ETHERS_ERROR = 412
    MQTT_ERROR = 413
    MESSAGE_HANDLING_ERROR = 414

class DPSNError(Exception):
    def __init__(self, code: DPSN_ERROR_CODES, message: str, status: Optional[str] = None):
        self.code = code
        self.message = message
        self.status = status
        super().__init__(self.message)

    def to_dict(self):
        return {
            'code': self.code.value,
            'message': self.message,
            'status': self.status
        }

    def __str__(self):
        return str(self.to_dict())

class DpsnClient(Events):
    __events__ = ('on_msg', 'on_error')

    def __init__(self, dpsn_url: str, private_key: str, chain_options: Dict[str, Any], connection_options: Dict[str, Any] = None):
        super().__init__()
        connection_options = connection_options or {}
        self.web3 = Web3()
        self.validate_private_key(private_key)
        account = self.web3.eth.account.from_key(private_key)
        self.account = account
        self.wallet_address = account.address
        self.mainnet = chain_options.get('network') == 'mainnet'
        self.testnet = chain_options.get('network') == 'testnet'
        self.blockchain_type = chain_options.get('wallet_chain_type')
        self.hostname = dpsn_url
        self.secure = connection_options.get('ssl', True)
        self.full_url = f"{'mqtts' if self.secure else 'mqtt'}://{self.hostname}"
        self.dpsn_broker = None
        self.connected = False
        self._init_done = False
        self._connect_event = threading.Event()
        self._validate_initialization(chain_options)

        try:
            with files('dpsn_client.abi').joinpath('contract_abi.json').open('r') as f:
                self.contract_abi = json.load(f)
        except FileNotFoundError:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "Contract ABI file not found"
            )
        except json.JSONDecodeError:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "Failed to parse contract ABI JSON"
            )
        
    def _validate_initialization(self, chain_options: Dict[str, Any]) -> None:
        if chain_options.get('network') not in ['mainnet', 'testnet']:
            raise ValueError('Network must be either mainnet or testnet')
        if chain_options.get('wallet_chain_type') != 'ethereum':
            raise ValueError('Only Ethereum wallet_chain_type is supported')

    def validate_private_key(self, private_key: str) -> None:
        try:
            clean_key = private_key.replace('0x', '')
            if not (len(clean_key) == 64 and all(c in '0123456789abcdefABCDEF' for c in clean_key)):
                raise ValueError("Invalid private key format")
            self.web3.eth.account.from_key(private_key)
        except Exception as e:
            raise DPSNError(DPSN_ERROR_CODES.INVALID_PRIVATE_KEY, f"Invalid private key: {str(e)}", "disconnected")

    def init(self, options: Dict[str, Any] = None) -> mqtt.Client:
        if self._init_done and self.dpsn_broker and self.dpsn_broker.is_connected():
            return self.dpsn_broker

        options = options or {}
        message = "testing"
        signature = self.account.sign_message(encode_defunct(text=message))
        self.password = signature.signature.hex()

        self.dpsn_broker = mqtt.Client(protocol=mqtt.MQTTv5)
        self.dpsn_broker.username_pw_set(username=self.wallet_address, password=self.password)
        self.dpsn_broker.connect_timeout = options.get('connect_timeout', 5000)
        self.dpsn_broker.clean_session = True

        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                self.connected = True
                self._connect_event.set()
            else:
                self.connected = False
                self._connect_event.set()

        def on_disconnect(client, userdata, rc, properties=None):
            self.connected = False

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode("utf-8")
                try:
                    payload = json.loads(payload)
                except json.JSONDecodeError:
                    pass
                self.on_msg({'topic': msg.topic, 'payload': payload})
            except Exception as e:
                error = DPSNError(DPSN_ERROR_CODES.MESSAGE_HANDLING_ERROR, str(e), "connected")
                self.on_error(error)

        self.dpsn_broker.on_connect = on_connect
        self.dpsn_broker.on_disconnect = on_disconnect
        self.dpsn_broker.on_message = on_message

        self._connect_with_retry(options.get('retry_options', {}))
        self._init_done = True
        return self.dpsn_broker

    def _connect_with_retry(self, retry_options: Dict[str, Any]) -> None:
        max_retries = retry_options.get('max_retries', 3)
        initial_delay = retry_options.get('initial_delay', 1000) / 1000
        max_delay = retry_options.get('max_delay', 5000) / 1000
        port = 8883 if self.secure else 1883
        if self.secure:
            self.dpsn_broker.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)

        for attempt in range(max_retries):
            try:
                self.dpsn_broker.connect(self.hostname, port=port, keepalive=60)
                self.dpsn_broker.loop_start()
                self._connect_event.wait(timeout=10)
                if self.connected:
                    return
                else:
                    raise Exception("MQTT connection failed")
            except Exception as e:
                if attempt == max_retries - 1:
                    raise DPSNError(DPSN_ERROR_CODES.CONNECTION_ERROR, str(e), "disconnected")
                delay = min(initial_delay * (2 ** attempt), max_delay)
                time.sleep(delay)

    def disconnect(self):
        if not self.dpsn_broker:
            raise DPSNError(DPSN_ERROR_CODES.CLIENT_NOT_INITIALIZED, "Cannot disconnect: client not initialized", "disconnected")
        try:
            self.dpsn_broker.loop_stop()
            self.dpsn_broker.disconnect()
            self.connected = False
        except Exception as e:
            raise DPSNError(DPSN_ERROR_CODES.DISCONNECT_ERROR, str(e), "disconnected")

    def subscribe(self, topic: str, options: Dict[str, Any] = None) -> None:
        if not self.dpsn_broker or not self.dpsn_broker.is_connected():
            raise DPSNError(DPSN_ERROR_CODES.CLIENT_NOT_CONNECTED, "Cannot subscribe: client not connected", "disconnected")
        options = options or {}
        qos = options.get('qos', 1)
        result, mid = self.dpsn_broker.subscribe(topic, qos=qos)
        if result != mqtt.MQTT_ERR_SUCCESS:
            raise DPSNError(DPSN_ERROR_CODES.SUBSCRIBE_ERROR, f"Failed to subscribe to topic '{topic}'", "connected")

    def unsubscribe(self, topic: str) -> None:
        if not self.dpsn_broker or not self.connected:
            raise DPSNError(DPSN_ERROR_CODES.CLIENT_NOT_CONNECTED, "Cannot unsubscribe: client not connected", "disconnected")
        result, mid = self.dpsn_broker.unsubscribe(topic)
        if result != mqtt.MQTT_ERR_SUCCESS:
            raise DPSNError(DPSN_ERROR_CODES.SUBSCRIBE_ERROR, f"Failed to unsubscribe from topic '{topic}'", "connected")

    def publish(self, topic: str, message: Any, options: Dict[str, Any] = None) -> None:
        """
        Publishes a message to a DPSN MQTT topic with a signature.

        Args:
            topic (str): The full topic to publish to (e.g., '0x1234abcd/data').
            message (Any): The message payload (will be JSON serialized).
            options (Dict[str, Any], optional): QoS, retain, etc.

        Raises:
            DPSNError: If client is not connected or publishing fails.
        """
        if not self.dpsn_broker or not self.connected:
            raise DPSNError(
                DPSN_ERROR_CODES.CLIENT_NOT_CONNECTED,
                "Cannot publish: client not connected",
                "disconnected"
            )

        parent_topic = topic.split('/')[0]
        if not parent_topic.startswith('0x'):
            raise DPSNError(
                DPSN_ERROR_CODES.PUBLISH_ERROR,
                f"Invalid topic format: must start with '0x'. Got: {parent_topic}",
                "connected"
            )

        try:
            # Convert hex topic to bytes and then sign it directly
            # Instead of trying to encode bytes again, pass the hex string to encode_defunct
            topic_hex = parent_topic[2:]  # Remove '0x' prefix
            signature = self.account.sign_message(encode_defunct(hexstr=topic_hex))
            # MQTT v5 properties
            properties = mqtt.Properties(mqtt.PacketTypes.PUBLISH)
            properties.UserProperty = [("signature", signature.signature.hex())]

            # Handle QoS/retain from options
            options = options or {}
            qos = options.get('qos', 1)
            retain = options.get('retain', False)

            result = self.dpsn_broker.publish(
                topic,
                payload=json.dumps(message),
                qos=qos,
                retain=retain,
                properties=properties
            )
            result.wait_for_publish()
            print(f"message published on topic {topic} with qos {qos}")
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                raise DPSNError(
                    DPSN_ERROR_CODES.PUBLISH_ERROR,
                    f"MQTT publish failed with return code {result.rc}",
                    "connected"
                )

        except Exception as e:
            raise DPSNError(
                DPSN_ERROR_CODES.PUBLISH_ERROR,
                f"Failed to publish message: {str(e)}",
                "connected"
            )

    def set_blockchain_config(self, rpc_url: Optional[str] = None, contract_address: Optional[str] = None) -> Web3Contract:
        """
        Sets the Web3 provider and smart contract instance based on RPC and contract address.

        Args:
            rpc_url (str, optional): The JSON-RPC URL (e.g., Infura, Alchemy).
            contract_address (str, optional): The deployed smart contract address.

        Returns:
            Web3Contract: The initialized contract instance.

        Raises:
            DPSNError: If ABI is missing, web3 fails to connect, or contract setup fails.
        """
        if rpc_url:
            self.web3 = Web3(Web3.HTTPProvider(rpc_url))
            if not self.web3.is_connected():
                raise DPSNError(
                    DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                    f"Failed to connect to RPC: {rpc_url}",
                )
        if not self.contract_abi:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "Contract ABI not loaded.",
            )


        if contract_address:
            try:
                self.contract = self.web3.eth.contract(
                    address=self.web3.to_checksum_address(contract_address),
                    abi=self.contract_abi
                )
                self.contract_address = self.web3.to_checksum_address(contract_address)
            except Exception as e:
                raise DPSNError(
                    DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                    f"Failed to initialize contract: {str(e)}",
                )
        elif not hasattr(self, 'contract') or self.contract is None:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "No contract address provided and contract not previously set.",
            )

        return self.contract

        
    def generate_topic_hash(self, topic_name: str) -> str:
        nonce = os.urandom(8).hex()
        topic_seed = f"{nonce}_{topic_name}"
        return self.web3.keccak(text=topic_seed).hex()

    def wait_for_transaction_confirmation(
        self,
        tx_hash: str,
        confirmations: int = 2,
        timeout: int = 120,
        poll_interval: int = 5
    ) -> Any:
        """
        Waits for a transaction to be confirmed with a given number of confirmations.

        Args:
            tx_hash (str): Transaction hash (hex string).
            confirmations (int): Number of confirmations required.
            timeout (int): Timeout in seconds.
            poll_interval (int): Time to wait between polling attempts.

        Returns:
            Receipt object with confirmation.

        Raises:
            DPSNError if transaction is not confirmed within timeout.
        """
        start_time = time.time()
        print(f"Waiting for transaction {tx_hash} to be mined...")

        try:
            # Wait until receipt exists (transaction is mined)
            while True:
                try:
                    receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                    break  # exit loop once receipt is found
                except Exception as e:
                    print("⏳ Transaction not yet mined, waiting...")
                    if time.time() - start_time > timeout:
                        raise DPSNError(
                            DPSN_ERROR_CODES.ETHERS_ERROR,
                            f"Transaction {tx_hash} not found within timeout of {timeout}s.",
                            "disconnected"
                        )
                    time.sleep(poll_interval)

            # Now wait for the required number of confirmations
            print(f"🔍 Mined in block {receipt['blockNumber']}, waiting for {confirmations} confirmations...")
            while True:
                current_block = self.web3.eth.block_number
                confirmations_count = current_block - receipt['blockNumber'] + 1
                if confirmations_count >= confirmations:
                    print(f"✅ Transaction {tx_hash} confirmed with {confirmations_count} blocks.")
                    return receipt

                print(f"⏳ Waiting for confirmations: {confirmations_count}/{confirmations}")
                if time.time() - start_time > timeout:
                    raise DPSNError(
                        DPSN_ERROR_CODES.ETHERS_ERROR,
                        f"Timeout: only {confirmations_count} confirmations after {timeout}s.",
                        "disconnected"
                    )

                time.sleep(poll_interval)

        except DPSNError:
            raise
        except Exception as e:
            raise DPSNError(
                DPSN_ERROR_CODES.ETHERS_ERROR,
                f"Error while waiting for confirmation: {str(e)}",
                "disconnected"
            )

    def get_topic_price(self) -> int:
        """
        Fetches the current price to register a topic from the smart contract.

        Returns:
            int: Topic price in wei.

        Raises:
            DPSNError: If contract is not initialized or call fails.
        """
        if not self.contract:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "Smart contract is not initialized. Please call set_blockchain_config() first.",
                "disconnected"
            )

        try:
            price = self.contract.functions.getTopicPrice().call()
            return price
        except Exception as e:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                f"Failed to fetch topic price: {str(e)}"
            )


    def purchase_topic(
            self,
            topic_name:str,
            contract_address: Optional[str] = None,
            confirmations:int=2,
            timeout:int = 120
    ) -> Dict[str,Any]:
        """
        Registers a topic on the blockchain by calling the smart contract.

    Args:
        topic_name (str): Human-readable topic string (e.g., "BTC/USD").
        contract_address (Optional[str]): Address of the deployed TopicRegistry contract.
                                         If None, uses the address set via set_blockchain_config.
        confirmations (int): Confirmations to wait for.
        timeout (int): Timeout in seconds.

    Returns:
        dict: { 'topic_hash': str, 'tx_hash': str, 'receipt': dict }

    Raises:
        DPSNError if something goes wrong, ABI/contract not set, or address missing.
        """
        # Determine which contract address and instance to use
        addr_to_use = None
        if contract_address:
            try:
                addr_to_use = self.web3.to_checksum_address(contract_address)
            except ValueError as e:
                 raise DPSNError(DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR, f"Invalid provided contract address: {e}")
        elif hasattr(self, 'contract_address') and self.contract_address:
            addr_to_use = self.contract_address
        else:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "Contract address not provided and not configured via set_blockchain_config."
            )
        
        # Get the contract instance to use
        contract_instance = None
        if hasattr(self, 'contract') and self.contract and self.contract.address == addr_to_use:
             contract_instance = self.contract
        elif self.contract_abi:
            # Initialize contract instance if ABI is available but instance doesn't match or exist
            try:
                contract_instance = self.web3.eth.contract(address=addr_to_use, abi=self.contract_abi)
                # Optionally update self.contract if the provided address should become the default
                # self.contract = contract_instance 
                # self.contract_address = addr_to_use
            except Exception as e:
                 raise DPSNError(DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR, f"Failed to initialize contract instance: {e}")
        else:
             raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "Contract ABI not loaded, cannot interact with contract."
            )
        
        if not contract_instance:
            raise DPSNError(DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR, "Failed to obtain contract instance.")

        if not self.contract_abi: # Redundant check, but safe
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "Smart contract ABI not loaded."
            )
            
        try:
            topic_hash = self.generate_topic_hash(topic_name=topic_name)

            message = encode_defunct(hexstr=topic_hash)
            # Keep signature as bytes, don't convert to hex
            signature_bytes = self.account.sign_message(message).signature 

            # Use the determined contract instance
            value = contract_instance.functions.getTopicPrice().call()

            nonce = self.web3.eth.get_transaction_count(self.wallet_address)
            gas_price = self.web3.eth.gas_price

            # Convert topic_hash hex string to bytes for the contract call
            topic_hash_bytes = bytes.fromhex(topic_hash.replace('0x', ''))

            # Use the determined contract instance and pass bytes
            txn = contract_instance.functions.registerTopic(
                topic_name, 
                topic_hash_bytes, # Pass bytes
                signature_bytes   # Pass bytes
            ).build_transaction({
                'from': self.wallet_address,
                'value': value,
                'nonce': nonce,
                'gasPrice': gas_price,
                'gas': 500_000  # Estimate or use estimate_gas()
            })

            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.account.key)
            try:
                raw_tx = signed_txn.raw_transaction
            except AttributeError:
                try:
                    raw_tx = signed_txn["rawTransaction"]
                except(TypeError,KeyError):
                    raise DPSNError(
                        DPSN_ERROR_CODES.ETHERS_ERROR,
                        "Unable to extract raw transaction from signed_txn"
                    )
            
            tx_hash = self.web3.eth.send_raw_transaction(raw_tx)
            
            # waiting for confirmation
            receipt = self.wait_for_transaction_confirmation(
                tx_hash.hex(), confirmations=confirmations, timeout=timeout
            )
            print(f"topic registered successfully 0x{topic_hash}")

            return {
                "topic": "0x"+topic_hash,
                "tx_hash": tx_hash.hex()
                }
        
        except DPSNError:
            raise
        except Exception as e:
            raise DPSNError(
                DPSN_ERROR_CODES.ETHERS_ERROR,
                f"Error during topic purchase: {str(e)}"
            )
        
    def fetch_owned_topics(self) -> list:
        """
        Fetch topics registered by the current wallet from the initialized contract.

        Returns:
            list[dict]: List of topics with hash, name, and registeredAt.

        Raises:
            DPSNError: If contract is not set or if there is a failure in the call.
        """
        if not self.contract:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                "Smart contract is not initialized. Please call set_contract_address() first.",
                "disconnected"
            )
        
        try:
            topic_data = self.contract.functions.getUserTopics(self.wallet_address).call()

            formatted_topics = []
            for entry in topic_data:
                if isinstance(entry, (tuple, list)) and len(entry) == 3:
                    topic_name, topic_hash_bytes, timestamp = entry
                    formatted_topics.append({
                        "name": topic_name,
                        "topic": self.web3.to_hex(topic_hash_bytes),
                        "registered_at": timestamp
                    })
                else:
                    continue
            return formatted_topics
        
        except Exception as e:
            raise DPSNError(
                DPSN_ERROR_CODES.BLOCKCHAIN_CONFIG_ERROR,
                f"Error fetching owned topics: {str(e)}",
            )
