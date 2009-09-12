Introduction
============

Fixers for Zope Component Architecture and the frameworks built with it.

Currently, there is only one fixer, fix_implements. This fixer will change
all uses of implements(IFoo) in a class body to the class decorator
@implementer(IFoo), which is the most likely Python 3 syntax for 
zope.interfaces implements statements.

zope.fixers requires Python 3.1.


Usage
-----

To use this you typically want all teh fixers from lib2to3, and add the
fixers from zope.fixers to it. Like so:

    >>> from lib2to3.refactor import RefactoringTool, get_fixers_from_package
    >>> fixers = get_fixers_from_package('lib2to3.fixes') + \
    ...          get_fixers_from_package('zope.fixers')

And the run the fixing with the fixers:

    >>> tool = RefactoringTool(fixers)
    >>> tool.refactor(files, write=True)

For an example usage within setuptools, look at:

http://svn.zope.org/zope.interface/branches/regebro-python3/build_ext_3.py?rev=98993&view=markup

