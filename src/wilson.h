#ifndef WILSON_H
#define WILSON_H
uint8_t set_rng_seed(int64_t);
uint8_t init_rng(int64_t);
void destroy_rng(void);
uint64_t RandomTreeWithRoot(uint32_t ,uint32_t , void *, 
        void *, void *, void *);
#endif /*WILSON_H*/
