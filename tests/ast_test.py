foo : int = 42  # <_ast.AnnAssign 
dsf={'AST': (), 'Add': (), 'And': (), 'AnnAssign': ('target', 'annotation', 'value', 'simple'), 'Assert': ('test', 'msg'), 'Assign': ('targets', 'value'), 'AsyncFor': ('target', 'iter', 'body', 'orelse'), 'AsyncFunctionDef': ('name', 'args', 'body', 'decorator_list', 'returns'), 'AsyncWith': ('items', 'body'), 'Attribute': ('value', 'attr', 'ctx'), 'AugAssign': ('target', 'op', 'value'), 'AugLoad': (), 'AugStore': (), 'Await': ('value',), 'BinOp': ('left', 'op', 'right'), 'BitAnd': (), 'BitOr': (), 'BitXor': (), 'BoolOp': ('op', 'values'), 'Break': (), 'Bytes': ('s',), 'Call': ('func', 'args', 'keywords'), 'ClassDef': ('name', 'bases', 'keywords', 'body', 'decorator_list'), 'Compare': ('left', 'ops', 'comparators'), 'Constant': ('value',), 'Continue': (), 'Del': (), 'Delete': ('targets',), 'Dict': ('keys', 'values'), 'DictComp': ('key', 'value', 'generators'), 'Div': (), 'Ellipsis': (), 'Eq': (), 'ExceptHandler': ('type', 'name', 'body'), 'Expr': ('value',), 'Expression': ('body',), 'ExtSlice': ('dims',), 'FloorDiv': (), 'For': ('target', 'iter', 'body', 'orelse'), 'FormattedValue': ('value', 'conversion', 'format_spec'), 'FunctionDef': ('name', 'args', 'body', 'decorator_list', 'returns'), 'GeneratorExp': ('elt', 'generators'), 'Global': ('names',), 'Gt': (), 'GtE': (), 'If': ('test', 'body', 'orelse'), 'IfExp': ('test', 'body', 'orelse'), 'Import': ('names',), 'ImportFrom': ('module', 'names', 'level'), 'In': (), 'Index': ('value',), 'Interactive': ('body',), 'Invert': (), 'Is': (), 'IsNot': (), 'JoinedStr': ('values',), 'LShift': (), 'Lambda': ('args', 'body'), 'List': ('elts', 'ctx'), 'ListComp': ('elt', 'generators'), 'Load': (), 'Lt': (), 'LtE': (), 'MatMult': (), 'Mod': (), 'Module': ('body',), 'Mult': (), 'Name': ('id', 'ctx'), 'NameConstant': ('value',), 'Nonlocal': ('names',), 'Not': (), 'NotEq': (), 'NotIn': (), 'Num': ('n',), 'Or': (), 'Param': (), 'Pass': (), 'Pow': (), 'RShift': (), 'Raise': ('exc', 'cause'), 'Return': ('value',), 'Set': ('elts',), 'SetComp': ('elt', 'generators'), 'Slice': ('lower', 'upper', 'step'), 'Starred': ('value', 'ctx'), 'Store': (), 'Str': ('s',), 'Sub': (), 'Subscript': ('value', 'slice', 'ctx'), 'Suite': ('body',), 'Try': ('body', 'handlers', 'orelse', 'finalbody'), 'Tuple': ('elts', 'ctx'), 'UAdd': (), 'USub': (), 'UnaryOp': ('op', 'operand'), 'While': ('test', 'body', 'orelse'), 'With': ('items', 'body'), 'Yield': ('value',), 'YieldFrom': ('value',)}
import sys;'qgb.U' in sys.modules or sys.path.append('C:/QGB/babun/cygwin/bin/');from qgb import *
from _ast import AST
import ast
import json

def ast2json( node ):

    if not isinstance( node, AST ):
        raise TypeError( 'expected AST, got %r' % node.__class__.__name__ )


    def _format( node ):
        if isinstance( node, AST ):
            fields = [ ( '_PyType', _format( node.__class__.__name__ ) ) ]
            fields += [ ( a, _format( b ) ) for a, b in iter_fields( node ) ]

            return '{ %s }' % ', '.join( ( '"%s": %s' % field for field in fields ) )

        if isinstance( node, list ):
            return '[ %s ]' % ', '.join( [ _format( x ) for x in node ] )
        return T.json_dumps(node)    
        try:
            return json.dumps( node )
        except Exception as e:
            import pdb;pdb.set_trace()

    return _format( node )



def iter_fields( node ):

    for field in node._fields:
        try:
            yield field, getattr( node, field )
        except AttributeError:
            pass