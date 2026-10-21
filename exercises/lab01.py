"""Lab 01 starter: extend a working single-type selector to accept iterables.

Edit this file, then run: uv run qclab check
Read labs/01-select-operation-nodes.md for the contract and progressive hints.
"""


def select_op_nodes(dag, operation_types=None):
    """Return matching operation nodes from dag, without modifying it.

    Accept None, one Python class, or an iterable of Python classes.
    Return a list in the order of dag.op_nodes(). Empty iterables match nothing.
    Raise TypeError for non-iterables or any iterable element that is not a class.
    """
    # This works for None and a single class, but not every required iterable.
    # The exercise is to generalize it. Keep the tests unchanged.
    if operation_types is None:
        return list(dag.op_nodes())
    if not isinstance(operation_types, type):
        raise TypeError("operation_types must be a class")
    return [node for node in dag.op_nodes() if isinstance(node.op, operation_types)]
