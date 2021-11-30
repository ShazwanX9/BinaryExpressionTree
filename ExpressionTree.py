"""
The expression tree is a binary tree in which 
each internal node corresponds to the operator 
and each leaf node corresponds to the operand.

This file contains the logic of expression tree
This file allows the tree to be printed using
postorder tranversal;
    Recursively traverse the node’s left subtree in post-order
    Recursively traverse the node’s right subtree in post-order
    Access the node
"""

from math import log
from re import findall
from ExpressionClass import Node, get_node

class ExpressionTree:
    """
    CONCRETE
    Class that wiring all the other class
    by performing the logics to get the
    full expression tree
    """
    priorities = {
            '+' : 1,
            '-' : 1,
            '*' : 2,
            '/' : 2,
            '^' : 3
    }

    def __init__(self, expression="") -> None:
        self.node_count = 0
        self.node = self.get_tree(expression)

    def __repr__(self) -> str:
        return self.node.__str__()

    def get_pattern_(self)->str:
        """@return: str   regular expression"""
        operators = ''.join(f"\\{c}|" for c in self.priorities)
        decimals    = "\d+\.?\d+"; operands    = "\w+"; brackets = "\(|\)";
        return '|'.join((decimals,operands,brackets,operators)).rstrip('|')

    def get_tree(self, expression="")->Node:
        """
        performing the iteration
        @param  expression :    str  	Word character or Operator
        @return:                Node    Root of the tree
        """
        node_stack, iter_stack = [], []
        iteration = findall(self.get_pattern_(), f"({expression})")
        self.node_count = len(iteration)

        for exp in iteration:

            if exp=='(': iter_stack.append('(')
            elif exp.isalnum() or exp.replace('.','',1).isdigit(): node_stack.append(get_node(exp))

            elif self.priorities.get(exp, False):
                while (
                    iter_stack and iter_stack[-1] != '('
                    and (exp != '^' and self.priorities.get(iter_stack[-1], 0)>=self.priorities.get(exp, 0))
                    or (exp == '^' and self.priorities.get(iter_stack[-1], 0)>self.priorities.get(exp, 0))
                ):
                    chk = get_node(iter_stack.pop())
                    chk.right, chk.left = node_stack.pop(), node_stack.pop()
                    node_stack.append(chk)
                iter_stack.append(exp)

            elif exp==')':
                while iter_stack and iter_stack[-1]!='(':
                    chk = get_node(iter_stack.pop())
                    chk.right, chk.left = node_stack.pop(), node_stack.pop()
                    node_stack.append(chk)
                iter_stack.pop()

        self.node = node_stack[-1] if node_stack else Node()
        return self.node

    def evaluate(self) -> float:
        """@return: float   expression calculation"""
        return self.node.evaluate()

def printTreeHorizontal(node:Node)->None:
    """
    Print the tree sideways to the right
    @param node:    Node    Root of the tree
    @return         None
    """
    line_spacing = 4
    def printTreeUtil(node, space=0):
        if not (node and node.value): return
        if not node.value.isalnum(): printTreeUtil(node.left, space+line_spacing)
        print(' ' * (line_spacing + space*2) + '->', node.value)
        if not node.value.isalnum(): printTreeUtil(node.right, space+line_spacing)
    return printTreeUtil(node)

def printTreeVertical(node:Node, node_count:int)->None:
    """
    Print the tree vertical
    @param node:        Node    Root of the tree
    @param node_count:  int     Number of nodes
    @return             None
    """
    line_spacing = int(log(node_count, 2)+1)*(node_count//2)
    print(' '*line_spacing+node.value)
    def printTreeUtil(node, space=2):
        print(
            ' '*(line_spacing//space+1) + (' ' if node.value.isalnum() else node.left.value), 
            ' '*(line_spacing//space+1) + (' ' if node.value.isalnum() else node.right.value),
            sep=' '*(line_spacing//space),
            end="\n"*(not node.value.isalnum())
        )
        if not (node and node.value): return
        if not node.value.isalnum(): printTreeUtil(node.left, space*2)
        if not node.value.isalnum(): printTreeUtil(node.right, space*2)
    printTreeUtil(node)
    print()
    return

if __name__=="__main__":
    print(__doc__)

    root=ExpressionTree("a/b-c+3*d+45")
    print("Testing with Expression: ", root)
    print("Testing print vertical tree: ")
    printTreeVertical(root.node, root.node_count)
    print("Testing print horizontal tree: ")
    printTreeHorizontal(root.node)

    print("Testing for evaluation: ")
    testcase = (
        ("1+1",          2, "basic addition"),
        ("3-1",          2, "basic subtraction"),
        ("1*2",          2, "basic multiplication"),
        ("4/2",          2, "basic division"),
        ("5 - 5",        0, "line spacing"),
        ("1+3-7",       -3, "negative number"),
        ("(1+4)*7",     35, "bracket"),
        ("1+4*7",       29, "BODMAS"),
        ("9+3*6-2",     25, "complex operation"),
        ("19.2-16/2", 11.2, "floating number"),
    )

    for exp, res, test in testcase:
        root.get_tree(exp)
        chk = root.evaluate()
        print(f"\tTesting {test:22}: {exp}")
        print(f"\t\t{root.__str__():20} = {chk:5}  {chk==res}")
        print()