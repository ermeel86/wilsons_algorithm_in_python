#include "cluster_statistics.h"
#include <stdio.h>
#include <math.h>
#include "uf.h"
#define LOG_ADD(a,b) ( (a) > (b) ? (a) + log1p(exp((b)-(a))) : (b) + log1p(exp((a)-(b))))  
static int64_t *uf=NULL;
static uint64_t length_1d=0;
static uint64_t nvertices=0;
static uint64_t num_cluster=0;
static uint64_t size_giant=0;
static double log_sum_csm2,log_sum_csm4;

uint8_t cluster_stat_init_cubic(uint64_t l) {
    length_1d = l;
    nvertices = pow(length_1d,3);
    uf= uf_init(nvertices);
    return uf ? 1 : 0;  
}
uint64_t cluster_stat_analyse_cubic(void * ee, uint64_t n_edges) {
    if(!ee) return nvertices;
    uint64_t *edge_list = (uint64_t *)ee;
    uint64_t i;
    double tmp;
    if(num_cluster)for(i=0;i<nvertices;++i)uf[i] = -1; 
    for(i=0;i<n_edges;i++)uf_unite(edge_list[2*i],edge_list[2*i+1],uf);
    log_sum_csm2=log_sum_csm4=0;
    num_cluster=size_giant=0;
    for(i=0;i<nvertices;i++) {
        //here we can calculate cluster size moments later
        if(uf[i] < 0) { 
            num_cluster++;
            if((uint64_t)(-uf[i]) > size_giant) size_giant = -uf[i]; 
            tmp = 2*log(-uf[i]);
            log_sum_csm2 = LOG_ADD(log_sum_csm2,tmp);
            tmp *= 2;
            log_sum_csm4 = LOG_ADD(log_sum_csm4,tmp);
        }
    }
    return num_cluster;
}
double cluster_stat_log_csm2(void) {
    return log_sum_csm2;
}
double cluster_stat_log_csm4(void) {
    return log_sum_csm4;
}
uint64_t cluster_stat_size_giant(void) {
    return size_giant;
}
uint64_t cluster_stat_num_cluster(void) {
    return num_cluster;
}
void cluster_stat_destroy(void) {
    if(uf) uf_destroy(uf);
}




