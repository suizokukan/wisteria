# https://en.wikipedia.org/wiki/Comparison_of_data-serialization_formats

# TODO:
# * quelle version est utilisée ?
# * résumé concernant la méthode X ()
# * vrai objet (musamusa_atext)
#
# génération automatique de rapports du type (améliorer l'anglais):
# * Iaswn vs jsonpickle:
# `Iaswn` seems faster than `jsonpickle` and produces shorter json-strings; `jsonpickle` handles much more types than `Iaswn`.
# * Iaswn vs pyyaml:
# `Iaswn` seems faster than `pyyaml` and produces shorter json-strings; `Iaswn` handles many more types than `pyyaml`.


# à quoi sert Quaternion ?
# ça ne va pas: impossible de comparer Quaternion et Quaternion2
# TODO: quels objets donner ?
# [DONE]: tableau de détail
# TODO: écarts max.
# TODO: il manque marshmallow

# mieux faire: un .ini pour sélectionner les méthodes
# mieux faire: un .ini pour sélectionner les données

# DOC: la longueur des bytes est calculée, parfois il faut encoder utf-8 la string de sortie.
import collections
import contextlib
import decimal
import json
import marshal
import msgpack
import numbers
import pickle
import timeit
import re

from iaswn.iaswn import Iaswn, IaswnError
from iaswn.iaswn import to_jsonstr as iaswn_to_jsonstr
from iaswn.iaswn import from_jsonstr as iaswn_from_jsonstr

import jsonpickle
import yaml
import rich
import rich.table

TIMEITNUMBER = 10

METHODNAMES = set()


bigdict1 = {"1": 2,
            "2": 3,
            "3": None,
            }
bigdict2 = {"None": bigdict1,
            "4": None}
bigdict3 = {"None": 3,
            "False": bigdict2}
bigdict4 = {"None": 3,
            "False": 4,
            "5": bigdict3}
bigdict5 = {"None": 5,
            "False": 6,
            "6": 7,
            "null": 8,
            "list": bigdict4}
bigdict6 = {"None": 1,
            "False": 2,
            "7": 3,
            "null": 4,
            "True": 5,
            "list": bigdict5}
bigdict7 = {"None": 1,
            "False": 2,
            "8": 3,
            "null": {"3": 4},
            "True": 5,
            "9": 6,
            "list": bigdict6}


class MetaClass(type):
    pass

class RegularClass:

    def __eq__(self, other):
        return type(self) == type(other)

    async def async_method():
        pass

    @classmethod
    def class_method(cls):
        pass

    def generator(self):
        yield None

    def method(self):
        pass

    @staticmethod
    def static_method():
        pass


