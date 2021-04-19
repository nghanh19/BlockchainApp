# Thanks for a article: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

import  hashlib
from    hashlib import sha256
import  json
from    time import time
from    uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain= []
        self.current_transactions = []

    def proof_of_work(self, last_proof):
        """
        Simple Proof Of Work algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previours p'
        - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int> 
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        '''
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not 
        '''  

        guess       = f'{last_proof}{proof}'.encode()
        guess_hash  = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    # Creates a new Block and adds it to the chain
    # Param "proof": <int> The proof given by the Proof of Work algorithm
    # param "previous_hash": (Optional) <str> Hash of previous Block
    # Return: <Dict> New Block
    def new_block(self, proof, previous_hash=None):
        block = {
            'index'     : len(self.chain) + 1,
            'timestamp' : time(),
            'transaction' : self.current_transactions,
            'proof'     : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    
    # Creates a new transaction to go into the next mined Block
    # Param "sender": <str> Address of the Sender
    # Param "recipient": <str> Address of the Recipient
    # Param "amount": <int> Amount
    # Return: <int> The index of the Block that will hold this Transaction
    def new_transaction(self, sender, recipient, amout):
        self.current_transactions.append({
            'sender'    : sender,
            'recipient' : recipient,
            'amount'    : amout
        })

        return self.last_block['index'] + 1

    # Creates a SHA-256 hash of Block
    # :Param block: <Dict> Block
    # :return: <str>
    @staticmethod
    def hash(block):

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Return the last Block in the chain
        return self.chain[-1]