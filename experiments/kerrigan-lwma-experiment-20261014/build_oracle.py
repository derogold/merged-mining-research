from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent;r=Path('/tmp/kerrigan-research-20261014/src');s=(r/'pow.cpp').read_text();fn=s[s.index('unsigned int LwmaPerAlgo('):s.index('\nunsigned int GetNextWorkRequired(')]
head='''#include <arith_uint256.h>
#include <uint256.h>
#include <vector>
#include <algorithm>
#include <iostream>
const int NUM_ALGOS=4;
namespace Consensus { struct Params {int nPowTargetSpacing=120;int nDiffFloorHeight=0;bool rescue=false;uint256 powLimitAlgo[4],powLimitFloorAlgo[4];bool IsHMPRearmActive(int) const{return rescue;} }; }
struct CBlockIndex {int nHeight,nTime;unsigned nBits;int algo;const CBlockIndex *pprev;int GetAlgo()const{return algo;}int64_t GetBlockTime()const{return nTime;} };
static unsigned EffectivePowLimitForAlgo(const Consensus::Params&p,int a,int h){return UintToArith256(p.nDiffFloorHeight>0&&h>=p.nDiffFloorHeight?p.powLimitFloorAlgo[a]:p.powLimitAlgo[a]).GetCompact();}
'''
main='''int main(){int n,lane,rescue,active;unsigned limit,floor;while(std::cin>>n>>lane>>rescue>>active>>limit>>floor){Consensus::Params p;p.rescue=rescue;p.nDiffFloorHeight=active?1:0;arith_uint256 t;for(int a=0;a<4;a++){t.SetCompact(limit);p.powLimitAlgo[a]=ArithToUint256(t);t.SetCompact(floor);p.powLimitFloorAlgo[a]=ArithToUint256(t);}std::vector<CBlockIndex>b(n);for(int i=0;i<n;i++){std::cin>>b[i].nTime>>b[i].nBits>>b[i].algo;b[i].nHeight=i;b[i].pprev=i?&b[i-1]:nullptr;}std::cout<<LwmaPerAlgo(&b.back(),p,lane)<<"\\n";}}
'''
(p/'oracle.cpp').write_text(head+fn+main)
cmd=['clang++','-std=c++20','-O2','-ffunction-sections','-fdata-sections','-Wl,-dead_strip','-I'+str(r),str(p/'oracle.cpp'),str(r/'arith_uint256.cpp'),'-o',str(p/'oracle')]
z=subprocess.run(cmd,capture_output=True,text=True);(p/'build.log').write_text(z.stdout+z.stderr);print(z.returncode,z.stderr[-2000:])
