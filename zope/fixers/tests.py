import unittest
from lib2to3.refactor import RefactoringTool

# Check that various import syntaxes get renamed properly.
imports_source = """
from zope.interface import Interface, implements, providedBy
from zope.interface import providedBy, implements, Interface
from zope.interface import providedBy, implements
from zope.interface import implements, Interface
from zope.interface import implements
from zope.interface import implements as renamed
"""

imports_target = """
from zope.interface import Interface, implementer, providedBy
from zope.interface import providedBy, implementer, Interface
from zope.interface import providedBy, implementer
from zope.interface import implementer, Interface
from zope.interface import implementer
from zope.interface import implementer as renamed
"""

# Test a simple case.
simple_source = """
from zope.interface import implements

class IFoo(Interface):
    pass

class Foo:
    "An IFoo class"
    
    implements(IFoo)
"""

simple_target = """
from zope.interface import implementer

class IFoo(Interface):
    pass

@implementer(IFoo)
class Foo:
    "An IFoo class"
"""

# Multiple interfaces:
multi_source = """
from zope.interface import implements

class IFoo(Interface):
    pass

class IBar(Interface):
    pass

class Foo:
    "An IFoo class"
    
    implements(IFoo, IBar)
"""

multi_target = """
from zope.interface import implementer

class IFoo(Interface):
    pass

class IBar(Interface):
    pass

@implementer(IFoo, IBar)
class Foo:
    "An IFoo class"
"""

# Make sure it works even if implements gets renamed.
renamed_source = """
from zope.interface import implements as renamed

class IBar(Interface):
    pass
    
class Bar:
    "An IBar class"
    
    renamed(IBar)
"""

renamed_target = """
from zope.interface import implementer as renamed

class IBar(Interface):
    pass
    
@renamed(IBar)
class Bar:
    "An IBar class"
"""

# Often only the module gets imported.
module_import_source = """
from zope import interface

class IFoo(Interface):
    pass

class Foo:
    "An IFoo class"
    
    interface.implements(IFoo)
"""

module_import_target = """
from zope import interface

class IFoo(Interface):
    pass

@interface.implementer(IFoo)
class Foo:
    "An IFoo class"
"""

# Interface can get renamed. It's unusual, but should be supported.
module_renamed_source = """
from zope import interface as zopeinterface

class IFoo(Interface):
    pass

class Foo:
    "An IFoo class"
    
    zopeinterface.implements(IFoo)
"""

module_renamed_target = """
from zope import interface as zopeinterface

class IFoo(Interface):
    pass

@zopeinterface.implementer(IFoo)
class Foo:
    "An IFoo class"
"""

# Many always uses the full module name.
full_import_source = """
import zope.interface

class IFoo(Interface):
    pass

class Foo:
    "An IFoo class"
    
    zope.interface.implements(IFoo)
"""

full_import_target = """
import zope.interface

class IFoo(Interface):
    pass

@zope.interface.implementer(IFoo)
class Foo:
    "An IFoo class"
"""

# Empty classes:
empty_class_source = """
import zope.interface

class IFoo(Interface):
    pass

class Foo:
    zope.interface.implements(IFoo)

"""

empty_class_target = """
import zope.interface

class IFoo(Interface):
    pass

@zope.interface.implementer(IFoo)
class Foo:
    pass

"""

# Classes with indentation:
indented_class_source = """
import zope.interface

class IFoo(Interface):
    pass

def forceindent():
    class Foo:
        zope.interface.implements(IFoo)
        
    class Bar:
        zope.interface.implements(IFoo)
        
"""

indented_class_target = """
import zope.interface

class IFoo(Interface):
    pass

def forceindent():
    @zope.interface.implementer(IFoo)
    class Foo:
        pass
        
    @zope.interface.implementer(IFoo)
    class Bar:
        pass
        
"""
class FixerTest(unittest.TestCase):
    
    def setUp(self):
        self.tool = RefactoringTool(['zope.fixers.fix_implements'])
    
    def _test(self, source, target):
        refactored = str(self.tool.refactor_string(source, 'zope.fixer.test'))
        if refactored != target:
            match = ''
            for i in range(min(len(refactored), len(target))):
                if refactored[i] == target[i]:
                    match += refactored[i]
                else:
                    break
            msg = "\nResult:\n" + refactored
            msg += "\nFailed:\n" + refactored[i:]
            msg += "\nTarget:\n" + target[i:]
            # Make spaces and tabs visible:
            msg = msg.replace(' ', '°')
            msg = msg.replace('\t', '------->')
            msg = ("Test failed at character %i" % i) + msg
            self.fail(msg)
        
    def test_imports(self):
        self._test(imports_source, imports_target)

    def test_simple(self):
        self._test(simple_source, simple_target)

    def test_multi(self):
        self._test(multi_source, multi_target)
        
    def test_renamed(self):
        self._test(renamed_source, renamed_target)
        
    def test_module_import(self):
        self._test(module_import_source, module_import_target)
        
    def test_module_renamed(self):
        self._test(module_renamed_source, module_renamed_target)
        
    def test_full_import(self):
        self._test(full_import_source, full_import_target)

    def test_empty_class(self):
        self._test(empty_class_source, empty_class_target)

    def test_indented_class(self):
        self._test(indented_class_source, indented_class_target)
        