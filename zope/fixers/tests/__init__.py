import unittest
from lib2to3.refactor import RefactoringTool

example = """
# Basic test:
from zope.interface import Interface, implements, providedBy
from zope.interface import providedBy, implements, Interface
from zope.interface import providedBy, implements
from zope.interface import implements, Interface
from zope.interface import implements
from zope.interface import implements as renamed

class IFoo(Interface):
    pass

class Foo:
    "An IFoo class"
    
    implements(IFoo)
    
class IBar(Interface):
    pass
    
class Bar:
    "An IBar class"
    
    renamed(IBar)
    
# Test ends
"""

target = """
# Basic test:
from zope.interface import Interface, implementor, providedBy
from zope.interface import providedBy, implementor, Interface
from zope.interface import providedBy, implementor
from zope.interface import implementor, Interface
from zope.interface import implementor
from zope.interface import implementor as renamed

class IFoo(Interface):
    pass

@implementor(IFoo)
class Foo:
    "An IFoo class"
    
class IBar(Interface):
    pass
    
@renamed(IBar)
class Bar:
    "An IBar class"
    
# Test ends
"""

class FixerTest(unittest.TestCase):
    
    def test_test(self):
        #import pdb;pdb.set_trace()
        tool = RefactoringTool(['zope.fixers.fix_implements'])
        refactored = str(tool.refactor_string(example, 'zope.fixer.test'))

        assert refactored == target
        