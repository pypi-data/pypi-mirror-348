"""
.. moduleauthor:: Dave Faulkmore <https://mastodon.social/@msftcangoblowme>

..

Want desired context's locals
------------------------------

From a module function, **get the locals** and return value

When testing and an Exception occurs, the locals are only available in
the context of where the error occurred, not necessarily where need to
debug.

.. epigraph::

   As you read this, keep in mind

   To understand our motivation, how badly we want to see those locals,
   background on those locals:

   - param_a -- Satoshi Nakamoto's private key to the genesis block

   - param_b -- the passphrase to that private key

   ^^ is exactly how it feels when don't have access to those locals and
   then suddenly do!

   -- Betty White <-- everything is attributed to her

Limited to:

- module function; not a: class method, Generator, Iterator, or Iterable

- function must end in a single ``return`` statement; not ``yield``,
  ``yield from``, or ``raise``

And wait! There's more
^^^^^^^^^^^^^^^^^^^^^^^^^

In return, value can be: normal or **tuple (packed values)**

Wow!

Great!

Yea!

One return value example
-------------------------

Example function found in :py:mod:`logging_strict.tech_niques.context_locals`.
Lets pretend this is the module level function would like to see the locals

.. code-block:: text

   def _func(param_a: str, param_b: Optional[int] = 10) -> str:
       param_a = f"Hey {param_a}"  # Local only
       param_b += 20  # Local only
       return "bar"


So there are two locals we'd really really like to see:

- param_a
- param_b

Returns ``"bar"``

.. testcode::

    from logging_strict.tech_niques.context_locals import get_locals_dynamic, _func


    def main():
        # If in same script file try, f"{__name__}._func"
        func_path = f"logging_strict.tech_niques.context_locals._func"

        args = ("A",)
        kwargs = {}
        t_ret = get_locals_dynamic(_func, *args, **kwargs)
        ret, d_locals = t_ret
        assert ret == "bar"
        assert "param_a" in d_locals.keys()
        assert "param_b" in d_locals.keys()
        print(d_locals)


    main()

.. testoutput::

   {'full_name': '_func', 'param_a': 'Hey A', 'param_b': 30}

Woooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooah!

.. note:: pretty print is your friend

   For better readability, :py:func:`pprint.pprint` is better than
   :py:func:`print`

.. note:: ``__name__`` is also your friend

   This technique requires the absolute dotted path to the module
   function. **if** in the same (python script) file, use
   :code:`f"{__name__}.myfunc"` instead.

   Useful knowhow, if the module function is in the same file as a unittest

.. caution:: Especially applies to JSON

   tl;dr;

   In a str, preserve escape characters, use raw string, e.g. r"\\\\\\\\n"

   "\\\\\\\\n" --> "\\\\n"

   Unpreserved, ^^ may happen

   Escape characters need to be preserved. JSON str is an example where
   a raw string would preserve the escaped characters and remain valid JSON.

.. seealso::

   `Credit <https://stackoverflow.com/a/56469201>`_


**Module private variables**

.. py:data:: __all__
   :type: tuple[str, str, str]
   :value: ("get_locals", "get_locals_dynamic", "FuncWrapper")

   This modules exports

.. py:data:: _T
   :type: typing.TypeVar
   :value: typing.TypeVar("_T")

   Equivalent to :py:data:`~typing.Any`

.. py:data:: _P
   :type: typing.ParamSpec
   :value: typing_extensions.ParamSpec('_P')

   Equivalent to :py:data:`~typing.Any`

**Module objects**

"""

import functools
import inspect
import re
import sys
from textwrap import dedent
from typing import TypeVar
from unittest.mock import patch

from logging_strict.util.check_type import is_not_ok

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec

__all__ = (
    "FuncWrapper",
    "get_locals",
    "get_locals_dynamic",
)

_T = TypeVar("_T")  # Can be anything
_P = ParamSpec("_P")


