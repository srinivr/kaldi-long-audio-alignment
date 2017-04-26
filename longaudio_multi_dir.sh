#!/bin/bash
# create a new directory for training data by:
#	making approximately 15 seconds length segments from word timing information obtained by doing 0th iteration for the given directories
#	note: include unaligned words whenever possible
set -e
. ./path.sh
update_train_dir=false
train_dir=data/train
train_dict=data/local/dict
test_dict=data/local/dict_test
train_lang=data/lang
test_lang=data/lang_test
new_train_dir=data/train_expanded # to be created
log_dir=log
#for x in aug2015 dec2014 dec2015 july2015 may2015 nov2014 oct2014 sep2015;do
mkdir -p $log_dir
for x in may2015; do
	echo "data/test_${x}">data/test_dir_location
	echo `cat dir_location`
	./longaudio_alignment.sh --working-dir data/working_dir_${x} --stage 1
	echo "finished long audio alignment $x"
done;
mkdir -p $new_train_dir
if [ "$update_train_dir" = true ]; then
	echo "in update train"
	# copy test lexicon to train lexicon, prepare_lang
	cat $test_dict/lexicon.txt >> $train_dict/lexicon.txt
	cp $train_dict/lexicon.txt $train_dict/lexicon.txt.bkp
	sort -u <  $train_dict/lexicon.txt.bkp >  $train_dict/lexicon.txt
	rm  $train_dict/lexicon.txt.bkp  $train_dict/lexiconp.txt
	mv $train_lang ${train_lang}.bkp
	cat $train_dict/lexicon.txt | cut -d' ' -f2- | sed 's/ /\n/g' | grep -v '^$' | grep -v 'sil' | sort -u > $train_dict/nonsilence_phones.txt
	utils/prepare_lang.sh $train_dict sil tmpdir $train_lang >> $log_dir/output.log 2> $log_dir>err.log # sil is the <oov-dict-entry> change it match your settings

	cp $train_dir/* $new_train_dir
	rm $new_train_dir/cmvn.scp $new_train_dir/feats.scp
	# create segments file for train_dir if it does not exist
	if [ ! -f $new_train_dir/segments ]; then
		wav-to-duration scp:$new_train_dir/wav.scp ark,t:$new_train_dir/wav_duration >> $log_dir/output.log 2> $log_dir>err.log
		cut -d ' ' -f1 < $new_train_dir/wav_duration > $new_train_dir/wav_duration.1
		cut -d ' ' -f2 < $new_train_dir/wav_duration > $new_train_dir/wav_duration.2
		paste -d ' ' $new_train_dir/wav_duration.1 $new_train_dir/wav_duration.1 | sed 's/$/ 0.0/g' > $new_train_dir/wav_duration.3
		paste -d ' ' $new_train_dir/wav_duration.3 $new_train_dir/wav_duration.2 > $new_train_dir/segments
		rm $new_train_dir/wav_duration*
		# check the following steps. can we keep the original utt2spk and spk2utt?!
		rm $new_train_dir/utt2spk $new_train_dir/spk2utt
		cut -d ' ' -f1 $new_train_dir/segments > $new_train_dir/utt
		paste -d ' ' $new_train_dir/utt $new_train_dir/utt > $new_train_dir/utt2spk
		cp $new_train_dir/utt2spk $new_train_dir/spk2utt
		rm $new_train_dir/utt
	fi
fi
#for x in aug2015 dec2014 dec2015 july2015 june2015 may2015 nov2014 oct2014 sep2015;do
for x in may2015; do
	scripts/timing_to_segment_and_text.py data/working_dir_${x}/WORD_TIMINGS.words $x $new_train_dir/segments.${x} $new_train_dir/text.${x} `wav-to-duration scp:data/test_may2015/wav.scp ark,t:- | cut -d' ' -f2`
	ls $new_train_dir/segments.${x} $new_train_dir/text.${x}
	echo "${x} `cat data/test_${x}/wav.scp|cut -d' ' -f2-`" >> $new_train_dir/wav.scp
	cat $new_train_dir/text.${x} >> $new_train_dir/text
	cat $new_train_dir/segments.${x} >> $new_train_dir/segments
#	cut -d ' ' -f1 $new_train_dir/segments.${x} > $new_train_dir/utt
#	paste -d ' ' $new_train_dir/utt $new_train_dir/utt >> $new_train_dir/utt2spk
#	paste -d ' ' $new_train_dir/utt $new_train_dir/utt >> $new_train_dir/spk2utt
	cut -d ' ' -f1 $new_train_dir/segments.${x} | sed "\"s/$/ $x/g\"" >> $new_train_dir/utt2spk
	cut -d ' ' -f1 $new_train_dir/segments.${x} | sed "\"s/^/$x /g\"" >> $new_train_dir/spk2utt
	rm $new_train_dir/utt
done;
utils/validate_data_dir.sh $new_train_dir # not expected to succeed. Just to display any mismatch in number of lines,etc.
# update utt2spk, spk2utt
