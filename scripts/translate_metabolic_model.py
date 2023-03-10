"""
Script to translate Genome Scale Metabolic Models from one format to another
"""
# Standard Library Imports
import argparse

# External Library
import cobra


def parse_args():
    """
    Parse command line arguments
    :return:argparse.Namespace object with arguments
    """
    # Create parser
    parser = argparse.ArgumentParser(description="Translate between Genome Scale Metabolic Model formats")
    parser.add_argument("-f", "--file-input",
                        dest="input_file",
                        help="Path to input file")
    parser.add_argument("-o", "--output-path",
                        dest="output_path",
                        help="Path to output translated model")
    parser.add_argument("-i", "--input-format",
                        dest="input_format",
                        help="Format of input file")
    parser.add_argument("-t", "--translate-to",
                        dest="output_format",
                        help="Format to translate model to")
    return parser.parse_args()


def main():
    # Parse the command line arguments into args object
    args = parse_args()
    # Determine format and read in model
    model = None
    if args.input_format in ["json", "JSON", "Json", ".json"]:
        model = cobra.io.load_json_model(args.input_file)
    elif args.input_format in ["sbml", "SBML", "Sbml", "xml", "XML", ".xml"]:
        model = cobra.io.read_sbml_model(args.input_file)
    elif args.input_format in ["yaml", "YAML", "Yaml", ".yml", ".ymal"]:
        model = cobra.io.load_yaml_model(args.input_file)
    elif args.input_format in ["MAT", "M", "m", ".m", ".mat", "mat"]:
        model = cobra.io.load_matlab_model(args.input_file)
    # Determine output format, and write the translated model
    if args.output_format in ["json", "JSON", "Json", ".json"]:
        cobra.io.save_json_model(model, args.output_path)
    elif args.output_format in ["sbml", "SBML", "Sbml", "xml", "XML", ".xml"]:
        cobra.io.write_sbml_model(model, args.output_path)
    elif args.output_format in ["yaml", "YAML", "Yaml", ".yml", ".ymal"]:
        cobra.io.save_yaml_model(model, args.output_path)
    elif args.output_format in ["MAT", "M", "m", ".m", ".mat", "mat"]:
        cobra.io.save_matlab_model(model, args.output_path)


if __name__ == "__main__":
    main()
