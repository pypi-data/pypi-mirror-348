from typing                          import Dict, Set, Any, Type
from osbot_utils.helpers.Obj_Id      import Obj_Id
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Schema__MGraph__Change__Data(Type_Safe):                      # For node data changes
    from_value : Dict[str, Any]
    to_value   : Dict[str, Any]

class Schema__MGraph__Change__Type(Type_Safe):                      # For type changes
    from_value : Type
    to_value   : Type

class Schema__MGraph__Change__Node(Type_Safe):                      # For node reference changes
    from_value : Obj_Id
    to_value   : Obj_Id

class Schema__MGraph__Node__Changes(Type_Safe):
    data : Schema__MGraph__Change__Data = None                       # Changed node data
    type : Schema__MGraph__Change__Type = None                       # Changed node type

class Schema__MGraph__Edge__Changes(Type_Safe):
    type      : Schema__MGraph__Change__Type = None                 # Changed edge type
    from_node : Schema__MGraph__Change__Node = None                 # Changed source node reference
    to_node   : Schema__MGraph__Change__Node = None                 # Changed target node reference

class Schema__MGraph__Diff(Type_Safe):
    nodes_added      : Set[Obj_Id]                                  # Nodes present in graph_b but not in graph_a
    nodes_removed    : Set[Obj_Id]                                  # Nodes present in graph_a but not in graph_b
    nodes_modified   : Dict[Obj_Id, Schema__MGraph__Node__Changes]  # Nodes present in both but with differences
    edges_added      : Set[Obj_Id]                                  # Edges present in graph_b but not in graph_a
    edges_removed    : Set[Obj_Id]                                  # Edges present in graph_a but not in graph_b
    edges_modified   : Dict[Obj_Id, Schema__MGraph__Edge__Changes]  # Edges present in both but with differences
    nodes_count_diff : int                                          # Difference in total node count (graph_b - graph_a)
    edges_count_diff : int                                          # Difference in total edge count (graph_b - graph_a)