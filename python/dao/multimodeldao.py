import abc
from profilehooks import timecall


class MultiModelDao(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    @timecall(immediate=True)
    def get_neighbors_for_node(self, node_key, graph_name):
        """
        Returns the neighbors of a specific node.

        Args:
            node_key (str): The key of the node.
            graph_name (str): The name of the graph.

        Returns:
            list: list of neighbor nodes as documents
        """
        return

    @abc.abstractmethod
    @timecall(immediate=True)
    def get_shortest_path(self, node_a, node_b, graph_name):
        """
        Returns the shortest path between two nodes.

        Args:
            node_a (str): The key of one of the two nodes.
            node_b (str): The key of the other node.
            graph_name (str): The name of the graph.

        Returns:
            list: list of the nodes as documents contained
                    by the shortest path.
        """
        return

    @abc.abstractmethod
    @timecall(immediate=True)
    def get_distance(self, node_a, node_b, graph_name):
        """
        Returns the distance between the two nodes..

        Args:
            node_a (str): The key of one of the two nodes.
            node_b (str): The key of the other node.
            graph_name (str): The name of the graph.

        Returns:
            int: the distance between the two nodes.
        """
        return

    @abc.abstractmethod
    @timecall(immediate=True)
    def get_age_group_statistic(self, collection_name):
        """
        Groups the profiles according to 5 years and gender.

        Args:
            collection_name (str): The name of the collection
             to group.

        Returns:
            document: the grouped statistic of the profiles.
        """
        return

    @abc.abstractmethod
    @timecall(immediate=True)
    def get_leaves(self, vertex_collection, edge_collection):
        """
        Returns the leaf nodes of a graph identified by its vertex
        and edge collection.

        Args:
            vertex_collection (str): The name of the collection
             of the nodes.
            edge_collection (str): The name of the collection
             of the edges.
        Returns:
            document: list of leaf nodes.
        """
        return

    @abc.abstractmethod
    @timecall(immediate=True)
    def get_edge_count(self):
        """
        Returns the number of edges.

        Returns:
            int: number of edges.
        """
        return

    @abc.abstractmethod
    @timecall(immediate=True)
    def get_node_count(self):
        """
        Returns the number of nodes.

        Returns:
            int: number of nodes.
        """
        return

    @abc.abstractmethod
    @timecall(immediate=True)
    def decrease_not_provided_age(self):
        """
        Decreases the AGE less than 0 by 1.
        """
        return
