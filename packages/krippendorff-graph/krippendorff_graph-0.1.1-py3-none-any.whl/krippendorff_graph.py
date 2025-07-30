from itertools import combinations

import numpy as np
import networkx as nx
from tqdm import tqdm
from typing import Optional, Union, Callable


def instantiate_networkx_graph(triples: list[tuple], graph_type=nx.MultiDiGraph):
    G = graph_type()
    for (subj, rel, obj) in triples:
        G.add_edge(subj, obj, relation=rel)
    return G


def nominal_metric(a, b, graph_type=None):
    return a != b


def node_overlap_metric(a, b, graph_type=None):
    return len(a & b) == 0


def graph_overlap_metric(triples_1: list[tuple], triples_2: list[tuple], graph_type=None):
    """
    If two graphs overlaps, distance = 0, else 1.
    """
    return len(list(set(triples_1) & set(triples_2))) == 0


def graph_edit_distance(triples_1: list[tuple], triples_2: list[tuple],
                        graph_type: Optional[
                            Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph]] = nx.MultiDiGraph,
                        timeout: Optional[int] = 60):
    """
    Normalized graph edit distance from networkx.
    """
    g0 = nx.empty_graph()
    g1 = instantiate_networkx_graph(triples_1, graph_type)
    g2 = instantiate_networkx_graph(triples_2, graph_type)
    normalized_ged = nx.graph_edit_distance(g1, g2, timeout=timeout) / (nx.graph_edit_distance(g1, g0, timeout=timeout) + nx.graph_edit_distance(g2, g0, timeout=timeout))
    return normalized_ged


def compute_distance_matrix(df, feature_column: str,
                            graph_distance_metric: Callable,
                            empty_graph_indicator: str = "*",
                            save_path: Optional[str] = "./distance_matrix.npy",
                            graph_type: Optional[
                                Union[nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph]] = nx.MultiDiGraph,
                            timeout: Optional[int] = 60):
    """
    Compute distance matrix with custom graph distance metric from a pandas data frame object.
    A graph must be represented as a list of tuple, such as [("subject_1", "predicate_1", "object_1"), ("subject_2", "predicate_2", "object_2")]

    :param df: a pandas data frame object containing a feature_column storing all graph annotations for all annotators.
    :param feature_column: name of the column storing all graph annotations for all annotators.
    :param graph_distance_metric: a callable function to compute distance between any two graphs.
    :param empty_graph_indicator: a string indicating an empty graph
    :param save_path: local path to store the computed distance matrix
    :param graph_type: a networkx graph type. Bear in mind the interaction between graph type and graph distance metric.
    :return: distance matrix as numpy array.
    """
    distance_matrix = np.zeros(shape=(len(df[feature_column]), len(df[feature_column])))

    graph_pair_indices = list(combinations(range(len(df[feature_column].to_list())), 2))
    for (i, j) in tqdm(graph_pair_indices):
        g1 = df[feature_column].to_list()[i]
        g2 = df[feature_column].to_list()[j]
        if g1 == empty_graph_indicator or g2 == empty_graph_indicator:
            # ignore missing graph annotation by assign 0 distance to other graphs for faster computation by observed and expected disagreement.
            distance_matrix[i][j] = 0
        else:
            d = graph_distance_metric(g1, g2, graph_type=graph_type, timeout=timeout)
            distance_matrix[i][j] = d
            distance_matrix[j][i] = d
    with open(save_path, 'wb') as f:
        np.save(f, distance_matrix)
    return distance_matrix


def construct_units(data: list[dict], missing_items=None):
    # set of constants identifying missing values
    if missing_items is None:
        maskitems = []
    else:
        maskitems = list(missing_items)

    # convert input data to a dict of items
    units = {}
    for d in data:
        try:
            # try if d behaves as a dict
            diter = d.items()
        except AttributeError:
            # sequence assumed for d
            diter = enumerate(d)

        for it, g in diter:
            if g not in maskitems:
                try:
                    its = units[it]
                except KeyError:
                    its = []
                    units[it] = its
                its.append(set(g))
    # A unit is a set of annotation per item
    units = dict((it, d) for it, d in units.items() if len(d) > 1)  # units with pairable values
    return units


def compute_alpha(data: list[dict], distance_matrix: np.array, missing_items=None):
    '''
    Compute Krippendorrf's alpha for graph.
    Modified from https://github.com/grrrr/krippendorff-alpha/tree/master
        1. strictly enforce data to be of type list of dict
        2. requires now a distance matrix for efficient computation

    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    distance_matrix: a numpy array of size number_items*number_items
    missing_items: indicator for missing items (default: None)
    '''
    number_annotator = len(data)
    item_per_annotator = len(data[0])
    units = construct_units(data, missing_items)
    n = sum(len(pv) for pv in units.values())  # number of pairable values
    if n == 0:
        raise ValueError("No items to compare.")

    # Compute within-unit disagreement
    Do = 0
    for item, grades in units.items():
        indices_of_item_all_annotator = [item + (item_per_annotator * i) for i in range(number_annotator)]
        indices = [(i, j) for i in indices_of_item_all_annotator for j in indices_of_item_all_annotator if i != j]
        Du = sum([distance_matrix[i, j] for (i, j) in indices])
        Do += Du / float(len(grades) - 1)

    Do /= float(n)

    # Compute within- and between-unit disagreement (expectation of total disagreement by chance)
    De = 0
    for item_1, g1 in units.items():
        for item_2, g2 in units.items():
            indices_of_item_all_annotator_1 = [item_1 + (item_per_annotator * i) for i in range(number_annotator)]
            indices_of_item_all_annotator_2 = [item_2 + (item_per_annotator * i) for i in range(number_annotator)]
            indices = [(i, j) for i in indices_of_item_all_annotator_1 for j in indices_of_item_all_annotator_2]
            De += sum(distance_matrix[gi, gj] for (gi, gj) in indices)
    De /= float(n * (n - 1))
    alpha = 1 - Do / De if (Do and De) else 1
    return alpha

