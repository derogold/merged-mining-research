from pathlib import Path
import re,sys
p=Path(sys.argv[1])
def edit(name,f):
 q=p/name;s=q.read_text();q.write_text(f(s))
def cfg(s):
 s='#ifndef DEGO_RESEARCH_TESTNET\n#error "Isolated research build only"\n#endif\n'+s
 for v in range(2,8): s=re.sub(r'(UPGRADE_HEIGHT_V%d = )\d+'%v,lambda m:m[1]+str(v-2),s)
 s=re.sub(r'(CRYPTONOTE_NETWORK = \{).*?;',r'\1 {0x44,0x45,0x47,0x4f,0x54,0x45,0x53,0x54,0x26,0x10,0x14,0x00,0x01,0x02,0x03,0x04}};',s,flags=re.S)
 s=re.sub(r'const char \*const SEED_NODES\[\] = \{.*?\};','const std::array<const char *, 0> SEED_NODES{};',s,flags=re.S)
 return '#include <array>\n'+s
edit('src/config/CryptoNoteConfig.h',cfg)
edit('src/config/CryptoNoteCheckpoints.h',lambda s:re.sub(r'const CheckpointData CHECKPOINTS\[\] = \{.*?\};','const CheckpointData CHECKPOINTS[] = {{0, "7fb97df81221dd1366051b2d0bc7f49c66c22ac4431d879c895b06d66ef66f4c"}};',s,flags=re.S))
edit('src/cryptonotecore/Difficulty.cpp',lambda s:s.replace('    int64_t T =','    return 100; // ISOLATED RESEARCH TESTNET ONLY\n    int64_t T =',1))
# Explicit research-domain identifier: ASCII DEGO-AUX-TESTNET-20261014, zero padded.
header='''#pragma once
#include <crypto/hash.h>
#include <cstring>
namespace CryptoNote {
inline Crypto::Hash researchAuxId() { Crypto::Hash h{}; const char domain[]="DEGO-AUX-TESTNET-20261014"; std::memcpy(&h,domain,sizeof(domain)-1); return h; }
}
'''
(p/'src/config/ResearchAux.h').write_text(header)
edit('src/cryptonotecore/Currency.cpp',lambda s:'#include <config/ResearchAux.h>\n'+s.replace('        Crypto::Hash auxBlocksMerkleRoot;','        const Crypto::Hash auxPath = cachedBlock.getBlockIndex() >= 7 ? researchAuxId() : cachedGenesisBlock->getBlockHash();\n        Crypto::Hash auxBlocksMerkleRoot;').replace('&cachedGenesisBlock->getBlockHash(),','&auxPath,'))
def miner(s):
 s='#include <config/ResearchAux.h>\n#include <cryptonotecore/CachedBlock.h>\n#include <cstdlib>\n'+s
 return s.replace('mmTag.depth = 0;\n                mmTag.merkleRoot = getMerkleRoot(blockTemplate);','''mmTag.depth = 1;
                Crypto::Hash path{};
                const unsigned char legacy[32] = {0x7f,0xb9,0x7d,0xf8,0x12,0x21,0xdd,0x13,0x66,0x05,0x1b,0x2d,0x0b,0xc7,0xf4,0x9c,0x66,0xc2,0x2a,0xc4,0x43,0x1d,0x87,0x9c,0x89,0x5b,0x06,0xd6,0x6e,0xf6,0x6f,0x4c};
                std::memcpy(&path,legacy,32);
                bool useNew = CryptoNote::CachedBlock(blockTemplate).getBlockIndex() >= 7;
                const char *mode = std::getenv("DEGO_TEST_AUX_MODE");
                if (mode) { if (std::string(mode)=="legacy") useNew=false; if (std::string(mode)=="new") useNew=true; }
                if (useNew) path=CryptoNote::researchAuxId();
                blockTemplate.parentBlock.blockchainBranch.assign(1,Crypto::Hash{});
                Crypto::tree_hash_from_branch(blockTemplate.parentBlock.blockchainBranch.data(),1,getMerkleRoot(blockTemplate),&path,mmTag.merkleRoot);''')
edit('src/miner/MinerManager.cpp',miner)
