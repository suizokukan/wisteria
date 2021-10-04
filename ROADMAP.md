Wisteria's roadmap & todos
==========================

* data types à compléter
        RegularClass
        IntheritedList
        IntheritedDict
        ("R01:class::meta class", MetaClass),

        ("R02:class::reg. class::RegularClass()", RegularClass()),
        ("R03:class::reg. class::async method", RegularClass.async_method),
        ("R04:class::reg. class::generator", RegularClass.generator),
        ("R05:class::reg. class::method", RegularClass.method),
        ("R06:class::reg. class::class method", RegularClass.class_method),
        ("R07:class::reg. class::static method", RegularClass.static_method),

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

0.1.4:
* README.md acceptable

0.1.3:
* i18n() + --i18n=en|fr|de|it|es|ru (ou plutôt FR_fr ???, important pour le mandarin)

0.1.2:
* --method = "serializer=shuffle/sorted/raw;dataobj=shuffle/sorted/raw;lenmethod=str|bytes;timeitnumber=10;iteration=1+2+...+n|n"
* --meta: comparer avec les différentes versions de --method, graphique montrant ce qui se passe qd on augmente TIMEITNUMBER
  chercher si une combinaison donne des résultats vraiment différents des autres

0.1.1:
tests

0.1.0: 
cwc

0.0.9:
* serializers à compléter




===============================================================================

[CURRENT] v. 0.0.8
* (git message for 0.0.8) doubloon > duplicate

* data types à compléter
qu'est-ce qui est disponible ?
- Python-dateutil
- rich console/table/
- float('nan') & math.isnan(x), re, time, collections, hashlib, csv, random, 
- bool/false(True); > bool/false(False) dans checkup()

[DONE] task-102

Improved checkup() display by adding project's name & version and the current
timestamp. (task-102)

    * Improved checkup() display by adding project's name & version and the current
      timestamp. (task-102)

    * pylint: 10/10

[DONE] task-101

Improved code readibility by adding a parameter to aspect_list(, func),
func() being called on each item inserted in the result string.

    * Improved code readibility by adding a parameter to aspect_list(, func),
      func() being called on each item inserted in the result string. (task-101)

    * pylint: 10/10

[DONE] task-100

Documentation in reportaspect.py.

    * documentation in reportaspect.py  (task-100)

    * pylint: 10/10

[DONE] task-99

Replaced some doubloons in code by two fonctions, partial_report__data()
and partial_report__serializers().

    * replaced some doubloons in code by two fonctions, partial_report__data()
      and partial_report__serializers() (task-99)

    * pylint: 10/10

[DONE] task-98

Improved messages in read_cmpstring() and in checkup().

    * improved messages in read_cmpstring() and in checkup() (task-98)
    * new aspect method: aspect_nounplural() (task-98)

    * pylint: 10/10

[DONE] task-97

Improved error messages in read_cmpstring(); improved message in checkup().

    * improved error messages in read_cmpstring(); improved message in checkup()
      (task-97)

    * pylint: 10/10

[DONE] task-96

Improved the message displayed by checkup().

    * improved the message displayed by checkup() : .internet string
      displayed for unavailable serializer (task-96)

    * pylint: 10/10

[DONE] task-95

Fixed a color problem in report_section_d2c().

    * fixed a color problem in report_section_d2c() (task-95)
    
    * pylint: 10/10
    
[DONE] task-94

If no argument has been given on the command line, we modify the output
to help the user (verbosity and report).

    * If no argument has been given on the command line, we modify the output
      to help the user (verbosity and report). (task-94)

    * pylint: 10/10

[DONE] task-93

UNAVAILABLE_SERIALIZERS now contains serializers that can't be used.

    * globs.py:UNAVAILABLE_SERIALIZERS now contains serializers that can't be 
      used. (task-93)
    * .available is not an attribute of SerializerData anymore (task-93)
    * SerializerData has now a new attribute, .modulename (task-93)
    * modified init_serializers() so that serializers that can't be used
      are stored in globs.py:UNAVAILABLE_SERIALIZERS (task-93)
    * new aspect_xxx() method: aspect_serializer0(); aspect_serializer()
      is now based on it. (task-93)

    * pylint: 10/10

[DONE] task-92

Fixed a typo: 'extremly' > 'extremely'.

    * fixed a typo: 'extremly' > 'extremely' (task-92)
    
    * pylint: 10/10

[DONE] task-91

globs.py:UNAVAILABLE_DATA; improved init_data() messages.

    * modified data.py:init_data() so that this functions stores in
      UNAVAILABLE_DATA the data objects that can't be used (task-91)
    * globs.py:UNAVAILABLE_DATA stores the data objects that can't be used (task-91)
    * rewrote the sections' numbers of wisteria.py: no more '09bis' (task-91)
    * rewrote how checkup() displays the serializers and the data objects (task-91)

    * pylint: 10/10

[DONE] v. 0.0.7
---------------

--mymachine option
report sections E1a and E1b
new report shortcuts: 'full+', 'full_debug' and 'glance' which is the default report shortcut.
Improved English phraseology.
Added py-cpuinfo and psutil to project's dependencies.


