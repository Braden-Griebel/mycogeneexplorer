"""
Contains functions for analyzing the structure of networks using centrality measures
"""
# Core library Imports
from typing import Union
import warnings

# External library imports
import networkx as nx
import pandas as pd


# warning for failure to converge
class convergenceFailure(Warning):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


# warning for graph not connected
class graphNotConnected(Warning):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def degree_centrality(graph: Union[nx.Graph, nx.DiGraph]) -> pd.DataFrame:
    """
    Calculate the degree centrality of a networkx graph
    :param graph: Graph to calculate the centrality of its nodes
    :return: degree_centrality
        A pandas dataframe of the centrality
    """
    centrality = pd.DataFrame.from_dict(nx.degree_centrality(graph),
                                        orient="index",
                                        columns=["degree_centrality"])
    return centrality


def closeness_centrality(graph: Union[nx.Graph, nx.DiGraph], weighted: bool = True) -> pd.DataFrame:
    """
    Calculate the closeness centrality of a networkx graph
    :param weighted: Whether graph is weighted
    :param graph: Graph to calculate the centrality of its nodes
    :return: degree_centrality
        A pandas dataframe of the centrality
    """
    if weighted:
        centrality = pd.DataFrame.from_dict(nx.closeness_centrality(graph, distance="weight"),
                                            orient="index",
                                            columns=["closeness_centrality"])
    else:
        centrality = pd.DataFrame.from_dict(nx.closeness_centrality(graph),
                                            orient="index",
                                            columns=["closeness_centrality"])
    return centrality


def betweeness_centrality(graph: Union[nx.Graph, nx.DiGraph], weighted: bool = True) -> pd.DataFrame:
    """
    Calculate the betweeness centrality of a networkx graph
    :param weighted: Whether graph is weighted
    :param graph: Graph to calculate the centrality of its nodes
    :return: degree_centrality
        A pandas dataframe of the centrality
    """
    if weighted:
        centrality = pd.DataFrame.from_dict(nx.betweenness_centrality(graph, weight="weight"),
                                            orient="index",
                                            columns=["betweeness_centrality"])
    else:
        centrality = pd.DataFrame.from_dict(nx.betweenness_centrality(graph),
                                            orient="index",
                                            columns=["betweeness_centrality"])
    return centrality


def pagerank_centrality(graph: Union[nx.Graph, nx.DiGraph], **kwargs) -> pd.DataFrame:
    """
    Calculate the pagerank centrality of a networkx graph
    :param graph: Graph to calculate the centrality of its nodes
    :param kwargs: keyword args to pass to pagerank function
    :return: degree_centrality
        A pandas dataframe of the centrality
    """
    centrality = pd.DataFrame.from_dict(nx.pagerank(graph, **kwargs),
                                        orient="index",
                                        columns=["pagerank_centrality"])
    return centrality


def eigenvector_centrality(graph: Union[nx.Graph, nx.DiGraph], weighted: bool = True) -> pd.DataFrame:
    """
    Calculate the eigenvector centrality of a networkx graph
    :param weighted: Whether graph is weighted
    :param graph: Graph to calculate the centrality of its nodes
    :return: degree_centrality
        A pandas dataframe of the centrality
    """
    if weighted:
        centrality = pd.DataFrame.from_dict(nx.eigenvector_centrality(graph, weight="weight"),
                                            orient="index",
                                            columns=["eigenvector_centrality"])
    else:
        centrality = pd.DataFrame.from_dict(nx.eigenvector_centrality(graph),
                                            orient="index",
                                            columns=["eigenvector_centrality"])
    return centrality


def information_centrality(graph: Union[nx.Graph, nx.DiGraph], weighted: bool = True) -> pd.DataFrame:
    """
    Calculate the information centrality of a networkx graph
    :param weighted: Whether graph is weighted
    :param graph: Graph to calculate the centrality of its nodes
    :return: degree_centrality
        A pandas dataframe of the centrality
    """
    if weighted:
        centrality = pd.DataFrame.from_dict(nx.information_centrality(graph, weight="weight"),
                                            orient="index",
                                            columns=["information_centrality"])
    else:
        centrality = pd.DataFrame.from_dict(nx.information_centrality(graph),
                                            orient="index",
                                            columns=["information_centrality"])
    return centrality


def load_centrality(graph: Union[nx.Graph, nx.DiGraph], weighted: bool = True) -> pd.DataFrame:
    """
    Calculate the load centrality of a networkx graph
    :param weighted: Whether graph is weighted
    :param graph: Graph to calculate the centrality of its nodes
    :return: degree_centrality
        A pandas dataframe of the centrality
    """
    if weighted:
        centrality = pd.DataFrame.from_dict(nx.load_centrality(graph, weight="weight"),
                                            orient="index",
                                            columns=["load_centrality"])
    else:
        centrality = pd.DataFrame.from_dict(nx.load_centrality(graph),
                                            orient="index",
                                            columns=["load_centrality"])
    return centrality


def find_centrality(graph: Union[nx.Graph, nx.DiGraph],
                    weighted: bool = True,
                    directed: bool = True,
                    verbose: bool = False) -> pd.DataFrame:
    """

    :param directed: Whether graph is directed
    :param verbose: Whether a verbose output is desired
    :param graph: Networkx graph to calculate centrality measures of
    :param weighted: Whether the graph should be treated as weighted
    :return: centrality_dataframe
        Dataframe containing various centrality measures
    """
    centrality_list = []
    if verbose:
        print("Finding Degree Centrality")
    centrality_list.append(degree_centrality(graph))
    if verbose:
        print("Finding Closeness Centrality")
    centrality_list.append(closeness_centrality(graph, weighted))
    if verbose:
        print("Finding Betweeness Centrality")
    centrality_list.append(betweeness_centrality(graph, weighted))
    if verbose:
        print("Finding pagerank Centrality")
    try:
        centrality_list.append(pagerank_centrality(graph))
    except nx.PowerIterationFailedConvergence:
        warnings.warn("Pagerank failed to converge, dropping column", convergenceFailure)
    if verbose:
        print("Finding eigenvector Centrality")
    try:
        centrality_list.append(eigenvector_centrality(graph, weighted))
    except nx.PowerIterationFailedConvergence:
        warnings.warn("Eigenvector centrality failed to converge, dropping column", convergenceFailure)
    if verbose:
        print("Finding Information Centrality")
    if not directed:
        try:
            centrality_list.append(information_centrality(graph, weighted))
        except nx.exception.NetworkXError:
            warnings.warn("Graph isn't connected, dropping information centrality", graphNotConnected)
    if verbose:
        print("Finding Load Centrality")
    centrality_list.append(load_centrality(graph, weighted))
    if verbose:
        print("Found all centrality measures, concatenating dataframe")
    return pd.concat(centrality_list, axis=1)
