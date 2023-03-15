"""
Module with functions to analyze the metabolites of a genome scale metabolic model
"""
# Core library

# External libraries
import cobra

# Local imports


def find_metabolite_gene_essentiality(model: cobra.core.Model, genes: list,
                                      essentiality_prop: float = 0.95) -> dict:
    """
    Find which metabolites depend on provided gene list
    :param essentiality_prop: Proportion of growth defect for a gene to be considered essential,
        i.e., 0.95 would indicate a growth less than 5% maximum would be a growth defect
    :param genes: List of genes to find which metabolites that depend on them
    :param model: Cobra model to use for analysis
    :return: Dict of gene:list of metabolites that depend on that gene
    """
    # Create a copy of the model so that it remains unchanged
    metabolic_model = model.copy()
    # Crete the dictionary
    essentiality_dict = {}
    for gene in genes:
        essentiality_dict[gene] = []
    # Go through all metabolites in the model
    for metabolite in metabolic_model.metabolites:
        # Use model as context so that changes are reverted
        # Add a demand for the metabolite
        metabolic_model.add_boundary(metabolite, "demand", f"{metabolite.id}_demand")
        # Set this metabolite demand as the objective function
        metabolic_model.objective = f"{metabolite.id}_demand"
        # Find the maximum that this can take on to find essential genes
        max_objective = metabolic_model.slim_optimize()
        # Perform single gene knockdown
        results = cobra.flux_analysis.single_gene_deletion(metabolic_model, genes)
        # Find the proportion of maximum growth that can be achieved after the knockdown
        results["growth"] = results["growth"]/max_objective
        # Find the essential genes
        essential = results[results["growth"] <= (1-essentiality_prop)]
        # Add the metabolite to the list in the dictionary for all essential genes
        for row in essential:
            gene, = row["ids"]
            essentiality_dict[gene].append(metabolite.id)
    return essentiality_dict
