#include <stdio.h>
#include <stdlib.h>
#include "uf.h"
uint64_t uf_findroot(uint64_t i, int64_t *ptr)
{
  if(ptr[i] < 0) return i;
  return ptr[i] = uf_findroot(ptr[i],ptr); //path compression!
}
/********************************************************************************************/
void uf_unite(uint64_t a,uint64_t b, int64_t *ptr)
{	
	uint64_t rt_a, rt_b;
	rt_a = uf_findroot(a,ptr);
	rt_b = uf_findroot(b,ptr);
	if(rt_a != rt_b) {
	if(ptr[rt_a] <= ptr[rt_b]) { //balancing
		ptr[rt_a] = ptr[rt_a] + ptr[rt_b];
		ptr[rt_b] = rt_a;
	}
	else {
		ptr[rt_b] = ptr[rt_b] + ptr[rt_a];
		ptr[rt_a] = rt_b;
	}
 }


}
/********************************************************************************************/
uint8_t uf_connected(uint64_t a, uint64_t b, int64_t *ptr)
{
	return uf_findroot(a,ptr) == uf_findroot(b,ptr);

}
/********************************************************************************************/
int64_t * uf_init(uint64_t length)
{
uint64_t i;
int64_t *ptr;

ptr = malloc(sizeof(*ptr)*length);
if(!ptr) {
	fprintf(stderr,"Error in initUF(): Could not allocate memory!\n");
	exit(1);
}
for(i=0;i<length;i++) {
ptr[i] = -1;
}
return ptr;
}
/********************************************************************************************/
void uf_destroy(int64_t *ptr)
{
	
		free(ptr);
		ptr = NULL;
}
/********************************************************************************************/