command line arguments

    * new option: --mymachine (task-77)
    * updated REPORT_SHORTCUTS["full"], now set to "titles;A;B;C;D;E1a;" (task-77)
    * globs.py::REPORT_SHORTCUTS['full+'] is a new shortcut; its value is set
      to "titles;A;B;C;D;E1b;" (task-78)
    * globs.py::REPORT_SHORTCUTS['full_debug'] is a new shortcut; its value is set
      to "titles;A;B;C;D;E;" (task-78)
    * new report shortcut 'glance' which is the default report shortcut. 
      (task-86)
    
code organization

    * new file: wisteria/cmdline_mymachine.py --mymachine (task-77)
    * new functions in reports.py: report_section_e1a() and report_section_e1b() 
      (task-77)
    * new exit value (3: normal exit code after --mymachine) (task-77)
    * keys in globs.py::REPORT_SHORTCUTS are now alphabetically sorted (task-78)
    * rewrote humanratio(): if the new argument is not None, this function
      returns an explanation of the value by humanratio(ratio, explanations=None)
      (task-79)
    * new file: wisteria/textandnotes.py (task-79)
    * in wisteria/textandnotes.py, new class TextAndNote.
      With the TextAndNotes class, add bunch of text that may contains notes;
      these notes are added with a special syntax (__note:XXXXX__) and are
      automatically numbered and added at the end of the final text. (task-79)
      By example:
              txt = TextAndNotes()
              txt.append("First line with a note (__note:myfirstnote__)")
              txt.notes.append(("__note:myfirstnote__",
                                "This is a footnote about first line."))

              txt.output() will produce:
                      "First line with a note(¹)"
                      ""
                      "(¹) This is a footnote about first line."
    * modified report_section_d2c() so that this function uses a TextAndNotes
      object (task-79)
    * SerializerData class has a new instance attribute, 'name'. (task-81)
    * in init_serializers(), updated wisteria.globs.SERIALIZERS initialization
      to take in account SerializerData new instance attribute (task-81)
    * report.py: improved code readibility by adding a call to aspect_nodata()
      instead of using a string like '[red]no data[/red]' (task-84)
    * new aspect method: reportaspect.py::aspect_nodata() (task-84)
    * added py-cpuinfo and psutil to project's dependencies. (task-85)
    
bugfixes

    * (bugfix) added 'report_section_e1a' and 'report_section_e1b' to 
      STR2REPORTSECTION. (task-78)
    * fixed a very minor glitch (useless space) in cmdline_mymachine.py (task-78)
    * in pylintrc, max-args=5 > max-args=6 (task-82)
    * bugfix: serializers_classes.py::total_xxx() functions handle correctly the 
              case where there is no base100 reference available. (task-84)
    * removed some now useless `pylint: disable` in mymachine.py::mymachine() (task-85)
    * bugfix: improved report.py::report() to avoid that " B1b" report section
      raises an error. Therefore all report sections strings are stripped. (task-87)

documentation:

    * updated documentations to take in account --mymachine and report sections 
      E1a and E1b --mymachine (task-77)
    * updated pimydoc to take in account the new "3" exit value (task-77)
    * updated --help message to take in account --mymachine (task-77, task-83)
    * slightly improved message from report_section_b1d() (task-90)
    * doc. : improved ROADMAP.md (task-80)
    * updated README.md (task-82)
    * improved doc. (task-89)
    
messages

    * improved english phraseology (task-81)
    * added units everywhere it was possible to add them, in tables and in texts.
      (task-89)
    * unit is not added in aspect_xxx() method and therefore aspect_stringlength()
      has been modified to remove the 'chars' string that was added to the result
      (task-89)
    * improved grammar in ratio2phrase(): worst > worse (task-88)
    * improved D2c by using the new 'good/bad' option defined
      for ratio2phrase() (task-88)
    * slightly improved message from report_section_b1d() (task-90)
    
version

    * set version to 0.0.7

tasks

    * task(s): task-77, task-78, task-79, task-80, task-81,
               task-82, task-83, task-84, task-85, task-86,
               task-87, task-88, task-89, task-90

    * pylint: 10/10
               
