#include <stdlib.h>
#include <gsl/gsl_rng.h>
#include <stdint.h>
#include <string.h>

static gsl_rng * r; 

uint8_t set_rng_seed(int64_t seed) {
    if(!r) return 0;
    gsl_rng_set(r,seed);
    return 1;
}

uint8_t init_rng(int64_t seed) {

    r = gsl_rng_alloc (gsl_rng_mt19937);
    return set_rng_seed(seed);
}


void destroy_rng(void) {
    if(r)gsl_rng_free(r);
}
static inline uint64_t RandomSuccessor(uint32_t v,double *weights,uint32_t *adj_list) {
    if(!weights) return 0;
    double urv =gsl_rng_uniform(r);
    int32_t i,offset=v*4;
    for(i=0;i<4;++i)
        if(weights[offset+i] > urv) return adj_list[offset+i]; 
    return 3;
} 

uint64_t RandomTreeWithRoot(uint32_t r,uint32_t l, void *_InTree, 
        void *_adj_list, void *_Next, void *_weights) {
    
    if(!_adj_list || !_InTree || !_Next || !_weights || !r) return 0;
    uint8_t * InTree = (uint8_t *)_InTree;
    uint32_t * adj_list = (uint32_t *)_adj_list;
    uint32_t * Next = (uint32_t *)_Next;
    double * weights = (double *)_weights;

    uint32_t nv=l*l;
    if(r >= nv) return 0;
    uint32_t iterations=0;
    InTree = memset(InTree,0,nv);
    uint32_t i=0,u;
    Next[r] = -1;
    InTree[r] = 1;
    for(;i<nv;++i) {
        u = i;
        while(!InTree[u]) {
            ++iterations;
            Next[u] = RandomSuccessor(u,weights,adj_list);
            u = Next[u];
        }
        u = i;
        while(!InTree[u]) {
            InTree[u] = 1;
            u = Next[u];
        }

    }
    return iterations;
}

