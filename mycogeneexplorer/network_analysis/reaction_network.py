"""
Module to create graph representations of genome scale metabolic models
"""
# Core python imports
import itertools
from typing import Sequence

# External library imports
import cobra
import networkx as nx
import numpy as np
import pandas as pd

# Local imports
import mycogeneexplorer.progress_bar
from mycogeneexplorer.network_analysis.utils import load_cobra_model_from_file


# Create a dictionary to map kinases to their gene ids

# Create a list of kinases


def find_edges_from_model(model: cobra.core.model, verbose: bool = False) -> Sequence[tuple]:
    reaction_metabolite_dict = {
        "rxn": [],
        "met": []
    }
    # Iterate through the reactions to find all the associated metabolites
    if verbose:
        print("Finding edges of graph")
        print("Creating dataframe of reactions and metabolites")
        bar = mycogeneexplorer.progress_bar.ProgressBar(total=len(model.reactions), divisions=10)
    for r in model.reactions:
        if verbose:
            bar.inc()
        rxn_name = r.id
        for m in r.metabolites:
            met_name = m.id
            reaction_metabolite_dict["rxn"].append(rxn_name)
            reaction_metabolite_dict["met"].append(met_name)
    rxn_met_df = pd.DataFrame(reaction_metabolite_dict)
    edge_list = []
    if verbose:
        print("Finding which reactions are connected")
        bar = mycogeneexplorer.progress_bar.ProgressBar(total=len(rxn_met_df["met"].unique()), divisions=10)
    # Find all the edges that need to be added and append them to edge_list
    for group, item in rxn_met_df.groupby("met"):
        if verbose:
            bar.inc()
        for i, j in itertools.combinations(list(item["rxn"]), 2):
            if i != j:
                edge_list.append((i, j, {"metabolite": group}))
    if verbose:
        print("Found edges")
    return edge_list


def find_directed_edges_from_model(model: cobra.core.model,
                                   reciprocal_weight: bool = True,
                                   do_loopless: bool = False,
                                   fva_prop: float = 0.95,
                                   verbose: bool = False) -> Sequence[tuple]:
    """
    Find edges for directed graph from cobra metabolic model
    :param verbose: Whether verbose output is desired
    :param model: Cobra genome scale metabolic model
    :param reciprocal_weight: Whether the reciprocal of the weight function should be taken
        (if true, higher metabolite fluxes leads to lower weights)
    :param do_loopless: Whether to perform loopless fva
    :param fva_prop: FVA proportion to pass to flux variability analysis method
    :return: list of edge tuples
    """
    # Perform the flux variability analysis
    if verbose:
        print("Finding edges of graph")
        print("Performing FVA")
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
    if verbose:
        print("Creating Reaction Metabolite Dataframe")
        bar = mycogeneexplorer.progress_bar.ProgressBar(total=len(model.reactions), divisions=10)
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
    if verbose:
        print("Finding edge weights")
        bar = mycogeneexplorer.progress_bar.ProgressBar(total=len(rxn_met_df["met"].unique()), divisions=10)
    # Create the edge_list to hold the edge_tuples
    edge_weight_dict = {
        "source": [],
        "sink": [],
        "weight": [],
        "metabolite": []
    }
    for metabolite, df in rxn_met_df.groupby("met"):
        if verbose:
            bar.inc()
        # First, deal with the reactions which are irreversible
        irreversible_df = df.loc[~df["reversible"]]
        sources_irreversible_df = irreversible_df.loc[(irreversible_df["coefficient"] > 0)].drop(
            ["flux_min", "reversible"], axis=1).rename({"flux_max": "flux"}, axis=1)
        sinks_irreversible_df = irreversible_df.loc[(irreversible_df["coefficient"] < 0)].drop(
            ["flux_min", "reversible"], axis=1).rename({"flux_max": "flux"}, axis=1)
        # Sometimes the flux variability analysis can generate a small negative value, these should be set to 0
        sources_irreversible_df.loc[sources_irreversible_df["flux"] < 0] = 0
        # Now, the reversible reactions
        reversible_df = df.loc[df["reversible"]]
        # Case where the metabolite is a product, and the reaction can operate forward
        reversible_source_pos_coef_df = reversible_df.loc[
            (reversible_df["coefficient"] > 0) & (reversible_df["flux_max"] > 0)].drop(
            ["flux_min", "reversible"], axis=1).rename({"flux_max": "flux"}, axis=1)
        # Case where the metabolite is a reactant, and the reaction can operate in reverse
        #   also change the sign on the coefficient and the flux (flux_min)
        reversible_source_neg_coef_df = reversible_df.loc[
            (reversible_df["coefficient"] < 0) & (reversible_df["flux_min"] < 0)].drop(
            ["flux_max", "reversible"], axis=1).rename({"flux_min": "flux"}, axis=1)
        reversible_source_neg_coef_df["coefficient"] = np.negative(reversible_source_neg_coef_df["coefficient"])
        reversible_source_neg_coef_df["flux"] = np.negative(reversible_source_neg_coef_df["flux"])
        # Now, finding the sinks for the reversible reactions
        # Case where metabolite is a product, and the reaction can operate in reverse
        reversible_sink_pos_coef_df = reversible_df[
            (reversible_df["coefficient"] > 0) & (reversible_df["flux_min"] < 0)].drop(
            ["flux_max", "reversible"], axis=1).rename({"flux_min": "flux"}, axis=1)
        reversible_sink_pos_coef_df["coefficient"] = np.negative(reversible_sink_pos_coef_df["coefficient"])
        reversible_sink_pos_coef_df["flux"] = np.negative(reversible_sink_pos_coef_df["flux"])
        # Case where metabolite is a reactant, and the reaction can operate forward
        reversible_sink_neg_coef_df = reversible_df[
            (reversible_df["coefficient"] < 0) & (reversible_df["flux_max"] > 0)].drop(
            ["flux_min", "reversible"], axis=1).rename({"flux_max": "flux"}, axis=1)
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
    if verbose:
        print("Resolving multiple weights for edges")
        length = len(list(edge_weight_df.groupby(["source", "sink"])))
        bar = mycogeneexplorer.progress_bar.ProgressBar(total=length, divisions=10)
    for (source, sink), df in edge_weight_df.groupby(["source", "sink"]):
        if verbose:
            bar.inc()
        if source != sink:
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
    if verbose:
        print("Found edges")
    return edge_list


