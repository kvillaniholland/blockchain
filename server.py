from flask import Flask, jsonify, request
from blockchain import Blockchain
from uuid import uuid4

server = Flask(__name__)
nodeIdentifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@server.route('/chain', methods=['GET'])
def fullChain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@server.route('/transactions/new', methods=['POST'])
def newTransaction():
    postData = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in postData for k in required):
        return 'Missing values', 400

    index = blockchain.newTransaction(*postData)

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@server.route('/mine', methods=['GET'])
def mine():
    lastBlock = blockchain.lastBlock
    lastProof = lastBlock['proof']
    proof = blockchain.proofOfWork(lastProof)

    blockchain.newTransaction(
        sender="0", # The sender is "0" to signify that this node has mined a new coin.
        recipient=nodeIdentifier,
        amount=1,
    )

    previousHash = blockchain.hash(lastBlock)
    block = blockchain.newBlock(proof, previousHash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
