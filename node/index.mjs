import Blockchain from './blockchain';

const chain = new Blockchain();
chain.newTransaction('me', 'you', 10);
const proof = chain.proofOfWork(chain.lastBlock.proof);
chain.newBlock(proof);
console.log(chain.chain, chain.currentTransactions);