def create_reaction_network(model, file_type=None, verbose: bool = False) -> nx.Graph:
    """
    Creates a networkx graph from a cobra genome scale metabolic model
    :param verbose: Whether verbose output is desired
    :param file_type: Type of file being read, must be provided if model is file pointer
    :param model: Genome scale metabolic model, either cobra model or path to file containing one
    :return: Graph: a networkx graph representing the metabolic network
    """
    # Read in the cobra model
    if verbose:
        print("Reading cobra model")
    if not type(model) == cobra.core.Model:
        metabolic_model = load_cobra_model_from_file(model, file_type=file_type)
    else:
        metabolic_model = model
    metabolic_graph = nx.Graph()
    if verbose:
        print("Adding nodes to graph")
    # Add all the reaction names as nodes in the graph
    for rxn in metabolic_model.reactions:
        metabolic_graph.add_node(rxn.id)
    # Now find all the edges that need to be added
    metabolic_graph.add_edges_from(find_edges_from_model(metabolic_model, verbose=verbose))
    if verbose:
        print("Finished creating Metabolic Network")
    return metabolic_graph


def create_directed_reaction_network(model,
                                     file_type=None,
                                     reciprocal_weight: bool = True,
                                     do_loopless: bool = False,
                                     fva_prop: float = 0.95,
                                     verbose: bool = False) -> nx.DiGraph:
    """
    Create a directed graph from a cobra genome scale metabolic model
    :param verbose: Whether output should be verbose
    :param reciprocal_weight: reciprocal_weight: Whether the reciprocal of the weight function should be taken
        (if true, higher metabolite fluxes leads to lower weights)
    :param fva_prop: FVA proportion to pass to flux variability analysis method
    :param do_loopless: Whether to perform loopless fba (can decrease performance significantly)
    :param model: Cobra model, either str, cobra model object, or IO object
    :param file_type: Type of file in which the model is stored
    :return: metabolic_network: nx.DiGraph created from cobra model
    """
    if verbose:
        print("Reading cobra model")
    # Read in the cobra model
    if not type(model) == cobra.core.model.Model:
        metabolic_model = load_cobra_model_from_file(model, file_type=file_type)
    else:
        metabolic_model = model
    metabolic_graph = nx.DiGraph()
    if verbose:
        print("Adding reaction nodes to graph")
    # Add all the reaction names as nodes in the graph
    for rxn in metabolic_model.reactions:
        metabolic_graph.add_node(rxn.id)
    # Find all the edges that need to be added
    metabolic_graph.add_edges_from(
        find_directed_edges_from_model(
            model=metabolic_model,
            reciprocal_weight=reciprocal_weight,
            fva_prop=fva_prop,
            do_loopless=do_loopless,
            verbose=verbose))
    return metabolic_graph
