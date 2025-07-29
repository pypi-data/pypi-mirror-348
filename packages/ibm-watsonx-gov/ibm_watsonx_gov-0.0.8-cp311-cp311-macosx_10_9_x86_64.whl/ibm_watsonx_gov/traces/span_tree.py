# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

class SpanNode:

    """
    Contains the span.
    """

    def __init__(
            self,
            service_name: str,
            span: dict
        ):
        self.service_name = service_name
        self.span = span

        return

class SpanTree:
    
    """
    The span tree for a given trace.
    """
    
    def __init__(self, node: SpanNode):
        self.node = node
        self.children = []

    def insert(self, child_node_val: SpanNode):
        """
        Inserts a child node under the node with span_id as parent_span_id.
        """
        parent_span_id = child_node_val.span.get("parent_span_id")
        if parent_span_id is None:
            return False
        
        parent_node = self.search(parent_span_id)
        if parent_node is not None:
            child_node = SpanTree(child_node_val)
            parent_node.children.append(child_node)
            return True
        return False

    def search(self, target_span_id: str) -> SpanNode:
        """
        Searches the tree for a node with target_span_id using DFS.
        """
        if self.node.span.get("span_id", "") == target_span_id:
            return self

        for child in self.children:
            result = child.search(target_span_id)
            if result:
                return result

        return None

    def print_tree(self, level=0) -> None:
        """
        Prints the tree using DFS, indenting based on level.
        """
        print(" " * (level * 2) + str(self.node.span.get("span_id")))
        for child in self.children:
            child.print_tree(level + 1)
        
        return
