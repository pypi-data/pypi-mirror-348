# Typed environment variables

This module implements the mundane task of getting typed values from
 environment variables.

Copyright ® 2020-2025, Luís Gomes luismsgomes@gmail.com. All rights reserved.

Links: https://github.com/luismsgomes/envil | https://pypi.org/project/envil/

Usage
-----

Assuming your environment has two variables set as follows (bash syntax):

    export FOO=123
    export BAR=y

Then, you may access them in Python code as follows:

    import envil as env

    foo = env.get_int("FOO", 0)
    bar = env.get_bool("BAR", False)

The set of strings considered to be falsy values for boolean variables are
specified in `envil.FALSY_VALUES`:

    >>> print(repr(envil.FALSY_VALUES))
    {"0", "false", "f", "no", "n"}

If needed you may override this list with your own, as in this example:

    bar = env.get_bool("BAR", falsy_strings={"nope", "zilch", "zero", "nada"})


The second argument is the default value to be returned if the variable is not defined.
If not specified, this argument will default to `envil.RAISE`, which will
cause an `EnvironmentVariableNotSet` exception to be raised if the variable is not defined.

Note that, unlike in Python's `getenv()`, you may specify `None` as a valid default value.


License
-------

This library is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License version 3 as published
by the Free Software Foundation.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License version 3 for more details.

You should have received a copy of the GNU General Public License along
with this library; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