```
$ poetry show --tree
psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.11.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ ./check_tools.sh
* about poetry:
Poetry version 1.1.10
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
PYLINTHOME is now '/home/proguser/.cache/pylint' but obsolescent '/home/proguser/.pylint.d' is found; you can safely remove the latter
pylint 2.11.1
astroid 2.8.0
Python 3.9.7 (default, Aug 31 2021, 13:28:12) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-90

Slightly improved message from report_section_b1d().

    * slightly improved message from report_section_b1d() (task-90)

    * pylint: 10/10

[DONE] task-89

Added units everywhere it was possible to add them, in tables and in texts.

    * added units everywhere it was possible to add them, in tables and in texts.
      (task-89)
    * unit is not added in aspect_xxx() method and therefore aspect_stringlength()
      has been modified to remove the 'chars' string that was added to the result
      (task-89)
    * improved doc. (task-89)
    
    * pylint: 10/10

[DONE] task-88

Improved grammar in ratio2phrase() and in D2c report section.

    * improved grammar in ratio2phrase(): worst > worse (task-88)
    * improved D2c by using the new 'good/bad' option defined
      for ratio2phrase() (task-88)

    * pylint: 10/10

[DONE] task-87

Bugfix: improved report.py::report() to avoid that " B1b" report section 
        raises an error. Therefore all report sections strings are stripped.

    * Bugfix: improved report.py::report() to avoid that " B1b" report section
      raises an error. Therefore all report sections strings are stripped. (task-87)

    * pylint: 10/10

[DONE] task-86

New report shortcut 'glance' which is the default report shortcut.

    * new report shortcut 'glance' which is the default report shortcut. 
      (task-86)

    * pylint: 10/10

[DONE] task-85

Added py-cpuinfo and psutil to project's dependencies.

    * added py-cpuinfo and psutil to project's dependencies. (task-85)
    * removed some now useless `pylint: disable` in mymachine.py::mymachine() (task-85)

    * pylint: 10/10
               
[DONE] task-84

Bugfix: serializers_classes.py::total_xxx() functions handle correctly the case
        where there is no base100 reference available.

    * Bugfix: serializers_classes.py::total_xxx() functions handle correctly the 
              case where there is no base100 reference available. (task-84)
    * report.py: improved code readibility by adding a call to aspect_nodata()
      instead of using a string like '[red]no data[/red]' (task-84)
    * new aspect method: reportaspect.py::aspect_nodata() (task-84)

    * pylint: 10/10

[DONE] task-83

Improved --help message.

    * improved --help message (task-83)

    * pylint: 10/10

[DONE] task-82

In pylintrc, max-args=5 > max-args=6.

    * in pylintrc, max-args=5 > max-args=6 (task-82)
    * updated README.md (task-82)

    * pylint: 10/10

[DONE] task-81

Improved English phraseology.

    * improved english phraseology (task-81)
    * SerializerData class has a new instance attribute, 'name'. (task-81)
    * in init_serializers(), updated wisteria.globs.SERIALIZERS initialization
      to take in account SerializerData new instance attribute (task-81)

    * pylint: 9.99/10
    
[DONE] task-80

doc. : improved ROADMAP.md

    * doc. : improved ROADMAP.md (task-80)

[DONE] task-79

TextAndNotes class, humanratio() can now return an explanation about the
value it computes.

    * rewrote humanratio(): if the new argument is not None, this function
      returns an explanation of the value by humanratio(ratio, explanations=None)
      (task-79)
    * new file: wisteria/textandnotes.py (task-79)
    * in wisteria/textandnotes.py, new class TextAndNote.
      With the TextAndNotes class, add bunch of text that may contains notes;
      these notes are added with a special syntax (__note:XXXXX__) and are
      automatically numbered and added at the end of the final text. (task-79)
      By example:
              txt = TextAndNotes()
              txt.append("First line with a note (__note:myfirstnote__)")
              txt.notes.append(("__note:myfirstnote__",
                                "This is a footnote about first line."))

              txt.output() will produce:
                      "First line with a note(¹)"
                      ""
                      "(¹) This is a footnote about first line."
    * modified report_section_d2c() so that this function uses a TextAndNotes
      object (task-79)

    * pylint: 10/10
    
[DONE] task-78

new report shortcuts: 'full+' and 'full_debug'.

    * globs.py::REPORT_SHORTCUTS['full+'] is a new shortcut; its value is set
      to "titles;A;B;C;D;E1b;" (task-78)
    * globs.py::REPORT_SHORTCUTS['full_debug'] is a new shortcut; its value is set
      to "titles;A;B;C;D;E;" (task-78)
    * keys in globs.py::REPORT_SHORTCUTS are now alphabetically sorted (task-78)
    * fixed a very minor glitch (useless space) in cmdline_mymachine.py (task-78)
    * (bugfix) added 'report_section_e1a' and 'report_section_e1b' to 
      STR2REPORTSECTION. (task-78)

    * pylint: 10/10

[DONE] task-77

--mymachine option, report sections E1a and E1b

    * new option: --mymachine (task-77)
    * new file: wisteria/cmdline_mymachine.py --mymachine (task-77)
    * updated documentations to take in account --mymachine and report sections 
      E1a and E1b --mymachine (task-77)
    * updated REPORT_SHORTCUTS["full"], now set to "titles;A;B;C;D;E1a;" (task-77)
    * new functions in reports.py: report_section_e1a() and report_section_e1b() 
      (task-77)
    * new exit value (3: normal exit code after --mymachine) (task-77)
    * updated pimydoc to take in account the new "3" exit value (task-77)
    * updated --help message to take in account --mymachine (task-77)

    * pylint: 10/10

[DONE] v. 0.0.6
---------------

Various improvements: code, doc., messages. Pylint note is now 10/10.

bugfixes

    * fixed a bug in read_cmpstring():
      Since cmpdata is the real name of cmp (cf task-68), group('data') becomes
      group('cmpdata') (task-71)
    * Fixed a minor error in report_section_c1a(): forgotten f- prefix
      for a f-string. (task-74)

code improvements

    * improved SerializationResults.get_dataobjs_base() and 
      SerializationResults.get_serializers_base():
      In both methods the reference is obtained only after all possible 
      serializers/data objects have been browsed. (task-75)
    * improved shortenedstr() in the very special case when
      len(suffix) > maximallength . (task-72)
    * new variable defined in DEFAULT_CONFIG_FILENAME and
      initialized in wisteria.py (task-72)
    * improved exit_handler(): added two debug messages (task-72)
    * improved exit_handler(): forced FILECONSOLE_FILEOBJECT closing (task-72)

documentation

    * very slightly improved message displayed by downloadconfigfile() (task-76)
    * improved messages in checkup() about config file download (task-76)
    * improved SerializationResults.get_dataobjs_base() and 
      SerializationResults.get_serializers_base() documentation (task-75)
    * docstring of all methods & functions (task-71)
    * improved comments (task-68)
    * slightly improved ROADMAP.md (cf task-74, task-76, task-73)
    
pylint & code readibility

    * Code pylinted; pylintrc has been updated; first version to get 10/10.
    * removed almost all TODOs (task-72)
    * improved code readibility: replaced 'data' by 'cmpdata' everywhere it 
      made sense. (task-68)
    * added some assert() to explicit arguments specificities

version

    * set version to '0.0.6'

pylint

    * pylint: 10/10
    
tasks

    * task(s): task-68, task-69, task-70, task-71, task-72, 
      task-73, task-74, task-75, task-76 
    
```
$ poetry show --tree
rich 10.11.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ ./check_tools.sh
* about poetry:
Poetry version 1.1.10
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
PYLINTHOME is now '/home/proguser/.cache/pylint' but obsolescent '/home/proguser/.pylint.d' is found; you can safely remove the latter
pylint 2.11.1
astroid 2.8.0
Python 3.9.7 (default, Aug 31 2021, 13:28:12) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```
  
[DONE] task-76

Improved messages relative to config file.

    * very slightly improved message displayed by downloadconfigfile() (task-76)
    * improved messages in checkup() about config file download (task-76)

    * pylint: 10/10

[DONE] task-75

Improved SerializationResults.get_dataobjs_base() and 
SerializationResults.get_serializers_base(): doc. and code redefinition.
  
    * improved SerializationResults.get_dataobjs_base() and 
      SerializationResults.get_serializers_base():
      In both methods the reference is obtained only after all possible 
      serializers/data objects have been browsed. (task-75)
    * improved SerializationResults.get_dataobjs_base() and 
      SerializationResults.get_serializers_base() documentation (task-75)
    * updated documentation in classes' headers (task-70)

    * pylint: 10/10

[DONE] task-74

Fixed a minor error in report_section_c1a(): forgotten f- prefix
for a f-string.

    * Fixed a minor error in report_section_c1a(): forgotten f- prefix
      for a f-string. (task-74)

    * pylint: 10/10
  
[DONE] task-73

Code pylinted; pylintrc has been updated; first version to get 10/10.

    * Code pylinted; pylintrc has been updated; first version to get 10/10. 
      (task-73)
    
    * pylint: 10/10

[DONE] task-72

Removed all TODOs, improved exit_handler and added DEFAULT_CONFIG_FILENAME
to globs.py

    * removed almost all TODOs (task-72)
    * improved shortenedstr() in the very special case when
      len(suffix) > maximallength . (task-72)
    * new variable defined in DEFAULT_CONFIG_FILENAME and
      initialized in wisteria.py (task-72)
    * improved exit_handler(): added two debug messages (task-72)
    * improved exit_handler(): forced FILECONSOLE_FILEOBJECT closing (task-72)
    
[DONE] task-71

Docstring of all methods & functions; fixed a bug in read_cmpstring().

    * docstring of all methods & functions (task-71)
    * fixed a bug in read_cmpstring():
      Since cmpdata is the real name of cmp (cf task-68), group('data') becomes
      group('cmpdata') (task-71)
    * added some assert() to explicit arguments specificities

[DONE] task-70

Updated documentation in classes' headers.

    * updated documentation in classes' headers (task-70)

[DONE] task-69

Updated documentation in Python files headers.

    * Updated documentation in Python files headers. (task-69)
    * fixed a minor error in STR2REPORTSECTION: "B1d" belongs to "B", too. 
      (task-69)

[DONE] task-68

Improved code readibility: replaced 'data' by 'cmpdata' everywhere it made sense.

    * improved code readibility: replaced 'data' by 'cmpdata' everywhere it 
      made sense. (task-68)
    * improved comments (task-68)

[DONE] v. 0.0.5
---------------

Fixed pyproject.toml so that wisteria can be an executable command.

    * fixed pyproject.toml so that wisteria can be an executable command. 
      (task-67)
      
    * set version to '0.0.5'

    * task(s): task-67

```
$ poetry show --tree
rich 10.11.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ ./check_tools.sh
* about poetry:
Poetry version 1.1.10
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
PYLINTHOME is now '/home/proguser/.cache/pylint' but obsolescent '/home/proguser/.pylint.d' is found; you can safely remove the latter
pylint 2.11.1
astroid 2.8.0
Python 3.9.7 (default, Aug 31 2021, 13:28:12) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-67

