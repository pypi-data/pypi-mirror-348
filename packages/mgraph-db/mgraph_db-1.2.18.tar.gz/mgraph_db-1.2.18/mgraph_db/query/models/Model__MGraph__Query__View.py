from typing                                              import Set, Optional, Dict, Any
from osbot_utils.helpers.Obj_Id                          import Obj_Id
from mgraph_db.query.schemas.Schema__MGraph__Query__View import Schema__MGraph__Query__View
from osbot_utils.type_safe.Type_Safe                     import Type_Safe


class Model__MGraph__Query__View(Type_Safe):
    data: Schema__MGraph__Query__View

    def view_id(self) -> Obj_Id:
        return self.data.view_id

    def nodes_ids(self) -> Set[Obj_Id]:
        return self.data.view_data.nodes_ids

    def edges_ids(self) -> Set[Obj_Id]:
        return self.data.view_data.edges_ids

    def previous_view_id(self) -> Optional[Obj_Id]:
        return self.data.view_data.previous_view_id

    def next_view_ids(self) -> Set[Obj_Id]:
        return self.data.view_data.next_view_ids

    def query_operation(self) -> str:
        return self.data.view_data.query_operation

    def query_params(self) -> Dict[str, Any]:
        return self.data.view_data.query_params

    def stats(self):
        with self as _:
            return { 'has_next'   : len(_.next_view_ids()) > 0       ,
                     'has_prev'   : _.previous_view_id() is not None ,
                     'operation'  : _.query_operation()              ,
                     'params'     : _.query_params   ()              ,
                     'view_edges' : len(self.edges_ids())            ,
                     'view_nodes' : len(_.nodes_ids())               }