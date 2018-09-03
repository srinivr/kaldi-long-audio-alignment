# kaldi-long-audio-alignment
Long audio alignment using Kaldi i.e chops a long audio and the corresponding transcript into multiple segments such that the transcripts for smaller segment correspond to the small audio segment. It is useful in ASR training since the small segments take much lesser total time compared to using the entire audio at once.

The algorithm is similar to the one in SAILALIGN toolkit (https://github.com/nassosoassos/sail_align).

Refer to "A RECURSIVE ALGORITHM FOR THE FORCED ALIGNMENT OF VERY LONG AUDIO SEGMENTS" and "A SYSTEM FOR AUTOMATIC ALIGNMENT OF BROADCAST MEDIA CAPTIONS USING WEIGHTED FINITE-STATE TRANSDUCERS" to get started.

**NOTE:** Adaptation after each pass has not been implemented yet.

**License:** Apache License 2.0

**Copyright:** Speech Lab (of [Prof. S Umesh](http://www.ee.iitm.ac.in/~umeshs/)), EE department, IIT Madras


<h2>Overview of the tool</h2>

Performs long audio alignment and optionally appends the segmented data to train set.

The input, among others, is a directory containing **only one audio file** i.e wav.scp, utt2spk, spk2utt and text (with the key as "key_1") have only one entry.

There are two top level scripts, **longaudio_multi_dir.sh** and **longaudio_alignment.sh**.

**longaudio_multi_dir.sh** can be used if there are several audio files (and hence several directories) and/or if you want to append the segmented long audio to the train data. However, I am **not** going to explain this script now since I think this usecase could be rare.

<h2>Running longaudio_alignment.sh</h2>

**Step 1:** path.sh, cmd.sh, etc. are needed as you would for running any kaldi experiment.

**Step 2:** Create a file named test_dir_location in the data directory and add the "path_to_test_directory"
e.g: `echo "test_may2015" > data/test_dir_location`

**Step 3:** Change `longaudio_vars.sh` to set the path of your directories.

**Step 4:** longaudio_alignment.sh takes 3 arguments.

`--working-dir` - the directory where temporary files are placed

`--stage` - takes two values. --stage 1 means only iter0 and --stage 2 means additional n-1 iterations (n is specified in longaudio_vars.sh) are performed. 

`--create-dir` - takes true or false. If true, creates a new data folder containing the segments file. 

**example:** `./longaudio_alignment.sh --stage 1 --working-dir data/working_dir_may2015/ --create-dir true`

**Note:** Iterations 0 to n-3 use trigram and iterations n-2 and n-1 are the two passes described in [2] but with a difference. the LM is built only on the exact text which corresponds to the segment rather than from a longer context hence larger deletions are still a problem.


[1]: "A RECURSIVE ALGORITHM FOR THE FORCED ALIGNMENT OF VERY LONG AUDIO SEGMENTS"

[2]: "A SYSTEM FOR AUTOMATIC ALIGNMENT OF BROADCAST MEDIA CAPTIONS USING WEIGHTED FINITE-STATE TRANSDUCERS"
