"""
Module for translating a genome scale metabolic network into a metabolite network
"""
from __future__ import annotations

# Core Library Imports
import itertools
import json
from typing import IO, Union

# External Library imports
import cobra
import networkx as nx

# Local imports
from reaction_network import load_cobra_model_from_file
import progress_bar


def find_edges_from_model(model: cobra.core.model, verbose) -> list:
    """
    Find edges between metabolites from a cobra genome scale metabolic model
    :param verbose: Whether verbose output is desired
    :param model: Genome Scale Metabolic Model
    :return: edge_list: List of tuples with edge information
    """
    if verbose:
        print("Finding edges")
        bar = progress_bar.ProgressBar(total=len(model.reactions), divisions=10)
    edge_list = []
    for rxn in model.reactions:
        if verbose:
            bar.inc()
        rxn_name = rxn.id
        sources = []
        targets = []
        reversibility = rxn.reversibility
        for met in rxn.metabolites:
            met_name = met.id
            if not reversibility:
                if rxn.get_coefficient(met_name) < 0:
                    sources.append(met_name)
                elif rxn.get_coefficient(met_name) > 0:
                    targets.append(met_name)
            else:
                sources.append(met_name)
                targets.append(met_name)
        for source, target in itertools.product(sources, targets):
            if source != target:
                edge_list.append((source, target, {"reaction": rxn_name}))
    if verbose:
        print("Found edges")
    return edge_list


def create_metabolite_network(model: Union[str, IO, cobra.core.model],
                              file_type: str = None,
                              verbose: bool = False) -> nx.DiGraph:
    """
    Create a metabolite network from a genome scale metabolic model
    :param model: Genome scale metabolic model, can be cobra model, path string to file, or file pointer
    :param file_type: Type of file the model is in
    :param verbose: Whether verbose output is desired
    :return: metabolite_network: networkx graph representing metabolite network
    """
    if not type(model) == cobra.core.model.Model:
        metabolic_model = load_cobra_model_from_file(model, file_type=file_type)
    else:
        metabolic_model = model
    metabolite_network = nx.DiGraph()
    if verbose:
        print("Adding nodes to graph")
    for met in metabolic_model.metabolites:
        metabolite_network.add_node(met.id)
    if verbose:
        print("Adding edges to graph")
    metabolite_network.add_edges_from(find_edges_from_model(metabolic_model, verbose))
    return metabolite_network


def write_network(network: Union[nx.Graph, nx.DiGraph],
                  out_path: str,
                  ) -> None:
    """
    Writes a networkx graph to the out_path, a json file
    :param network: metabolic network
    :param out_path: path to write the network to
    :return: None
    """
    with open(out_path, "w") as f:
        json.dump(nx.node_link_data(network), f)


def read_network(in_file: Union[str, IO]) -> nx.DiGraph:
    """
    Read in a networkx graph from a json file
    :param in_file: Path or file object where network is stored (json file)
    :return: None
    """
    if type(in_file) == str:
        with open(in_file, "r") as f:
            graph = nx.node_link_graph(json.load(f), directed=True)
    else:
        graph = nx.node_link_graph(json.load(in_file), directed=True)
    return graph
