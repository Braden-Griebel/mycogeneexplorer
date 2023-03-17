"""
Script to compute all centrality metrics, and write the data to a csv or parquet file
"""

# Core library imports
import argparse
import warnings

# External library imports
import pyarrow

# Local imports
import mycogeneexplorer.network_analysis.centrality as cn
from mycogeneexplorer.network_analysis import utils


# Define warning for when dataframe can't be converted to parquet file
class parquetConversionError(Warning):
    """
    Error for when the dataframe can't be converted to a parquet file
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def parse_args():
    """
    Function to parse the command line arguments
    :return: argparse namespace object
    """
    # Create parser
    parser = argparse.ArgumentParser(
        prog="Compute Centrality",
        usage="Script to compute centrality metrics of a provided networkx graph"
    )
    parser.add_argument("-g", "--graph-path",
                        dest="graph_path",
                        default=None,
                        help="Path to graph")
    parser.add_argument("-o", "--output",
                        dest="output_path",
                        default=None,
                        help="Desired output path, not including file extension")
    parser.add_argument("-f", "--output-format",
                        dest="output_format",
                        default="csv",
                        help="Desired format for output, can be csv, parquet, or both")
    parser.add_argument("-w", "--weighted",
                        dest="weighted",
                        action="store_true",
                        default=False,
                        help="Flag for whether graph should be treated as weighted")
    parser.add_argument("-d", "--directed",
                        action="store_true",
                        dest="directed",
                        default=False,
                        help="Flag for whether graph is directed")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        dest="verbose",
                        default=False,
                        help="Flag for whether verbose output is desired")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        print("Reading network")
    graph = utils.read_network(args.graph_path)
    if args.verbose:
        print("Finding Centrality")
    centrality_dataframe = cn.find_centrality(graph,
                                              weighted=args.weighted,
                                              verbose=args.verbose,
                                              directed=args.directed)
    if args.verbose:
        print("Writing dataframe to file")
    if args.output_format.lower() in ["csv", ".csv"]:
        centrality_dataframe.to_csv(args.output_path + ".csv")
    elif args.output_format.lower() in ["parquet", ".parquet"]:
        try:
            centrality_dataframe.to_parquet(args.output_path + ".parquet")
        except pyarrow.lib.ArrowTypeError:
            warnings.warn("Couldn't Convert to Parquet", parquetConversionError)
    elif args.output_format.lower() in ["both"]:
        centrality_dataframe.to_csv(args.output_path + ".csv")
        try:
            centrality_dataframe.to_parquet(args.output_path + ".parquet")
        except pyarrow.lib.ArrowTypeError:
            warnings.warn("Couldn't convert to Parquet", parquetConversionError)
    else:
        raise ValueError("Couldn't Parse Output Format, should be 'csv', 'parquet' or 'both'")
    if args.verbose:
        print("Finished!")


if __name__ == "__main__":
    main()
