from pathlib import Path
import sys
p=Path(sys.argv[1]);q=p/'src/miner/MinerManager.cpp';s=q.read_text().replace('        std::thread reporter(std::bind(&MinerManager ::printHashRate, this));','        // No periodic reporter thread in bounded research runs.');q.write_text(s)
q=p/'src/miner/main.cpp';s=q.read_text().replace('            app.start();','            app.start();\n            return 0;').replace('Attempting to relaunch...','Research miner stopping.').replace('<< std::endl;','<< std::endl;\n            return 1;');q.write_text(s)
