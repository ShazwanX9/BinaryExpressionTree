"""
The expression tree is a binary tree in which 
each internal node corresponds to the operator 
and each leaf node corresponds to the operand
"""

class Node:
    """
    ABSTRACT
    Super Class for (
        Operand,
        Operator
    )
    """
    def __init__(self, value="") -> None:
        self.value = value
    def __repr__(self) -> str:
        return self.value
    def evaluate(self) -> float:
        """@return: float   expression calculation"""
        return 0
    def get_braces(self) -> str: 
        """@return: str   expression priorities"""
        return self.__str__()

class Operand(Node):
    """
    CONCRETE
    Inherit from Node
    Store Value representation for Numbers (int or float)
    """
    def __init__(self, number) -> None:
        super().__init__(number)
    def evaluate(self) -> float:
        """@return: float   expression calculation"""
        return float(self.value)

class Operator(Node):
    """
    ABSTRACT
    Super Class for (
        Addition,
        Subtraction,
        Multiplication,
        Division,
        Bitwise
    )
    Inherit from Node
    """
    def __init__(self, operation="", left=None, right=None) -> None:
        super().__init__(operation)
        self.left       = left
        self.right      = right
    def __repr__(self) -> str:
        return f"({self.left.__str__()} {self.value} {self.right.__str__()})"

class Addition(Operator):
    """
    CONCRETE
    Inherit from Operator
    Perform Addition operation
    """
    def __init__(self, left=None, right=None) -> None:
        super().__init__('+', left=left, right=right)
    def evaluate(self) -> float:
        """@return: float   Addition calculation"""
        return self.left.evaluate()+self.right.evaluate()

class Subtraction(Operator):
    """
    CONCRETE
    Inherit from Operator
    Perform Subtraction operation
    """
    def __init__(self, left=None, right=None) -> None:
        super().__init__('-', left=left, right=right)
    def evaluate(self) -> float:
        """@return: float   Subtraction calculation"""
        return self.left.evaluate()-self.right.evaluate()

class Multiplication(Operator):
    """
    CONCRETE
    Inherit from Operator
    Perform Multiplication operation
    """
    def __init__(self, left=None, right=None) -> None:
        super().__init__('*', left=left, right=right)
    def evaluate(self) -> float:
        """@return: float   Multiplication calculation"""
        return self.left.evaluate()*self.right.evaluate()

class Division(Operator):
    """
    CONCRETE
    Inherit from Operator
    Perform Division operation
    """
    def __init__(self, left=None, right=None) -> None:
        super().__init__('/', left=left, right=right)
    def evaluate(self) -> float:
        """@return: float   Division calculation"""
        return self.left.evaluate()/self.right.evaluate()

class Bitwise(Operator):
    """
    CONCRETE
    Inherit from Operator
    Perform Bitwise operation
    """
    def __init__(self, left=None, right=None) -> None:
        super().__init__('^', left=left, right=right)
    def evaluate(self) -> int:
        """@return: int     Bitwise calculation"""
        return int(self.left.evaluate())^int(self.right.evaluate())

def get_node(expression):
    """
    FACTORY
    Create Node Class
    @param  expression :    str  	            Word character or Operator
    @return :               Operator subclass   Operation class
    """
    return {
        '+' : Addition,
        '-' : Subtraction,
        '*' : Multiplication,
        '/' : Division,
        '^' : Bitwise
    }.get(expression, Operand)(expression)

if __name__=="__main__":
    print(__doc__)