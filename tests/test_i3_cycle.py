# -*- coding: utf-8 -*-

import json

import pytest
from i3_tree import i3Tree

from i3_cycle import find_focusable, find_parent_split, cycle_windows, cycle_outputs

TREE_PATHS = {
    "first": "tests/fixtures/first_tree.json",
    "second": "tests/fixtures/second_tree.json",
}


@pytest.fixture
def trees():
    tree_list = []

    with open(TREE_PATHS["first"], "r") as handle:
        tree_list.append(i3Tree(json.load(handle)))

    with open(TREE_PATHS["second"], "r") as handle:
        tree_list.append(i3Tree(json.load(handle)))

    return tree_list


def test_find_focusable(trees):
    # Get the current workspace
    workspace = trees[0].root.focused_child.focused_child.focused_child
    focusable = find_focusable(workspace)

    assert focusable == trees[0].focused

    # Workspace without focus
    workspace = workspace.parent.children[1]

    focusable = find_focusable(workspace)

    assert focusable.name == "emacs"


def test_find_split(trees):
    split = find_parent_split(trees[0].focused, "vertical")

    # The current workspace has no vertical split
    assert split is None

    split = find_parent_split(trees[0].focused, "horizontal")
    # Current workspace
    assert split.name == "1"

    split = find_parent_split(trees[1].focused, "vertical")
    assert split.focused_child == trees[1].focused


def test_cycle_windows(trees):

    # Right has the cycling behavior
    left = cycle_windows(trees[0], "left")
    right = cycle_windows(trees[0], "right")

    assert left == right

    # Left has the cycling behavior
    left = cycle_windows(trees[1], "left")
    right = cycle_windows(trees[1], "right")

    assert left == right

    # Focused window is not in a vertical split
    # up and down should return None
    up = cycle_windows(trees[0], "up")
    down = cycle_windows(trees[0], "down")

    assert up == down == None
