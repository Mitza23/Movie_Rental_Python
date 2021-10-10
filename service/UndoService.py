"""
UndoService module
"""


class UndoServiceError(Exception):
    """
    UndoServiceError handles all the errors related to operations performed inside the UndoService module
    """
    def __init__(self, message):
        self._message = message


class FunctionCall:
    """
    FunctionCall class implements the idea of a function with function name and function parameters
    Attributes:
        function_name: name of the function - string
        function_params: parameters of the function - string
    """
    def __init__(self, fun_name, *fun_params):
        self._function_name = fun_name
        self.function_parameters = fun_params

    def __call__(self):
        self._function_name(*self.function_parameters)


class Operation:
    """
    Operation class is used for calling the undo and redo functions of an operation done at the rental shop
    Attributes:
        _undo: undoing the function - FunctionCall
        _redo: redoing the function - FunctionCall
    """
    def __init__(self, undo, redo):
        self._undo = undo
        self._redo = redo

    def undo(self):
        self._undo()

    def redo(self):
        self._redo()


class CascadedOperation:
    """
    CascadedOperation class is used for storing operations which come as a single one in a undo/redo request
    Attributes
        operations: list of Operation
    Methods:
        add_operation
        undo
        redo

    """
    def __init__(self, operations=None):
        if operations is None:
            operations = []
        self._operations = operations

    def add_operation(self, operation):
        self._operations.append(operation)

    def undo(self):
        for op in self._operations:
            op.undo()

    def redo(self):
        for op in self._operations:
            op.redo()


class UndoService:
    """
    UndoService class handles the undo and redo operations
    Attributes:
        history: stores the order of operations done by the user - list of Operation
        index: points to the current position in the operation list - int

    """
    def __init__(self):
        self._history = []
        self._index = -1

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, list):
        self._history = list

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    def record(self, operation):
        # When recording a new operation, discard all previous undone operations
        self._history = self._history[0:self._index + 1]

        self.history.append(operation)
        self.index += 1

    def undo(self):
        if self.index == -1:
            raise UndoServiceError("No more operations to be undone")
        self.history[self.index].undo()
        self.index -= 1

    def redo(self):
        if self.index == len(self.history)-1:
            raise UndoServiceError("No more operations to be redone")
        self.index += 1
        self.history[self.index].redo()
