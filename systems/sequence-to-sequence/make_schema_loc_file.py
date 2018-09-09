import argparse
import os

def write_schema_locs(schema_loc, name, dataset_loc):
  with open(os.path.join(dataset_loc, "%s/%s_encode.txt" %(name, name)), 'r') as f:
    lines = f.readlines()
  with open(os.path.join(dataset_loc, "%s/%s_schema_locations.txt" %(name, name)), 
            'w') as f:
    for l in lines:
      f.write(schema_loc + "\n")


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description='Given a dataset location and a schema location, add schema_loc files to train, dev, and test that simply list the same schema location as many times as the dataset requires.')
    parser.add_argument(
        'dataset_loc', 
        help='location of dataset (folder containing train/ dev/ and test/')
    parser.add_argument(
        'schema_loc', 
        help='location of schema (should contain csv, embeddings, and map files')

    args = parser.parse_args()

    for dataset in ["train", "dev", "test"]:
        write_schema_locs(args.schema_loc, dataset, args.dataset_loc)
