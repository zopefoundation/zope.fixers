"""Fixer for implements(IX) -> @implementor(IX).

"""
# Author: Lennart Regebro, based on Jack Diederich's metaclass fixer

# Local imports
from lib2to3.fixer_base import BaseFix
from lib2to3.patcomp import PatternCompiler
from lib2to3.fixer_util import syms, Name
from lib2to3.fixer_util import Node, Leaf

helper = dict([(b,a) for (a,b) in syms.__dict__.items()])

class FixImplements(BaseFix):

    NAMED_IMPORT_PATTERN = """
    import_from< 'from' dotted_name< 'zope' '.' 'interface' > 'import' import_as_names< any* (name='implements') any* > >
    |
    import_from< 'from' dotted_name< 'zope' '.' 'interface' > 'import' name='implements' any* >
    """
    
    RENAMED_IMPORT_PATTERN = """
    import_from< 'from' dotted_name< 'zope' '.' 'interface' > 'import' import_as_name< name='implements' 'as' rename='renamed' any*> >
    """
    
    CLASS_PATTERN = """
    classdef< 'class' any* ':' suite< any* simple_stmt< power< statement='%s' trailer < '(' interface=any ')' > any* > any* > any* > >
    """

    IMPLEMENTS_PATTERN = """
    simple_stmt< power< old_statement='%s' trailer < '(' any* ')' > > any* >
    """
    #classdef< 'class' 'Foo' ':' suite<  simple_stmt< power< 'implements' trailer< '(' 'IFoo' ')' > > '\n' > '' > >
    
    fixups = []
    
    def compile_pattern(self):
        """Compiles self.PATTERN into self.pattern.

        Subclass may override if it doesn't want to use
        self.{pattern,PATTERN} in .match().
        """
        self.named_import_pattern = PatternCompiler().compile_pattern(self.NAMED_IMPORT_PATTERN)
        self.renamed_import_pattern = PatternCompiler().compile_pattern(self.RENAMED_IMPORT_PATTERN)
            
    def start_tree(self, tree, filename):
        self.matches = ['implements']
        super(FixImplements, self).start_tree(tree, filename)
        
    def match(self, node):
        # Matches up the imports
        results = {"node": node}
        if self.named_import_pattern.match(node, results):
            return results
        if self.renamed_import_pattern.match(node, results):
            return results
        for name in self.matches:
            pattern = PatternCompiler().compile_pattern(self.CLASS_PATTERN % name)
            if pattern.match(node, results):
                return results
            pattern = PatternCompiler().compile_pattern(self.IMPLEMENTS_PATTERN % name)
            if pattern.match(node, results):
                return results
                
    def transform(self, node, results):
        if 'name' in results:
            # This matched an import statement. Fix that up:
            name = results["name"]
            name.replace(Name("implementor", prefix=name.get_prefix()))
            if 'rename' in results:
                # The import statement use import as
                self.matches.append(results['rename'].value)
        if 'statement' in results:
            # This matched a class that has an impements(IFoo) statement.
            # Stick a class decorator first.
            statement = results['statement'].value
            interface = results['interface'].value
            if statement == 'implements':
                statement = 'implementor'
            else:
                statement = results['statement'].value
            decorator = Node(syms.decorator, [Leaf(50, '@'), Leaf(1, statement), 
                                              Leaf(7, '('), Leaf(1, interface), 
                                              Leaf(8, ')'), Leaf(4, '\n')])
            node.insert_child(0, decorator)
        if 'old_statement' in results:
            # This matched an implements statement. We'll remove it.
            self.fixups.append(node)
    
    def finish_tree(self, tree, filename):
        for node in self.fixups:
            node.remove()
