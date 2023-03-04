"""
Script to use Mycobrowser data to create dictionaries translating between naming conventions
"""
import argparse
# System Libraries
import json
import os

# External Libraries
import pandas as pd


def parse_args():
    """
    Function to parse the command line arguments
    :return:
        argparse.Namespace object
    """
    # initialize parser
    parser = argparse.ArgumentParser(description="Script to create translation dictionaries between locus, Name, "
                                                 "and UniProt")
    # Add argument for file path
    parser.add_argument("-f", "--f",
                        dest="path",
                        default="../mycogeneexplorer/data/mycobrowser/Mycobacterium_tuberculosis_H37Rv_txt_v4.txt",
                        help="File with locus, UniProt, and Name columns")
    # Add argument for out directory
    parser.add_argument("-o", "--out",
                        dest="out",
                        default="../mycogeneexplorer/data/name_dicts/",
                        help="Directory for the output dictionaries")
    # Add argument for seperator
    parser.add_argument("-s", "--sep",
                        dest="sep",
                        default="\t",
                        help="Seperator in input file")
    return parser.parse_args()


def main():
    """
    Function for
    :return:
        None
    """
    # Read Arguments
    args = parse_args()
    # Read in the mycobrowser release
    mycobrowser = pd.read_table(args.path, sep=args.sep)[["UniProt_AC", "Locus", "Name"]]
    # Create paths for the output dictionaries
    uniprot_out_path = os.path.join(args.out, "uniprot_to_locus.json")
    names_out_path = os.path.join(args.out, "names_to_locus.json")
    locus_list_out_path = os.path.join(args.out, "locus_list.json")
    # Create dictionary objects
    uniprot_to_locus = {}
    name_to_locus = {}
    locus_list = []
    # Find any missing entries in Locus, Name and UniProt_AC
    name_missing = mycobrowser["Name"].isna()
    uniprot_missing = mycobrowser["UniProt_AC"].isna()
    locus_missing = mycobrowser["Locus"].isna()
    # Fill dictionaries and locus_list
    for row in mycobrowser.index:
        # If there is no locus number, just skip
        if locus_missing[row]:
            continue
        locus_list += [mycobrowser.loc[row, "Locus"]]
        if not name_missing[row]:
            name_to_locus[mycobrowser.loc[row, "Name"]] = mycobrowser.loc[row, "Locus"]
        if not uniprot_missing[row]:
            uniprot_to_locus[mycobrowser.loc[row, "UniProt_AC"]] = mycobrowser.loc[row, "Locus"]
    with open(uniprot_out_path, "w") as f:
        json.dump(uniprot_to_locus, f)
    with open(names_out_path, "w") as f:
        json.dump(name_to_locus, f)
    with open(locus_list_out_path, "w") as f:
        json.dump(locus_list, f)


if __name__ == "__main__":
    main()
