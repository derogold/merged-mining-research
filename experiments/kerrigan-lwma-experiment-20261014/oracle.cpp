#include <arith_uint256.h>
#include <uint256.h>
#include <vector>
#include <algorithm>
#include <iostream>
const int NUM_ALGOS=4;
namespace Consensus { struct Params {int nPowTargetSpacing=120;int nDiffFloorHeight=0;bool rescue=false;uint256 powLimitAlgo[4],powLimitFloorAlgo[4];bool IsHMPRearmActive(int) const{return rescue;} }; }
struct CBlockIndex {int nHeight,nTime;unsigned nBits;int algo;const CBlockIndex *pprev;int GetAlgo()const{return algo;}int64_t GetBlockTime()const{return nTime;} };
static unsigned EffectivePowLimitForAlgo(const Consensus::Params&p,int a,int h){return UintToArith256(p.nDiffFloorHeight>0&&h>=p.nDiffFloorHeight?p.powLimitFloorAlgo[a]:p.powLimitAlgo[a]).GetCompact();}
unsigned int LwmaPerAlgo(const CBlockIndex* pindexLast, const Consensus::Params& params, int algo)
{
    const int nNextHeight = pindexLast->nHeight + 1;
    const int64_t T = (int64_t)params.nPowTargetSpacing * NUM_ALGOS; // per-algo spacing = 480s
    const int N = 60;                                                 // averaging window (same-algo blocks)

    // Collect up to N+1 most-recent same-algo blocks (newest first). Bounded walk so a
    // very sparse algo cannot force a full-chain scan.
    std::vector<const CBlockIndex*> a;
    a.reserve(N + 1);
    const int maxDepth = (N + 1) * NUM_ALGOS * 8;
    int depth = 0;
    for (const CBlockIndex* p = pindexLast;
         p != nullptr && (int)a.size() < N + 1 && depth < maxDepth;
         p = p->pprev, ++depth) {
        if (p->GetAlgo() == algo) a.push_back(p);
    }

    // Stranded-algo bounded gap reset (v1.3.2, height-gated at nHMPRearmHeight).
    // Plain LWMA has no rescue for an algo abandoned at high difficulty: it eases
    // only ~16%/block, so an algo left at m-times its sustainable difficulty takes
    // ~m hours of long blocks to recover, and past the bounded walk (maxDepth) it
    // finds < 2 same-algo blocks and snaps STRAIGHT to the floor -- seeding an
    // instant-block burst plus the k/20 anti-timewarp whiplash the legacy Hivemind
    // bounded reset was written to prevent. Port that reset here: if this algo has
    // not produced for >= the legacy gap threshold, ease its last difficulty 4x per
    // missed round toward the effective floor instead of crawling or snapping.
    // Pre-rearm this whole block is skipped, so v1.3.1 behaviour is byte-identical.
    if (params.IsHMPRearmActive(nNextHeight) && !a.empty()) {
        // Same threshold the legacy DAA used post-nDiffFloorHeight: one full
        // averaging window (NUM_ALGOS * 10 = 40 blocks) since this algo's last block.
        const int nGapThreshold = NUM_ALGOS * 10;
        const int algoGap = pindexLast->nHeight - a[0]->nHeight;
        if (algoGap >= nGapThreshold) {
            arith_uint256 bnEased;
            bnEased.SetCompact(a[0]->nBits);
            arith_uint256 bnLimit;
            bnLimit.SetCompact(EffectivePowLimitForAlgo(params, algo, nNextHeight));
            // 4x easier per missed round (one round = NUM_ALGOS blocks the stalled
            // algo skipped), capped at the floor so it never eases past the legacy
            // reset and never wraps past 256 bits when the floor is near 2^254.
            const int nSteps = 1 + (algoGap - nGapThreshold) / NUM_ALGOS;
            for (int i = 0; i < nSteps && bnEased < bnLimit; i++) {
                if (bnEased > (bnLimit >> 2)) {
                    bnEased = bnLimit;
                    break;
                }
                bnEased <<= 2;
            }
            if (bnEased > bnLimit) bnEased = bnLimit;
            return bnEased.GetCompact();
        }
    }

    // Bootstrap: need at least two same-algo blocks for one solvetime. On the v1.3.1
    // fork this never fires (pre-fork history holds > N same-algo blocks); it only
    // matters on a fresh chain (or, post-rearm, an algo stranded beyond the maxDepth
    // walk with zero same-algo blocks in range -- no reference to ease from, floor
    // is unavoidable).
    if (a.size() < 2) {
        return EffectivePowLimitForAlgo(params, algo, nNextHeight);
    }

    // Progressive window: use all available same-algo history, up to N.
    const int Neff = std::min<int>(N, (int)a.size() - 1);
    const int64_t k = (int64_t)Neff * (Neff + 1) / 2 * T;

    // a[0] = newest ... a[Neff] = oldest of the window. Iterate oldest->newest so the
    // linear weight i (1..Neff) gives the most recent block the highest weight.
    int64_t weightedSolvetimes = 0;
    arith_uint256 sumTarget;
    for (int i = 1; i <= Neff; ++i) {
        const CBlockIndex* cur  = a[Neff - i];       // i-th oldest block in the window
        const CBlockIndex* prev = a[Neff - i + 1];   // its same-algo predecessor
        int64_t st = (int64_t)cur->GetBlockTime() - (int64_t)prev->GetBlockTime();
        if (st > 6 * T)  st = 6 * T;                  // cap high outliers (timestamp attack)
        if (st < -5 * T) st = -5 * T;                 // bound out-of-order timestamps
        weightedSolvetimes += st * i;
        arith_uint256 tcur;
        tcur.SetCompact(cur->nBits);
        sumTarget += tcur;
    }

    // Anti-timewarp: never let the weighted solvetime collapse (would spike difficulty).
    if (weightedSolvetimes < k / 20) weightedSolvetimes = k / 20;

    // next_target = avg(target over window) * weightedSolvetimes / k.
    // Divide before the multiply to stay within 256 bits for the easiest algos; the
    // dropped low bits are far below compact-nBits precision (checked vs the oracle).
    arith_uint256 bnNew = sumTarget;
    bnNew /= (uint32_t)Neff;                 // average target over the window
    bnNew /= (uint32_t)k;                    // pre-divide by k (overflow-safe)
    bnNew *= (uint32_t)weightedSolvetimes;   // apply weighted solvetimes

    // Cap at the per-algo powLimit, then the tighter hardware floor (post nDiffFloorHeight).
    const arith_uint256 bnPowLimit = UintToArith256(params.powLimitAlgo[algo]);
    if (bnNew > bnPowLimit) bnNew = bnPowLimit;
    if (params.nDiffFloorHeight > 0 && nNextHeight >= params.nDiffFloorHeight &&
        algo >= 0 && algo < NUM_ALGOS) {
        const arith_uint256 bnFloor = UintToArith256(params.powLimitFloorAlgo[algo]);
        if (bnNew > bnFloor) bnNew = bnFloor;
    }
    if (bnNew == arith_uint256(0)) bnNew = UintToArith256(params.powLimitFloorAlgo[algo]);
    return bnNew.GetCompact();
}
int main(){int n,lane,rescue,active;unsigned limit,floor;while(std::cin>>n>>lane>>rescue>>active>>limit>>floor){Consensus::Params p;p.rescue=rescue;p.nDiffFloorHeight=active?1:0;arith_uint256 t;for(int a=0;a<4;a++){t.SetCompact(limit);p.powLimitAlgo[a]=ArithToUint256(t);t.SetCompact(floor);p.powLimitFloorAlgo[a]=ArithToUint256(t);}std::vector<CBlockIndex>b(n);for(int i=0;i<n;i++){std::cin>>b[i].nTime>>b[i].nBits>>b[i].algo;b[i].nHeight=i;b[i].pprev=i?&b[i-1]:nullptr;}std::cout<<LwmaPerAlgo(&b.back(),p,lane)<<"\n";}}
