#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef void (*dfn)(const void*,size_t,char*,int,int,int,uint32_t,uint32_t,uint32_t,uint64_t);
typedef void (*xfn)(const void*,size_t,char*,int,int,int,uint32_t,uint32_t,uint32_t);
// Returns both outputs for every nonce; absent XKR outputs are zero-filled.
// The immediate D->X call sequence binds the saved prefix to the exact same input.
int batch(dfn d,xfn x,dfn ordinary_d,const unsigned char *base,size_t len,uint32_t offset,uint32_t start,uint32_t count,uint32_t ratio,unsigned char *out){
 if(offset+4>len||ratio==0)return -1;
 unsigned char *work=malloc(len);if(!work)return -2;memcpy(work,base,len);
 for(uint32_t i=0;i<count;i++){
  uint32_t n=start+i;for(unsigned k=0;k<4;k++)work[offset+k]=(n>>(8*k))&255;
  unsigned char *row=out+(size_t)i*64;
  int paired=(i%ratio)==0;
  (paired?d:ordinary_d)(work,len,(char*)row,2,2,0,131072,131072,32768,0x1fff0);
  if(paired)x(work,len,(char*)row+32,1,2,0,262144,262144,131072);else memset(row+32,0,32);
 }
 free(work);return 0;
}
