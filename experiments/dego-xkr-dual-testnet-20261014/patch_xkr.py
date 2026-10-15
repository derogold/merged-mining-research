from pathlib import Path
import re,sys
p=Path(sys.argv[1]);q=p/'src/config/cryptonote_config.h';s=q.read_text();s='#ifndef USE_TESTNET\n#error "Research tree requires USE_TESTNET"\n#endif\n'+s
s=s.replace('TESTNET_FIXED_DIFFICULTY = 1;', 'TESTNET_FIXED_DIFFICULTY = 100;')
for v,h in [(2,0),(3,1),(4,2),(5,5)]:s=s.replace(f'UPGRADE_HEIGHT_V{v} = 0;',f'UPGRADE_HEIGHT_V{v} = {h};',1)
s=s.replace('0xf1, 0x4c, 0xb8, 0xc8, 0xb3, 0x56, 0x45, 0x2e, 0xee, 0xf0, 0xb4, 0x99, 0xab, 0x71, 0x6c, 0xcc','0x58, 0x4b, 0x52, 0x54, 0x45, 0x53, 0x54, 0x26, 0x10, 0x14, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05');q.write_text(s)
q=p/'src/miner/miner_manager.cpp';s=q.read_text();s='#include <fstream>\n#include <cstdlib>\n'+s
s=s.replace('        std::thread reporter(std::bind(&MinerManager::printHashRate, this));\n        reporter.detach();','        // Reporter disabled for bounded research runs.')
a=s.index('        if (!res || res->status == 200)',s.index('bool MinerManager::submitBlock'));b=s.index('\n    BlockMiningParameters',a)
s=s[:a]+'''        json reply = res ? json::parse(res->body, nullptr, false) : json();
        bool accepted = res && res->status == 200 && reply.is_object() && !reply.count("error") && reply.count("result") && reply["result"].value("status", "") == "OK";
        json receipt = {{"height", cachedBlock.getBlockIndex()}, {"version", minedBlock.majorVersion}, {"accepted", accepted}, {"request", j}, {"reply", reply}};
        if (const char *dest = std::getenv("XKR_TEST_RECEIPTS")) { std::ofstream f(dest,std::ios::app); f << receipt.dump() << "\\n"; }
        std::cout << "TEST_SUBMISSION " << receipt.dump() << std::endl;
        if (!accepted) throw std::runtime_error("Research candidate rejected (see RPC receipt)");
        return true;
    }
''' + s[b:];q.write_text(s)
q=p/'src/miner/main.cpp';s=q.read_text().replace('            app.start();','            app.start();\n            return 0;').replace('Attempting to relaunch...','Research miner stopping.').replace('<< std::endl;','<< std::endl;\n            return 1;');q.write_text(s)
q=p/'src/CMakeLists.txt';s=q.read_text().replace('include_directories(${CMAKE_SOURCE_DIR}/external/rocksdb/include)','').replace('include_directories(${CMAKE_SOURCE_DIR}/external/cryptopp)','');q.write_text(s)
q=p/'src/p2p/net_node.cpp';s=q.read_text().replace('        // Add UPnP port mapping','        return; // Isolated Docker research network: never request UPnP mappings.\n        // Add UPnP port mapping');q.write_text(s)
