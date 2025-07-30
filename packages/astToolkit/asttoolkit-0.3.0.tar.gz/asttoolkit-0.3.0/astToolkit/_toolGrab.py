# ruff: noqa: F403, F405
"""This file is generated automatically, so changes to this file will be lost."""
from astToolkit import NodeORattribute
from astToolkit._astTypes import *
from collections.abc import Callable, Sequence
from typing import Any, Literal
import ast
import sys

class Grab:
    """
	Modify specific attributes of AST nodes while preserving the node structure.

	The Grab class provides static methods that create transformation functions to modify specific attributes of AST
	nodes. Unlike DOT which provides read-only access, Grab allows for targeted modifications of node attributes without
	replacing the entire node.

	Each method returns a function that takes a node, applies a transformation to a specific attribute of that node, and
	returns the modified node. This enables fine-grained control when transforming AST structures.
	"""

    @staticmethod
    def andDoAllOf(listOfActions: list[Callable[[NodeORattribute], NodeORattribute]]) -> Callable[[NodeORattribute], NodeORattribute]:

        def workhorse(node: NodeORattribute) -> NodeORattribute:
            for action in listOfActions:
                node = action(node)
            return node
        return workhorse

    @staticmethod
    def annotationAttribute(action: Callable[[ast.expr], ast.expr] | Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTannotation], hasDOTannotation]:

        def workhorse(node: hasDOTannotation) -> hasDOTannotation:
            node.annotation = action(node.annotation) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def argAttribute(action: Callable[[str | None], str | None] | Callable[[str], str]) -> Callable[[hasDOTarg], hasDOTarg]:

        def workhorse(node: hasDOTarg) -> hasDOTarg:
            node.arg = action(node.arg) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def argsAttribute(action: Callable[[ast.arguments], ast.arguments] | Callable[[list[ast.arg]], list[ast.arg]] | Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTargs], hasDOTargs]:

        def workhorse(node: hasDOTargs) -> hasDOTargs:
            node.args = action(node.args) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def argtypesAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTargtypes], hasDOTargtypes]:

        def workhorse(node: hasDOTargtypes) -> hasDOTargtypes:
            node.argtypes = action(node.argtypes)
            return node
        return workhorse

    @staticmethod
    def asnameAttribute(action: Callable[[str | None], str | None]) -> Callable[[hasDOTasname], hasDOTasname]:

        def workhorse(node: hasDOTasname) -> hasDOTasname:
            node.asname = action(node.asname)
            return node
        return workhorse

    @staticmethod
    def attrAttribute(action: Callable[[str], str]) -> Callable[[hasDOTattr], hasDOTattr]:

        def workhorse(node: hasDOTattr) -> hasDOTattr:
            node.attr = action(node.attr)
            return node
        return workhorse

    @staticmethod
    def basesAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTbases], hasDOTbases]:

        def workhorse(node: hasDOTbases) -> hasDOTbases:
            node.bases = action(node.bases)
            return node
        return workhorse

    @staticmethod
    def bodyAttribute(action: Callable[[ast.expr], ast.expr] | Callable[[list[ast.stmt]], list[ast.stmt]]) -> Callable[[hasDOTbody], hasDOTbody]:

        def workhorse(node: hasDOTbody) -> hasDOTbody:
            node.body = action(node.body) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def boundAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTbound], hasDOTbound]:

        def workhorse(node: hasDOTbound) -> hasDOTbound:
            node.bound = action(node.bound)
            return node
        return workhorse

    @staticmethod
    def casesAttribute(action: Callable[[list[ast.match_case]], list[ast.match_case]]) -> Callable[[hasDOTcases], hasDOTcases]:

        def workhorse(node: hasDOTcases) -> hasDOTcases:
            node.cases = action(node.cases)
            return node
        return workhorse

    @staticmethod
    def causeAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTcause], hasDOTcause]:

        def workhorse(node: hasDOTcause) -> hasDOTcause:
            node.cause = action(node.cause)
            return node
        return workhorse

    @staticmethod
    def clsAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTcls], hasDOTcls]:

        def workhorse(node: hasDOTcls) -> hasDOTcls:
            node.cls = action(node.cls)
            return node
        return workhorse

    @staticmethod
    def comparatorsAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTcomparators], hasDOTcomparators]:

        def workhorse(node: hasDOTcomparators) -> hasDOTcomparators:
            node.comparators = action(node.comparators)
            return node
        return workhorse

    @staticmethod
    def context_exprAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTcontext_expr], hasDOTcontext_expr]:

        def workhorse(node: hasDOTcontext_expr) -> hasDOTcontext_expr:
            node.context_expr = action(node.context_expr)
            return node
        return workhorse

    @staticmethod
    def conversionAttribute(action: Callable[[int], int]) -> Callable[[hasDOTconversion], hasDOTconversion]:

        def workhorse(node: hasDOTconversion) -> hasDOTconversion:
            node.conversion = action(node.conversion)
            return node
        return workhorse

    @staticmethod
    def ctxAttribute(action: Callable[[ast.expr_context], ast.expr_context]) -> Callable[[hasDOTctx], hasDOTctx]:

        def workhorse(node: hasDOTctx) -> hasDOTctx:
            node.ctx = action(node.ctx)
            return node
        return workhorse

    @staticmethod
    def decorator_listAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTdecorator_list], hasDOTdecorator_list]:

        def workhorse(node: hasDOTdecorator_list) -> hasDOTdecorator_list:
            node.decorator_list = action(node.decorator_list)
            return node
        return workhorse
    if sys.version_info >= (3, 13):

        @staticmethod
        def default_valueAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTdefault_value], hasDOTdefault_value]:

            def workhorse(node: hasDOTdefault_value) -> hasDOTdefault_value:
                node.default_value = action(node.default_value)
                return node
            return workhorse

    @staticmethod
    def defaultsAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTdefaults], hasDOTdefaults]:

        def workhorse(node: hasDOTdefaults) -> hasDOTdefaults:
            node.defaults = action(node.defaults)
            return node
        return workhorse

    @staticmethod
    def eltAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTelt], hasDOTelt]:

        def workhorse(node: hasDOTelt) -> hasDOTelt:
            node.elt = action(node.elt)
            return node
        return workhorse

    @staticmethod
    def eltsAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTelts], hasDOTelts]:

        def workhorse(node: hasDOTelts) -> hasDOTelts:
            node.elts = action(node.elts)
            return node
        return workhorse

    @staticmethod
    def excAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTexc], hasDOTexc]:

        def workhorse(node: hasDOTexc) -> hasDOTexc:
            node.exc = action(node.exc)
            return node
        return workhorse

    @staticmethod
    def finalbodyAttribute(action: Callable[[list[ast.stmt]], list[ast.stmt]]) -> Callable[[hasDOTfinalbody], hasDOTfinalbody]:

        def workhorse(node: hasDOTfinalbody) -> hasDOTfinalbody:
            node.finalbody = action(node.finalbody)
            return node
        return workhorse

    @staticmethod
    def format_specAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTformat_spec], hasDOTformat_spec]:

        def workhorse(node: hasDOTformat_spec) -> hasDOTformat_spec:
            node.format_spec = action(node.format_spec)
            return node
        return workhorse

    @staticmethod
    def funcAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTfunc], hasDOTfunc]:

        def workhorse(node: hasDOTfunc) -> hasDOTfunc:
            node.func = action(node.func)
            return node
        return workhorse

    @staticmethod
    def generatorsAttribute(action: Callable[[list[ast.comprehension]], list[ast.comprehension]]) -> Callable[[hasDOTgenerators], hasDOTgenerators]:

        def workhorse(node: hasDOTgenerators) -> hasDOTgenerators:
            node.generators = action(node.generators)
            return node
        return workhorse

    @staticmethod
    def guardAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTguard], hasDOTguard]:

        def workhorse(node: hasDOTguard) -> hasDOTguard:
            node.guard = action(node.guard)
            return node
        return workhorse

    @staticmethod
    def handlersAttribute(action: Callable[[list[ast.ExceptHandler]], list[ast.ExceptHandler]]) -> Callable[[hasDOThandlers], hasDOThandlers]:

        def workhorse(node: hasDOThandlers) -> hasDOThandlers:
            node.handlers = action(node.handlers)
            return node
        return workhorse

    @staticmethod
    def idAttribute(action: Callable[[str], str]) -> Callable[[hasDOTid], hasDOTid]:

        def workhorse(node: hasDOTid) -> hasDOTid:
            node.id = action(node.id)
            return node
        return workhorse

    @staticmethod
    def ifsAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTifs], hasDOTifs]:

        def workhorse(node: hasDOTifs) -> hasDOTifs:
            node.ifs = action(node.ifs)
            return node
        return workhorse

    @staticmethod
    def is_asyncAttribute(action: Callable[[int], int]) -> Callable[[hasDOTis_async], hasDOTis_async]:

        def workhorse(node: hasDOTis_async) -> hasDOTis_async:
            node.is_async = action(node.is_async)
            return node
        return workhorse

    @staticmethod
    def itemsAttribute(action: Callable[[list[ast.withitem]], list[ast.withitem]]) -> Callable[[hasDOTitems], hasDOTitems]:

        def workhorse(node: hasDOTitems) -> hasDOTitems:
            node.items = action(node.items)
            return node
        return workhorse

    @staticmethod
    def iterAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTiter], hasDOTiter]:

        def workhorse(node: hasDOTiter) -> hasDOTiter:
            node.iter = action(node.iter)
            return node
        return workhorse

    @staticmethod
    def keyAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTkey], hasDOTkey]:

        def workhorse(node: hasDOTkey) -> hasDOTkey:
            node.key = action(node.key)
            return node
        return workhorse

    @staticmethod
    def keysAttribute(action: Callable[[list[ast.expr]], list[ast.expr]] | Callable[[list[ast.expr | None]], list[ast.expr | None]]) -> Callable[[hasDOTkeys], hasDOTkeys]:

        def workhorse(node: hasDOTkeys) -> hasDOTkeys:
            node.keys = action(node.keys) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def keywordsAttribute(action: Callable[[list[ast.keyword]], list[ast.keyword]]) -> Callable[[hasDOTkeywords], hasDOTkeywords]:

        def workhorse(node: hasDOTkeywords) -> hasDOTkeywords:
            node.keywords = action(node.keywords)
            return node
        return workhorse

    @staticmethod
    def kindAttribute(action: Callable[[str | None], str | None]) -> Callable[[hasDOTkind], hasDOTkind]:

        def workhorse(node: hasDOTkind) -> hasDOTkind:
            node.kind = action(node.kind)
            return node
        return workhorse

    @staticmethod
    def kw_defaultsAttribute(action: Callable[[list[ast.expr | None]], list[ast.expr | None]]) -> Callable[[hasDOTkw_defaults], hasDOTkw_defaults]:

        def workhorse(node: hasDOTkw_defaults) -> hasDOTkw_defaults:
            node.kw_defaults = action(node.kw_defaults)
            return node
        return workhorse

    @staticmethod
    def kwargAttribute(action: Callable[[ast.arg | None], ast.arg | None]) -> Callable[[hasDOTkwarg], hasDOTkwarg]:

        def workhorse(node: hasDOTkwarg) -> hasDOTkwarg:
            node.kwarg = action(node.kwarg)
            return node
        return workhorse

    @staticmethod
    def kwd_attrsAttribute(action: Callable[[list[str]], list[str]]) -> Callable[[hasDOTkwd_attrs], hasDOTkwd_attrs]:

        def workhorse(node: hasDOTkwd_attrs) -> hasDOTkwd_attrs:
            node.kwd_attrs = action(node.kwd_attrs)
            return node
        return workhorse

    @staticmethod
    def kwd_patternsAttribute(action: Callable[[list[ast.pattern]], list[ast.pattern]]) -> Callable[[hasDOTkwd_patterns], hasDOTkwd_patterns]:

        def workhorse(node: hasDOTkwd_patterns) -> hasDOTkwd_patterns:
            node.kwd_patterns = action(node.kwd_patterns)
            return node
        return workhorse

    @staticmethod
    def kwonlyargsAttribute(action: Callable[[list[ast.arg]], list[ast.arg]]) -> Callable[[hasDOTkwonlyargs], hasDOTkwonlyargs]:

        def workhorse(node: hasDOTkwonlyargs) -> hasDOTkwonlyargs:
            node.kwonlyargs = action(node.kwonlyargs)
            return node
        return workhorse

    @staticmethod
    def leftAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTleft], hasDOTleft]:

        def workhorse(node: hasDOTleft) -> hasDOTleft:
            node.left = action(node.left)
            return node
        return workhorse

    @staticmethod
    def levelAttribute(action: Callable[[int], int]) -> Callable[[hasDOTlevel], hasDOTlevel]:

        def workhorse(node: hasDOTlevel) -> hasDOTlevel:
            node.level = action(node.level)
            return node
        return workhorse

    @staticmethod
    def linenoAttribute(action: Callable[[int], int]) -> Callable[[hasDOTlineno], hasDOTlineno]:

        def workhorse(node: hasDOTlineno) -> hasDOTlineno:
            node.lineno = action(node.lineno)
            return node
        return workhorse

    @staticmethod
    def lowerAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTlower], hasDOTlower]:

        def workhorse(node: hasDOTlower) -> hasDOTlower:
            node.lower = action(node.lower)
            return node
        return workhorse

    @staticmethod
    def moduleAttribute(action: Callable[[str | None], str | None]) -> Callable[[hasDOTmodule], hasDOTmodule]:

        def workhorse(node: hasDOTmodule) -> hasDOTmodule:
            node.module = action(node.module)
            return node
        return workhorse

    @staticmethod
    def msgAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTmsg], hasDOTmsg]:

        def workhorse(node: hasDOTmsg) -> hasDOTmsg:
            node.msg = action(node.msg)
            return node
        return workhorse

    @staticmethod
    def nameAttribute(action: Callable[[ast.Name], ast.Name] | Callable[[str | None], str | None] | Callable[[str], str]) -> Callable[[hasDOTname], hasDOTname]:

        def workhorse(node: hasDOTname) -> hasDOTname:
            node.name = action(node.name) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def namesAttribute(action: Callable[[list[ast.alias]], list[ast.alias]] | Callable[[list[str]], list[str]]) -> Callable[[hasDOTnames], hasDOTnames]:

        def workhorse(node: hasDOTnames) -> hasDOTnames:
            node.names = action(node.names) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def opAttribute(action: Callable[[ast.boolop], ast.boolop] | Callable[[ast.operator], ast.operator] | Callable[[ast.unaryop], ast.unaryop]) -> Callable[[hasDOTop], hasDOTop]:

        def workhorse(node: hasDOTop) -> hasDOTop:
            node.op = action(node.op) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def operandAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOToperand], hasDOToperand]:

        def workhorse(node: hasDOToperand) -> hasDOToperand:
            node.operand = action(node.operand)
            return node
        return workhorse

    @staticmethod
    def opsAttribute(action: Callable[[list[ast.cmpop]], list[ast.cmpop]]) -> Callable[[hasDOTops], hasDOTops]:

        def workhorse(node: hasDOTops) -> hasDOTops:
            node.ops = action(node.ops)
            return node
        return workhorse

    @staticmethod
    def optional_varsAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOToptional_vars], hasDOToptional_vars]:

        def workhorse(node: hasDOToptional_vars) -> hasDOToptional_vars:
            node.optional_vars = action(node.optional_vars)
            return node
        return workhorse

    @staticmethod
    def orelseAttribute(action: Callable[[ast.expr], ast.expr] | Callable[[list[ast.stmt]], list[ast.stmt]]) -> Callable[[hasDOTorelse], hasDOTorelse]:

        def workhorse(node: hasDOTorelse) -> hasDOTorelse:
            node.orelse = action(node.orelse) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def patternAttribute(action: Callable[[ast.pattern], ast.pattern] | Callable[[ast.pattern | None], ast.pattern | None]) -> Callable[[hasDOTpattern], hasDOTpattern]:

        def workhorse(node: hasDOTpattern) -> hasDOTpattern:
            node.pattern = action(node.pattern) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def patternsAttribute(action: Callable[[list[ast.pattern]], list[ast.pattern]]) -> Callable[[hasDOTpatterns], hasDOTpatterns]:

        def workhorse(node: hasDOTpatterns) -> hasDOTpatterns:
            node.patterns = action(node.patterns)
            return node
        return workhorse

    @staticmethod
    def posonlyargsAttribute(action: Callable[[list[ast.arg]], list[ast.arg]]) -> Callable[[hasDOTposonlyargs], hasDOTposonlyargs]:

        def workhorse(node: hasDOTposonlyargs) -> hasDOTposonlyargs:
            node.posonlyargs = action(node.posonlyargs)
            return node
        return workhorse

    @staticmethod
    def restAttribute(action: Callable[[str | None], str | None]) -> Callable[[hasDOTrest], hasDOTrest]:

        def workhorse(node: hasDOTrest) -> hasDOTrest:
            node.rest = action(node.rest)
            return node
        return workhorse

    @staticmethod
    def returnsAttribute(action: Callable[[ast.expr], ast.expr] | Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTreturns], hasDOTreturns]:

        def workhorse(node: hasDOTreturns) -> hasDOTreturns:
            node.returns = action(node.returns) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def rightAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTright], hasDOTright]:

        def workhorse(node: hasDOTright) -> hasDOTright:
            node.right = action(node.right)
            return node
        return workhorse

    @staticmethod
    def simpleAttribute(action: Callable[[int], int]) -> Callable[[hasDOTsimple], hasDOTsimple]:

        def workhorse(node: hasDOTsimple) -> hasDOTsimple:
            node.simple = action(node.simple)
            return node
        return workhorse

    @staticmethod
    def sliceAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTslice], hasDOTslice]:

        def workhorse(node: hasDOTslice) -> hasDOTslice:
            node.slice = action(node.slice)
            return node
        return workhorse

    @staticmethod
    def stepAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTstep], hasDOTstep]:

        def workhorse(node: hasDOTstep) -> hasDOTstep:
            node.step = action(node.step)
            return node
        return workhorse

    @staticmethod
    def subjectAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTsubject], hasDOTsubject]:

        def workhorse(node: hasDOTsubject) -> hasDOTsubject:
            node.subject = action(node.subject)
            return node
        return workhorse

    @staticmethod
    def tagAttribute(action: Callable[[str], str]) -> Callable[[hasDOTtag], hasDOTtag]:

        def workhorse(node: hasDOTtag) -> hasDOTtag:
            node.tag = action(node.tag)
            return node
        return workhorse

    @staticmethod
    def targetAttribute(action: Callable[[ast.expr], ast.expr] | Callable[[ast.Name], ast.Name] | Callable[[ast.Name | ast.Attribute | ast.Subscript], ast.Name | ast.Attribute | ast.Subscript]) -> Callable[[hasDOTtarget], hasDOTtarget]:

        def workhorse(node: hasDOTtarget) -> hasDOTtarget:
            node.target = action(node.target) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def targetsAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTtargets], hasDOTtargets]:

        def workhorse(node: hasDOTtargets) -> hasDOTtargets:
            node.targets = action(node.targets)
            return node
        return workhorse

    @staticmethod
    def testAttribute(action: Callable[[ast.expr], ast.expr]) -> Callable[[hasDOTtest], hasDOTtest]:

        def workhorse(node: hasDOTtest) -> hasDOTtest:
            node.test = action(node.test)
            return node
        return workhorse

    @staticmethod
    def typeAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTtype], hasDOTtype]:

        def workhorse(node: hasDOTtype) -> hasDOTtype:
            node.type = action(node.type)
            return node
        return workhorse

    @staticmethod
    def type_commentAttribute(action: Callable[[str | None], str | None]) -> Callable[[hasDOTtype_comment], hasDOTtype_comment]:

        def workhorse(node: hasDOTtype_comment) -> hasDOTtype_comment:
            node.type_comment = action(node.type_comment)
            return node
        return workhorse

    @staticmethod
    def type_ignoresAttribute(action: Callable[[list[ast.TypeIgnore]], list[ast.TypeIgnore]]) -> Callable[[hasDOTtype_ignores], hasDOTtype_ignores]:

        def workhorse(node: hasDOTtype_ignores) -> hasDOTtype_ignores:
            node.type_ignores = action(node.type_ignores)
            return node
        return workhorse

    @staticmethod
    def type_paramsAttribute(action: Callable[[list[ast.type_param]], list[ast.type_param]]) -> Callable[[hasDOTtype_params], hasDOTtype_params]:

        def workhorse(node: hasDOTtype_params) -> hasDOTtype_params:
            node.type_params = action(node.type_params)
            return node
        return workhorse

    @staticmethod
    def upperAttribute(action: Callable[[ast.expr | None], ast.expr | None]) -> Callable[[hasDOTupper], hasDOTupper]:

        def workhorse(node: hasDOTupper) -> hasDOTupper:
            node.upper = action(node.upper)
            return node
        return workhorse

    @staticmethod
    def valueAttribute(action: Callable[[ast.expr], ast.expr] | Callable[[ast.expr | None], ast.expr | None] | Callable[[bool | None], bool | None] | Callable[[Any], Any]) -> Callable[[hasDOTvalue], hasDOTvalue]:

        def workhorse(node: hasDOTvalue) -> hasDOTvalue:
            node.value = action(node.value) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]
            return node
        return workhorse

    @staticmethod
    def valuesAttribute(action: Callable[[list[ast.expr]], list[ast.expr]]) -> Callable[[hasDOTvalues], hasDOTvalues]:

        def workhorse(node: hasDOTvalues) -> hasDOTvalues:
            node.values = action(node.values)
            return node
        return workhorse

    @staticmethod
    def varargAttribute(action: Callable[[ast.arg | None], ast.arg | None]) -> Callable[[hasDOTvararg], hasDOTvararg]:

        def workhorse(node: hasDOTvararg) -> hasDOTvararg:
            node.vararg = action(node.vararg)
            return node
        return workhorse