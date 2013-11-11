#ifndef CLUSTER_STATISTICS_H
#define CLUSTER_STATISTICS_H
#include <stdint.h>
uint8_t cluster_stat_init_cubic(uint64_t);
uint64_t cluster_stat_analyse_cubic(void *, uint64_t);
void cluster_stat_destroy(void);

double cluster_stat_log_csm2(void);
double cluster_stat_log_csm4(void);
uint64_t cluster_stat_size_giant(void);
uint64_t cluster_stat_num_cluster(void);

#endif /*CLUSTER_STATISTICS_H*/
