# Krippendorff-alpha-for-graph
Compute Krippendorff's alpha for graph, modified from https://github.com/grrrr/krippendorff-alpha/

### Changes
1. Used Networkx to instantiate graph 
2. Added custom node/edge and graph metrics (see below)
3. Forced a pre-computation of distance matrix to boost efficiency for computing, and store it as .npy
   - within-units disagreement (Do) 
   - within- and between-units expected total disagreement (De)
4. Not properly tested, but as long as you have a pandas dataframe that satisfies the following shape, it works.
   - the df has a feature column storing annotated graphs (list of tuples, such as [("subject_1", "predicate_1", "object_1"), ("subject_2", "predicate_2", "object_2")])
   - feature column can also be nodes or edges (tuple of strings)
   - a column indicating annotator id
   - annotation id is ordered the same way for all annotator
5. Note that, distance metric interacts with the networkx graph type when calling instantiate_networkx_graph(). There are the following graph types,
   - nx.Graph
   - nx.DiGraph
   - nx.MultiGraph
   - nx.MultiDiGraph
6. Two categories of distance metric are implemented. 
   - Lenient metric: node/edge or graph overlap
   - Strict metric: nominal metric, graph edit distance
7. Depending on your how many graphs you have, computation of graph distance matrix can take a long time. 

### Python installation
Open your terminal, activate your preferred environment, then type in
```
pip install krippendorff_graph
```

### Node/edge Metrics
#### Lenient metric
1. Node overlap metric: if two sets of nodes or edges overlap, the distance between these two sets is 0; else 1.

#### Strict metric
1. Nominal metric: exact match of two sets of ndoes or edges.

### Graph Metrics
#### Lenient metric
1. Graph overlap metric: if two graphs overlap, the distance between these two sets is 0; else 1.

#### Strict metric
1. Normalized graph edit distance
    - normalized by computing distance between g1 and g0 and between g2 and g0
    - g0 is an empty graph

### Example Usage
###### Compute distance matrix of graphs 
```
import pandas as pd
from krippendorff_graph import compute_alpha, compute_distance_matrix, graph_edit_distance, graph_overlap_metric, nominal_metric

df = pd.DataFrame.from_dict({"annotator": [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4],
                             "narrative": [
                                       ["bla, ela, pla, mla."],["bla, ela, pla, mla."],["bla, ela, pla, mla."],["bla, ela, pla, mla."],
                                       ["bla, ela, pla, mla."],["bla, ela, pla, mla."],["bla, ela, pla, mla."],["bla, ela, pla, mla."], 
                                       ["bla, ela, pla, mla."],["bla, ela, pla, mla."],["bla, ela, pla, mla."],["bla, ela, pla, mla."],
                                       ["bla, ela, pla, mla."],["bla, ela, pla, mla."],["bla, ela, pla, mla."],["bla, ela, pla, mla."]
                             ],
                             "graph_feature": [
                                       {("sub", "pre", "obj")},{("sub1", "pre1", "obj1"), ("sub2", "pre2", "obj2")},{("sub", "pre", "obj")},{("sub", "pre", "obj")},
                                       *,{("sub", "pre", "obj")},{("sub", "pre", "obj")},{("sub", "pre", "obj")}, 
                                       {("sub", "pre", "obj")},{("sub1", "pre1", "obj1"), ("sub2", "pre2", "obj2")},{("sub", "pre", "obj")},{("sub1", "pre1", "obj1"), ("sub2", "pre2", "obj2")},
                                       *,{("sub", "pre", "obj")},{("sub", "pre", "obj")},{("sub1", "pre1", "obj1"), ("sub2", "pre2", "obj2")}
                             ]
                             })
data = [
    df[df["annotator"]==1].graph_feature.to_list(),
    df[df["annotator"]==2].graph_feature.to_list(),
    df[df["annotator"]==3].graph_feature.to_list(),
    df[df["annotator"]==4].graph_feature.to_list()
]

empty_graph_indicator = "*" # indicator for missing values
save_path = "./lenient_distance_matrix.npy"
feature_column="graph_feature"

graph_distance_metric= node_overlap_metric
forced = True

if not Path(save_path).exists() or forced:
    distance_matrix = compute_distance_matrix(df_task2_annotation, feature_column=feature_column, graph_distance_metric=graph_distance_metric, 
                                              empty_graph_indicator=empty_graph_indicator, save_path=save_path, graph_type=nx.Graph)
else: 
    distance_matrix = np.load(save_path)
    
print("Lenient node metric: %.3f" % compute_alpha(data, distance_matrix=distance_matrix, missing_items=empty_graph_indicator))
```

(Please help contributing by making a PR - it will be faster than reporting an issue since the maintainer might be slower than you.) 