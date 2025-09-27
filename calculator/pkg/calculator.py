import ast
import operator

class Calculator:
    def __init__(self):
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        try:
            node = ast.parse(expression, mode='eval').body
            return self.visit(node)
        except (SyntaxError, TypeError) as e:
            raise ValueError(f"Invalid expression: {e}")

    def visit(self, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self.visit(node.left), self.visit(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self.visit(node.operand))
        elif isinstance(node, ast.Name):
            raise NameError('names are not supported')
        elif isinstance(node, ast.Call):
            raise NameError('function calls are not supported')
        else:
            raise TypeError(node)
