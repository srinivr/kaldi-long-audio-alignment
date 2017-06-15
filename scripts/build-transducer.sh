#!/bin/bash
. ./path.sh
. ./longaudio_vars.sh
working_dir=$1
input_file=$2
include_skip=$3
if [ $include_skip == "false" ]; then
	echo "doing linear transducer"
	scripts/gen_transducer.py $input_file > $working_dir/G.txt
else
	echo "doing linear transducer with skip connection"
	scripts/gen_transducer.py $input_file --include-skip > $working_dir/G.txt
fi
fstcompile --isymbols=$lang_dir/words.txt --osymbols=$lang_dir/words.txt $working_dir/G.txt | fstdeterminizestar | fstminimize > $lang_dir/G.fst
