#include "cryptonote_core/cached_block.h"
#include "cryptonote_core/cryptonote_tools.h"
#include "cryptonote_core/transaction_extra.h"
#include "cryptonote_core/check_difficulty.h"
#include <iostream>
#include <iomanip>
#include <sstream>
#include <cstring>
using namespace cryptonote;
using namespace crypto;
using namespace common;
std::string hex(const void* p,size_t n){std::ostringstream o;auto b=(const unsigned char*)p;for(size_t i=0;i<n;i++)o<<std::hex<<std::setw(2)<<std::setfill('0')<<(unsigned)b[i];return o.str();}
Hash h(std::string s){Hash v{};for(int i=0;i<32;i++)v.data[i]=std::stoul(s.substr(i*2,2),0,16);return v;}
// Verbatim checkProofOfWorkV2 body extracted from pinned source, with logger
// replaced by a null stream and cachedGenesisBlock bound to native genesis.
bool proof(const CachedBlock &cachedBlock,uint64_t currentDifficulty,const CachedBlock* cachedGenesisBlock){

        const auto &block = cachedBlock.getBlock();
        if (block.majorVersion < BLOCK_MAJOR_VERSION_2)
        {
            return false;
        }

        if (!check_hash(cachedBlock.getBlockLongHash(), currentDifficulty))
        {
            return false;
        }

        TransactionExtraMergeMiningTag mmTag;
        if (!getMergeMiningTagFromExtra(block.parentBlock.baseTransaction.extra, mmTag))
        {
            (void)0;
            return false;
        }

        if (8 * sizeof(cachedGenesisBlock->getBlockHash()) < block.parentBlock.blockchainBranch.size())
        {
            return false;
        }

        crypto::Hash auxBlocksMerkleRoot;
        crypto::tree_hash_from_branch(block.parentBlock.blockchainBranch.data(), block.parentBlock.blockchainBranch.size(),
                                      cachedBlock.getAuxiliaryBlockHeaderHash(), &cachedGenesisBlock->getBlockHash(), auxBlocksMerkleRoot);

        if (auxBlocksMerkleRoot != mmTag.merkleRoot)
        {
            (void)0;
            return false;
        }

        return true;
    
}
int main(int argc,char**argv){try{
 BlockTemplate genesis{};BinaryArray b;fromHex(parameters::GENESIS_COINBASE_TX_HEX,b);if(!fromBinaryArray(genesis.baseTransaction,b))return 2;genesis.majorVersion=1;genesis.timestamp=0;genesis.nonce=70;CachedBlock gc(genesis);
 BlockTemplate block{};block.majorVersion=5;block.minorVersion=0;block.timestamp=1800000000;block.nonce=0;block.baseTransaction=genesis.baseTransaction;block.baseTransaction.inputs.clear();block.baseTransaction.inputs.push_back(BaseInput{3000000});
 block.parentBlock.majorVersion=1;block.parentBlock.minorVersion=0;block.parentBlock.transactionCount=1;block.parentBlock.baseTransaction.version=1;block.parentBlock.baseTransaction.unlockTime=0;block.parentBlock.baseTransaction.inputs.push_back(BaseInput{1});
 if(argc==1){CachedBlock cb(block);auto a=cb.getAuxiliaryBlockHeaderHash();auto g=gc.getBlockHash();std::cout<<hex(g.data,32)<<"\n"<<hex(a.data,32)<<"\n";return 0;}
 TransactionExtraMergeMiningTag tag;tag.depth=argc-3;tag.merkleRoot=h(argv[1]);for(int i=3;i<argc;i++)block.parentBlock.blockchainBranch.push_back(h(argv[i]));appendMergeMiningTagToExtra(block.parentBlock.baseTransaction.extra,tag);block.nonce=std::stoul(argv[2]);CachedBlock cb(block);
 auto work=cb.getParentBlockHashingBinaryArray(true);auto pow=cb.getBlockLongHash();auto serialized=cb.getParentBlockBinaryArray(false);std::cout<<hex(work.data(),work.size())<<"\n"<<hex(pow.data,32)<<"\n"<<serialized.size()<<"\n"<<proof(cb,1,&gc)<<"\n"<<proof(cb,UINT64_MAX,&gc)<<"\n";
 block.parentBlock.blockchainBranch[0].data[0]^=1;CachedBlock bad(block);std::cout<<proof(bad,1,&gc)<<"\n";
}catch(std::exception&e){std::cerr<<e.what()<<"\n";return 3;}}
