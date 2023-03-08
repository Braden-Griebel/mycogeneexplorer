"""
Script to create Gene Ontology Annotation file (GAF) from mycobrowser data
"""
# System imports
import argparse
import os

# External Library Imports
import pandas as pd


def parse_args():
    """
    Function to parse the command line arguments
    :return:
        argparse.Namespace object
    """
    # initialize parser
    parser = argparse.ArgumentParser(description="Script to create GO annotation for GOAtools file from Mycobrowser "
                                                 "data")
    # Add argument for file path
    parser.add_argument("-f", "--f",
                        dest="path",
                        default=os.path.join("..","mycogeneexplorer",
                                             "data","mycobrowser",
                                             "Mycobacterium_tuberculosis_H37Rv_txt_v4.txt"),
                        help="File with Locus tag and GO terms")
    # Add argument for out directory
    parser.add_argument("-o", "--out",
                        dest="out",
                        default=os.path.join("..","mycogeneexplorer","data","gene_ontology"),
                        help="Output directory")
    # Add argument for seperator
    parser.add_argument("-s", "--sep",
                        dest="sep",
                        default="\t",
                        help="Seperator in input file")
    return parser.parse_args()


def main():
    # Parse command line arguments
    args = parse_args()
    mycobrowser = pd.read_table(args.path, sep=args.sep)[["Locus", "Gene Ontology"]]
    out_path = os.path.join(args.out, "myco.annotation.tab")
    go_terms_na = mycobrowser["Gene Ontology"].isna()
    with open(out_path, "w") as f:
        for row in mycobrowser.index:
            locus = mycobrowser.loc[row, "Locus"]
            if go_terms_na[row]:
                continue
            go_terms = ";".join(mycobrowser.loc[row, "Gene Ontology"].split(","))
            line = f"{locus}\t{go_terms}\n"
            f.write(line)


if __name__ == "__main__":
    main()
