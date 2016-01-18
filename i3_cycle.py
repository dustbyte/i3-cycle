#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cycle through i3 containers
"""

from argparse import ArgumentParser

import i3


class i3Node(object):
    """
    Handful representation of an i3 tree node
    """
    # pylint: disable=invalid-name,too-few-public-methods

    @staticmethod
    def find(node, function=None, **conditions):
        """
        Search for a node given a function criteria or conditions on attributes
        """

        def search_conditions(node, **conditions):
            """
            Match a given node against given conditions
            """
            for condition, expected_value in conditions.iteritems():
                if getattr(node, condition, None) == expected_value:
                    return node

        if ((function and function(node))
            or search_conditions(node, **conditions)):
            return node

        for child in node.children:
            if function and function(child):
                return child

            result = search_conditions(child, **conditions)
            if result:
                return result

            result = i3Node.find(child, function, **conditions)
            if result:
                return result

        return None

    def __init__(self, node, parent=None):
        self.raw_node = node
        self.parent = parent
        self.children = []
        self.children_dict = {}
        self.has_focus = self.focused
        self.focused_child = None
        self.orientation = self.raw_node["orientation"]

        for child_node in self.nodes:
            child_i3_node = i3Node(child_node, self)
            if child_i3_node.has_focus:
                self.has_focus = True
                self.focused_child = child_i3_node
            self.children.append(child_i3_node)
            self.children_dict[child_i3_node.id] = child_i3_node

    def __getattr__(self, attr):
        try:
            return self.raw_node[attr]
        except NameError:
            raise AttributeError("{} instance has no attribute '{}'".format(
                self.__class__.__name__,
                attr
            ))

    def __repr__(self):
        return '<{}, "{}">'.format(self.id, self.name)

    def __unicode__(self):
        return '<{}, "{}">'.format(self.id, self.name)


class i3Tree(object):
    """
    Handful representation of an i3 tree
    """
    # pylint: disable=invalid-name,too-few-public-methods

    def __init__(self, tree=None):
        if not tree:
            tree = i3.get_tree()

        self.raw_tree = tree
        self.root = i3Node(self.raw_tree)

    @property
    def focused_container(self):
        """
        Return the focused container within the i3 tree
        """
        return i3Node.find(self.root, focused=True)

def find_focusable(node, direction):
    """
    Search the first focusable window that is not the focused current one
    """

    def finder(node):
        """
        Search the focusable leaf
        """

        if not node.children:
            return node

        if node.focus:
            return finder(node.children_dict[node.focus[0]])

    # Get the next child given the direction
    child_ids = [child.id for child in node.children]
    focus_idx = child_ids.index(node.focused_child.id)
    next_node = node.children[(focus_idx + direction) % len(child_ids)]
    return finder(next_node)

def main():
    """
    Entry point
    """
    parser = ArgumentParser()
    parser.add_argument("direction", choices=("up", "down", "left", "right"),
                        help="Direction to put the focus on")
    args = parser.parse_args()

    wanted = {
        "orientation": ("vertical" if args.direction in ("up", "down")
                        else "horizontal"),
        "direction": (1 if args.direction in ("down", "right")
                      else -1),
    }

    tree = i3Tree()
    current = tree.focused_container.parent

    while True:

        # Not in a split
        if (current.orientation == wanted["orientation"]
            and len(current.children) > 1):
            focusable = find_focusable(current, wanted["direction"])
            if focusable:
                i3.focus(con_id=focusable.id)
            break

        if not current or current.type == "workspace":
            break

        current = current.parent


if __name__ == '__main__':
    main()