class FuncWrapper:
    """Wraps a function to provide basic info about it.

    :ivar func: the function to wrap
    :vartype func: (types.FunctionType | types.MethodType | types.BuiltinFunctionType | types.BuiltinMethodType | types.WrapperDescriptorType | types.MethodWrapperType | types.MethodDescriptorType | types.ClassMethodDescriptorType)

    .. seealso::

       Source code source
       https://gist.github.com/jwcompdev/65da6a59a6bcb44864de77b8a29baeed

       Conversation source
       https://stackoverflow.com/a/25959545

    """

    def __init__(self, func):
        """Class constructor"""
        if isinstance(func, functools.partial):
            self._name = func.func.__name__
        else:
            self._name = func.__name__
        self._module = inspect.getmodule(func)
        cls = type(self)
        self._cls = cls._get_method_parent(func)

    @staticmethod
    def _get_method_parent(meth):
        """Returns the class of the parent of the specified method.

        :param meth: the method to check
        :returns: the class of the parent of the specified method
        :rtype: type | None
        """
        # https://stackoverflow.com/users/1956611/user1956611
        if isinstance(meth, functools.partial):
            return FuncWrapper._get_method_parent(meth.func)

        if inspect.ismethod(meth) or (
            inspect.isbuiltin(meth)
            and getattr(meth, "__self__", None) is not None
            and getattr(meth.__self__, "__class__", None)
        ):
            for cls in inspect.getmro(meth.__self__.__class__):
                if meth.__name__ in cls.__dict__:
                    # bound method
                    return cls
            meth = getattr(meth, "__func__", meth)
        if inspect.isfunction(meth):
            # unbound method fallsback to __qualname__ parsing
            cls = getattr(
                inspect.getmodule(meth),
                meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
                None,
            )
            if isinstance(cls, type):
                return cls
        return getattr(meth, "__objclass__", None)  # handle special descriptor objects

    @property
    def name(self):
        """Returns the function's name.

        :returns: the function's name
        :rtype: str
        """
        return self._name

    @property
    def cls(self):
        """Returns the function's parent class.

        :returns: the parent class
        :rtype: type | None
        """
        return self._cls

    @property
    def cls_name(self):
        """Returns the function's parent class name.

        :returns: the parent class name
        :rtype: str | None
        """
        if self._cls is not None:
            ret = self._cls.__name__
        else:
            ret = None

        return ret

    @property
    def module(self):
        """Returns the function's parent module.

        :returns: the parent module
        :rtype: types.ModuleType | None
        """
        return self._module

    @property
    def module_name(self):
        """Returns the function's parent module name.

        :returns: the parent module name
        :rtype: str | None
        """
        if self._module is not None:
            ret = self._module.__name__
        else:  # pragma: no cover
            ret = None

        return ret

    @property
    def module_filename(self):
        """Returns the function's module filename.

        :returns: the module filename
        :rtype: str | None
        """
        if self._module is not None:
            ret = self._module.__file__
        else:
            ret = None

        return ret

    @property
    def package_name(self):
        """Returns the function's package name.

        :return: the package name
        :rtype: str
        """
        module = self.module
        if module is not None:
            ret = getattr(module, "__package__", "")
            if ret is None:
                str_ret = ""
            else:
                str_ret = ret
        else:
            """For functools.partial functions, on py310+ returns empty
            str. Do this consistently
            """
            str_ret = ""

        return str_ret

    @property
    def root_package_name(self):
        """Returns the function's root package name.

        :returns: the root package name
        :rtype: str
        """
        pkg_name = self.package_name
        if pkg_name is not None and isinstance(pkg_name, str):
            str_ret = self.package_name.partition(".")[0]
        else:
            str_ret = ""

        return str_ret

    @property
    def full_name(self):
        """Returns the function's full name with the class included.

        :returns: the full name
        :rtype: str
        """
        cls_name = self.cls_name
        if cls_name is None:
            ret = self.name
        else:
            ret = f"{self.cls_name}.{self.name}"

        return ret

    def get_dotted_path(self):
        """Returns the function's full path with class and package name.

        :returns: the full path
        :rtype: str
        :raises:

        - :py:exc:`ModuleNotFoundError` -- Cannot determine func module path

        """
        cls_name = self.cls_name
        mod_dotted_path = self.module_name
        if mod_dotted_path is None:  # pragma: no cover
            msg_warn = (
                "Could not determine func module path. Undeterminable origin "
                f"of func {self.name}"
            )
            raise ModuleNotFoundError(msg_warn)
        else:
            if cls_name is None:
                ret = f"{mod_dotted_path}.{self.name}"
            else:
                ret = f"{mod_dotted_path}.{cls_name}.{self.name}"

        return ret


