"""
Script to create metabolic graphs from the genome scale metabolic models
"""
# Core Library Imports
import argparse

# local imports
import mycogeneexplorer.metabolic_network as mn


def arg_parse() -> argparse.Namespace:
    """
    Function to parse the command line arguments provided to this script
    :return:
    argparse Namespace arguments
    """
    # Create the parser object
    parser = argparse.ArgumentParser()
    # Add argument for path to the model file
    parser.add_argument("-i", "--input",
                        dest="input_file",
                        default="",
                        help="Path to file containing the genome scale metabolic model")
    # Add argument for the path to the output
    parser.add_argument("-o", "--output",
                        dest="output_file",
                        default="",
                        help="Desired output file")
    # Add argument for filetype
    parser.add_argument("-f", "--file-type",
                        dest="file_type",
                        default=None,
                        help="File type of the input file")
    # Add argument for if the network should be directed (and weighted)
    parser.add_argument("-d", "--directed",
                        action="store_true",
                        dest="directed",
                        default=False,
                        help="Flag indicating whether output should be directed")
    # Add argument for whether output should be verbose
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        dest="verbose",
                        default=False,
                        help="Flag indicating verbose output desired")
    # Add argument for whether reciprocal weight should be used
    parser.add_argument("-r", "--reciprocal",
                        action="store_true",
                        dest="reciprocal",
                        default=True,
                        help="Flag indicating used of reciprocal of flux for the weight")
    # Add argument for fva_proportion using in flux variability analysis
    parser.add_argument("-p", "--fva-proportion",
                        dest="fva_prop",
                        default=0.95,
                        help="Proportion for use in flux variability analysis")
    # Add Argument for whether to perform loopless FVA
    parser.add_argument("-l", "--loopless",
                        action="store_true",
                        dest="loopless",
                        default=False,
                        help="Flag indicating whether loopless FVA should be performed")
    # Parse args and return namespace object
    return parser.parse_args()


def main():
    args = arg_parse()
    verbose = args.verbose
    if verbose:
        print("Reading model from file")
    model = mn.load_cobra_model_from_file(model=args.input_file, file_type=args.file_type)
    if verbose:
        print("Creating network from model")
    if args.directed:
        metabolic_network = mn.create_directed_metabolic_network(model,
                                                                 reciprocal_weight=args.reciprocal,
                                                                 do_loopless=args.loopless,
                                                                 fva_prop=args.fva_prop,
                                                                 verbose=verbose)
    else:
        metabolic_network = mn.create_metabolic_network(model, verbose=verbose)
    if verbose:
        print("Network created, writing to file")
    mn.write_network(metabolic_network, out_path=args.output_file)
    if verbose:
        print("Finished")


if __name__ == "__main__":
    main()
