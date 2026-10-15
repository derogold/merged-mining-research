from pathlib import Path
import sys
p=Path(sys.argv[1]);q=p/'src/cryptonotecore/RocksDBWrapper.cpp';s=q.read_text();a=s.index('        auto waitForCompactOptions =');b=s.index('\n        monitorStop.store(true);',a);s=s[:a]+'''        // Research build uses distro RocksDB 6.x: synchronous flush after CompactRange.
        rocksdb::FlushOptions flushOptions; flushOptions.wait = true;
        const rocksdb::Status waitStatus = rocksDb->Flush(flushOptions);
''' +s[b:];q.write_text(s)
for q in (p/'src').rglob('*.cpp'):
 s=q.read_text()
 if 'cxxopts::exceptions::exception' in s:q.write_text(s.replace('cxxopts::exceptions::exception','cxxopts::OptionException'))
q=p/'src/p2p/NetNode.cpp';s=q.read_text();s=s.replace('lanAddress, sizeof lanAddress, wanAddress, sizeof wanAddress','lanAddress, sizeof lanAddress');q.write_text(s)
q=p/'include/JsonHelper.h';q.write_text(q.read_text().replace('.GetObj()', '.GetObject()'))
q=p/'src/daemon/DaemonConfiguration.cpp';s=q.read_text().replace('PrettyWriter writer(stringBuffer);','PrettyWriter<StringBuffer> writer(stringBuffer);').replace('PrettyWriter writer(osw);','PrettyWriter<OStreamWrapper> writer(osw);');q.write_text(s)