def _func(param_a, param_b=10):
    """Sample function to inspect the locals

    Careful! In function signature, do not use ``|``. Results in
    impossible to track down ImportError

    :param param_a: To whom am i speaking to? Name please
    :type param_a: str
    :param param_b: Default 10. A int to be modified
    :type param_b: int | None
    :returns: Greetings from this function to our adoring fans
    :rtype: str
    """
    if is_not_ok(param_a):
        param_a = ""
    else:  # pragma: no cover
        pass

    if param_b is None or not isinstance(param_b, int):
        param_b = 10
    else:  # pragma: no cover
        pass

    param_a = f"Hey {param_a}"  # Local only
    param_b += 20  # Local only

    return "bar"


class MockFunction:
    """Defines a Mock, for functions, to explore the execution details.

    :var func: Function to mock
    :vartype func: collections.abc.Callable[logging_strict.tech_niques.context_locals._P, logging_strict.tech_niques.context_locals._T]

    .. seealso::

       Used by :py:func:`logging_strict.tech_niques.get_locals`

    """

    def __init__(self, func):
        """Class constructor"""
        self.func = func
        fw = FuncWrapper(func)
        self.full_name = fw.full_name

    def __call__(  # type: ignore[misc]  # missing self non-static method
        mock_instance,
        /,
        *args,
        **kwargs,
    ):
        """Mock modifies a target function.
        The locals are included into the :paramref:`mock_instance`.
        Return value passes through

        Must use on a function with a single return value. Not yield or raise.

        :param mock_instance:

           A generic module level function. Is modified and executed. piggy backing
           the module level function ``locals`` onto the return statement

        :type mock_instance: unittest.mock.MagicMock
        :param args: Generic positional args
        :type args: logging_strict.tech_niques.context_locals._P.args
        :param kwargs: Generic keyword args
        :type kwargs: logging_strict.tech_niques.context_locals._P.kwargs
        :returns:

            Module levels function normal return value

        :rtype: typing.Any

        .. seealso::

           :py:class:`typing.ParamSpec`

        """
        # Modify ``return`` statement, to include ``locals()``. Returns a tuple
        code = re.sub(
            "[\\s]return\\b",
            " return locals(), ",
            dedent(inspect.getsource(mock_instance.func)),
        )

        # Modify to call the modified function
        # code = code + f"\nloc, ret = {mock_instance.func.__name__}(*args, **kwargs)"
        # mock_instance.func.__name__ --> mock_instance.full_name
        support_return_tuple = (
            f"\nt_ret = {mock_instance.func.__name__}(*args, **kwargs)\n"
            "loc = t_ret[0]\n"
            "ret = t_ret[1] if len(t_ret[1:]) == 1 else t_ret[1:]"
        )
        code += support_return_tuple

        # Execute the modified function code passing in the params
        loc = {"args": args, "kwargs": kwargs}
        exec(code, mock_instance.func.__globals__, loc)

        # Put execution locals into mock instance. ``l`` is locals variable name
        for locals_name, locals_val in loc["loc"].items():  # type: ignore[attr-defined]
            setattr(mock_instance, locals_name, locals_val)

        # Return normal return value as if nothing was ever modified
        return loc["ret"]


class MockMethod:
    """Defines a Mock, for functions, to explore the execution details.

    :var func: Function to mock
    :vartype func: collections.abc.Callable[logging_strict.tech_niques.context_locals._P, logging_strict.tech_niques.context_locals._T]

    .. seealso::

       Used by :py:func:`logging_strict.tech_niques.get_locals`

    """

    def __init__(self, cls, func):
        """Class constructor"""
        self.cls = cls
        self.func = func

    def __call__(  # type: ignore[misc]  # missing self non-static method
        mock_instance,
        /,
        *args,
        **kwargs,
    ):
        """Mock modifies a target function.
        The locals are included into the :paramref:`mock_instance`.
        Return value passes through

        Must use on a function with a single return value. Not yield or raise.

        :param mock_instance:

           A generic module level function. Is modified and executed. piggy backing
           the module level function ``locals`` onto the return statement

        :type mock_instance: unittest.mock.MagicMock
        :param args: Generic positional args
        :type args: logging_strict.tech_niques.context_locals._P.args
        :param kwargs: Generic keyword args
        :type kwargs: logging_strict.tech_niques.context_locals._P.kwargs
        :returns:

            Module levels function normal return value

        :rtype: typing.Any

        .. seealso::

           :py:class:`typing.ParamSpec`

        """
        # Modify ``return`` statement, to include ``locals()``. Returns a tuple
        code = re.sub(
            "[\\s]return\\b",
            " return locals(), ",
            dedent(inspect.getsource(mock_instance.func)),
        )

        # Modify to call the modified function
        # code = code + f"\nloc, ret = {mock_instance.func.__name__}(*args, **kwargs)"
        # `usage of setattr <https://stackoverflow.com/a/18620569>`_
        support_return_tuple = (
            f"""setattr({mock_instance.cls.__name__}, "{mock_instance.func.__name__}", {mock_instance.func.__name__})\n"""
            f"\nt_ret = {mock_instance.cls.__name__}.{mock_instance.func.__name__}(*args, **kwargs)\n"
            "loc = t_ret[0]\n"
            "ret = t_ret[1] if len(t_ret[1:]) == 1 else t_ret[1:]"
        )
        code += support_return_tuple

        # Execute the modified function code passing in the params
        loc = {"args": args, "kwargs": kwargs}
        # exec(code, vars(mock_instance.module), loc)
        exec(code, mock_instance.func.__globals__, loc)

        # Put execution locals into mock instance. ``l`` is locals variable name
        for locals_name, locals_val in loc["loc"].items():  # type: ignore[attr-defined]
            setattr(mock_instance, locals_name, locals_val)

        # Return normal return value as if nothing was ever modified
        return loc["ret"]


