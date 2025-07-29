from typing                                         import Type
from mgraph_db.mgraph.actions.MGraph__Builder       import MGraph__Builder
from mgraph_db.mgraph.actions.MGraph__Values        import MGraph__Values
from mgraph_db.mgraph.actions.MGraph__Export        import MGraph__Export
from mgraph_db.mgraph.actions.MGraph__Screenshot    import MGraph__Screenshot
from mgraph_db.mgraph.domain.Domain__MGraph__Graph  import Domain__MGraph__Graph
from mgraph_db.mgraph.actions.MGraph__Data          import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Edit          import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Index         import MGraph__Index
from mgraph_db.query.MGraph__Query                  import MGraph__Query
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.type_safe.Type_Safe                import Type_Safe

class MGraph(Type_Safe):                                                                                        # Main MGraph class that users will interact with
    graph           : Domain__MGraph__Graph                                                                                       # Reference to the underlying graph model
    query_class     : Type[MGraph__Query     ]
    edit_class      : Type[MGraph__Edit      ]
    screenshot_class: Type[MGraph__Screenshot]

    def builder(self) -> MGraph__Builder:
        return MGraph__Builder(mgraph_edit=self.edit())

    def data(self) -> MGraph__Data:
        return MGraph__Data(graph=self.graph)

    @cache_on_self                                                                                      # make sure we always get the same object (important since the up-to-date index() object is inside this class)
    def edit(self) -> MGraph__Edit:
        return self.edit_class(graph=self.graph)

    def export(self) -> MGraph__Export:
        return MGraph__Export(graph=self.graph)

    def index(self) -> MGraph__Index:
        return self.edit().index()                                                                      # get the index from the .edit() logic (so that everybody is using the same object)

    def query(self) -> MGraph__Query:
        mgraph_data  = self.data()
        mgraph_index = self.index()
        mgraph_query = self.query_class(mgraph_data=mgraph_data, mgraph_index=mgraph_index).setup()
        return mgraph_query

    def values(self) -> MGraph__Values:
        return MGraph__Values(mgraph_edit=self.edit())

    def screenshot(self, **kwargs):                                                                                     # Access screenshot operations
        return self.screenshot_class(**kwargs, graph=self.graph)






