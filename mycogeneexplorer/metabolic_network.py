"""
Module to create graph representations of genome scale metabolic models
"""
import itertools
import json
import re
import warnings
from typing import IO, Sequence, Union

import cobra
import networkx as nx
import numpy as np
import pandas as pd


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


# Create a dictionary to map kinases to their gene ids
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

# Create a list of kinases
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


def find_edges_from_model(model) -> Sequence[tuple]:
    reaction_metabolite_dict = {
        "rxn": [],
        "met": []
    }
    # Iterate through the reactions to find all the associated metabolites
    for r in model.reactions:
        rxn_name = r.id
        for m in r.metabolites:
            met_name = m.id
            reaction_metabolite_dict["rxn"].append(rxn_name)
            reaction_metabolite_dict["met"].append(met_name)
    rxn_met_df = pd.DataFrame(reaction_metabolite_dict)
    edge_list = []
    # Find all the edges that need to be added and append them to edge_list
    for group, item in rxn_met_df.groupby("met"):
        for i, j in itertools.combinations(list(item["rxn"]), 2):
            edge_list.append((i, j, {"metabolite": group}))
    return edge_list


def find_directed_edges_from_model(model: cobra.core.model,
                                   reciprocal_weight: bool = True,
                                   do_loopless: bool = False,
                                   fva_prop: float = 0.95) -> Sequence[tuple]:
    """
    Find edges for directed graph from cobra metabolic model
    :param model: Cobra genome scale metabolic model
    :param reciprocal_weight: Whether the reciprocal of the weight function should be taken
        (if true, higher metabolite fluxes leads to lower weights)
    :param do_loopless: Whether to perform loopless fva
    :param fva_prop: FVA proportion to pass to flux variability analysis method
    :return: list of edge tuples
    """
    # Perform the flux variability analysis
    fva_results = cobra.flux_analysis.flux_variability_analysis(model, loopless=do_loopless,
                                                                fraction_of_optimum=fva_prop,
                                                                processes=1)
    edge_dict = {
        "rxn": [],
        "met": [],
        "reversible": [],
        "coefficient": [],
        "flux_max": [],
        "flux_min": []
    }
    for rxn in model.reactions:
        rxn_name = rxn.id
        for met in rxn.metabolites:
            met_name = met.id
            edge_dict["rxn"] += [rxn_name]
            edge_dict["met"] += [met_name]
            edge_dict["reversible"] += [rxn.reversibility]
            edge_dict["coefficient"] += [rxn.get_coefficient(met_name)]
            edge_dict["flux_max"] += [fva_results.loc[rxn_name, "maximum"]]
            edge_dict["flux_min"] += [fva_results.loc[rxn_name, "minimum"]]
    # Create a dataframe from the edge_dict
    rxn_met_df = pd.DataFrame(edge_dict)
    # Create the edge_list to hold the edge_tuples
    edge_weight_dict = {
        "source": [],
        "sink": [],
        "weight": [],
        "metabolite": []
    }
    for metabolite, df in rxn_met_df.groupby("met"):
        # First, deal with the reactions which are irreversible
        irreversible_df = df.loc[~df["reversible"]]
        sources_irreversible_df = irreversible_df.loc[(irreversible_df["coefficient"] > 0)].drop(
            "flux_min", axis=1).rename({"flux_max": "flux"}, axis=1)
        sinks_irreversible_df = irreversible_df.loc[(irreversible_df["coefficient"] < 0)].drop(
            "flux_min", axis=1).rename({"flux_max": "flux"}, axis=1)
        # Now, the reversible reactions
        reversible_df = df.loc[df["reversible"]]
        # Case where the metabolite is a product, and the reaction can operate forward
        reversible_source_pos_coef_df = reversible_df.loc[
            (reversible_df["coefficient"] > 0) & (reversible_df["flux_max"] > 0)].drop(
            "flux_min", axis=1).rename({"flux_max": "flux"}, axis=1)
        # Case where the metabolite is a reactant, and the reaction can operate in reverse
        #   also change the sign on the coefficient and the flux (flux_min)
        reversible_source_neg_coef_df = reversible_df.loc[
            (reversible_df["coefficient"] < 0) & (reversible_df["flux_min"] < 0)].drop(
            "flux_max", axis=1).rename({"flux_min": "flux"}, axis=1)
        reversible_source_neg_coef_df["coefficient"] = np.negative(reversible_source_neg_coef_df["coefficient"])
        reversible_source_neg_coef_df["flux"] = np.negative(reversible_source_neg_coef_df["flux"])
        # Now, finding the sinks for the reversible reactions
        # Case where metabolite is a product, and the reaction can operate in reverse
        reversible_sink_pos_coef_df = reversible_df[
            (reversible_df["coefficient"] > 0) & (reversible_df["flux_min"] < 0)].drop(
            "flux_max", axis=1).rename({"flux_min": "flux"}, axis=1)
        reversible_sink_pos_coef_df["coefficient"] = np.negative(reversible_sink_pos_coef_df["coefficient"])
        reversible_sink_pos_coef_df["flux"] = np.negative(reversible_sink_pos_coef_df["flux"])
        # Case where metabolite is a reactant, and the reaction can operate forward
        reversible_sink_neg_coef_df = reversible_df[
            (reversible_df["coefficient"] < 0) & (reversible_df["flux_max"] > 0)].drop(
            "flux_min", axis=1).rename({"flux_max": "flux"}, axis=1)
        source_df = pd.concat([sources_irreversible_df,
                               reversible_source_pos_coef_df,
                               reversible_source_neg_coef_df], axis=0)
        sinks_df = pd.concat([sinks_irreversible_df,
                              reversible_sink_pos_coef_df,
                              reversible_sink_neg_coef_df], axis=0)
        for source, sink in itertools.product(source_df["rxn"], sinks_df["rxn"]):
            edge_weight_dict["source"] += [source]
            edge_weight_dict["sink"] += [sink]
            edge_weight_dict["metabolite"] += [metabolite]
            if reciprocal_weight:
                edge_weight_dict["weight"] += [
                    np.reciprocal((source_df.loc[source_df["rxn"] == source, "flux"] *
                                   source_df.loc[source_df["rxn"] == source, "coefficient"]).values[0] +
                                  np.power(10., -30))]
            else:
                edge_weight_dict["weight"] += [
                    (source_df.loc[source_df["rxn"] == source, "flux"] *
                     source_df.loc[source_df["rxn"] == source, "coefficient"]).values[0]]
    edge_weight_df = pd.DataFrame(edge_weight_dict)
    edge_list = []
    for (source, sink), df in edge_weight_df.groupby(["source", "sink"]):
        if len(df) == 1:
            edge_list.append((source, sink, {"weight": df["weight"].values[0],
                                             "metabolite": df["metabolite"].values[0]}))
        else:
            if reciprocal_weight:
                min_rows = df.loc[df["weight"] == df["weight"].min()]
                min_row = min_rows.iloc[0]
                edge_list.append((source, sink, {"weight": min_row["weight"], "metabolite": min_row["metabolite"]}))
            else:
                max_rows = df.loc[df["weight"] == df["weight"].max()]
                max_row = max_rows.iloc[0]
                edge_list.append((source, sink, {"weight": max_row["weight"], "metabolite": max_row["metabolite"]}))
    return edge_list


