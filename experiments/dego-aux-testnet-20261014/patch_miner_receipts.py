from pathlib import Path
import sys
p=Path(sys.argv[1])/'src/miner/MinerManager.cpp'
s=p.read_text();s='#include <fstream>\n'+s
start=s.index('        if (!res || res->status == 200)',s.index('bool MinerManager::submitBlock'))
end=s.index('\n    CryptoNote::BlockMiningParameters',start)
s=s[:start]+'''        json reply = res ? json::parse(res->body, nullptr, false) : json();
        bool accepted = res && res->status == 200 && reply.is_object() && !reply.count("error") && reply.count("result") && reply["result"].value("status", "") == "OK";
        json receipt = {{"height", CryptoNote::CachedBlock(minedBlock).getBlockIndex()}, {"version", minedBlock.majorVersion}, {"accepted", accepted}, {"request", j}, {"reply", reply}};
        if (const char *dest = std::getenv("DEGO_TEST_RECEIPTS")) { std::ofstream f(dest,std::ios::app); f << receipt.dump() << "\\n"; }
        std::cout << "TEST_SUBMISSION " << receipt.dump() << std::endl;
        if (!accepted) throw std::runtime_error("Research candidate rejected (see RPC receipt)");
        return true;
    }
''' +s[end:]
p.write_text(s)