def get_locals_dynamic(
    func,
    /,
    *args,
    **kwargs,
):
    """Uses :py:func:`patch <unittest.mock.patch>` to retrieve the
    tested functions locals and return value!

    See this module docs for example

    Limitation: the function must end with a single ``return``, not
    ``yield`` or ``raise``.

    :param func_path: dotted path to func
    :type func_path: str
    :param func: The func
    :type func: collections.abc.Callable[logging_strict.tech_niques.context_locals._T, typing.Any]
    :param args: Positional arguments
    :type args: typing.ParamSpecArgs
    :param kwargs: Optional (keyword) arguments
    :type kwargs: typing.ParamSpecKwargs
    :returns: Tuple containing return value and the locals
    :rtype: tuple[logging_strict.tech_niques.context_locals._T, dict[str, typing.Any]]
    """
    fw = FuncWrapper(func)
    # may raise ModuleNotFoundError
    func_path_dynamic = fw.get_dotted_path()
    if fw.cls is None:
        # is_fcn = inspect.isfunction(func)
        callable_func = func
        side_effect = MockFunction(callable_func)
    else:
        is_has_funk = hasattr(func, "__func__")
        if is_has_funk:
            # staticmethod or classmethod func hidden by descriptor
            # fw.full_name
            # callable_func = getattr(cls, func.__name__)
            callable_func = func.__func__
            side_effect = MockMethod(fw.cls, callable_func)
        else:
            # normal method
            callable_func = func
            side_effect = MockMethod(fw.cls, callable_func)

    with patch(
        func_path_dynamic,
        autospec=True,
        side_effect=side_effect,
    ) as mocked:
        # mocked type is function
        ret = mocked(*args, **kwargs)
        # print(inspect.getmembers(mocked.side_effect))
        d_locals = {}
        for k, v in mocked.side_effect.__dict__.items():
            if k != "func":
                d_locals[k] = v

        return ret, d_locals


def get_locals(
    func_path,
    func,
    /,
    *args,
    **kwargs,
):
    """Uses :py:func:`patch <unittest.mock.patch>` to retrieve the
    tested functions locals and return value!

    See this module docs for example

    Limitation: the function must end with a single ``return``, not
    ``yield`` or ``raise``.

    :param func_path: dotted path to func
    :type func_path: str
    :param func: The func
    :type func: collections.abc.Callable[logging_strict.tech_niques.context_locals._T, typing.Any]
    :param args: Positional arguments
    :type args: typing.ParamSpecArgs
    :param kwargs: Optional (keyword) arguments
    :type kwargs: typing.ParamSpecKwargs
    :returns: Tuple containing return value and the locals
    :rtype: tuple[logging_strict.tech_niques.context_locals._T, dict[str, typing.Any]]

    .. deprecated:: 1.6.0

       get_locals_dynamic does not need func_path and has support for
       class methods.

       Removal not planned. Very popular, widely used, transition low
       priority and will take time.

    """
    with patch(
        func_path,
        autospec=True,
        side_effect=MockFunction(func),
    ) as mocked:
        # mocked type is function
        ret = mocked(*args, **kwargs)
        # print(inspect.getmembers(mocked.side_effect))
        d_locals = {}
        for k, v in mocked.side_effect.__dict__.items():
            if k != "func":
                d_locals[k] = v

        return ret, d_locals
