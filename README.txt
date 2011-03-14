Introduction
============

Fixers for Zope Component Architecture and the frameworks built with it.

Currently, there is only one fixer, fix_implements. This fixer will change
all uses of implements(IFoo) in a class body to the class decorator
@implementer(IFoo), which is the most likely Python 3 syntax for 
zope.interfaces implements statements.


Usage
-----

Typically you will use zope.fixers together with Distribute's 2to3 support.
This is done by adding zope.fixers to some parameters in setup():

    >>> setup(
    ...     install_requires = ['zope.fixers'],
    ...     use_2to3 = True,
    ...     use_2to3_fixers = ['zope.fixers'],
    ... )
    
For an example usage of a complex case, look at:

    http://svn.zope.org/zope.interface/branches/regebro-python3/setup.py?rev=106216&view=markup

That setup.py supports both distutils, setuptools and distribute, all versions
of python from 2.4 to 3.1, and has an optional C-extension, so don't worry if
it's overwhelming. For simple projects all you need is to use Distribute and
add the above three lines to the setup.py. Distribute has more documentation
on how to use it to support Python 3 porting.


If you don't want to use Distribute things get a bit more complex, as you have
to make the list of fixers yourself and call lib2to3 with that:

    >>> from lib2to3.refactor import RefactoringTool, get_fixers_from_package
    >>> fixers = get_fixers_from_package('lib2to3.fixes') + \
    ...          get_fixers_from_package('zope.fixers')

And the run the fixing with the fixers:

    >>> tool = RefactoringTool(fixers)
    >>> tool.refactor(files, write=True)
