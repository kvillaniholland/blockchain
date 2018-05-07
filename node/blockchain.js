import crypto from 'crypto';

class Blockchain {
  constructor() {
    this.chain = [];
    this.currentTransactions = [];
    this.nodes = [];

    this.newBlock(1, 100);
  }

  newBlock(proof, previousHash = null) {
    const block = {
      'index': this.chain.length + 1,
      'timestamp': Date.now(),
      'transactions': this.currentTransactions,
      'proof': proof,
      'previous_hash': previousHash || this.hash(this.chain[-1])
    }
    this.currentTransactions = [];
    this.chain.push(block);
    return block;
  }

  hash(block) {
    return crypto.createHash('sha256').update(block).digest('hex');
  }
}
