import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
         self.chain = []
         self.currentTransactions = []
         self.nodes = set()

         self.newBlock(previousHash = 1, proof = 100)

    def registerNode(self, address):
        parsedUrl = urlparse(address)
        self.nodes.add(parsedUrl.netloc)

    def validChain(self, chain):
        lastBlock = chain[0]
        currentIndex = 1

        while currentIndex < len(chain):
            block = chain[currentIndex]
            if block['previous_hash'] != self.hash(lastBlock):
                return False
            if not self.validProof(lastBlock['proof'], block['proof']):
                return False
            lastBlock = block
            currentIndex += 1
        return True

    def resolveConflicts(self):
        newChain = None
        maxLength = len(self.chain)

        for node in self.nodes:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > maxLength and self.valid_chain(chain):
                    maxLength = length
                    newChain = chain
        if new_chain:
            self.chain = newChain
            return True

        return False

    def newBlock(self, proof, previousHash = None):
         block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.currentTransactions,
            'proof': proof,
            'previous_hash': previousHash or self.hash(self.chain[-1])
         }
         self.currentTransactions = []
         self.chain.append(block)
         return block

    def newTransaction(self, sender, recipient, amount):
         self.currentTransactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
         })
         return self.lastBlock['index'] + 1

    def proofOfWork(self, lastProof):
        proof = 0
        while self.validProof(lastProof, proof, self.lastBlock) is False:
            proof += 1
        return proof

    @staticmethod
    def validProof(lastProof, proof, lastBlock):
        guess = f'{lastProof}{proof}{lastBlock}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        blockString = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()

    @property
    def lastBlock(self):
         return self.chain[-1]