def create_metabolic_network(model, file_type=None) -> nx.Graph:
    """
    Creates a networkx graph from a cobra genome scale metabolic model
    :param file_type: Type of file being read, must be provided if model is file pointer
    :param model: Genome scale metabolic model, either cobra model or path to file containing one
    :return: Graph: a networkx graph representing the metabolic network
    """
    # Read in the cobra model
    if not type(model) == cobra.core.Model:
        metabolic_model = load_cobra_model_from_file(model, file_type=file_type)
    else:
        metabolic_model = model
    metabolic_graph = nx.Graph()
    # Add all the reaction names as nodes in the graph
    for rxn in metabolic_model.reactions:
        metabolic_graph.add_node(rxn.id)
    # Now find all the edges that need to be added
    metabolic_graph.add_edges_from(find_edges_from_model(metabolic_model))
    return metabolic_graph


def create_directed_metabolic_network(model,
                                      file_type=None,
                                      reciprocal_weight: bool = True,
                                      do_loopless: bool = False,
                                      fva_prop: float = 0.95) -> nx.DiGraph:
    """
    Create a directed graph from a cobra genome scale metabolic model
    :param reciprocal_weight: reciprocal_weight: Whether the reciprocal of the weight function should be taken
        (if true, higher metabolite fluxes leads to lower weights)
    :param fva_prop: FVA proportion to pass to flux variability analysis method
    :param do_loopless: Whether to perform loopless fba (can decrease performance significantly)
    :param model: Cobra model, either str, cobra model object, or IO object
    :param file_type: Type of file in which the model is stored
    :return: metabolic_network: nx.DiGraph created from cobra model
    """
    # Read in the cobra model
    if not type(model) == cobra.core.model.Model:
        metabolic_model = load_cobra_model_from_file(model, file_type=file_type)
    else:
        metabolic_model = model
    metabolic_graph = nx.DiGraph()
    # Add all the reaction names as nodes in the graph
    for rxn in metabolic_model.reactions:
        metabolic_graph.add_node(rxn.id)
    # Find all the edges that need to be added
    metabolic_graph.add_edges_from(
        find_directed_edges_from_model(
            model=metabolic_model,
            reciprocal_weight=reciprocal_weight,
            fva_prop=fva_prop,
            do_loopless=do_loopless))
    return metabolic_graph


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
