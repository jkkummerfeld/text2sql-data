This directory contains the code for seq2seq with attention-based copying from
the input sequence.

Requirements:
- tensorflow==1.3.0 OR tensorflow-gpu==1.3.0
- nltk==3.2.5 and punkt tokenizer models
- numpy==1.13.1
- PyYAML==3.11
- scikit-learn==0.18.2
- scipy==0.19.0
- sqlparse==0.2.4


To run an example, starting from this directory:
```
export S2S_HOME=$(pwd)
./prep_advising.sh
python2 config_builder.py experimental_configs/example_config.yml
cd models/copy_input/advising_query_split/
./experiment.sh
```

Console output for the prep_advising script should look like the contents of `sample_output/expected_prep_script_output.txt`.
Console output for the config_builder should look like `sample_output/expected_config_builder_output.txt`.

The experiment will take several hours to run. Its output will be in `models/copy_input/advising_query_split/quick_eval.txt` (dev set) and `models/copy_input/advising_query_split/quick_eval_train.txt` (train set).
Examples of these output files are in `sample_output/`.

To run your own experiments, modify the `prep_advising.sh` to refer to the dataset
of your choice, and adjust the hyperparameters the config YAML file.
Note that the hyperparameters in example_config.yml are an example only.
Actual hyperparameters used in the paper are available [here](https://github.com/jkkummerfeld/text2sql-data/tree/master/systems/sequence-to-sequence/experimental_configs/hyperparameters).

If you use this code, please cite our ACL paper:
 ```TeX
@InProceedings{data-sql-advising,
  author    = {Catherine Finegan-Dollak, Jonathan K. Kummerfeld, Li Zhang, Karthik Ramanathan, Sesh Sadasivam, Rui Zhang, and Dragomir Radev},
  title     = {Improving Text-to-SQL Evaluation Methodology},
  booktitle = {Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  month     = {July},
  year      = {2018},
  address   = {Melbourne, Victoria, Australia},
  pages     = {351--360},
  url       = {http://aclweb.org/anthology/P18-1033},
}
```

This code is built on top of tf-seq2seq, which is documented [here](https://google.github.io/seq2seq/) and available [here](https://github.com/google/seq2seq) as of July 2018.
