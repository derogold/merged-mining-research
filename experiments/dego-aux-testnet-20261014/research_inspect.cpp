#include <cryptonotecore/CachedBlock.h>
#include <common/CryptoNoteTools.h>
#include <common/StringTools.h>
#include <common/TransactionExtra.h>
#include <common/CheckDifficulty.h>
#include <config/ResearchAux.h>
#include <json.hpp>
#include <iostream>
int main(){using namespace CryptoNote; using namespace Crypto; using namespace Common;
 std::string hex; while(std::cin>>hex){BinaryArray raw; BlockTemplate b{};if(!fromHex(hex,raw)||!fromBinaryArray(b,raw))return 2;
 CachedBlock cb(b); TransactionExtraMergeMiningTag tag; if(!getMergeMiningTagFromExtra(b.parentBlock.baseTransaction.extra,tag))return 3;
 Hash legacy{};podFromHex("7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c",legacy);Hash modern=researchAuxId(),oldRoot{},newRoot{};
 tree_hash_from_branch(b.parentBlock.blockchainBranch.data(),b.parentBlock.blockchainBranch.size(),cb.getAuxiliaryBlockHeaderHash(),&legacy,oldRoot);
 tree_hash_from_branch(b.parentBlock.blockchainBranch.data(),b.parentBlock.blockchainBranch.size(),cb.getAuxiliaryBlockHeaderHash(),&modern,newRoot);
 auto pow=cb.getBlockLongHash(); auto work=cb.getParentBlockHashingBinaryArray(true);
 nlohmann::json j={{"height",cb.getBlockIndex()},{"majorVersion",b.majorVersion},{"depth",tag.depth},{"pow_meets_100",check_hash(pow,100)},{"old_path_matches",oldRoot==tag.merkleRoot},{"new_path_matches",newRoot==tag.merkleRoot},{"block_hash",podToHex(cb.getBlockHash())},{"pow_hash",podToHex(pow)},{"work",toHex(work)}};std::cout<<j.dump()<<std::endl;
 }}
