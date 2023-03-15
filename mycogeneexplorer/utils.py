"""
Module containing utility functions
"""
import cobra.core


def create_irreversible_model(model: cobra.core.Model):
    """
    Creates a model with only irreversible reactions,
    splits reversible reactions into forward and reverse reactions.
    Does not modify model argument
    :param model: A cobra model to be changed
    :return: irr_model: A model with all reversible reactions split into forward and reverse reactions
    """
    irr_model = model.copy()
    for rxn in irr_model.reactions:
        # If this reaction is not reversible, no changes need to be made
        if not rxn.reversibility:
            continue
        # Find the bounds of the current reaction
        lower_bound, upper_bound = rxn.bounds
        # Split the bounds into forward and reverse
        forward_bounds = (0, upper_bound)
        reverse_bounds = (0, -lower_bound)
        # Create dictionary of metabolites for the reverse reaction
        reverse_metabolites = {}
        for metabolite, coefficient in rxn.metabolites:
            reverse_metabolites[metabolite] = -coefficient
        reverse_reaction = cobra.core.Reaction(f"{rxn.id}_reverse")
        # Add metabolites to reaction
        reverse_reaction.add_metabolites(reverse_metabolites)
        # Set reverse reaction bounds
        reverse_reaction.bounds = reverse_bounds
        # set forward reaction bounds
        rxn.bounds = forward_bounds
        # Set reverse reactions gpr to be the same as the forward reaction
        reverse_reaction.gpr = rxn.gpr
