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
    Search the first focusable window that is not the focused current one
    """

    if not node.children:
        return node

    if node.focus:
        return find_focusable(node.children_dict[node.focus[0]])


def find_split(node, wanted):
    """
    Find the appropriate split
    """

    if (node and node.orientation == wanted["orientation"]
        and len(node.children) > 1):
        # Get the next child given the direction
        child_ids = [child.id for child in node.children]
        focus_idx = child_ids.index(node.focused_child.id)
        next_idx = (focus_idx + wanted['direction']) % len(child_ids)
        next_node = node.children[next_idx]
        focusable = find_focusable(next_node)
        if focusable:
            i3.focus(con_id=focusable.id)
        return focusable

    if not node or node.type == "workspace":
        return

    return find_split(node.parent, wanted)


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

    if args.direction in ("next", "prev"):
        direction = 1 if args.direction == "next" else -1
        outputs = [output for output in tree.root.children
                   if output.name != "__i3"]
        focus_idx = outputs.index(tree.root.focused_child)
        next_idx = (focus_idx + direction) % len(outputs)
        next_output = outputs[next_idx]
        con = find_focusable(next_output)
        if con:
            i3.focus(con_id=con.id)
    else:
        wanted = {
            "orientation": ("vertical" if args.direction in ("up", "down")
                            else "horizontal"),
            "direction": (1 if args.direction in ("down", "right")
                          else -1),
        }

        find_split(tree.focused.parent, wanted)


if __name__ == '__main__':
    main()
