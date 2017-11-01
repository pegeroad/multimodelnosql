import abc


class multi_model_dao(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
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
