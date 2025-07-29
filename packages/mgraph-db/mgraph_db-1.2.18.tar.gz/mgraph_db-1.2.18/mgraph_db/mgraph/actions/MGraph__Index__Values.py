from typing                                                         import Type, Optional, Union, Any
from mgraph_db.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data     import Schema__MGraph__Node__Value__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value           import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Value__Index__Data    import Schema__MGraph__Value__Index__Data
from osbot_utils.helpers.Obj_Id                                     import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                     import type_safe
from osbot_utils.utils.Dev                                          import pprint
from osbot_utils.utils.Misc                                         import str_md5

SIZE__VALUE_HASH = 10                                                                    # only use 10 chars from the md5 for the value (which is still 8 billion combinations

class MGraph__Index__Values(Type_Safe):
    index_data : Schema__MGraph__Value__Index__Data                                      # Value index data

    @type_safe
    def add_value_node(self, node: Union[Domain__MGraph__Node, Schema__MGraph__Node__Value]) -> None:                # Add a value node to index
        node_id    = node.node_id
        node_data  = node.node_data
        if isinstance(node_data, Schema__MGraph__Node__Value__Data) is False:
            raise ValueError("Node data is not a subclass of Schema__MGraph__Node__Value")

        value_hash = self.calculate_hash(value_type = node_data.value_type,
                                         value      = node_data.value     ,
                                         key        = node_data.key       ,
                                         node_type  = node.node_type      )

        if value_hash in self.index_data.hash_to_node:                                  # Check uniqueness
            raise ValueError(f"Value with hash {value_hash} already exists")

        self.index_data.hash_to_node[value_hash] = node_id                       # Add to main indexes
        self.index_data.node_to_hash[node_id   ] = value_hash

        if node_data.value_type not in self.index_data.values_by_type:             # Add to type indexes
            self.index_data.values_by_type[node_data.value_type] = set()
        self.index_data.values_by_type[node_data.value_type].add(value_hash)
        self.index_data.type_by_value [value_hash               ] = node_data.value_type

    def get_node_id_by_hash(self, value_hash: str) -> Optional[Obj_Id]:                         # returns node_id that matches value's hash
        return self.index_data.hash_to_node.get(value_hash)

    def get_node_id_by_value(self, value_type: Type                                    ,
                                   value     : str                                     ,
                                   key       : str                               = ''  ,
                                   node_type : Type[Schema__MGraph__Node__Value] = None
                              ) -> Optional[Obj_Id]:           # returns node_id that matches value
        if node_type is None:
            node_type = Schema__MGraph__Node__Value
        value_hash = self.calculate_hash(value_type=value_type, value=value, key=key, node_type=node_type)
        return self.get_node_id_by_hash(value_hash)

    def remove_value_node(self, node: Schema__MGraph__Node__Value) -> None:             # Remove from all indexes
        value_hash = self.index_data.node_to_hash.get(node.node_id)
        if value_hash:
            # Remove from main indexes
            del self.index_data.hash_to_node[value_hash]
            del self.index_data.node_to_hash[node.node_id]

            # Remove from type indexes
            if node.node_data.value_type in self.index_data.values_by_type:
                self.index_data.values_by_type[node.node_data.value_type].discard(value_hash)
                if not self.index_data.values_by_type[node.node_data.value_type]:
                    del self.index_data.values_by_type[node.node_data.value_type]

            if value_hash in self.index_data.type_by_value:
                del self.index_data.type_by_value[value_hash]

    @type_safe
    def calculate_hash(self, value_type: Type                                    ,
                             value     : Any                                     ,
                             key       : str                               = ''  ,
                             node_type : Type[Schema__MGraph__Node__Value] = None
                        ) -> str:                      # Calculate value hash
        if value_type is None:
            raise ValueError("In MGraph__Index__Values.calculate_hash , value_type was None")
        type_name = f"{value_type.__module__}.{value_type.__name__}"         # Get full type path
        if key:
            hash_data = f"{type_name}::{key}::{value}"                       # Combine with key and value
        else:
            hash_data = f"{type_name}::{value}"                              # Combine with value
        if node_type:
            hash_data = f"{node_type.__name__}::{hash_data}"
        hash_data = hash_data.lower()                       # todo: document and review this 'extra' part of the calculate hash formula (in this case we are making it all lower case to handle cases where we would have very simular nodes)
        #print(hash_data)
        return str_md5(hash_data)[:SIZE__VALUE_HASH]


    def print__values_index_data(self):
        pprint(self.index_data.json())