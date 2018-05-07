import crypto from 'crypto';
import _ from 'lodash';

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
      'previous_hash': previousHash || this.hash(JSON.stringify(this.lastBlock))
    }
    this.currentTransactions = [];
    this.chain.push(block);
    return block;
  }

  hash(block) {
    return crypto.createHash('sha256').update(block).digest('hex');
  }

  newTransaction(sender, recipient, amount) {
    this.currentTransactions.push({
      sender,
      recipient,
      amount
    });
    return this.lastBlock.index + 1;
  }

  get lastBlock() {
    return _.last(this.chain);
  }

  proofOfWork(self, lastProof) {
    let proof = 0;
    while (!this.validProof(lastProof, proof, self.lastBlock)) {
      proof++;
    }
    return proof;
  }

  validProof(lastProof, proof, lastBlock) {
    const guess = `${lastProof}${proof}${lastBlock}`;
    const hash = this.hash(guess);
    return hash.slice(0,4) == "0000"
  }
}

export default Blockchain;
