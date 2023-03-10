"""
Script to create a metabolite network from a genome scale metabolic model
"""

# Core library imports
import argparse

# Local imports
import mycogeneexplorer.metabolite_network


def arg_parse() -> argparse.Namespace:
    """
    Function to parse the command line arguments
    :return:
    argparse Namespace arguments
    """
    # Create the parser object
    parser = argparse.ArgumentParser(
        prog="Create Metabolite Network",
        description="Script to translate a genome scale metabolic model into a metabolite network"
    )
    # Add argument for the path to the model file
    parser.add_argument("-i", "--input",
                        dest="input_file",
                        default="",
                        help="Path to file containing genome scale metabolic model")
    # Add argument for path to output
    parser.add_argument("-o", "--output",
                        dest="output_file",
                        default="",
                        help="Path to output file")
    # Add argument for filetype
    parser.add_argument("-f", "--file-type",
                        dest="file_type",
                        default=None,
                        help="File type of the input file")
    # Add argument for if the output should be verbose
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        dest="verbose",
                        default=None,
                        help="Whether output should be verbose")
    # Parse args and return namespace object
    return parser.parse_args()


def main():
    args = arg_parse()
    verbose = args.verbose
    if verbose:
        print("Reading model from file")
    model = mycogeneexplorer.metabolite_network.load_cobra_model_from_file(model=args.input_file,
                                                                           file_type=args.file_type)
    if verbose:
        print("Creating network from model")
    metabolite_network = mycogeneexplorer.metabolite_network.create_metabolite_network(model, verbose=verbose)
    if verbose:
        print("Network created, writing to file")
    mycogeneexplorer.metabolite_network.write_network(metabolite_network, out_path=args.output_file)
    if verbose:
        print("Finished")


if __name__ == "__main__":
    main()