Fixed pyproject.toml so that wisteria can be an executable command.

    * fixed pyproject.toml so that wisteria can be an executable command. 
      (task-67)

[DONE] v. 0.0.4
---------------

Various bugfixes, minor improvements.

bugfixes:

    * new constant in globs.py, PROGRESSBAR_LENGTH, to define progress bar's 
      length. None is an accepted value which extends the length of the bar
      to the entire width of the terminal. ((task-66)
    * Bugfix: progress_bar displayed by compute_results() is now erased
      after it has been displayed. The text written over with the 
      next call to rprint() is now perfectly readable. (task-65)
    * Improved the content of main() and of bin/wisteria so that the
      returned value of main() is sys.exit-ed() . (task-64)
    * Fixed a bug in read_cfgfile(): ARGS.checkup > 
      wisteria.globs.ARGS.checkup (task-63)
    * New version of poetry_show_tree.sh (poetry_show_tree.sh v.6/2021-09-29)
      With this version, even a package like 'rich' will appear in 
      poetry_show_tree.md (task-62)
    * fixed a minor glitch in the messages: string(¹) > string (¹) 
      with a space that prevents rich to colorize the string before
      (¹) (task-61)
    * fixed a minor glitch: title D1a) should be written (D1a) ((task-60)
    * improved report_section_d2c(): the messages displayed are correct 
      if serializer1==serializer2=="all". (task-59)
    * fixed error codes: no more error code used twice (task-56)
    * every call to raise WisteriaError() is numbered (task-56)
    * aspect_serializer() now uses serializers' human name instead of the
      simple name. (task-55)
    * Bugfix: all percentages in the code are now displayed through aspect_percentage()
      (task-54)
    * Bugfix: D1a and D1b report sections use now <results.dataobjs> and not <data>,
              which was incorrect. (task-53)
    * report_section_d1a(), report_section_d1b() use now <results.dataobjs> and not <data>
      anymore. (task-53)
    * bugfix: report() handles now correctly ill-formed report string like "" 
      or "minimalZ" (task-52)
    * no more temp file on disk after a call with --help. (task-51)
    * wisteria.py: "temp file opening" step has been moved just
      before "known data init" step. (task-51)
    * bugfix: in report D2c, note (¹) now only apppears for "serializer1 vs all"; this
      note appeared previously and erroneously for "serializer1 vs serializer2" (task-50)

various improvements:

    * "bestof" is now defined as "B1c;D2b;D2c" (task-60)
    * improved error messages in report() (task-52)
    * new function in reportaspect.py: aspect_percentage() (task-54)
    * New file (serializers_classes.py) to store all classes used to handle 
      serializers. (task-57)
    * new method: SerializationResults.get_overallscore_bestrank() (task-58)
    * new method: SerializationResults.get_overallscore_worstrank() (task-58)
    
    * set version to '0.0.4'

    * task(s): task-50, task-51, task-52, task-53, task-54, task-55, 
               task-56, task-57, task-58, task-59, task-60, task-61,
               task-62, task-63, task-64, task-65, task-66

```
$ poetry show --tree
rich 10.11.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ ./check_tools.sh
* about poetry:
Poetry version 1.1.10
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
PYLINTHOME is now '/home/proguser/.cache/pylint' but obsolescent '/home/proguser/.pylint.d' is found; you can safely remove the latter
pylint 2.11.1
astroid 2.8.0
Python 3.9.7 (default, Aug 31 2021, 13:28:12) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-66

New constant in globs.py, PROGRESSBAR_LENGTH, to define progress bar's length.

    * new constant in globs.py, PROGRESSBAR_LENGTH, to define progress bar's 
      length. None is an accepted value which extends the length of the bar
      to the entire width of the terminal.

[DONE] task-65

Bugfix: progress_bar displayed by compute_results() is now erased
        after it has been displayed.
        The problem occured with something like:
        ./bin/wisteria --cmp="iaswn against json(all)" --report="titles;A2"

    * Bugfix: progress_bar displayed by compute_results() is now erased
      after it has been displayed. The text written over with the 
      next call to rprint() is now perfectly readable.

[DONE] task-64

Improved the content of main() and of bin/wisteria so that the
returned value of main() is sys.exit-ed() .

     * Improved the content of main() and of bin/wisteria so that the
       returned value of main() is sys.exit-ed() .

[DONE] task-63

Fixed a bug in read_cfgfile(): ARGS.checkup > wisteria.globs.ARGS.checkup.

    * Fixed a bug in read_cfgfile(): ARGS.checkup > 
      wisteria.globs.ARGS.checkup

[DONE] task-62

New version of poetry_show_tree.sh (poetry_show_tree.sh v.6/2021-09-29)
fixing a minor glitch.

    * New version of poetry_show_tree.sh (poetry_show_tree.sh v.6/2021-09-29)
      With this version, even a package like 'rich' will appear in 
      poetry_show_tree.md

[DONE] task-61

Fixed a minor glitch in the messages: string(¹) > string (¹) with a space.

    * fixed a minor glitch in the messages: string(¹) > string (¹) 
      with a space that prevents rich to colorize the string before
      (¹)

[DONE] task-60

"bestof" is now defined as "B1c;D2b;D2c".

    * "bestof" is now defined as "B1c;D2b;D2c"

[DONE] task-59

Fixed a minor glitch: title D1a) should be written (D1a).

    * fixed a minor glitch: title D1a) should be written (D1a)

[DONE] task-58

Improved report_section_d2c(): the messages displayed are now correct 
if serializer1==serializer2=="all".

    * improved report_section_d2c(): the messages displayed are correct 
      if serializer1==serializer2=="all".
    * new method: SerializationResults.get_overallscore_bestrank()
    * new method: SerializationResults.get_overallscore_worstrank()
    
[DONE] task-57

New file (serializers_classes.py) to store all classes used to handle serializers.

    * New file (serializers_classes.py) to store all classes used to handle 
      serializers.
      
[DONE] task-56

Fixed error codes.

    * fixed error codes: no more error code used twice
    * every call to raise WisteriaError() is numbered

[DONE] task-55

Fixed a display problem: when a serializer name is displayed, its 'human_name'
is now displayed.

    * aspect_serializer() now uses serializers' human name instead of the
      simple name.

[DONE] task-54

Bugfix: all percentages in the code are now displayed through aspect_percentage().

    * Bugfix: all percentages in the code are now displayed through aspect_percentage()
    * new function in reportaspect.py: aspect_percentage()

[DONE] task-53

Bugfix: D1a and D1b report sections use now <results.dataobjs> and not <data>,
        which was incorrect.

    * Bugfix: D1a and D1b report sections use now <results.dataobjs> and not <data>,
              which was incorrect.
    * report_section_d1a(), report_section_d1b() use now <results.dataobjs> and not <data>
      anymore.

[DONE] task-52

Bugfix: report() handles now correctly ill-formed report string like "" or "minimalZ"

    * bugfix: report() handles now correctly ill-formed report string like "" 
      or "minimalZ"
    * improved error messages in report()

[DONE] task-51

Bugfix: no more temp file on disk after a call with --help.

    * no more temp file on disk after a call with --help.
    * wisteria.py: "temp file opening" step has been moved just
      before "known data init" step.

[DONE] task-50

Bugfix: in report D2c, note (¹) now only apppears for "serializer1 vs all"; this
note appeared previously and erroneously for "serializer1 vs serializer2"

    * bugfix: in report D2c, note (¹) now only apppears for "serializer1 vs all"; this
      note appeared previously and erroneously for "serializer1 vs serializer2"

[DONE] v. 0.0.3
---------------

    * report sections: A1, A2, A3, B1a, B1b, B1c, B1d, B2a, B2b,
                       C1a, C1b, C2a, C2b, D1a, D1b, D2a, D2b, D2c
    * log messages to the console and to the log file. (task-44)
    * --output option (task-44)
    * documentation & pylint (task-32, task-37, task-40, task-41, task-43, task-49)
    * progress bar support. (task-38)
    * new files: utils.py (task-35), results.py (task-40), msg.py, 'cmdline_output.py' 
      (task-44 + task-48), reportaspect.py (task-46), cfgfile.py and cmdline_cmp.py (task-49)
    * DATA, SERIALIZERS moved to globs.py
    * 4 report shortcuts have been defined: "bestof", "laconic", "minimal", "full" (task-42)
    * several bugs have been fixed (task-31, task-33, task-40)
    * Messages displayed by checkup() are now displayed with msgreport(), not
      with msginfo() anymore. (task-47)
    * no more REPORT_FULL_STRING and REPORT_MINIMAL_STRING in globs.py;
      these constants have been replaced by the REPORT_SHORTCUTS dict. (task-42)
    * Added a timestamp to first info message (project name, version, timestamp) (task-45)
    * new serializers: json, pickle, marshal
    * new function in wisteria.py: compute_results(). (task-39)
    * resized image in README.md
    * --downloadconfigfile option
    * new constants in globs.py: DEFAULT_CONFIG_FILENAME, DEFAULTCFGFILE_URL

    * set version to '0.0.3'
    
    * task(s): task-29, task-30, task-31, task-32, task-33, task-34
               task-35, task-36, task-37, task-38, task-39, task-40, 
               task-41, task-42, task-43, task-44, task-45, task-46,
               task-47, task-48, task-49
               
```
$ poetry show --tree
```

```
$ ./check_tools.sh
* about poetry:
Poetry version 1.1.10
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
PYLINTHOME is now '/home/proguser/.cache/pylint' but obsolescent '/home/proguser/.pylint.d' is found; you can safely remove the latter
pylint 2.11.1
astroid 2.8.0
Python 3.9.7 (default, Aug 31 2021, 13:28:12) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```
               
[DONE] task-49

new files: cfgfile.py and cmdline_cmp.py; documentation.

    * new files: cfgfile.py and cmdline_cmp.py
    * moved some functions from wisteria.py to cfgfile.py and cmdline_cmp.py
    * improved comments in wisteria.py

[DONE] task-48

'output.py' > 'cmdline_output.py'

    * 'output.py' > 'cmdline_output.py'
    * updated in wisteria.py the import of cmdline_output.py:parse_output_argument()

[DONE] task-47

Messages displayed by checkup() are now displayed with msgreport(), not
with msginfo() anymore.

    * Messages displayed by checkup() are now displayed with msgreport(), not
      with msginfo() anymore.

[DONE] task-46

New file (reportaspect.py) to define some text attributes for some parts
of the report.

    * New file (reportaspect.py) to define some text attributes for some parts
      of the report.
    * in reportaspect.py, 3 functions: aspect_title(), aspect_serializer()
      and aspect_data().

[DONE] task-45

Added a timestamp to first info message (project name, version, timestamp)

    * Added a timestamp to first info message (project name, version, timestamp)

[DONE] task-44

Log messages to the console and to the log file.

    * log messages to the console and to the log file.
    * --output option
    * new files: msg.py, output.py
    * rprint() has been replaced by msgxxx() functions.

[DONE] task-43

Documentation.

    * pimydoc: improved exit codes section
    * fixed a minor glitch in ROADMAP.md
    * removed one TODO.

[DONE] task-42

--report has now 4 shortcuts ("bestof", "laconic", "minimal", "full")

    * 4 report shortcuts have been defined: "bestof", "laconic", "minimal", "full"
    * no more REPORT_FULL_STRING and REPORT_MINIMAL_STRING in globs.py;
      these constants have been replaced by the REPORT_SHORTCUTS dict.

[DONE] task-41

Improved help message.

    * (--help) improved description in argparse.ArgumentParser:
      some examples have been given helping the user to start with

[DONE] task-40

New file: results.py

    * new file: results.py
    * DATA, SERIALIZERS moved to globs.py
    * improved messages in read_cmpstring()
    * normpath() moved from wisteria.py to utils.py
    * in report.py, STR2REPORTSECTION stores all accepted keywords for --report 
      string
    * improved ERRORID017 message
    * improved argparse message for --report
    * in report.py, report() handles now correctly the case where
      wisteria.globs.ARGS.report.split(";") returns an empty string.

[DONE] task-39

new function in wisteria.py: compute_results(). All computations have been
moved from main() to compute_results()

    * new function in wisteria.py: compute_results().

[DONE] task-38

Progress bar support. This progress bar cannot be displayed in debug mode.

    * progress bar support.

[DONE] task-37

pylint & doc.

    * improved message shown by --help for --checkup argument.
    * in SerializationResults._format_base100(), 
      bool_is_base100_value > bool_is_base100_reference
    * SerializationResults._get_base() > SerializationResults.get_base()
    * SerializationResults._get_serializers_base() > SerializationResults.get_serializers_base()
    * SerializationResults._get_dataobjs_base() > SerializationResults.get_dataobjs_base()

[DONE] task-36

report: B1d, D1a, D1b, D2a, D2b, D2c

    * report: B1d, D1a, D1b, D2a, D2b, D2c
    * REPORT_FULL_STRING = "titles;A;B;C;D;"
    * new functions in report.py: humanratio(), cmpdata2phrase(), ratio2phrase()
    * new functions in report.py: report_section_b1d(), report_section_d1a(),
                                  report_section_d1b(), report_section_d2a(),
                                  report_section_d2b(), report_section_d2c()

[DONE] task-35

report: A1, A2, A3 sections

    * new report sections: A1, A2, A3 sections
    * added to report.py new functions: report_section_a1(),
      report_section_a2(), report_section_a3()
    * REPORT_FULL_STRING set to "titles;A1;A2;A3;B1a;B1b;B1c;B2a;B2b;C1a;C1b;C2a;C2b;"
    * new file: utils.py

[DONE] task-34

new serializers: json, pickle, marshal

    * new serializers: json, pickle, marshal
    * added to serializers.py 3 new functions: serializer_json(), serializer_marshal()
      and serializer_pickle()

[DONE] task-33

bugfix in serializers.py: special cases are now correctly handled.

    * bugfix in serializers.py: special cases are now correctly handled.
      if some values can't be computed they now are displayed as "no data".

[DONE] task-32

Documentation.

    * improved doc.
    * ROADME.md > ROADMAP.md

[DONE] task-31

Bugfix: special keyword "titles" is now correctly handled by report()

    * Bugfix: special keyword "titles" is now correctly handled by report()

[DONE] task-30

--downloadconfigfile option.

    * --downloadconfigfile option
    * downloadconfigfile()
    * new constants in globs.py: DEFAULT_CONFIG_FILENAME, DEFAULTCFGFILE_URL

[DONE] task-29

Resized image in README.md.

    * resized image in README.md

[DONE] v. 0.0.2
---------------

Minor improvements: ERRXXX > ERRORIDXXX, err_codes.sh, image in README.md

    * ERRXXX > ERRORIDXXX
    * README.md: first try to add an image in the markdown file.
    * version number set to 0.0.2
  
    * task(s): tasks-28

```
$ poetry show --tree
```

```
$ ./check_tools.sh
* about poetry:
Poetry version 1.1.10
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
PYLINTHOME is now '/home/proguser/.cache/pylint' but obsolescent '/home/proguser/.pylint.d' is found; you can safely remove the latter
pylint 2.11.1
astroid 2.8.0
Python 3.9.7 (default, Aug 31 2021, 13:28:12) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-28

Minor improvements: ERRXXX > ERRORIDXXX, err_codes.sh, image in README.md

    * ERRXXX > ERRORIDXXX
    * README.md: first try to add an image in the markdown file.

[DONE] v. 0.0.1
---------------

First real version of the project. Somehow usable for a very limited amount
of serializers and different data. Try by example:
$ /bin/wisteria --help
$ /bin/wisteria --checkup
$ /bin/wisteria --cmp="jsonpickle against iaswn(ini)" --verbosity=2

    * tasks: task-1, task-2, task-3, task-4, task-5, 
             task-6, task-7, task-8, task-9, task-10, 
             task-11, task-12, task-13, task-14, task-15, 
             task-16, task-17, task-18, task-19, task-20, 
             task-21, task-22, task-23, task-24, task-25, 
             task-26, task-27

```
$ poetry show --tree
```

```
$ ./check_tools.sh
* about poetry:
Poetry version 1.1.10
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
PYLINTHOME is now '/home/proguser/.cache/pylint' but obsolescent '/home/proguser/.pylint.d' is found; you can safely remove the latter
pylint 2.11.1
astroid 2.8.0
Python 3.9.7 (default, Aug 31 2021, 13:28:12) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-27

Minor modifications to the doc. and minor bugfix.

    * linden.ini > wisteria.ini
    * fix a minor bug in report(): forgotten prefix 'f' in an f-string.
    * fix a minor bug in report(): '' is somehow a valid report section when splitting args.report.
    * improved doc. in wisteria.py

[DONE] task-26

Project new name is 'wisteria', cf https://en.wikipedia.org/wiki/Wisteria

[DONE] task-25

Improved documentation & output messages.

    * move the output of project name & version to the very beginning of the code.
    * new entry in pimydoc, namely 'code structure'

[DONE] task-24

Doc.

    * improved 'report sections' entry in pimydoc
    * new entry in pimydoc: 'console messages'
    * doc.

[DONE] task-23

report (C1a+C2a)

    * report (C1a+C2a)
    * 'stringlength' > 'strlen'
    * doc.

[DONE] task-22

Report code moved to new file linden.py/report.py .

    * Report code moved to new file linden.py/report.py .

[DONE] task-21

Report sections defined in --report are now read in their right order.

    * Report sections defined in --report are now read in their right order.
    * fixed a minor bug in SerializationResults.ratio_similarity()
    * fixed REPORT_FULL_STRING to "titles;A;B1a;B1b;B1c;B2a;B2b;C1b;C2b;"

[DONE] task-20

Code has been pylinted.

    * Code has been pylinted.
    * new entry in pimydoc: "exit codes"

[DONE] task-19

report (C1b)
 
    * report (C1b)

[DONE] task-18

Report (A, B1a, B1b, B2a, B2b, C2b)

    * Report (A, B1a, B1b, B2a, B2b, C2b)
    * doc.

[DONE] task-17

'identity' > 'similarity'.

    * 'identity' > 'similarity'
    * improved doc.

[DONE] task-16

Check that the input data are valid.

    * _finish_initialization() now returns (bool)success
    * main() checks the value of results._finish_initialization
      and results.data_objs_number

[DONE] task-15

Documentation & pimydoc.

    * documentation.
    * pimydoc file

[DONE] task-14

Report (A, B1a, B1b, B2a, B2b)

    * --report option
    * report()
    * globs.py: REPORT_MINIMAL_STRING and REPORT_FULL_STRING 

[DONE] task-13

Call SERIALIZERS[].func() to do the tests.

    * SERIALIZERS[].func() are now called
    * improved documentation; error code for each error message.
    * code pylinted.
                                  
[DONE] task-12

--checkup option: show some informations and quit.

    * --checkup option: show some informations and quit.
    * checkup() function
    * read_cfgfile() now prints an error message if an error occured while
      reading the configuration file.
    * no more calls to print(), replaced by calls to rprint().

[DONE] task-11

--cmp option

    * --cmp option: value is interpreted by read_cmpstring()
    * modify config file content: no more [main]tasks

[DONE] task-10

Fixed a minor bug: tmp file is now created only if there's no 
--help/--version argument on the command line.

    * Improved help message..
    * Fixed a minor bug: tmp file is now created only if there's no 
      --help/--version argument on the command line.

[DONE] task-9

--inifile argument: modify config file name.

    * --inifile argument

[DONE] task-8

Code has been splitted: data in linden/data.py and serializers in 
linden/serializers.py

    * linden/data.py and linden/serializers.py
    * --verbosity value has now to be choosed among VERBOSITY_xxx values

[DONE] task-7

--verbosity option

    * --verbosity option
    * VERBOSITY_xxx variables

[DONE] task-6

temp. file is now deleted at the end of the program.

    * temp. file is now deleted at the end of the program.
    * TMPFILE > TMPFILENAME 

[DONE] task-5

normpath() method to explicit file paths.

    * normpath(), method to explicit file paths.
    * improved print() output using normpath()

[DONE] task-4

bin/, linden.ini, arguments: -v, --version, --showwarmup, --debug

    * improved doc. in README.md
    * linden.ini
    * bin/ directory
    * main() function
    * LindenError class
    * SerializationResult class
    * arguments: -v, --version, --showwarmup, --debug

[DONE] task-3

New file: aboutproject.py.

    * new file: aboutproject.py

[DONE] task-2

Poetry stuff.

[DONE] task-1
-------------

Basic files.

    * various scripts
    * linden/linden.py
