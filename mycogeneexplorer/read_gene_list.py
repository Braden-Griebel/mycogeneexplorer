"""
Contains functions to parse a string into a list of genes
"""
# System imports
import json
import re


def parse_list(genes: str) -> list:
    """
    Separates a string into a list of genes
    :param genes:
    :return:
    """
    return re.findall("[a-zA-Z0-9]+", genes)


def translate_list(genes: str,
                   names_to_locus_path: str = "./data/name_dicts/names_to_locus.json",
                   uniprot_to_locus_path: str = "./data/name_dicts/uniprot_to_locus.json",
                   locus_list_path: str = "./data/name_dicts/locus_list.json") -> list:
    """
    Translates list of genes in Name, Locus, or UniProt form to Locus form
    :param names_to_locus_path: Path to names to locus dictionary json
    :param uniprot_to_locus_path: Path to uniprot to locus dictionary json
    :param locus_list_path: Path to locus list json
    :param genes: String with a list of genes seperated by any non-alphanumeric characters
    :return: list of locus tags
    """
    # Parse the genes list
    genes_list = parse_list(genes)
    # read in the dictionaries for translation
    with open(names_to_locus_path, "r") as f:
        names_to_locus = json.load(f)
    with open(uniprot_to_locus_path, "r") as f:
        uniprot_to_locus = json.load(f)
    with open(locus_list_path, "r") as f:
        locus_list = json.load(f)
    final_list = []
    for gene in genes_list:
        if gene in locus_list:
            final_list += [gene]
        elif gene in uniprot_to_locus:
            final_list += [uniprot_to_locus[gene]]
        elif gene in names_to_locus:
            final_list += [names_to_locus[gene]]
    return final_list
