Introduction
============

Fixers for Zope Component Architecture and the frameworks built with it.

Currently, there is only one fixer, fix_implements. This fixer will change
all uses of implements(IFoo) in a class body to the class decorator
@implementor(IFoo), which is the most likely Python 3 syntax for 
zope.interfaces implements statements.


Usage
-----

TODO!
