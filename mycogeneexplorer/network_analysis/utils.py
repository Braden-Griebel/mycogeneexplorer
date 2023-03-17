"""
Module with utility function for working with networkx graph
"""
import json
import re
import warnings
from typing import Union, IO

import cobra
import networkx as nx
import numpy as np


def set_to_element(singleElementSet):
    """
    Returns first element of a set
    :param singleElementSet: Set with a single element
    :return: First element from set
    """
    if len(singleElementSet) != 1:
        warnings.warn("Set is not a single element, returning first element only")
    (element,) = singleElementSet
    return element


def find_intersect(list1, list2):
    """
    Find the intersection between two lists (preserving order based on list1)
    :param list1: First list
    :param list2: Second list
    :return: list with intersection between the two lists
    """
    return [value for value in list1 if value in list2]


def unpack_lengths_generator(gen):
    """
    Returns a np array of lengths from a lengths' generator (from networkx)
    :param gen: Lengths generator from networkx
    :return: array of lengths
    """
    unpacked_list = []
    for i in gen:
        for j in i[1]:
            unpacked_list.append(i[1][j])
    unpacked_array = np.asarray(unpacked_list)
    return unpacked_array


def get_unique_list(list_in):
    """
    Finds unique elements in a given list
    :param list_in: list with possibly repeated elements
    :return: list containing only unique elements
    """
    return list(np.unique(list_in))


def get_connected_graph(graph) -> nx.Graph or nx.DiGraph:
    """
    Find the largest connected component of a graph
    :param graph: A networkx graph or digraph
    :return: largest connected subcomponent as networkx graph
    """
    sub = graph.copy()
    if not nx.is_directed(graph):
        nodes = max(nx.connected_components(graph), key=len)
        sub.remove_nodes_from([n for n in graph if n not in nodes])
    if nx.is_directed(graph):
        nodes = max(nx.strongly_connected_components(graph), key=len)
        sub.remove_nodes_from([n for n in graph if n not in nodes])
    return sub


kgid_dict = {
    "PknA": "Rv0015c",
    "PknB": "Rv0014c",
    "PknD": "Rv0931c",
    "PknE": "Rv1743",
    "PknF": "Rv1746",
    "PknG": "Rv0410c",
    "PknH": "Rv1266c",
    "PknI": "Rv2914c",
    "PknJ": "Rv2088",
    "PknK": "Rv3080c",
    "PknL": "Rv2176"
}
kList = list(kgid_dict.keys())


def load_cobra_model_from_file(model: Union[str, IO], file_type: str = None):
    """
    Loads a cobra model
    :param file_type: Type of file containing cobra file
    :param model:
    :return:
    """
    metabolic_model = None
    if type(model) == str:
        if not file_type:
            file_type = re.findall("\.[a-z]+$", model)[-1][1:]
    if not file_type:
        raise AttributeError("If model isn't str, must provide file_type")
    if file_type in ["JSON", "json", ".json"]:
        metabolic_model = cobra.io.load_json_model(model)
    elif file_type in ["sbml", "xml", "SBML", ".xml"]:
        metabolic_model = cobra.io.read_sbml_model(model)
    elif file_type in ["yaml", ".yml", "YAML"]:
        metabolic_model = cobra.io.load_yaml_model(model)
    elif file_type in ["matlab", "mat", ".mat", "Matlab", "MatLab"]:
        metabolic_model = cobra.io.load_matlab_model(model)
    return metabolic_model


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


def read_network(in_file: Union[str, IO], directed: bool = False) -> Union[nx.Graph, nx.DiGraph]:
    """
    Read in a networkx graph from a json file
    :param in_file: Path or file object where network is stored (json file)
    :param directed: Whether the graph is directed or not
    :return: None
    """
    if type(in_file) == str:
        with open(in_file, "r") as f:
            graph = nx.node_link_graph(json.load(f), directed=directed)
    else:
        graph = nx.node_link_graph(json.load(in_file), directed=directed)
    return graph
