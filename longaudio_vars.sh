# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

set -e
data_dir=`cat data/test_dir_location`
lang_dir=data/lang_test
model_dir=exp_expanded/tri2_1200_14400
graph_dir=$model_dir/graph
island_length=5
num_iters=2
