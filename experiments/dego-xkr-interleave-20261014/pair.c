/* Research-only AES-NI / variant-2 prototype. Uses pinned DEGO helper definitions.
 * Includes upstream source with its original notices; no consensus modifications. */
#include "/tmp/dego-aux-testnet-20261014/source/src/crypto/slow-hash-x86.c"
typedef struct {
 union cn_slow_hash_state state;
 RDATA_ALIGN16 uint64_t a[2], b[4];
 uint64_t division_result,sqrt_result;
 uint8_t *scratch;
 int light;
 uint32_t size;
} ctx;
static void begin(ctx *q,const void *data,size_t length,int light,uint32_t size) {
 q->light=light;q->size=size;q->scratch=aligned_alloc(64,size);assert(q->scratch);
 hash_process(&q->state.hs,data,length);
 RDATA_ALIGN16 uint8_t text[128], key[240];
 memcpy(text,q->state.init,128);aes_expand_key(q->state.hs.b,key);
 for(unsigned i=0;i<size;i+=128){aes_pseudo_round(text,text,key,8);memcpy(q->scratch+i,text,128);}
 for(int i=0;i<2;i++){q->a[i]=q->state.hs.w[i]^q->state.hs.w[i+4];q->b[i]=q->state.hs.w[i+2]^q->state.hs.w[i+6];q->b[i+2]=q->state.hs.w[i+8]^q->state.hs.w[i+10];}
 q->division_result=q->state.hs.w[12];q->sqrt_result=q->state.hs.w[13];
}
static inline void mix(ctx *q,unsigned count) {
 const int variant=2,light=q->light;const uint64_t mask=0x1fff0,tweak1_2=0;
 uint8_t *hp_state=q->scratch;
 RDATA_ALIGN16 uint64_t a[2],b[4],c[2];
 memcpy(a,q->a,sizeof(a));memcpy(b,q->b,sizeof(b));
 uint64_t division_result=q->division_result,sqrt_result=q->sqrt_result,hi,lo,*p;size_t j;
 __m128i _a,_b=_mm_load_si128(R128(b)),_b1=_mm_load_si128(R128(b)+1),_c;
 for(unsigned i=0;i<count;i++){pre_aes();_c=_mm_aesenc_si128(_c,_a);post_aes();}
 memcpy(q->a,a,sizeof(a));_mm_store_si128(R128(q->b),_b);_mm_store_si128(R128(q->b)+1,_b1);
 q->division_result=division_result;q->sqrt_result=sqrt_result;
}
static void finish(ctx *q,char *hash) {
 RDATA_ALIGN16 uint8_t text[128],key[240];memcpy(text,q->state.init,128);aes_expand_key(q->state.hs.b+32,key);
 for(unsigned i=0;i<q->size;i+=128)aes_pseudo_round_xor(text,text,key,q->scratch+i,8);
 memcpy(q->state.init,text,128);hash_permutation(&q->state.hs);
 void (*const hashes[4])(const void*,size_t,char*)={hash_extra_blake,hash_extra_groestl,hash_extra_jh,hash_extra_skein};
 hashes[q->state.hs.b[0]&3](&q->state,200,hash);free(q->scratch);
}
void pair_hash(const void *data,size_t length,char *out,unsigned chunk) {
 ctx d,x;begin(&d,data,length,2,131072);begin(&x,data,length,1,262144);
 if(!chunk){mix(&d,16384);mix(&x,65536);}else{
  unsigned nd=0,nx=0;
  while(nd<16384||nx<65536){if(nd<16384){unsigned n=16384-nd;if(n>chunk)n=chunk;mix(&d,n);nd+=n;}if(nx<65536){unsigned n=65536-nx;if(n>chunk*4)n=chunk*4;mix(&x,n);nx+=n;}}
 }
 finish(&d,out);finish(&x,out+32);
}
int pair_batch(const unsigned char *data,size_t length,unsigned offset,unsigned start,unsigned count,unsigned chunk,unsigned char *out){
 if(offset+4>length)return 1;unsigned char *work=malloc(length);memcpy(work,data,length);
 for(unsigned i=0;i<count;i++){unsigned nonce=start+i;memcpy(work+offset,&nonce,4);pair_hash(work,length,(char*)out+i*64,chunk);}free(work);return 0;
}
