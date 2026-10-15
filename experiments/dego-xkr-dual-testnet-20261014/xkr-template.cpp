#include <cryptonote_core/cached_block.h>
#include <cryptonote_core/cryptonote_tools.h>
#include <common/string_tools.h>
#include <cryptonote_core/transaction_extra.h>
#include <json.hpp>
#include <iostream>
using namespace cryptonote;
using namespace crypto;
using namespace common;
int main(){try {std::string line;while(std::getline(std::cin,line)){
 auto j=nlohmann::json::parse(line);BinaryArray raw;BlockTemplate b{};if(!fromHex(j["blob"].get<std::string>(),raw)||!fromBinaryArray(b,raw))return 2;
 if(j.count("timestamp"))b.timestamp=j["timestamp"].get<uint64_t>();
 if(j.count("sibling")){
  Hash sibling{},path{};podFromHex(j["sibling"].get<std::string>(),sibling);podFromHex(j["path"].get<std::string>(),path);
  b.parentBlock=ParentBlock{};b.parentBlock.majorVersion=1;b.parentBlock.minorVersion=0;b.parentBlock.transactionCount=1;
  b.parentBlock.baseTransaction.version=1;b.parentBlock.baseTransaction.unlockTime=0;b.parentBlock.baseTransaction.inputs.push_back(BaseInput{1});
  b.parentBlock.blockchainBranch.assign(1,sibling);b.nonce=j.value("nonce",uint32_t(0));
  TransactionExtraMergeMiningTag tag;tag.depth=1;
  CachedBlock leaf(b);tree_hash_from_branch(&sibling,1,leaf.getAuxiliaryBlockHeaderHash(),&path,tag.merkleRoot);
  appendMergeMiningTagToExtra(b.parentBlock.baseTransaction.extra,tag);
 }
 if(j.count("nonce"))b.nonce=j["nonce"].get<uint32_t>();
 if(j.value("corrupt_branch",false))b.parentBlock.blockchainBranch.at(0).data[0]^=1;
 CachedBlock cb(b);nlohmann::json out={{"leaf",podToHex(cb.getAuxiliaryBlockHeaderHash())},{"height",cb.getBlockIndex()},{"version",b.majorVersion},{"blob",toHex(toBinaryArray(b))},{"block_hash",podToHex(cb.getBlockHash())},{"work",toHex(cb.getParentBlockHashingBinaryArray(true))}};
 if(j.value("verify_pow",false))out["pow"]=podToHex(cb.getBlockLongHash());
 std::cout<<out.dump()<<std::endl;
 }}catch(std::exception&e){std::cerr<<e.what()<<std::endl;return 3;}}
