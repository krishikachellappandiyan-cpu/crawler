import json
import os
import networkx as nx


class GraphBuilder:

    def __init__(self):

        self.graph = nx.DiGraph()

    # -----------------------------
    # ADD NODE
    # -----------------------------

    def add_node(self, node, node_type):

        self.graph.add_node(
            node,
            type=node_type
        )

    # -----------------------------
    # ADD EDGE
    # -----------------------------

    def add_edge(
        self,
        source,
        target,
        relation
    ):

        self.graph.add_edge(
            source,
            target,
            relation=relation
        )

    # -----------------------------
    # EXPORT GRAPH JSON
    # -----------------------------

    def export_json(self):

        nodes = []

        edges = []

        # -----------------------------
        # STORE NODES
        # -----------------------------

        for node, data in self.graph.nodes(data=True):

            nodes.append({
                "id": node,
                "type": data.get("type")
            })

        # -----------------------------
        # STORE EDGES
        # -----------------------------

        for source, target, data in self.graph.edges(data=True):

            edges.append({
                "source": source,
                "target": target,
                "relation": data.get("relation")
            })

        graph_data = {
            "nodes": nodes,
            "edges": edges
        }

        # -----------------------------
        # CREATE OUTPUT DIRECTORY
        # -----------------------------

        os.makedirs(
            "output",
            exist_ok=True
        )

        # -----------------------------
        # SAVE GRAPH
        # -----------------------------

        with open(
            "output/graph.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                graph_data,
                file,
                indent=4
            )

        print(
            "\n[GRAPH SAVED] output/graph.json"
        )