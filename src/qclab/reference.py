"""Instructor reference implementation. Try the exercise before reading this file."""


def select_op_nodes(dag, operation_types=None):
    """Return operation nodes matching the Lab 01 selection contract."""
    if operation_types is None:
        return list(dag.op_nodes())
    types = (operation_types,) if isinstance(operation_types, type) else tuple(operation_types)
    if not all(isinstance(operation_type, type) for operation_type in types):
        raise TypeError("Every operation_types entry must be a Python class")
    return [node for node in dag.op_nodes() if isinstance(node.op, types)]