class RegularClassDict(dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        self["3"] = 5


class RegularClassDict2(dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        self["3"] = RegularClassDict()
        self["4"] = bigdict3


class RegularClassDict3(dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        self["3"] = None
        self["4"] = RegularClassDict()
        self["5"] = bigdict1


class RegularClassDict3bis(dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        self["3"] = RegularClassDict()
        self["4"] = "something"
        self["5"] = bigdict7

class RegularClassList(list):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self) == tuple(items for items in other)

    def __init__(self):
        list.__init__(self)
        self.append(3j)


class RegularClassIaswn(Iaswn):
    def __init__(self):
        Iaswn.__init__(self)


class RegularClassDictIaswn(dict, Iaswn):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        Iaswn.__init__(self)
        self["3"] = 5

class RegularClassDictIaswn2(Iaswn, dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        Iaswn.__init__(self)
        self["3"] = RegularClassDictIaswn()
        self["4"] = bigdict3


class RegularClassDictIaswn3(Iaswn, dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        Iaswn.__init__(self)
        self["3"] = None
        self["4"] = RegularClassDictIaswn()
        self["5"] = bigdict1


class RegularClassDictIaswn3bis(Iaswn, dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        Iaswn.__init__(self)
        self["3"] = RegularClassDictIaswn()
        self["4"] = "something"
        self["5"] = bigdict7


class RegularClassListIaswn(Iaswn, list):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self) == tuple(items for items in other)

    def __init__(self):
        list.__init__(self)
        Iaswn.__init__(self)
        self.append(4j)


class RegularClassDictIaswn(Iaswn, dict):
    def __eq__(self, other):
        return type(self) == type(other) and \
            tuple(items for items in self.items()) == tuple(items for items in other.items())

    def __init__(self):
        dict.__init__(self)
        Iaswn.__init__(self)
        self["3"] = 5


class Quaternion:
    def __init__(self,
                 a=0,
                 b=0,
                 c=0,
                 d=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def __eq__(self,
               other):
        if type(other) != type(self):
            return False
        return self.a == other.a and \
            self.b == other.b and \
            self.c == other.c and \
            self.d == other.d

class Quaternion2(Iaswn):
    def __init__(self,
                 a=0,
                 b=0,
                 c=0,
                 d=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def __eq__(self,
               other):
        if type(other) != type(self):
            return False
        return self.a == other.a and \
            self.b == other.b and \
            self.c == other.c and \
            self.d == other.d


class ResData:
    def __init__(self,
                 encode_success = False,
                 encode_time = 0,
                 encode_length = 0,
                 decode_success = False,
                 decode_time = 0,
                 decode_identity = False):
        self.encode_success = encode_success
        self.encode_time = encode_time
        self.encode_length = encode_length
        self.decode_success = decode_success
        self.decode_time = decode_time
        self.decode_identity = decode_identity
    def __repr__(self):
        return f"({self.encode_success}; {self.encode_time}; {self.encode_length}; " \
            f"{self.decode_success}; {self.decode_time}; {self.decode_identity})"


def _len(obj):
    if type(obj) is str:
        return len(bytes(obj, "utf-8"))
    else:
        return len(obj)

NONASCII_STRING = "".join(chr(i) for i in range(1000, 10000))

rawres = {}
for obj_description, obj in (
        ("A1:None", None),
        ("A2:bool:True", True),
        ("A3:bool:False", False),
        ("A4:int", 3),
        ("A5:float", 3.0),

        ("B1:str(empty)", ""),
        ("B2:str", "0123456789"),
        ("B3:str(long)", "abc"*20000),
        ("B4:str(with non ascii)", NONASCII_STRING),

        ("C1:complex", 9+3j),

        ("D1:range(empty)", range(0)),
        ("D2:range", range(1000)),

        ("E1:bytes(empty)", bytes),
        ("E2:bytes", b"123"),

        ("F1:bytearray(empty)", bytearray()),
        ("F2:bytearray", bytearray(b"123")),

        ("G1:memoryview(empty)", memoryview(b"")),
        ("G2:memoryview", memoryview(b"123")),

        ("H1:type(int)", type(int)),
        ("H2:type(type(int))", type(type(int))),

        ("I1:tuple(empty)", tuple()),
        ("I2:tuple", (1, 2, 3)),
        ("I3:tuple inside a tuple (l.1)", (1, 2, 3)),
        ("I4:tuple inside a tuple (l.2)", (1, 2, (1, 2, 3))),
        ("I5:tuple inside a tuple (l.3)", (1, 2, (1, 2, (1, 2, 3)))),

        ("J1:list(empty)", list()),
        ("J2:list", [1, 2, 3]),
        ("J3:list inside a list (l.1)", [1, 2, 3]),
        ("J4:list inside a list (l.2)", [1, 2, [1, 2, 3]]),
        ("J5:list inside a list (l.3)", [1, 2, [1, 2, [1, 2, 3]]]),

        ("K1:dict(empty)", dict()),
        ("K2:dict(keys:str)", {"": 0, "1": 2, "3": 4}),
        ("K2:dict(keys:None)", {None: 2,}),
        ("K2:dict(keys:int)", {1: "2", 2: "4"}),
        ("K2:dict(keys:float)", {1.0: "1.0", 1.1: "1.1"}),
        ("K2:dict(keys:complex)", {3+2j: "3+2j", 4: "4"}),
        ("K2:dict(keys:bool)", {True: "True", False: "False"}),
        ("K2:dict(keys:tuple)", {(): "empty tuple", (1,): "tuple"}),
        ("K2:dict(keys:frozenset)", {frozenset(): "empty frozenset", frozenset((1,)): "frozenset"}),
        ("K2:dict(keys:bytes)", {bytes(): "empty bytes", bytes(b"bytes"): "bytes"}),  
        ("K3:dict/problematic keys", {3: None, "3": None, None: None, "none": None, "null": None, "": None}),
        ("K4:dict inside a dict (l.1)", {"1": "2", "3": {"4": 5}}),
        ("K5:dict inside a dict (l.2)", {"1": "2", "3": {"4": {"5": 6}}}),
        ("K6:dict inside a dict (l.3)", {"1": "2", "3": {"4": {"5": {"6": 7}}}}),

        ("L1:set(empty)", set()),
        ("L2:set", set((1, 2, 3))),

        ("M1:frozenset(empty)", frozenset()),
        ("M2:frozenset", frozenset((1, 2, 3))),

        ("N1:re.Pattern", re.compile(".*")),
        ("N2:re.Pattern(bytes)", re.compile(b".*")),
        ("N3:re.Pattern+flag", re.compile(".*", re.M)),
        ("N4:re.Pattern+flag(bytes)", re.compile(b".*", re.M)),

        ("O1:re.Match/1", re.match(".*", "abc")),
        ("O2:re.Match/2", re.match("def", "abc")),

        ("P1:NotImplemented", NotImplemented),

        ("Q1:NotImplementedError", NotImplementedError),
        ("Q2:TypeError", TypeError),

        ("R01:class::meta class", MetaClass),

        ("R02:class::reg. class::RegularClass()", RegularClass()),
        ("R03:class::reg. class::async method", RegularClass.async_method),
        ("R04:class::reg. class::generator", RegularClass.generator),
        ("R05:class::reg. class::method", RegularClass.method),
        ("R06:class::reg. class::class method", RegularClass.class_method),
        ("R07:class::reg. class::static method", RegularClass.static_method),

        ("R08:class::reg. class::RegularClassList()", RegularClassList()),
        ("R09:class::reg. class::RegularClassDict()", RegularClassDict()),
        ("R10:class::reg. class::RegularClassDict2()", RegularClassDict2()),
        ("R11:class::reg. class::RegularClassDict3()", RegularClassDict3()),
        ("R12:class::reg. class::RegularClassDict3bis()", RegularClassDict3bis()),

        ("R13:class::reg. class<Iaswn::RegularClassIaswn()", RegularClassIaswn()),

        ("R14:class::reg. classlist<Iaswn::RegularClassListIaswn()", RegularClassListIaswn()),
        ("R15:class::reg. classdict<Iaswn::RegularClassDictIaswn()", RegularClassDictIaswn()),
        ("R16:class::reg. classdict<Iaswn::RegularClassDictIaswn2()", RegularClassDictIaswn2()),
        ("R17:class::reg. classdict<Iaswn::RegularClassDictIaswn3()", RegularClassDictIaswn3()),
        ("R18:class::reg. classdict<Iaswn::RegularClassDictIaswn3bis()", RegularClassDictIaswn3bis()),

        ("S1:function", _len),

        ("T1:imported module", timeit),
        ("T2:imported module(class)", timeit.Timer),
        ("T3:imported module(function)", timeit.timeit),

        ("U1:Python function", print),

        ("V1:numbers::Number", numbers.Number),
        ("V2:numbers::Number()", numbers.Number()),
        ("V3:numbers::Integral", numbers.Integral),
        ("V4:numbers::Real", numbers.Real),
        ("V5:numbers::Complex", numbers.Complex),

        ("W1:file descriptor", open("comparisons.py")),

        ("X1:bigdict1", bigdict1),
        ("X2:bigdict2", bigdict2),
        ("X3:bigdict3", bigdict3),
        ("X4:bigdict4", bigdict4),
        ("X5:bigdict5", bigdict5),
        ("X6:bigdict6", bigdict6),
        ("X7:bigdict7", bigdict7),

        ("Y01:collections.deque(empty)", collections.deque()),
        ("Y02:collections.deque", collections.deque((1, 2))),
        ("Y03:collections.defaultdict(empty)", collections.defaultdict()),
        ("Y04:collections.defaultdict", collections.defaultdict(None, {1: 2})),
        ("Y05:collections.OrderedDict(empty)", collections.OrderedDict()),
        ("Y06:collections.OrderedDict", collections.OrderedDict({1: 2})),
        ("Y07:collections.Counter(empty)", collections.Counter()),
        ("Y08:collections.Counter", collections.Counter((1, 2))),
        ("Y09:collections.ChainMap", collections.ChainMap()),
        ("Y10:collections.ChainMap", collections.ChainMap({1: 2}, {2: 3})),
        ("Y11:collections.abc.Awaitable", collections.abc.Awaitable),
        ("Y12:collections.abc.Coroutine", collections.abc.Coroutine),
        ("Y13:collections.abc.AsyncIterable", collections.abc.AsyncIterable),
        ("Y14:collections.abc.AsyncIterator", collections.abc.AsyncIterator),
        ("Y15:collections.abc.AsyncGenerator", collections.abc.AsyncGenerator),
        ("Y16:collections.abc.Reversible", collections.abc.Reversible),
        ("Y17:collections.abc.Container", collections.abc.Container),
        ("Y18:collections.abc.Collection", collections.abc.Collection),
        ("Y19:collections.abc.Callable", collections.abc.Callable),
        ("Y20:collections.abc.Set", collections.abc.Set),
        ("Y21:collections.abc.MutableSet", collections.abc.MutableSet),
        ("Y22:collections.abc.Sequence", collections.abc.Sequence),
        ("Y23:collections.abc.MutableSequence", collections.abc.MutableSequence),
        ("Y24:collections.abc.ByteString", collections.abc.ByteString),
        ("Y25:collections.abc.MappingView", collections.abc.MappingView),
        ("Y26:collections.abc.KeysView", collections.abc.KeysView),
        ("Y27:collections.abc.ItemsView", collections.abc.ItemsView),
        ("Y28:collections.abc.ValuesView", collections.abc.ValuesView),
        ("Y29:contextlib.AbstractContextManager", contextlib.AbstractContextManager),
        ("Y30:contextlib.AbstractAsyncContextManager", contextlib.AbstractAsyncContextManager),

        ("Z01:decimal.localcontext", decimal.localcontext()),
):

    rawres[obj_description] = {}

    # ---- iaswn
    method_name = "iaswn v."+iaswn.iaswn.aboutproject.__version__
    METHODNAMES.add(method_name)
    rawres[obj_description][method_name] = ResData()
    _error = False
    try:
        _res = iaswn_to_jsonstr(obj)
        _timeit = timeit.Timer("iaswn_to_jsonstr(obj)",
                               globals=globals())
        rawres[obj_description][method_name].encode_success = True
        rawres[obj_description][method_name].encode_length = _len(_res)
        rawres[obj_description][method_name].encode_time = _timeit.timeit(TIMEITNUMBER)
    except IaswnError:
        _error = True

    if not _error:
        try:
            _res2 = iaswn_from_jsonstr(_res)
            rawres[obj_description][method_name].decode_success = True
            _timeit = timeit.Timer("iaswn_from_jsonstr(_res)",
                                   globals=globals())
            rawres[obj_description][method_name].decode_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                rawres[obj_description][method_name].decode_identity = True
        except IaswnError:
            pass

    # ---- marshal
    method_name = "marshal"
    METHODNAMES.add(method_name)
    rawres[obj_description][method_name] = ResData()
    _error = False
    try:
        _res = marshal.dumps(obj)
        _timeit = timeit.Timer("marshal.dumps(obj)",
                               globals=globals())
        rawres[obj_description][method_name].encode_success = True
        rawres[obj_description][method_name].encode_length = _len(_res)
        rawres[obj_description][method_name].encode_time = _timeit.timeit(TIMEITNUMBER)
    except ValueError:
        _error = True

    if not _error:
        try:
            _res2 = marshal.loads(_res)
            _timeit = timeit.Timer("marshal.loads(_res)",
                                   globals=globals())
            rawres[obj_description][method_name].decode_success = True
            rawres[obj_description][method_name].decode_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                rawres[obj_description][method_name].decode_identity = True
        except ValueError:
            pass

    # ---- pickle
    method_name = "pickle"
    METHODNAMES.add(method_name)
    rawres[obj_description][method_name] = ResData()
    _error = False
    try:
        _res = pickle.dumps(obj)
        _timeit = timeit.Timer("pickle.dumps(obj)",
                               globals=globals())
        rawres[obj_description][method_name].encode_success = True
        rawres[obj_description][method_name].encode_length = _len(_res)
        rawres[obj_description][method_name].encode_time = _timeit.timeit(TIMEITNUMBER)
    except pickle.PicklingError:
        _error = True
    except ValueError:
        _error = True
    except TypeError:
        _error = True

    if not _error:
        try:
            _res2 = pickle.loads(_res)
            _timeit = timeit.Timer("pickle.loads(_res)",
                                   globals=globals())
            rawres[obj_description][method_name].decode_success = True
            rawres[obj_description][method_name].decode_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                rawres[obj_description][method_name].decode_identity = True
        except ValueError:
            pass

    # ---- jsonpickle
    method_name = "jsonpickle"
    METHODNAMES.add(method_name)
    rawres[obj_description][method_name] = ResData()
    _error = False
    try:
        _res = jsonpickle.encode(obj)
        _timeit = timeit.Timer("jsonpickle.encode(obj)",
                               globals=globals())
        rawres[obj_description][method_name].encode_success = True
        rawres[obj_description][method_name].encode_length = _len(_res)
        rawres[obj_description][method_name].encode_time = _timeit.timeit(TIMEITNUMBER)
    except:    # TODO je ne sais pas quelle exception peut être envoyée par jsonpickle
        _error = True

    if not _error:
        try:
            _res2 = jsonpickle.decode(_res)
            _timeit = timeit.Timer("jsonpickle.decode(_res)",
                                   globals=globals())
            rawres[obj_description][method_name].decode_success = True
            rawres[obj_description][method_name].decode_time = _timeit.timeit(TIMEITNUMBER)
            if obj == _res2:
                rawres[obj_description][method_name].decode_identity = True
        except:  # TODO je ne sais pas quelle exception peut être envoyée par jsonpickle
            pass

    # ---- json
    method_name = "json"
    METHODNAMES.add(method_name)
    rawres[obj_description][method_name] = ResData()
    _error = False
    try:
        _res = json.dumps(obj)
        _timeit = timeit.Timer("json.dumps(obj)",
                               globals=globals())
        rawres[obj_description][method_name].encode_success = True
        rawres[obj_description][method_name].encode_length = _len(_res)
        rawres[obj_description][method_name].encode_time = _timeit.timeit(TIMEITNUMBER)
    except:    # TODO je ne sais pas quelle exception peut être envoyée par json
        _error = True

    if not _error:
        try:
            _res2 = json.loads(_res)
            _timeit = timeit.Timer("json.loads(_res)",
                                   globals=globals())
            rawres[obj_description][method_name].decode_success = True
            rawres[obj_description][method_name].decode_time = _timeit.timeit(TIMEITNUMBER)
            if obj == _res2:
                rawres[obj_description][method_name].decode_identity = True
        except:  # TODO je ne sais pas quelle exception peut être envoyée par jsonpickle
            pass


    # ---- pyyaml
    method_name = "pyyaml"
    METHODNAMES.add(method_name)
    rawres[obj_description][method_name] = ResData()
    _error = False
    try:
        _res = yaml.dump(obj, Dumper=yaml.Dumper)
        _timeit = timeit.Timer("yaml.dump(obj, Dumper=yaml.Dumper)",
                               globals=globals())
        rawres[obj_description][method_name].encode_success = True
        rawres[obj_description][method_name].encode_length = _len(_res)
        rawres[obj_description][method_name].encode_time = _timeit.timeit(TIMEITNUMBER)
    except:    # TODO je ne sais pas quelle exception peut être envoyée par json
        _error = True

    if not _error:
        try:
            _res2 = yaml.load(_res, Loader=yaml.Loader)
            _timeit = timeit.Timer("yaml.load(_res, Loader=yaml.Loader)",
                                   globals=globals())
            rawres[obj_description][method_name].decode_success = True
            rawres[obj_description][method_name].decode_time = _timeit.timeit(TIMEITNUMBER)
            if obj == _res2:
                rawres[obj_description][method_name].decode_identity = True
        except:  # TODO je ne sais pas quelle exception peut être envoyée par Yaml
            pass

    # ---- msgpack
    method_name = "msgpack"
    METHODNAMES.add(method_name)
    rawres[obj_description][method_name] = ResData()
    _error = False
    try:
        _res = msgpack.dumps(obj)
        _timeit = timeit.Timer("msgpack.dumps(obj)",
                               globals=globals())
        rawres[obj_description][method_name].encode_success = True
        rawres[obj_description][method_name].encode_length = _len(_res)
        rawres[obj_description][method_name].encode_time = _timeit.timeit(TIMEITNUMBER)
    except:    # TODO je ne sais pas quelle exception peut être envoyée par json
        _error = True

    if not _error:
        try:
            _res2 = msgpack.loads(_res)
            _timeit = timeit.Timer("msgpack.loads(_res)",
                                   globals=globals())
            rawres[obj_description][method_name].decode_success = True
            rawres[obj_description][method_name].decode_time = _timeit.timeit(TIMEITNUMBER)
            if obj == _res2:
                rawres[obj_description][method_name].decode_identity = True
        except:  # TODO je ne sais pas quelle exception peut être envoyée par Yaml
            pass

        

rich.print("[bold][red]* [0.1a] RAW RESULTS PER OBJ DESCRIPTION/METHOD NAME:[/red][/bold]")
rich.print("")
table = rich.table.Table(show_header=True, header_style="bold blue")
table.add_column("obj description/method name", style="dim", width=40)
table.add_column("enc. ok ?")
table.add_column("enc. time")
table.add_column("jsonstr. length")
table.add_column("dec. ok ?")
table.add_column("decoding time")
table.add_column("identity")

for obj_description in sorted(rawres):
    table.add_row(obj_description+":")
    for method_name in sorted(rawres[ obj_description]):
        table.add_row("> "+ method_name,
                      str(rawres[obj_description][method_name].encode_success),
                      str(rawres[obj_description][method_name].encode_time),
                      str(rawres[obj_description][method_name].encode_length),
                      str(rawres[obj_description][method_name].decode_success),
                      str(rawres[obj_description][method_name].decode_time),
                      str(rawres[obj_description][method_name].decode_identity))
    table.add_row()

rich.print(table)

rich.print("")
rich.print("[bold][red]* [0.1b] RAW RESULTS PER METHOD NAME/OBJ DESCRIPTION:[/red][/bold]")
rich.print("")
table = rich.table.Table(show_header=True, header_style="bold blue")
table.add_column("method name/obj description", style="dim", width=40)
table.add_column("enc. ok ?")
table.add_column("enc. time")
table.add_column("jsonstr. length")
table.add_column("dec. ok ?")
table.add_column("decoding time")
table.add_column("identity")

for method_name in sorted(METHODNAMES):
    table.add_row(method_name+":")
    for obj_description in sorted(rawres):
        table.add_row("> "+obj_description,
                      str(rawres[obj_description][method_name].encode_success),
                      str(rawres[obj_description][method_name].encode_time),
                      str(rawres[obj_description][method_name].encode_length),
                      str(rawres[obj_description][method_name].decode_success),
                      str(rawres[obj_description][method_name].decode_time),
                      str(rawres[obj_description][method_name].decode_identity))
    table.add_row()

rich.print(table)

# ============================================
# ==== RAW STATISTICS per obj description ====
# ============================================
stats1 = {}

for obj_description in sorted(rawres):
    stats1[obj_description] = {"encode_time": None,
                               "encode_success": None,
                               "decode_success": None,
                               "decode_time": None,
                               "jsonstring length": None,
                               "decode_identity": None,
                               }
    for method_name in sorted(rawres[obj_description]):
        if rawres[obj_description][method_name].encode_success:
            if stats1[obj_description]["encode_success"] is None:
                stats1[obj_description]["encode_success"] = 0
            stats1[obj_description]["encode_success"] += 1

            if stats1[obj_description]["encode_time"] is None:
                stats1[obj_description]["encode_time"] = 0
            stats1[obj_description]["encode_time"] += rawres[obj_description][method_name].encode_time

            if stats1[obj_description]["jsonstring length"] is None:
                stats1[obj_description]["jsonstring length"] = 0
            stats1[obj_description]["jsonstring length"] += rawres[obj_description][method_name].encode_length
        if rawres[obj_description][method_name].decode_success:
            if stats1[obj_description]["decode_success"] is None:
                stats1[obj_description]["decode_success"] = 0
            stats1[obj_description]["decode_success"] += 1

            if stats1[obj_description]["decode_time"] is None:
                stats1[obj_description]["decode_time"] = 0
            stats1[obj_description]["decode_time"] += rawres[obj_description][method_name].decode_time
        if rawres[obj_description][method_name].decode_identity:
            if stats1[obj_description]["decode_identity"] is None:
                stats1[obj_description]["decode_identity"] = 0
            stats1[obj_description]["decode_identity"] += 1

rich.print("")
rich.print("[bold][red]* [0.2] RAW STATISTICS per obj description:[/red][/bold]")
table = rich.table.Table(show_header=True, header_style="bold blue")
table.add_column("obj description", style="dim", width=40)
table.add_column(f"enc. ok ? (max. = {len(METHODNAMES)})")
table.add_column("enc. time")
table.add_column("jsonstr. length")
table.add_column(f"dec. ok ? (max. = {len(METHODNAMES)})")
table.add_column("decoding time")
table.add_column(f"identity (max. = {len(METHODNAMES)})")

for obj_description in sorted(rawres):
    table.add_row(obj_description,
                  str(stats1[obj_description]["encode_success"]),
                  str(stats1[obj_description]["encode_time"]),
                  str(stats1[obj_description]["jsonstring length"]),
                  str(stats1[obj_description]["decode_success"]),
                  str(stats1[obj_description]["decode_time"]),
                  str(stats1[obj_description]["decode_identity"]),
                  )

rich.print("")
rich.print(table)

# ========================================
# ==== RAW STATISTICS per method name ====
# ========================================
stats2 = {}

for obj_description in sorted(rawres):
    for method_name in sorted(rawres[obj_description]):
        if method_name not in stats2:
            stats2[method_name] = {"encode_time": None,
                                   "encode_success": None,
                                   "decode_success": None,
                                   "decode_time": None,
                                   "jsonstring length": None,
                                   "decode_identity": None,
                                   "failure": [],
                                   }

        if rawres[obj_description][method_name].encode_success:
            if stats2[method_name]["encode_success"] is None:
                stats2[method_name]["encode_success"] = 0
            stats2[method_name]["encode_success"] += 1

            if stats2[method_name]["encode_time"] is None:
                stats2[method_name]["encode_time"] = 0
            stats2[method_name]["encode_time"] += rawres[obj_description][method_name].encode_time

            if stats2[method_name]["jsonstring length"] is None:
                stats2[method_name]["jsonstring length"] = 0
            stats2[method_name]["jsonstring length"] += rawres[obj_description][method_name].encode_length
        if rawres[obj_description][method_name].decode_success:
            if stats2[method_name]["decode_success"] is None:
                stats2[method_name]["decode_success"] = 0
            stats2[method_name]["decode_success"] += 1

            if stats2[method_name]["decode_time"] is None:
                stats2[method_name]["decode_time"] = 0
            stats2[method_name]["decode_time"] += rawres[obj_description][method_name].decode_time
        if rawres[obj_description][method_name].decode_identity:
            if stats2[method_name]["decode_identity"] is None:
                stats2[method_name]["decode_identity"] = 0
            stats2[method_name]["decode_identity"] += 1
        else:
            stats2[method_name]["failure"].append(obj_description)

rich.print("")
rich.print("[bold][red]* [0.3] RAW STATISTICS per method name:[/red][/bold]")
table = rich.table.Table(show_header=True, header_style="bold blue")
table.add_column("method name", style="dim", width=40)
table.add_column(f"enc. ok ? (max. = {len(rawres)})")
table.add_column("enc. time")
table.add_column("jsonstr. length")
table.add_column(f"dec. ok ? (max. = {len(rawres)})")
table.add_column("dec. time")
table.add_column(f"identity (max. = {len(rawres)})")

for method_name in sorted(METHODNAMES):
    table.add_row(method_name,
                  str(stats2[method_name]["encode_success"]),
                  str(stats2[method_name]["encode_time"]),
                  str(stats2[method_name]["jsonstring length"]),
                  str(stats2[method_name]["decode_success"]),
                  str(stats2[method_name]["decode_time"]),
                  str(stats2[method_name]["decode_identity"]),
                  )

rich.print("")
rich.print(table)

for method_name in sorted(METHODNAMES):
    rich.print(f"* [bold]{method_name}[bold] can't successfully encode then decode:")
    for obj in stats2[method_name]["failure"]:
        rich.print(f"  - {obj}")

# ================================================
# ==== IMPROVED STATISTICS by obj description ====
# ================================================

# encode time reference ?
ref__encode_time = None
ref__encode_time__name = None
for obj_description in sorted(rawres):
    if stats1[obj_description]["encode_time"] is not None:
        ref__encode_time = stats1[obj_description]["encode_time"]
        ref__encode_time__name = obj_description
        break

# jsonstring length reference ?
ref__jsonstring_length = None
ref__jsonstring_length__name = None
for obj_description in sorted(rawres):
    if stats1[obj_description]["jsonstring length"] is not None:
        ref__jsonstring_length = stats1[obj_description]["jsonstring length"]
        ref__jsonstring_length__name = obj_description
        break

# decode time reference ?
ref__decode_time = None
ref__decode_time__name = None
for obj_description in sorted(rawres):
    if stats1[obj_description]["decode_time"] is not None:
        ref__decode_time = stats1[obj_description]["decode_time"]
        ref__decode_time__name = obj_description
        break

rich.print("")
rich.print("[bold][red]* [1.1] STATISTICS per obj description:[/red][/bold]")
table = rich.table.Table(show_header=True, header_style="bold blue")
table.add_column("obj description", style="dim", width=40)
table.add_column(f"% enco.")
table.add_column(f"enco. time (100: '{str(ref__encode_time__name)}')")
table.add_column(f"len(jsonstr) (100: '{str(ref__jsonstring_length__name)}')")
table.add_column(f"% deco.")
table.add_column(f"deco. time (100: '{str(ref__decode_time__name)}')")
table.add_column(f"% success")


for obj_description in sorted(rawres):
    if stats1[obj_description]["encode_success"] is None:
        encode_success = "-"
    else:
        encode_success = "{0:.2f} %".format(100*stats1[obj_description]["encode_success"]/len(METHODNAMES))

    if stats1[obj_description]["encode_time"] is None or \
       ref__encode_time is None:
        encode_time = "-"
    else:
        encode_time = "{0:.2f}".format(100*stats1[obj_description]["encode_time"]/ref__encode_time)

    if stats1[obj_description]["jsonstring length"] is None or \
       ref__encode_time is None:
        jsonstring_length = "-"
    else:
        jsonstring_length = "{0:.2f}".format(100*stats1[obj_description]["jsonstring length"]/ref__jsonstring_length)

    if stats1[obj_description]["decode_success"] is None:
        decode_success = "-"
    else:
        decode_success = "{0:.2f} %".format(100*stats1[obj_description]["decode_success"]/len(METHODNAMES))

    if stats1[obj_description]["decode_time"] is None or \
       ref__decode_time is None:
        decode_time = "-"
    else:
        decode_time = "{0:.2f}".format(100*stats1[obj_description]["decode_time"]/ref__decode_time)

    if stats1[obj_description]["decode_identity"] is None:
        decode_identity = "-"
    else:
        decode_identity = "{0:.2f} %".format(100*stats1[obj_description]["decode_identity"]/len(METHODNAMES))

    table.add_row(obj_description,
                  encode_success,
                  encode_time,
                  jsonstring_length,
                  decode_success,
                  decode_time,
                  decode_identity,
                  )

rich.print("")
rich.print(table)


# ============================================
# ==== IMPROVED STATISTICS by method name ====
# ============================================

# encode time reference ?
ref__encode_time = None
ref__encode_time__name = None
for method_name in sorted(METHODNAMES):
    if stats2[method_name]["encode_time"] is not None:
        ref__encode_time = stats2[method_name]["encode_time"]
        ref__encode_time__name = method_name
        break

# jsonstring length reference ?
ref__jsonstring_length = None
ref__jsonstring_length__name = None
for method_name in sorted(METHODNAMES):
    if stats2[method_name]["jsonstring length"] is not None:
        ref__jsonstring_length = stats2[method_name]["jsonstring length"]
        ref__jsonstring_length__name = method_name
        break

# decode time reference ?
ref__decode_time = None
ref__decode_time__name = None
for method_name in sorted(METHODNAMES):
    if stats2[method_name]["decode_time"] is not None:
        ref__decode_time = stats2[method_name]["decode_time"]
        ref__decode_time__name = method_name
        break

rich.print("")
rich.print("[bold][red]* [1.2] STATISTICS per method name:[/red][/bold]")
table = rich.table.Table(show_header=True, header_style="bold blue")
table.add_column("method name", style="dim", width=40)
table.add_column(f"% enco.")
table.add_column(f"enco. time (100: '{str(ref__encode_time__name)}')")
table.add_column(f"len(jsonstr) (100: '{str(ref__jsonstring_length__name)}')")
table.add_column(f"% deco.")
table.add_column(f"deco. time (100: '{str(ref__decode_time__name)}')")
table.add_column(f"% success")


for method_name in sorted(METHODNAMES):
    if stats2[method_name]["encode_success"] is None:
        encode_success = "-"
    else:
        encode_success = "{0:.2f} %".format(100*stats2[method_name]["encode_success"]/len(rawres))

    if stats2[method_name]["encode_time"] is None or \
       ref__encode_time is None:
        encode_time = "-"
    else:
        encode_time = "{0:.2f}".format(100*stats2[method_name]["encode_time"]/ref__encode_time)

    if stats2[method_name]["jsonstring length"] is None or \
       ref__encode_time is None:
        jsonstring_length = "-"
    else:
        jsonstring_length = "{0:.2f}".format(100*stats2[method_name]["jsonstring length"]/ref__jsonstring_length)

    if stats2[method_name]["decode_success"] is None:
        decode_success = "-"
    else:
        decode_success = "{0:.2f} %".format(100*stats2[method_name]["decode_success"]/len(rawres))

    if stats2[method_name]["decode_time"] is None or \
       ref__decode_time is None:
        decode_time = "-"
    else:
        decode_time = "{0:.2f}".format(100*stats2[method_name]["decode_time"]/ref__decode_time)

    if stats2[method_name]["decode_identity"] is None:
        decode_identity = "-"
    else:
        decode_identity = "{0:.2f} %".format(100*stats2[method_name]["decode_identity"]/len(rawres))

    table.add_row(method_name,
                  encode_success,
                  encode_time,
                  jsonstring_length,
                  decode_success,
                  decode_time,
                  decode_identity,
                  )

rich.print("")
rich.print(table)
