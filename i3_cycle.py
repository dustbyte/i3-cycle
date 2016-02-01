#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cycle through i3 containers
"""

from argparse import ArgumentParser

from i3_tree import i3Tree
import i3

def find_focusable(node):
    """
    Search for the first focusable window within the node tree
    """

    if not node.children:
        return node

    if node.focus:
        return find_focusable(node.children_dict[node.focus[0]])


def find_parent_split(node, orientation):
    """
    Find the first parent split relative to the given node
    according to the desired orientation
    """

    if (node and node.orientation == orientation
        and len(node.children) > 1):
        return node

    if not node or node.type == "workspace":
        return None

    return find_parent_split(node.parent, orientation)


def cycle_windows(tree, direction):
    """
    Cycle through windows of the current workspace
    """
    wanted = {
        "orientation": ("vertical" if direction in ("up", "down")
                        else "horizontal"),
        "direction": (1 if direction in ("down", "right")
                      else -1),
    }
    split = find_parent_split(tree.focused.parent, wanted["orientation"])

    if split:
        # Get the next child given the direction
        child_ids = [child.id for child in split.children]
        focus_idx = child_ids.index(split.focused_child.id)
        next_idx = (focus_idx + wanted['direction']) % len(child_ids)
        next_node = split.children[next_idx]
        return find_focusable(next_node)
    return None


def cycle_outputs(tree, direction):
    """
    Cycle through directions
    """
    direction = 1 if direction == "next" else -1
    outputs = [output for output in tree.root.children
               if output.name != "__i3"]
    focus_idx = outputs.index(tree.root.focused_child)
    next_idx = (focus_idx + direction) % len(outputs)
    next_output = outputs[next_idx]
    return find_focusable(next_output)


def main():
    """
    Entry point
    """
    parser = ArgumentParser()
    parser.add_argument("direction",
                        choices=(
                            "up", "down", "left", "right",
                            "next", "prev"
                        ),
                        help="Direction to put the focus on")
    args = parser.parse_args()

    tree = i3Tree()
    con = None

    if args.direction in ("next", "prev"):
        con = cycle_outputs(tree, args.direction)
    else:
        con = cycle_windows(tree, args.direction)

    if con:
        i3.focus(con_id=con.id)


if __name__ == '__main__':
    main()
