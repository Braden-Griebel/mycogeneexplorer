"""
Module for analyzing the knock down of genes
"""
# Core library imports
from typing import Union

# External imports
import cobra
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb

# Local imports
from mycogeneexplorer.utils import create_irreversible_model


def find_dependent_reactions(model, gene: Union[str, cobra.Gene]) -> list[cobra.core.Reaction]:
    """
    Find reactions which depend on a given gene
    :param model: Cobra model to find the reactions in
    :param gene: Gene to find effects of knockdown
    :return: reaction_list: List of reactions which depend on a gene
    """
    reaction_list = []
    # If given a gene object, convert it to its id string
    if type(gene) == cobra.core.Gene:
        gene = gene.id
    # for each reaction in the model
    for rxn in model.reactions:
        # determine if the knockout of the gene leads to the reaction being off
        if not rxn.GPR.eval(knockouts=gene):
            # if it does, add it to the reaction_list
            reaction_list.append(rxn)
    # Return list
    return reaction_list


def gene_knockdown(model: cobra.core.Model,
                   genes: Union[str, list[str]],
                   max_flux: str = "min",
                   num: int = 20,
                   fva_prop: float = 0.95,
                   loopless: bool = False,
                   objective_ratio: bool = True,
                   model_irreversible: bool = False) -> pd.DataFrame:
    """
    Determine the effects of the knockdown of a gene or list of genes
    :param model_irreversible: Whether the model is already irreversible
    :param loopless: Whether to perform loopless FVA
    :param fva_prop: Proportion to use for fva
    :param num: number of samples to take
    :param objective_ratio: Whether objective value should be scaled by maximum objective function
    :param model: Cobra model to use
    :param genes: Gene or list of genes to knockdown
    :param max_flux: Value to use as fully on for the reactions,
        can either be the maximum flux for a reaction found through FVA,
        or the minimum
    :return: Dataframe of the objective function value at various knockdown levels
    """
    # Create an irreversible version of the model if needed
    if not model_irreversible:
        irr_model = create_irreversible_model(model)
    else:
        irr_model = model.copy()
    # Get a list of reactions which depend on the gene or genes
    if type(genes) == str:
        reaction_list = find_dependent_reactions(irr_model, genes)
    elif type(genes) == list:
        reaction_list = []
        for g in genes:
            reaction_list.append(find_dependent_reactions(irr_model, g))
    else:
        raise ValueError(f"gene parameter must be either a str or list of str, but was {type(genes)}")
    # Perform FVA to find what the max flux allowed through each reaction should be
    fluxes = cobra.flux_analysis.flux_variability_analysis(irr_model,
                                                           reaction_list,
                                                           loopless=loopless,
                                                           fraction_of_optimum=fva_prop)
    # Create a series which describes the max flux
    if max_flux.upper() in ["MAX", "MAX_FLUX"]:
        fluxes = fluxes["maximum"]
    elif max_flux.upper() in ["MIN", "MIN_FLUX"]:
        fluxes = fluxes["minimum"]
    else:
        raise ValueError("Invalid max_flux specification")
    kd_dict = {
        "knockdown": [],
        "objective": []
    }
    objective_max = 0
    if objective_ratio:
        objective_max = irr_model.slim_optimize()
    for kd in np.linspace(0, 1, num=num):
        kd_dict["knockdown"].append(kd)
        # Use the model as a context so that the changes get reverted
        with irr_model:
            # For the reactions which depend on the gene, knock them down by kd
            for rxn in reaction_list:
                reaction = irr_model.reactions.get_by_id(rxn.id)
                reaction.upper_bound = fluxes[rxn.id] * (1 - kd)
            kd_dict["knockdown"] = kd
            if objective_ratio:
                kd_dict["objective"] = irr_model.slim_optimize() / objective_max
            else:
                kd_dict["objective"] = irr_model.slim_optimize()
    return pd.DataFrame(kd_dict)


def gene_list_knockdown(model: cobra.core.Model,
                        genes: list[str],
                        total_knockdown: bool = False,
                        **kwargs) -> pd.DataFrame:
    """
    Perform knockdown on each of a list of genes, can optionally also knockdown entire list
    :param total_knockdown: Whether to also include results from knocking down all genes simultaneously
    :param model: Cobra model to analyze knockdown with
    :param genes: list of genes to knockdown
    :param kwargs: Keyword arguments passes to gene_knockdown function when it is called
    :return: Dataframe of objective function at various levels of knockdown, with gene column
    """
    # Create a list to hold the dataframes to be concatenated
    df_list = []
    # Create irreversible model
    irr_model = create_irreversible_model(model)
    for gene in genes:
        df = gene_knockdown(model=irr_model, genes=gene, model_irreversible=True, **kwargs)
        df["gene"] = [gene] * len(df)
        df_list.append(df)
    if total_knockdown:
        df_total = gene_knockdown(model=irr_model, genes=genes, model_irreversible=True, **kwargs)
        df_total["gene"] = ["all_kd"] * len(df_total)
        df_list.append(df_total)
    return pd.concat(df_list)


def plot_gene_kd(model: cobra.core.Model, genes: list[str], **kwargs):
    """
    Function to create a plot
    :param model: Cobra model to use
    :param genes: List of genes to knockdown
    :param kwargs: Keyword arguments passed to gene_list_knockdown
    :return: matplotlib figure with the
    """
    # Create figure and axes matplotlib objects
    fig = plt.figure()
    ax = plt.axes()
    # Plot data
    sb.lineplot(data=gene_list_knockdown(model=model,genes=genes, **kwargs),
                x="knockdown", y="objective", hue="gene", style="gene", ax=ax)
    # Return figure
    return fig
