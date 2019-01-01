#!/bin/bash
for i in 1 10001 1001 10201 10401 10601 10801 11001 11201 11401 11601 11801 12001 1201 12201 12401 12601 12801 13001 13201 13401 13601 13801 14001 1401 14201 14401 14601 14801 15000 1601 1801 2001 201 2201 2401 2601 2801 3001 3201 3401 3601 3801 4001 401 4201 4401 4601 4801 5001 5201 5401 5601 5801 6001 601 6201 6401 6601 6801 7001 7201 7401 7601 7801 8001 801 8201 8401 8601 8801 9001 9201 9401 9601 9801
do
  python -m bin.infer \
  --tasks "
    - class: DecodeText" \
  --model_dir $MODEL_DIR \
  --input_pipeline "
    class: ParallelTextAndSchemaCopyingPipeline
    params:
      source_files:
        - $DEV_SOURCES
        - $TRAIN_SOURCES
      schema_file:
        - $SCHEMA_LOC" \
   --checkpoint_path ${MODEL_DIR}/model.ckpt-$i \
  >  ${PRED_DIR}/predictions-$i.txt
done
