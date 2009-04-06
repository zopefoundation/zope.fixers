##############################################################################
#
# Copyright (c) 2009 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Fixer for implements(IX) -> @implementer(IX).

$Id$
"""

# Local imports
from lib2to3.fixer_base import BaseFix
from lib2to3.patcomp import PatternCompiler
from lib2to3.fixer_util import syms, Name
from lib2to3.fixer_util import Node, Leaf

helper = dict([(b,a) for (a,b) in syms.__dict__.items()])

class FixImplements(BaseFix):

    IMPORT_PATTERN = """
    import_from< 'from' dotted_name< 'zope' '.' 'interface' > 'import' import_as_names< any* (name='implements') any* > >
    |
    import_from< 'from' dotted_name< 'zope' '.' 'interface' > 'import' name='implements' any* >
    |
    import_from< 'from' dotted_name< 'zope' > 'import' name='interface' any* >
    |
    import_from< 'from' dotted_name< 'zope' '.' 'interface' > 'import' import_as_name< name='implements' 'as' rename=(any) any*> >
    |
    import_from< 'from' dotted_name< 'zope' > 'import' import_as_name< name='interface' 'as' rename=(any) any*> >
    |
    import_from< 'from' 'zope' 'import' import_as_name< 'interface' 'as' interface_rename=(any) > >
    """
    
    CLASS_PATTERN = """
    classdef< 'class' any* ':' suite< any* simple_stmt< power< statement=(%s) trailer < '(' interface=any ')' > any* > any* > any* > >
    """

    IMPLEMENTS_PATTERN = """
    simple_stmt< power< old_statement=(%s) trailer < '(' any* ')' > > any* >
    """

    fixups = []
    
    def should_skip(self, node):
        module = str(node)
        return not ('zope' in module and 'interface' in module)

    def compile_pattern(self):
        # Compile the import pattern.
        self.named_import_pattern = PatternCompiler().compile_pattern(self.IMPORT_PATTERN)
        
    def start_tree(self, tree, filename):
        # Compile the basic class/implements matches. This is done per tree,
        # as further matches (based on what imports there are) also are done
        # per tree.
        self.class_patterns = []
        self.implements_patterns = []
        self._add_pattern("'implements'")
        self._add_pattern("'interface' trailer< '.' 'implements' >")
        self._add_pattern("'zope' trailer< '.' 'interface' > trailer< '.' 'implements' >")
    
    def _add_pattern(self, match):
            self.class_patterns.append(PatternCompiler().compile_pattern(
                self.CLASS_PATTERN % match))
            self.implements_patterns.append(PatternCompiler().compile_pattern(
                self.IMPLEMENTS_PATTERN % match))
        
    def match(self, node):
        # Matches up the imports
        results = {"node": node}
        if self.named_import_pattern.match(node, results):
            return results

        # Now match classes on all import variants found:
        for pattern in self.class_patterns:
            if pattern.match(node, results):
                return results

        # And lastly on all actual calls to implements:
        for pattern in self.implements_patterns:
            if pattern.match(node, results):
                return results
                
    def transform(self, node, results):
        if 'name' in results:
            # This matched an import statement. Fix that up:
            name = results["name"]
            name.replace(Name("implementer", prefix=name.get_prefix()))
        if 'rename' in results:
            # The import statement use import as
            self._add_pattern("'%s'" % results['rename'].value)
        if 'interface_rename' in results:
            self._add_pattern("'%s' trailer< '.' 'implements' > " % results['interface_rename'].value)
        if 'statement' in results:
            # This matched a class that has an implements(IFoo) statement.
            # We must convert that statement to a class decorator
            # and put it before the class definition.
            
            statement = results['statement']
            if not isinstance(statement, list):
                statement = [statement]
            # Make a copy for insertion before the class:
            statement = [x.clone() for x in statement]
            # Get rid of leading whitespace:
            statement[0].prefix = ''
            # Rename implements to implementer:
            if statement[-1].children:
                implements = statement[-1].children[-1]
            else:
                implements = statement[-1]
            if implements.value == 'implements':
                implements.value = 'implementer'
            
            interface = results['interface']
            if not isinstance(interface, list):
                interface = [interface]
            interface = [x.clone() for x in interface]

            # Create the decorator:
            decorator = Node(syms.decorator, [Leaf(50, '@'),] + statement +
                             [Leaf(7, '(')] + interface + [Leaf(8, ')')])
                
            # And stick it in before the class defintion:
            prefix = node.get_prefix()
            if prefix and prefix[0] == '\n':
                decorator.set_prefix(prefix)
            elif prefix:
                node.set_prefix('\n' + prefix)
            else:
                # Find previous node:
                previous = str(node.get_prev_sibling())
                if '\n' in previous:
                    prefix = previous[previous.rfind('\n'):]
                else:
                    prefix = '\n' + previous
                node.set_prefix(prefix)                
            node.insert_child(0, decorator)
            
        if 'old_statement' in results:
            # This matched an implements statement. We'll remove it.
            self.fixups.append(node)
    
    def finish_tree(self, tree, filename):
        for node in self.fixups:
            parent = node.parent
            node.remove()
            if not str(parent).strip():
                # This is an empty class. Stick in a pass
                parent.insert_child(2, Leaf(0, 'pass'))
                parent.insert_child(3, Leaf(0, '\n'))
                