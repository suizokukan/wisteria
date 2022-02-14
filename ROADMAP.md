Wisteria's roadmap & todos
==========================

===============================================================================
What's next ?

[? 0.2.1] petites corrections avant de passer à la suite
* --skimthedata="no" | "exclude ??? data"
* Ce message est étonnant:
    The following informations may have been written in the report file
  car le programme sait si les informations seront ou non écrites.
* "can't handle following data objects:"
   >
  "can't handle the following data objects:"  (??? vérifier)
* généraliser le mot 'transcoding'
* checkup: vérifier que demonstrationobj est sérialisable par tous les serializers
  Si c'est le cas, n'afficher ce résultat que si verbosity=3
* lorsque le programme plante (ou s'arrête après un CTRL+Z), le curseur de la console est modifiée; rétablir le cuseur normal via
    atexit
* data_object, dataobj_name: c'est le bazar
* avant chaque _______ : 1 ligne suffit
* "str(long)": "abhg12234"*10000, > "str(long)": "abhg12234"*1000

[? 0.2.2] vrais tests
* tests
        * prendre un jeu de données

[? 0.2.3] modification du hall of fame
* indiquer de surcroît la lisibilité donnée de cette chaîne.
  encodedstring illisibility: 0=not readable, 1=readable but with difficulty, 2=very readable
* extrawork: 0=no extrawork, 1=minimal (Iaswn), 2=maximal

[? 0.2.4] terminer --cmp="iaswn+pickle(int+str)"
? wisteria "mainstring": "pickle vs all(ini)++++"
? --cmp="iaswn vs json+pickle(array(q))" / liste des serializers dans le .ini (?)
      syntaxe de cmp string: 'others' ("iaswn vs others")  > l'indiquer dans README.md
* j'aimerais que --cmp="iaswn" ne parle que de iaswn

[? 0.2.5] améliorer la méthode utilisée (moyenne,)
* --method = "serializer=shuffle/sorted/raw;dataobj=shuffle/sorted/raw;lenmethod=str|bytes;timeitnumber=10;iteration=1+2+...+n|n"
* moyenne: calculer les résultats en plusieurs fois, en faisant la moyenne

[? 0.2.6] classer les serializers (A6+checkup) selon leur coverage rate:
0: n'arrive pas au niveau 1
1: arrive à transcoder une sélection de types Python élémentaires
2: arrive à transcoder cwc.simple
3: arrive à transcoder cwc.pgnreader

[? 0.2.7] wisteria "xyz"
* ce serait bien si... on pouvait utiliser Wisteria depuis la console Python; quid des arguments de la ligne de commande ?
* ce serait bien si... tous les arguments de la ligne de commande étaient définissables depuis le fichier de configuration.

[? 0.2.8] avant d'ajouter un max de serializers/datas:
* bestof : ??? > ne pas mettre overallscore dans les rapports sauf pour 'halloffame'

[? 0.2.9]
* finir de couvrir le plus de datas possible:
    - third-party à ajouter, en particulier panda+numpy
    - écrire les adaptations spécifiques pour cwc
    - fonctions wae pour les types de base
    
[? 0.3]
* finir de couvrir le plus de serializers possible
        https://en.wikipedia.org/wiki/Comparison_of_data-serialization_formats
        xdrlib (https://docs.python.org/3/library/xdrlib.html)
        Django (https://www.django-rest-framework.org/api-guide/serializers/)
        serpy (https://serpy.readthedocs.io/en/latest/performance.html)
        messagegpack (https://msgpack.org/)
        python-cjson (https://pypi.org/project/python-cjson/)
        python-rapidjson (https://pypi.org/project/python-rapidjson/)
        ujson (https://pypi.org/project/ujson/)
        jsons (via pip)
        jsonweb (https://docs.python.org/3/library/shelve.html#module-shelve)
        xmlrpclib (https://stackoverflow.com/questions/32022656/python-cannot-marshal-class-decimal-decimal-objects)

[III] pour écrire à V.S.
[? 0.3.1]
* README.md : %%français > anglais
* README.md acceptable
      + __init__.py

* vérifier que l'on peut installer et utiliser Wisteria 0.1.3 sur Windows
    C:\Users\Poste 1\AppData\Local\Programs\Python\Python39\python39.exe
  cela est important pour la discussion sur l'utilisation de la mémoire sous Linux & sous Windows.
  
[III] au-delà
* comment expliquer les différences d'utilisation de la mémoire entre Win+Linux ?
* comment expliquer que pickle n'utilise pas de mémoire pour pgnreader, mais Iaswn, si ?
* branche doublecheck
  branche doublecheckmemusage qui ne doit être rien d'autre que (1) main < virer #MEMMACHIN
  + (2) __version__ = "0.1.3 (doublecheckmemusage branch)", il nous faut donc un script de
  conversion, à grand coups de grep(?) __version__ = "0.1.3" + "(doub...)" (??)
* peak memory usage:
    remplacer le vague "memory usage" par "peak memory usage"; mais est-ce vrai sur Windows ?
    https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
* --meta: comparer avec les différentes versions de --method, graphique montrant ce qui se passe qd on augmente TIMEITNUMBER
      chercher si une combinaison donne des résultats vraiment différents des autres
* anomalie statistique: pyyaml a vraiment un problème avec strlong; calculer l'écart par rapport à la moyenne
      comment signaler cette anomalie ?

===============================================================================

[CURRENT] v. 0.2
* avec --checkup, arrêter de mettre en rouge (msgerror) le fait qu'il n'y ait pas de matplotlib
* quand verbosity==3, arrêter de couper la chaîne de caractères dans
   ! All 3 Unavailable Data Objects:
   dateutil(parser.parse)('missing package: dateutil'); cwc:pgnreader.cwc_iaswn.chessgames("this cwc module couldn't be imported[…]); cwc:simple.cwc_iaswn.simpleclass("this cwc module couldn't be 
imported[…])
* ! All 1 Unavailable Data Object:
  >
  1 Unavailable Data Object(s):
* get_missing_required_modules > get_missing_required_internal_modules
* il reste des TODOs

[DONE] task-277

Documentation.

    * Improved doc: (A/00) minimal imports > (A/00) minimal internal imports

    * tests: 7 tests ok out of 7    

[DONE] task-276

Added new fmt_xxx() functions.

    * added new fmt_xxx() functions
    * improved documentation

    * tests: 7 tests ok out of 7    

[DONE] task-275

Documentation.

    * improved README.md

    * tests: 7 tests ok out of 7    

[DONE] task-274

New function: data.py:check()
Updated dependencies modules defined in poetry.lock

    * improved error messages for ERRORDID037, ERRORDID038 and ERRORDID039
    * updated dependencies modules defined in poetry.lock:
      rich/version = "10.16.2"
      pywin/version = "303"
      pygments/version = "2.11.2"
      psutil/version = "5.9.0"
    * new function: data.py:check()
    * improved doc.

```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.9.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.16.2 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
wmi 1.5.1 Windows Management Instrumentation
└── pywin32 *
```

    * tests: 7 tests ok out of 7    

[DONE] task-273

Code is now compatible with Python3.8

    * in tests.sh, replaced 'python3.9' by 'python3'
    * in several .py, files, fixed the problem of the multi-lines with statement

    * tests: 7 tests ok out of 7

[DONE] v. 0.1.9

Fixed A2 and A3 report sections which now display only the serializers/data that
are required by PLANNED_TRANSCODINGS.


bugfixes

    * (bugfix) fixed a bug present in all serializers function; if an error occured
               while transcoding the source object, None is not returned anymore (task-272)
    * (bugfix) fixed a bug in SerializationResults.total_encoding_plus_decoding_time():
               if output == "fmtstr" if an incoherent value is computed, None is no
               more returned (task-272)
               
code quality

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

code structure

    * new types checked by works_as_expected(): 
      - collections.defaultdict(int)
      - collections.defaultdict(list)
      - collections.defaultdict(none)
      - collections.defaultdict(set) (task-270)
    * new signature for works_as_expected() functions, namely
      works_as_expected(data_name, obj=None) instead of
      works_as_expected(data_name=None, obj=None) (task-270)

dependencies

    * updated dependencies (`poetry update`) (task-269)
    
documentation

    * updated doc. (task-270)
    * improved messages displayed by serializers (task-270)
    
interface

    * fixed A2 and A3 report sections which now display only the serializers/data that
      are required by PLANNED_TRANSCODINGS (task-271)
    * improved fmt_boolsuccess() returned string (task-272)

task(s)

    * task(s): task-269, task-270, task-271, task-272

version

    * set version to '0.1.9'


```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.12.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
wmi 1.5.1 Windows Management Instrumentation
└── pywin32 *
```

```
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
pylint 2.11.1
astroid 2.8.5
Python 3.9.7 (default, Oct 10 2021, 15:13:22) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-272

Bugfixes.

    * improved fmt_boolsuccess() returned string (task-272)
    * (bugfix) fixed a bug present in all serializers function; if an error occured
               while transcoding the source object, None is not returned anymore (task-272)
    * (bugfix) fixed a bug in SerializationResults.total_encoding_plus_decoding_time():
               if output == "fmtstr" if an incoherent value is computed, None is no
               more returned (task-272)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-271

Fixed A2 and A3 report sections which now display only the serializers/data that
are required by PLANNED_TRANSCODINGS.

    * fixed A2 and A3 report sections which now display only the serializers/data that
      are required by PLANNED_TRANSCODINGS (task-271)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-270

    * new types checked by works_as_expected(): 
      - collections.defaultdict(int)
      - collections.defaultdict(list)
      - collections.defaultdict(none)
      - collections.defaultdict(set) (task-270)
    * new signature for works_as_expected() functions, namely
      works_as_expected(data_name, obj=None) instead of
      works_as_expected(data_name=None, obj=None) (task-270)
    * updated doc. (task-270)
    * improved messages displayed by serializers (task-270)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-269

Updated dependencies (`poetry update`).

    * updated dependencies (`poetry update`) (task-269)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] v. 0.1.8

-  Added a new serializer: 'amazon.ion.simpleion'.
-  --exportreport='md'.
-  If --checkup/--downloadconfigfile/--mymachine is set, no graph file is added
   to the exported report anymore.
-  fixed minor typos in ROADMAP.md
-  New report, named 'A4', displaying the list of the planned transcodings.
-  New report section, named 'A5 What do the Encoded Strings Look Like?' (task-266)


bugfixes

    * bugfix: hbar2png() draws now correctly xticks numbers (task-238)
    * bugfix: in exit_handler(), temp file is now closed before being removed
              (task-244)
    * bugfix: SerializationResults.finish_initialization() initializes now
      correctly self.dataobjs by browsing all dataobjs from all serializers
      (task-251)
    * bugfix: fixed SerializationResults.finish_initialization(); total_xxx()
              methods(output='value') return None, not a string if an error
              occured, hence some lines of code to be changed (task-252)
    * bugfix: cwc/pgnreader/iaswn.py:__init__.py methods now call Iaswn __init__
              (task-253)
    * bugfix: SerializationResults.finish_initialization() now initializes
              .hall more wiser since .hall["encoding_success"],
              .hall["decoding_success"] and .hall["reversibility"] may be
              not correctly initialized (task-253)
    * bugfix: improved the way some SerializationResults methods check that the
              results are coherent (.total_decoding_time(), .total_encoding_time(),
              .total_mem_usage) (task-253)
    * bugfix: in several SerializationResults methods like ratio_decoding_success()
            or total_decoding_time() the test:
            if not serializer_is_compatible_with_dataobj(serializer, dataobj)
            is now called before the other test:
                if self[serializer][dataobj] is None
            in order to discard an error if _dataobj is not in self[serializer] (task-257)

code quality

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

code structure

    * added a new serializer: 'amazon.ion.simpleion', hence the new
      serializer_simpleion() function (task-232)
    * improved exit_handler(): DATA['file descriptor'] is not closed if
      'file descriptor' isn't in DATA, as it may happen if an error occurs
      while DATA has not been fully initialized (task-232)
    * improved code readibilty in serializer_xxx() function; each serializer_xxx()
      function now starts with a `module = ` statement (task-232)
    * --exportreport='md:myfile.md', defined in exit_handler() (task-240)
    * new variable in globs.py: `DEFAULT_EXPORTREPORT_FILENAME` (task-240)
    * the normal way to open the report file is now `open_reportfile()` (task-240)
    * new class `SerializersDataNMVH`, used by SerializersData.__init__() (task-242)
    * new function get_python_version() to factorize some parts of the code.
    * new entry in pimydoc: dataobjs_number (task-251)
    * new cwc_utils.py function: are_two_cwc_variants_of_the_same_cwc() (task-251)
    * new cwc_utils.py function: count_dataobjs_number_without_cwc_variant() (task-251)
    * new cwc_utils.py function: serializer_is_compatible_with_dataobj() (task-251)
    * new cwc_utils.py function: shorten_cwc_name() (task-251)
    * new test: CWCUtils.test_count_dataobjs_number_without_cwc_variant() in a new
      file, namely tests/cwc_utils__tests.py (task-251)
    * fmt_ratio() now accepts None as dumb argument and not (None, None) anymore
      (task-253)
    * new globs.py variable, namely `CWC_MODULES`, added in order to add more
      easily new cwx classes (task-254)
    * planned transcodings are now stored in PLANNED_TRANSCODINGS instead of
      being set just before the main computes start. It will allow, in the
      future, to replay these transcodings. (task-254)
    * new variable: globs.py:PLANNED_TRANSCODINGS (task-254)
    * PLANNED_TRANSCODINGS is set by a new function, init_planned_transcodings()
      (task-254)
    * SerializationResults.dataobjs is now a sorted list of strings (task-261)
    * new data type: cwc.simple.*.simpleclass (task-267)
    * all cwc files' name starts now with the 'cwc_' prefix (task-268)
    * err_codes.sh: max_index=55 (task-236)
    * pylintrc: max-attributes=9 (task-243)
    * removed useless method SerializationResults.get_base() (task-251)
    * removed useless `dataobj` argument from
      SerializationResults.total_encoding_plus_decoding_time() (task-252)
    * variables in globs.py have been sorted (task-255)
    * (pylintrc) max-module-lines=3000 (task-266)
    * fixed a minor typo in serializers.py: 'konwn' > 'known' (task-233)
    * fixed a minor typo in serializers.py: 'konwn' > 'known' (task-234)
    * re-numbered all error codes (task-236)
    * command line arguments are now sorted in wisteria.py by alphabetical
      order (task-240)
    * new class `SerializersDataNMVH`, used by SerializersData.__init__() (task-242)
    * variables in globs.py have been sorted (task-255)
    * 'DEFAULTCFGFILE_URL' > 'DEFAULT_CONFIGFILE_URL' (task-255)
    * 'DEFAULT_CONFIG_FILENAME' > 'DEFAULT_CONFIGFILE_NAME'
    * the exit codes numbers have been renumbered to distinguish internal errors
      (-100, -101, ...) from other errors (-1, -2, ...) (task-257)

documentation

    * improved doc. in serializers.py (task-239)
    * improved doc in report.py (task-240)
    * new entry in `pimydoc`: `GRAPHS_DESCRIPTION format` (task-241)
    * improved doc. (task-241)
    * improved doc. in the code and debug message (task-245)
    * new entry in pimydoc: dataobjs_number (task-251)
    * improved documentation (task-251)
    * fixed a minor glitch in ROADMAP.MD in task-251 (task-252)
    * improved README.md: documentation about adding cwc classes (task-253)
    * new entry in pimydoc: `demonstration_dataobj` (task-253)
    * new entry in pimydoc: PLANNED_TRANSCODINGS (task-254)
    * improved documentation (task-254)
    * fixed a minor glitch in ROADMAP.md, cf task-253 (task-254)
    * improved doc. in globs.py (task-255)

interface, output messages

    * Improved a message in exit_handler(): "Let's close the filenconsole file" >
      "About to close the console file" (task-235)
    * improved checkup() message: added the report filename (task-237)
    * added a debug message in exit_handler() if an expected graph is missing
      (task-247)
    * replaced called to print() by called to rprint() (task-247)
    * improved results functions so that incoherent results are correctly marked
      as incoherent results. SerializationResults functions have been improved,
      and report_() functions too. (task-248)
    * If --checkup/--downloadconfigfile/--mymachine is set, no graph file is
      added to the exported report anymore (task-250)
    * improved text readibility in B1a and B2a tables (task-256)
    * improved debug message displayed while computing (task-258)
    * improved debug message in compute_results() (task-260)
    * If a graph file can't be created and if an ancient file having the same name
      exits, this ancient file is removed to avoid confusing the ancient file with
      the new one that couln't be created (task-262)
    * improved graph drawing when all values are (nearly or exactly) equal to 0
      (task-263)
    * Improved report/debug messages in report_section_graphs():
      English syntax and filename+normpath(filename) (task-264)
    * new report, named 'A4', displaying the list of the planned transcodings (task-265)
    * transcoding_index starts by 1 (not 0) when displayed (task-265)
    * new report section, named 'A5 What do the Encoded Strings Look Like?' (task-266)
    * `demonstration_dataobj` > `demonstration_dataobj_a5` (task-266)

task(s)

    task(s) : task-232, task-233, task-234, task-235, task-236, task-237,
              task-238, task-239, task-240, task-241, task-242, task-243,
              task-244, task-245, task-246, task-247, task-248, task-249,
              task-250, task-251, task-252, task-253, task-254, task-255,
              task-256, task-257, task-258, task-259, task-260, task-261,
              task-262, task-263, task-264, task-265, task-266, task-267,
              task-268

version

    * set version to "0.1.8"

```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.12.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
wmi 1.5.1 Windows Management Instrumentation
└── pywin32 *
```

```
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
pylint 2.11.1
astroid 2.8.4
Python 3.9.7 (default, Oct 10 2021, 15:13:22)
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-268

All cwc files' name starts now with the 'cwc_' prefix.

    * all cwc files' name starts now with the 'cwc_' prefix (task-268)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-267

New data type: cwc.simple.*.simpleclass .

    * new data type: cwc.simple.*.simpleclass (task-267)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-266

New report section, named 'A5 What do the Encoded Strings Look Like?'

    * new report section, named 'A5 What do the Encoded Strings Look Like?' (task-266)
    * `demonstration_dataobj` > `demonstration_dataobj_a5` (task-266)
    * (pylintrc) max-module-lines=3000 (task-266)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-265

New report, named 'A4', displaying the list of the planned transcodings.

    * new report, named 'A4', displaying the list of the planned transcodings (task-265)
    * transcoding_index starts by 1 (not 0) when displayed (task-265)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-264

Improved report/debug messages in report_section_graphs().

    * Improved report/debug messages in report_section_graphs():
      English syntax and filename+normpath(filename) (task-264)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-263

Improved graph drawing when all values are (nearly or exactly) equal to 0.

    * improved graph drawing when all values are (nearly or exactly) equal to 0
      (task-263)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-262

If a graph file can't be created and if an ancient file having the same name
exits, this ancient file is removed to avoid confusing the ancient file with
the new one that couln't be created.

    * If a graph file can't be created and if an ancient file having the same name
      exits, this ancient file is removed to avoid confusing the ancient file with
      the new one that couln't be created (task-262)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-261

SerializationResults.dataobjs is now a sorted list of strings.

    * SerializationResults.dataobjs is now a sorted list of strings (task-261)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-260

Improved debug message in compute_results().

    * improved debug message in compute_results() (task-260)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-259

Bugfix: in several SerializationResults methods like ratio_decoding_success()
        or total_decoding_time() the test:
            if not serializer_is_compatible_with_dataobj(serializer, dataobj)
        is now called before the other test:
            if self[serializer][dataobj] is None
        in order to discard an error if _dataobj is not in self[serializer].

    * bugfix: in several SerializationResults methods like ratio_decoding_success()
            or total_decoding_time() the test:
            if not serializer_is_compatible_with_dataobj(serializer, dataobj)
            is now called before the other test:
                if self[serializer][dataobj] is None
            in order to discard an error if _dataobj is not in self[serializer] (task-257)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-258

Improved debug message displayed while computing.

    * improved debug message displayed while computing (task-258)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-257

The exit codes numbers have been renumbered to distinguish internal errors
(-100, -101, ...) from other errors (-1, -2, ...)

    * the exit codes numbers have been renumbered to distinguish internal errors
      (-100, -101, ...) from other errors (-1, -2, ...) (task-257)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-256

Improved text readibility in B1a and B2a tables.

    * improved text readibility in B1a and B2a tables (task-256)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-255

Variables in globs.py have been sorted.

    * variables in globs.py have been sorted (task-255)
    * 'DEFAULTCFGFILE_URL' > 'DEFAULT_CONFIGFILE_URL' (task-255)
    * 'DEFAULT_CONFIG_FILENAME' > 'DEFAULT_CONFIGFILE_NAME'
    * improved doc. in globs.py (task-255)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-254

Planned transcodings are now stored in PLANNED_TRANSCODINGS instead of
being set just before the main computes start. It will allow, in the
future, to replay these transcodings. (task-254)

    * planned transcodings are now stored in PLANNED_TRANSCODINGS instead of
      being set just before the main computes start. It will allow, in the
      future, to replay these transcodings. (task-254)
    * new variable: globs.py:PLANNED_TRANSCODINGS (task-254)
    * PLANNED_TRANSCODINGS is set by a new function, init_planned_transcodings()
      (task-254)
    * new entry in pimydoc: PLANNED_TRANSCODINGS (task-254)
    * improved documentation (task-254)
    * fixed a minor glitch in ROADMAP.md, cf task-253 (task-254)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-253

Various bugfixes, documentation, CWC_MODULES variable.

    * bugfix: cwc/pgnreader/iaswn.py:__init__.py methods now call Iaswn __init__
              (task-253)
    * bugfix: SerializationResults.finish_initialization() now initializes
              .hall more wiser since .hall["encoding_success"],
              .hall["decoding_success"] and .hall["reversibility"] may be
              not correctly initialized (task-253)
    * bugfix: improved the way some SerializationResults methods check that the
              results are coherent (.total_decoding_time(), .total_encoding_time(),
              .total_mem_usage) (task-253)
    * fmt_ratio() now accepts None as dumb argument and not (None, None) anymore
      (task-253)
    * new globs.py variable, namely `CWC_MODULES`, added in order to add more
      easily new cwx classes (task-254)
    * improved README.md: documentation about adding cwc classes (task-253)
    * new entry in pimydoc: `demonstration_dataobj` (task-253)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-252

Bugfix: fixed SerializationResults.finish_initialization(); total_xxx()
        methods(output='value') return None, not a string if an error
        occured, hence some lines of code to be changed.

    * bugfix: fixed SerializationResults.finish_initialization(); total_xxx()
              methods(output='value') return None, not a string if an error
              occured, hence some lines of code to be changed (task-252)
    * removed useless `dataobj` argument from
      SerializationResults.total_encoding_plus_decoding_time() (task-252)
    * fixed a minor glitch in ROADMAP.MD in task-251 (task-252)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-251

Bugfixes: fixed several bugs preventing inconsistent results from being displayed.

    * bugfix: SerializationResults.finish_initialization() initializes now
      correctly self.dataobjs by browsing all dataobjs from all serializers
      (task-251)
    * new entry in pimydoc: dataobjs_number (task-251)
    * new cwc_utils.py function: are_two_cwc_variants_of_the_same_cwc() (task-251)
    * new cwc_utils.py function: count_dataobjs_number_without_cwc_variant() (task-251)
    * new cwc_utils.py function: serializer_is_compatible_with_dataobj() (task-251)
    * new cwc_utils.py function: shorten_cwc_name() (task-251)
    * improved documentation (task-251)
    * removed useless method SerializationResults.get_base() (task-251)
    * new test: CWCUtils.test_count_dataobjs_number_without_cwc_variant() in a new
      file, namely tests/cwc_utils__tests.py (task-251)

    * tests: 7 tests ok out of 7
    * Pylint: 10/10

[DONE] task-250

If --checkup/--downloadconfigfile/--mymachine is set, no graph file is added
to the exported report anymore.

    * If --checkup/--downloadconfigfile/--mymachine is set, no graph file is
      added to the exported report anymore (task-250)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-249

'fmt_stringlength' > 'fmt_strlen'.

    * 'fmt_stringlength' > 'fmt_strlen' (task-249)

    * tests: 6 tests ok out of 6

[DONE] task-248

Improved results functions so that incoherent results are correctly marked
as incoherent results.

    * improved results functions so that incoherent results are correctly marked
      as incoherent results. SerializationResults functions have been improved,
      and report_() functions too. (task-248)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-247

New function get_python_version() to factorize some parts of the code.

    * new function get_python_version() to factorize some parts of the code.

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-246

Added a debug message in exit_handler() if an expected graph is missing.

    * added a debug message in exit_handler() if an expected graph is missing
      (task-247)
    * replaced called to print() by called to rprint() (task-247)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-245

Improved doc. in the code and debug message in exit_handler().

    * improved doc. in the code and debug message (task-245)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-244

Bugfix: in exit_handler(), temp file is now closed before being removed.

    * bugfix: in exit_handler(), temp file is now closed before being removed
              (task-244)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-243

Updated pylintrc and README.md (pylintrc: max-attributes=9)

    * pylintrc: max-attributes=9 (task-243)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-242

New class `SerializersDataNMVH`, used by SerializersData.__init__().

    * new class `SerializersDataNMVH`, used by SerializersData.__init__() (task-242)

[DONE] task-241

Improved doc.

    * new entry in `pimydoc`: `GRAPHS_DESCRIPTION format` (task-241)
    * improved doc. (task-241)

[DONE] task-240

--exportreport='md'.

    * --exportreport='md:myfile.md', defined in exit_handler() (task-240)
    * command line arguments are now sorted in wisteria.py by alphabetical
      order (task-240)
    * new variable in globs.py: `DEFAULT_EXPORTREPORT_FILENAME` (task-240)
    * the normal way to open the report file is now `open_reportfile()` (task-240)
    * improved doc in report.py (task-240)

[DONE] task-239

Improved doc. in serializers.py.

    * improved doc. in serializers.py (task-239)

[DONE] task-238

Bugfix: hbar2png() draws now correctly xticks numbers.

    * bugfix: hbar2png() draws now correctly xticks numbers (task-238)

[DONE] task-237

Improved checkup() message: added the report filename.

    * improved checkup() message: added the report filename (task-237)

[DONE] task-236

Re-numbered all error codes.

    * re-numbered all error codes (task-236)
    * err_codes.sh: max_index=55 (task-236)

[DONE] task-235

Improved a message in exit_handler(): "Let's close the filenconsole file" >
"About to close the console file".

    * Improved a message in exit_handler(): "Let's close the filenconsole file" >
      "About to close the console file" (task-235)

[DONE] task-234

Fixed a minor typo in README.md: 'can be done on you system' > 'can be done on your system'

    * fixed a minor typo in serializers.py: 'konwn' > 'known' (task-234)

[DONE] task-233

Fixed a minor typo in serializers.py: 'konwn' > 'known'

    * fixed a minor typo in serializers.py: 'konwn' > 'known' (task-233)

[DONE] task-232

Added a new serializer: 'amazon.ion.simpleion'.

    * added a new serializer: 'amazon.ion.simpleion', hence the new
      serializer_simpleion() function (task-232)
    * improved exit_handler(): DATA['file descriptor'] is not closed if
      'file descriptor' isn't in DATA, as it may happen if an error occurs
      while DATA has not been fully initialized (task-232)
    * improved code readibilty in serializer_xxx() function; each serializer_xxx()
      function now starts with a `module = ` statement (task-232)

[DONE] v. 0.1.7

- Added a new serializer: 'yajl'.
- documentation and code readibility


code quality

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

code structure

    * added a new serializer: 'yajl' (task-229)
    * updated project dependencies with `poetry update` (task-230)
    * globs.py:REPORTFILE_NAME > globs.py:DEFAULT_REPORTFILE_NAME (task-231)
    * 'logfile' > 'reportfile' everywhere in the code (task-231)

documentation

    * new entry in `pimydoc`: `report filename format` (task-231)
    * improved documentation (task-231)

task(s):

    * task(s): task-229, task-230, task-231

version:

    * set version to '0.1.7'


```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.12.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
wmi 1.5.1 Windows Management Instrumentation
└── pywin32 *
```

```
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
pylint 2.11.1
astroid 2.8.4
Python 3.9.7 (default, Oct 10 2021, 15:13:22)
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-231

Improved code readibility and the documentation.

    * new entry in `pimydoc`: `report filename format` (task-231)
    * 'logfile' > 'reportfile' everywhere in the code (task-231)
    * globs.py:REPORTFILE_NAME > globs.py:DEFAULT_REPORTFILE_NAME (task-231)
    * improved documentation (task-231)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-230

Updated project dependencies with `poetry update`.

    * updated project dependencies with `poetry update` (task-230)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-229

Added a new serializer: 'yajl'.

    * added a new serializer: 'yajl' (task-229)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] v. 0.1.6

- added 'allbutcwc' as a valid cmp data string
- each data type may be tested thanks to the 'works_as_expected' (=wae) mechanism.


bugfix

    * bugfix: compute_results() now returns new exit code 4 if there's no
      data to handle (task-219)
    * bugfix: serializer_xxx() methods call now correctly works_as_expected()
              method (task-225)

code quality

    * (pylintrc) max-nested-blocks=5 > max-nested-blocks=6 (task-212)
    * "# pylint: disable" > "#   pylint: disable" (task-215)
    * modified pylintrc: max-attributes=8 & max-args=8 (task-223)
    * replaced double quotes in the code with single quotes for some arguments:
      "cwc" > 'cwc', "ini" > 'ini', ... (task-225)
    * functions in cwc_utils.py are now in alphabetical order.
     (task-226)
    * simplified code in pgnreader/[default|iaswn].py by using dataclass
      (task-228)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

code structure

    * (cwc_default.py): the tests are now partly in-memory (task-210)
    * new file: wisteria/dmfile.py (DMFile class) (task-210)
    * (cwc_default.py): test() function
      Like all cwc files, test() allows to check that the objects created in
      this file are usable. Return (bool)success. (task-211)
    * `cwc mode` works with 'pickle' (and all serializers requiring 'default' cwc
      module) and with 'iaswn'. Please note that cwc objects are not yet fully
      initialized. (task-212)
    * DATA[] contains cwc modules too (task-212)
    * new cwc/pgnreader file: iaswn.py (task-212)
    * new file (`cwc_utils.py`) with the following functions:
      - is_a_cwc_name()
      - moduleininame_to_modulefullrealname()
      - modulefullrealname_to_modulerealname()
      - modulefullrealname_to_objectname()
      - is_this_an_appropriate_module_for_serializer()
      (task-212)
    * (cwc/pgnreader) initialize() and works_as_expected() have been moved to
       the new file wisteria/cwc/pgnreader/works_as_expected.py (task-214)
    * new function in cwc_utils.py: modulefullrealname_to_waemodulename() (task-214)
    * (cwc/pgnreader) added __eq__ method to all classes so that evaluation
      (reversibility) is possible (task-214)
    * exit_handler() closes wisteria.globs.DATA['file descriptor'] (task-215)
    * new globs.py variable: DEBUG_CONSOLEWIDTH (task-221)
    * it's now possible to add a comment for a serializer:
      Serializer.comment may be None or a string. (task-223)
    * new function in cwc_utils.py: `select__works_as_expected__function()`
      (task-224)
    * all works_as_expected() functions have now two arguments (task-224)
    * 4 values are now accepted for cmpdata: 'cwc', 'ini', 'allbutcwc' and 'all'
      (task-225)

documentation

    * new entries in pimydoc: `cwc modules names` and `DATA format` (task-212)
    * improved documentation (task-212)
    * new entry in `pimydoc`: progress bar (task-213)
    * documentation (task-213)
    * pimydoc: added to 'exit codes' new exit code 4
    * improved partial_report__serializers()'s docstring (task-220)
    * updated README.md (task-223)
    * new entry in `pimydoc`: `works_as_expected arguments and returned value`
      (task-224)
    * new entry in `pimydoc`: `--cmp format` (task-225)
    * improved documentation in pgn/default.py and in pgn/iaswn.py (task-227)
    * improved ROADMAP.md (0.1.6)

interface

    * fixed a typo in partial_report__data() (task-212)
    * fixed a typo in `report_section_c2c__serializervsserializer()`
      (task-212)
    * Serializers can from now display the encoded string they have computed (task-213)
    * improved --help messages readibility: each sentence starts with an uppercase
      letter and ends with a point (task-216)
    * Improved debug messages displayed by exit_handler() (task-217)
    * improved message displayed by `tests.sh` (task-218)
    * checkup() now displays the internal serializer name (SERIALIZER.name)
      if it's different from the human name (SERIALIZER.human_name) (task-220)
    * added a message displayed at the beginning of --checkup messages,
      explaining (1) that the informations displayed may have been written in
      the report file and (2) that --verbosity value has an effect upon the
      displayed informations (task-220)
    * improved partial_report__data() display: DATA-s and UNAVAILABLE_DATA-s
      are now sorted (task-222)
    * modified --checkup output so that a works_as_expected() function linked
      to a data type is displayed (task-224)
    * 4 values are now accepted for cmpdata: 'cwc', 'ini', 'allbutcwc' and 'all'
      (task-225)

tasks

    * task(s): task-210, task-211, task-212, task-213, task-214, task-215,
               task-216, task-217, task-218, task-219, task-220, task-221,
               task-222, task-223, task-224, task-225, task-226, task-227,
               task-228

version

    * set version to '0.1.6'


```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.12.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
pylint 2.11.1
astroid 2.8.4
Python 3.9.7 (default, Oct 10 2021, 15:13:22)
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-228

Simplified code in pgnreader/[default|iaswn].py by using dataclass.

    * simplified code in pgnreader/[default|iaswn].py by using dataclass
      (task-228)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-227

Improved documentation in pgn/default.py and in pgn/iaswn.py.

    * improved documentation in pgn/default.py and in pgn/iaswn.py (task-227)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-226

Functions in cwc_utils.py are now in alphabetical order.

    * functions in cwc_utils.py are now in alphabetical order.
      (task-226)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-225

4 values are now accepted for cmpdata: 'cwc', 'ini', 'allbutcwc' and 'all'.

    * 4 values are now accepted for cmpdata: 'cwc', 'ini', 'allbutcwc' and 'all'
      (task-225)
    * replaced double quotes in the code with single quotes for some arguments:
      "cwc" > 'cwc', "ini" > 'ini', ... (task-225)
    * new entry in `pimydoc`: `--cmp format` (task-225)
    * bugfix: serializer_xxx() methods call now correctly works_as_expected()
              method (task-225)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-224

Modified --checkup output so that a works_as_expected() function linked
to a data type is displayed.

    * modified --checkup output so that a works_as_expected() function linked
      to a data type is displayed (task-224)
    * new entry in `pimydoc`: `works_as_expected arguments and returned value`
      (task-224)
    * new function in cwc_utils.py: `select__works_as_expected__function()`
      (task-224)
    * all works_as_expected() functions have now two arguments (task-224)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-223

It's now possible to add a comment for a serializer.

    * it's now possible to add a comment for a serializer:
      Serializer.comment may be None or a string. (task-223)
    * modified pylintrc: max-attributes=8 & max-args=8 (task-223)
    * updated README.md (task-223)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-222

Improved partial_report__data() display: DATA-s and UNAVAILABLE_DATA-s
are now sorted.

    * improved partial_report__data() display: DATA-s and UNAVAILABLE_DATA-s
      are now sorted (task-222)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-221

New globs.py variable: DEBUG_CONSOLEWIDTH.

    * new globs.py variable: DEBUG_CONSOLEWIDTH (task-221)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-220

checkup() now displays the internal serializer name (SERIALIZER.name)
if it's different from the human name (SERIALIZER.human_name)

    * checkup() now displays the internal serializer name (SERIALIZER.name)
      if it's different from the human name (SERIALIZER.human_name) (task-220)
    * added a message displayed at the beginning of --checkup messages,
      explaining (1) that the informations displayed may have been written in
      the report file and (2) that --verbosity value has an effect upon the
      displayed informations (task-220)
    * improved partial_report__serializers()'s docstring (task-220)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-219

Bugfix: compute_results() now returns new exit code 4 if there's no
data to handle.

    * bugfix: compute_results() now returns new exit code 4 if there's no
      data to handle (task-219)
    * pimydoc: added to 'exit codes' new exit code 4

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-218

Improved message displayed by `tests.sh`.

    * improved message displayed by `tests.sh` (task-218)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-217

Improved debug messages displayed by exit_handler().

    * Improved debug messages displayed by exit_handler() (task-217)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-216

Improved --help messages readibility: each sentence starts with an uppercase
letter and ends with a point.

    * improved --help messages readibility: each sentence starts with an uppercase
      letter and ends with a point (task-216)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-215

exit_handler() closes wisteria.globs.DATA['file descriptor'] (task-215)

    * exit_handler() closes wisteria.globs.DATA['file descriptor'] (task-215)
    * "# pylint: disable" > "#   pylint: disable" (task-215)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-214

Reversibility is now computed thanks to a call to works_as_expected() method
defined in the new file wisteria/cwc/pgnreader/works_as_expected.py.

    * (cwc/pgnreader) initialize() and works_as_expected() have been moved to
       the new file wisteria/cwc/pgnreader/works_as_expected.py (task-214)
    * new function in cwc_utils.py: modulefullrealname_to_waemodulename() (task-214)
    * (cwc/pgnreader) added __eq__ method to all classes so that evaluation
      (reversibility) is possible (task-214)

    * tests: 6 tests ok out of 6
    * Pylint: 10/10

[DONE] task-213

Serializers can from now display the encoded string they have computed.

    * Serializers can from now display the encoded string they have computed (task-213)
    * new entry in `pimydoc`: progress bar (task-213)
    * documentation (task-213)

    * tests: 6 tests ok out of 6.
    * Pylint: 10/10

[DONE] task-212

`cwc mode` works with 'pickle' (and all serializers requiring 'default' cwc
module) and with 'iaswn'. Please note that cwc objects are not yet fully
initialized.

    * `cwc mode` works with 'pickle' (and all serializers requiring 'default' cwc
      module) and with 'iaswn'. Please note that cwc objects are not yet fully
      initialized. (task-212)
    * DATA[] contains cwc modules too (task-212)
    * new cwc/pgnreader file: iaswn.py (task-212)
    * new entries in pimydoc: `cwc modules names` and `DATA format` (task-212)
    * new file (`cwc_utils.py`) with the following functions:
      - is_a_cwc_name()
      - moduleininame_to_modulefullrealname()
      - modulefullrealname_to_modulerealname()
      - modulefullrealname_to_objectname()
      - is_this_an_appropriate_module_for_serializer()
      (task-212)
    * fixed a typo in partial_report__data() (task-212)
    * fixed a typo in `report_section_c2c__serializervsserializer()`
      (task-212)
    * (pylintrc) max-nested-blocks=5 > max-nested-blocks=6 (task-212)
    * improved documentation (task-212)

[DONE] task-211

(cwc_default.py): test() function

    * (cwc_default.py): test() function
      Like all cwc files, test() allows to check that the objects created in
      this file are usable. Return (bool)success. (task-211)

    * tests: 6 tests ok out of 6.
    * Pylint: 10/10

[DONE] task-210

(cwc_default.py): the tests are now partly in-memory.

    * (cwc_default.py): the tests are now partly in-memory (task-210)
    * new file: wisteria/dmfile.py (DMFile class) (task-210)

    * tests: 6 tests ok out of 6.
    * Pylint: 10/10

[DONE] v. 0.1.5

wisteria/cwc/pgnreader/default.py


code structure

    * wisteria/cwc/pgnreader/default.py 
      (task-190, task-191, task-192, task-194, task-195, task-196, task-197, task-198,
       task-200, task-201, task-203, task-205, task-206, task-207, task-209)
    * tests; new directories: tests/, wisteria/cwc/pgnreader; new script: tests.sh
      (task-193, task-199, task-202, task-204, task-208)
    * codesearch.py: uncomment some lines in order to search in tests/ too 
      (task-208)

code quality

    * tests: 6 tests ok out of 6.
    * Pylint: 10/10
    
tasks

    * task(s): task-191, task-192, task-193, task-194, task-195, task-196, task-197, 
               task-198, task-199, task-200, task-201, task-202, task-203, task-204,
               task-205, task-206, task-207, task-208, task-209

version

    * set version to '0.1.5'


```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.12.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
pylint 2.11.1
astroid 2.8.3
Python 3.9.7 (default, Oct 10 2021, 15:13:22) 
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-209

(cwc_default.py): documentation.

    * (cwc_default.py): documentation (task-209)

    * tests: 6 tests ok out of 6.
    * Pylint: 10/10

[DONE] task-208

(cwc_default.py): reduced test numbers from 12 to 6.

    * (cwc_default.py): improved tests (added comparison to the value of 
                        human_repr() in one test) (task-208)
    * (cwc_default.py): reduced test numbers from 12 to 6 (task-208)
    * codesearch.py: uncomment some lines in order to search in tests/ too 
      (task-208)

    * tests: 6 tests ok out of 6.
    * Pylint: 10/10

[DONE] task-207

(cwc_default.py): documentation.

    * (cwc_default.py): documentation (task-207)

    * tests: 12 tests ok out of 12.
    * Pylint: 10/10

[DONE] task-206

(cwc_default.py): game result is now added to .pgn files

    * (cwc_default.py) game result is now added to .pgn files (task-206)
    * (cwc_default.py) read_pgn__simplemove: removed useless lines of code
      (task-206)
    * (cwc_default.py) documentation (task-206)

    * tests: 12 tests ok out of 12.
    * Pylint: 10/10

[DONE] task-205

(cwc_default.py): removed useless ChessMove.valid attribute

    * (cwc_default.py): removed useless ChessMove.valid attribute (task-205)
    * fixed a typo in ROADMAP.md (cf task-204)

    * tests: 12 tests ok out of 12.
    * Pylint: 10/10

[DONE] task-204

(cwc_default.py): reduced tests numbers from 22 to 12.

    * (cwc_default.py): reduced tests numbers from 22 to 12 (task-204)

    * tests: 12 tests ok out of 12.
    * Pylint: 10/10

[DONE] task-203

(cwc_default.py): pylinted the code

    * (cwc_default.py): pylinted the code (task-203)
    * (pylintrc) max-public-methods=20 > max-public-methods=30 (task-203)

    * tests: 22 tests ok out of 22.
    * Pylint: 10/10

[DONE] task-202

(cwc_default.py): new tests (CWCPgnreader.test_readwrite_*)

    * (cwc_default.py): new tests (CWCPgnreader.test_readwrite_*)
      (task-202)
    * (cwc_default.py): bugfix in ChessGame.write_pgn__listofmoves():
      duplicated final line
      (task-202)
    
    * tests: 22 tests ok out of 22.

[DONE] task-201

(cwc_default.py): cwc_default.py knows how to write a .pgn file

    * (cwc_default.py): cwc_default.py knows how to write a .pgn file
      (task-201)
    * ChessBoard.set_startpos(), ChessGame.write_pgn__listofmoves(), ChessGame.write_pgn()
      (task-201)

    * tests: 11 tests ok out of 11.
    * Pylint: 10/10

[DONE] task-200

(cwc_default.py): Removed useless .pieces attribute from ChessGameStatus.

    * (cwc_default.py): Removed useless .pieces attribute from ChessGameStatus
      (task-200)
    * fixed a typo in ROADMAP.md about task-199
    
    * tests: 11 tests ok out of 11.
    * Pylint: 10/10

[DONE] task-199

(cwc_default.py): two new tests (namely CWCPgnreader.test_game10pgn() and
                  CWCPgnreader.test_game11pgn()) to check if the PGN
                  reader knows how to handle long algebric notation.

    * (cwc_default.py): two new tests (namely CWCPgnreader.test_game10pgn() and
                        CWCPgnreader.test_game11pgn()) to check if the PGN
                        reader knows how to handle long algebric notation
                        (task-199)

    * tests: 11 tests ok out of 11.
    * Pylint: 10/10

[DONE] task-198

(cwc_default.py) 'get_unicode' > 'human_repr' (task-198);
                 removed useless ChessPlayer class and 
                 .white_player/.black_player attributes
                 from ChessGame.

    * (cwc_default.py) 'get_unicode' > 'human_repr' (task-198);
                       removed useless ChessPlayer class and 
                       .white_player/.black_player attributes
                       from ChessGame (task-198)

    * tests: 9 tests ok out of 9.
    * Pylint: 10/10

[DONE] task-197

(cwc_default.py): docstrings.

    * (cwc_default.py): docstrings (task-197)

    * tests: 9 tests ok out of 9.
    * Pylint: 10/10

[DONE] task-196

(cwc_default.py): no more NotImplemetedError; docstrings; no more ChessResult class

    * (cwc_default.py): no more NotImplemetedError; docstrings; 
                        no more ChessResult class (task-196)
    * tests: 9 tests ok out of 9.

[DONE] task-195

(cwc_default.py) x, y > xy

    * (cwc_default.py) x, y > xy
    * tests: 9 tests ok out of 9.

[DONE] task-194

'gameboard' > 'board'; no more TODOs

    * 'gameboard' > 'board'; no more TODOs (task-194)
    * tests: 9 tests ok out of 9.

[DONE] task-193

tests; new directories: tests/, wisteria/cwc/pgnreader; new script: tests.sh

    * tests; new directories: tests/, wisteria/cwc/pgnreader; new script: tests.sh
      (task-193)

[DONE] task-192

cwc_default.py knows how to read 6 different .pgn games.

    * cwc_default.py knows how to read 6 different .pgn games (task-192)

[DONE] task-191

Working on cwc_default.py: the code can read one .pgn file.
No en passant, no promotion.

    * working on cwc_default.py: the code can read one .pgn file
      No en passant, no promotion. (task-191)

[DONE] task-190

Working on cwc_default.py.

    * cwc_default.py: methods are now sorted by name (task-190)
    * cwc_default.py: better .pgn tags storage (task-190)

[DONE] task-189

First try to code a PGN reader/writer* as 'cwc_default'.
(*) https://fr.wikipedia.org/wiki/Portable_Game_Notation

    * first try to code a PGN reader/writer as 'cwc_default' (task-189)
    * new directory: wisteria/cwc (task-189)

[DONE] v. 0.1.4

Graphs with gradients, bugfix & documentation.


bugs:

    * bugfix: modified the way 'wmi' is required in pyproject.toml (task-185)
    
code quality

    * Pylint: 10/10

interface

    * improved message displayed when there's no command line argument 
      (task-186)
    * graphs with gradients (task-187) thanks to a new file, matplotgraphs.py.
      (task-187)
    * improved documentation and messages: no more 'simply' word (task-188)
    * improved documentation in README.md (task-188)
    * improved poetry_show_tree.sh: version "poetry_show_tree.sh v.7/2021-10-14"
      This version adds backquotes to format the text to be correctly displayed by GitHub.
      (task-188)

tasks:

    * task(s): task-185, task-186, task-187, task-188
    
version

    * set version to 0.1.3

```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.12.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ check_tools.sh

Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
pylint 2.11.1
astroid 2.8.2
Python 3.9.7 (default, Aug 31 2021, 13:28:12)
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```


[DONE] task-188

Documentation.

    * improved documentation and messages: no more 'simply' word (task-188)
    * improved documentation in README.md (task-188)
    * improved poetry_show_tree.sh: version "poetry_show_tree.sh v.7/2021-10-14"
      This version adds backquotes to format the text to be correctly displayed by GitHub.
      (task-188)
    
    * Pylint: 10/10

[DONE] task-187

Graphs with gradients.

    * graphs with gradients (task-187) thanks to a new file, matplotgraphs.py.
      (task-187)

    * Pylint: 10/10

[DONE] task-186

Improved message displayed when there's no command line argument.

    * improved message displayed when there's no command line argument 
      (task-186)

    * Pylint: 10/10

[DONE] task-185

Bugfix: modified the way 'wmi' is required in pyproject.toml.

    * bugfix: modified the way 'wmi' is required in pyproject.toml (task-185)
    
    * set version to '0.1.4rc2'

    * Pylint: 10/10

[DONE] v. 0.1.3

Wisteria can be executed on Linux & Windows systems; wim is now a dependency
for Windows systems.

We import a minimum of packages so that the user can see the --help message
even if some required package(s) are missing.


bugs:

    * bug: in total_mem_usage(), ERRORID028 > ERRORID025 (duplicated error number).
      (task-169)
    * bugfix: missing 'f' prefix in a f-string in win_memory() (task-174)
    * bugfix: PLATFORM_SYSTEM is now correctly read in report.py (task-174)
    * bug: fixed output message in report_section_c2c__allvsall()
      (task-176)
    * fixed a minor bug in report(): removed useless f- prefix before a string
      (task-180)
  
code quality

    * added a blank line at the end of the A1, D1a and D1b report sections (task-173)

    * Pylint: 10/10

code structure

    * fixed shebang in .py files: 'python3.9' > 'python3' (task-165, task-166)
    * we import a minimum of packages so that the user can show the --help message
      even if some required package(s) are missing (task-168)
    * --help message completed by help_helpcommandlineargument() (task-168)
    * STR2REPORTSECTION_KEYS contains the keys of STR2REPORTSECTION,
      and vice-versa (task-168)
    * check_str2reportsection_keys() checks if STR2REPORTSECTION_KEYS contains
      the keys of STR2REPORTSECTION, and vice-versa (task-168)
    * utils.py:get_missing_required_modules() gives the list of the
      missing required modules (task-168)
    * wisteria can be executed on Linux & Windows systems (task-173)
    * PLATFORM_SYSTEM is variable defined globs.py (task-173)
    * new aspect method, namely aspect_exaequo_hall() (task-178)
    * 'halloffame' > 'hall' (task-178)
    * all exceptions messages are now formatted with aspect_error()
      (task-180)
    * new aspect_xxx method: aspect_error() (task-180)
    * mymachine() has now (int)'detailslevel' as unique argument (task-181)
    * moved some parts of the code in a unique function
      (report_projectversion()) (task-182)
    * new aspect function, namely report_projectversion() (task-182)
    * 'aspect_' > '_fmt' and wisteria/reportaspect.py > wisteria/reprfmt.py
      (task-183)
    * added `wim` as a dependency for Windows systems (task-184)
    
documentation

    * improved SerializationResults docstring (task-167)
    * updated pimydoc: new exit codes (task-168)
    * improved documentation: no more TODOs (task-168)
    * improved documentation in utils.py: no third-party libraries in this file!
      (task-171)
    * improved get_missing_required_modules() docstring (task-172)
    * updated pimydoc (task-173)
    * updated pimydoc: new code structure (task-174)
    * improved documentation (task-178)
    * improved README.md documentation (task-179)
    * documentation: README.md (task-184)

command line

    * fixed default --report string when no command line arguments are given to
      "titles;A1;B1b;C2c;D1a;" instead of the dumb "titles;A1;B1b;D1a;D1b;D2a;D2b;D2c;"
      (task-173)
    * improved help message for --tolerateabsurdvalues command line option
      (task-179)
    * improved help message for --cfgfile command line argument (task-179)
    * fixed --tolerateabsurdvalues definition ('store' > 'store_true'),
      thus improving --help display (task-179)
    
interface

    * improved graph title in report_section_graphs(): "Speed" > "Slowness"
      (task-170)
    * added debug messages to init_serializers(), describing what has been
      imported/not imported (task-172)
    * improved message displayed in B/04 step: a 'f' prefix has been forgotten
      in a f-string (task-173)
    * improved aspect_mem_usage() output by changing all the thresholds
      to 0, 120000, 120000000, 120000000000, ... (task-175)
    * improved message in step "a special case: if no argument " \
      "has been given, we modify the output" (task-177)
    * improved report_section_c2c__allvsall() output by adding some calls
      to aspect_exaequoxxx() methods (task-178)
    * improved message displayed by help_graphsfilenames(): added a space
      before '(' (task-179)
    * improved error message in report(): ((...)) > (...) (task-179)
    * improved A1 report section output: platform system, serializers and
      data objects (task-181)

tasks:

    * task(s): task-165, task-166, task-167, task-168, task-169, task-170,
               task-171, task-172, task-173, task-174, task-175, task-176,
               task-177, task-178, task-179, task-180, task-181, task-182,
               task-183, task-184
               
version

    * set version to 0.1.3

```
$ poetry show --tree (thanks to ./poetry_show_tree.sh)

psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.12.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
wim 0.2.1 wim is a command line tool to create Web images.
├── click 3.3
└── pillow 2.7.0
```

```
$ check_tools.sh

Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
pylint 2.11.1
astroid 2.8.2
Python 3.9.7 (default, Aug 31 2021, 13:28:12)
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-184

Documentation: README.md; wim is now a dependency for Windows systems.

    * documentation: README.md (task-184)
    * added `wim` as a dependency for Windows systems (task-184)

    * Pylint: 10/10

[DONE] task-183

'aspect_' > '_fmt' and wisteria/reportaspect.py > wisteria/reprfmt.py

    * 'aspect_' > '_fmt' and wisteria/reportaspect.py > wisteria/reprfmt.py
      (task-183)

    * Pylint: 10/10

[DONE] task-182

Moved some parts of the code in a unique function (report_projectversion()).

    * moved some parts of the code in a unique function
      (report_projectversion()) (task-182)
    * new aspect function, namely report_projectversion() (task-182)

    * Pylint: 10/10

[DONE] task-181

Improved A1 report section output: platform system, serializers and data objects.

    * improved A1 report section output: platform system, serializers and
      data objects (task-181)
    * mymachine() has now (int)'detailslevel' as unique argument (task-181)

    * Pylint: 10/10

[DONE] task-180

All exceptions messages are now formatted with aspect_error().

    * all exceptions messages are now formatted with aspect_error()
      (task-180)
    * fixed a minor bug in report(): removed useless f- prefix before a string
      (task-180)
    * new aspect_xxx method: aspect_error() (task-180)

    * Pylint: 10/10

[DONE] task-179

README.md documentation; improved displayed messages.

    * improved README.md documentation (task-179)
    * improved help message for --tolerateabsurdvalues command line option
      (task-179)
    * improved message displayed by help_graphsfilenames(): added a space
      before '(' (task-179)
    * improved error message in report(): ((...)) > (...) (task-179)
    * improved help message for --cfgfile command line argument (task-179)
    * fixed --tolerateabsurdvalues definition ('store' > 'store_true'),
      thus improving --help display (task-179)

    * Pylint: 10/10

[DONE] task-178

Improved report_section_c2c__allvsall() output by adding some calls
to aspect_exaequoxxx() methods.

    * improved report_section_c2c__allvsall() output by adding some calls
      to aspect_exaequoxxx() methods (task-178)
    * new aspect method, namely aspect_exaequo_hall() (task-178)
    * improved documentation (task-178)
    * 'halloffame' > 'hall' (task-178)

    * Pylint: 10/10

[DONE] task-177

Improved message in step:
  (B/04) a special case: if no argument has been given, we modify the output

    * improved message in step "a special case: if no argument " \
      "has been given, we modify the output" (task-177)

    * Pylint: 10/10

[DONE] task-176

bug: fixed output message in report_section_c2c__allvsall().

    * bug: fixed output message in report_section_c2c__allvsall()
      (task-176)

    * Pylint: 10/10

[DONE] task-175

Improved aspect_mem_usage() output.

    * improved aspect_mem_usage() output by changing all the thresholds
      to 0, 120000, 120000000, 120000000000, ... (task-175)

    * Pylint: 10/10

[DONE] task-174

bugfix: missing 'f' prefix in a f-string in win_memory().
bugfix: PLATFORM_SYSTEM is now correctly read in report.py (task-174)

    * bugfix: missing 'f' prefix in a f-string in win_memory() (task-174)
    * bugfix: PLATFORM_SYSTEM is now correctly read in report.py (task-174)
    * updated pimydoc: new code structure (task-174)

    * Pylint: 10/10

[DONE] task-173

Wisteria can be executed on Linux & Windows systems.

    * wisteria can be executed on Linux & Windows systems (task-173)
    * PLATFORM_SYSTEM is variable defined globs.py (task-173)
    * improved message displayed in B/04 step: a 'f' prefix has been forgotten
      in a f-string (task-173)
    * updated pimydoc (task-173)
    * added a blank line at the end of the A1, D1a and D1b report sections (task-173)
    * fixed default --report string when no command line arguments are given to
      "titles;A1;B1b;C2c;D1a;" instead of the dumb "titles;A1;B1b;D1a;D1b;D2a;D2b;D2c;"
      (task-173)

    * Pylint: 10/10

[DONE] task-172

Added debug messages to init_serializers(), describing what has been
imported/not imported.

    * added debug messages to init_serializers(), describing what has been
      imported/not imported (task-172)
    * improved get_missing_required_modules() docstring (task-172)

    * Pylint: 10/10

[DONE] task-171

Improved documentation in utils.py: no third-party libraries in this file!

    * improved documentation in utils.py: no third-party libraries in this file!
      (task-171)

    * Pylint: 10/10

[DONE] task-170

Improved graph title in report_section_graphs(): "Speed" > "Slowness".

    * improved graph title in report_section_graphs(): "Speed" > "Slowness"
      (task-170)

    * Pylint: 10/10

[DONE] task-169

bug: in total_mem_usage(), ERRORID028 > ERRORID025 (duplicated error number).

    * bug: in total_mem_usage(), ERRORID028 > ERRORID025 (duplicated error number).
      (task-169)

    * Pylint: 10/10

[DONE] task-168

We import a minimum of packages so that the user can see the --help message
even if some required package(s) are missing.

    * we import a minimum of packages so that the user can show the --help message
      even if some required package(s) are missing (task-168)
    * updated pimydoc: new exit codes (task-168)
    * improved documentation: no more TODOs (task-168)
    * --help message completed by help_helpcommandlineargument() (task-168)
    * STR2REPORTSECTION_KEYS contains the keys of STR2REPORTSECTION,
      and vice-versa (task-168)
    * check_str2reportsection_keys() checks if STR2REPORTSECTION_KEYS contains
      the keys of STR2REPORTSECTION, and vice-versa (task-168)
    * utils.py:get_missing_required_modules() gives the list of the
      missing required modules (task-168)

    * Pylint: 10/10

[DONE] task-167

Improved SerializationResults docstring.

    * improved SerializationResults docstring (task-167)

    * Pylint: 10/10

[DONE] task-166

Fixed sheband in ./bin/wisteria: '#!/usr/bin/env python3.9'
> '#!/usr/bin/env python3' .

    * fixed sheband in ./bin/wisteria: '#!/usr/bin/env python3.9'
      > '#!/usr/bin/env python3' (task-166)

    * set version to "0.1.3rc2"

    * Pylint: 10/10

[DONE] task-165

Fixed shebang in .py files: 'python3.9' > 'python3'.

    * fixed shebang in .py files: 'python3.9' > 'python3' (task-165)

    * set version to "0.1.3pre1"

    * Pylint: 10/10

[DONE] v. 0.1.2

Removed everything that concerned the 'memory double check'.
In `pyproject.toml`, python = "^3.8".

bug

    * bug: in report_section_graphs(), msgdebug() is now called only in debug
      mode, if verbosity is set to VERBOSITY_DEBUG (task-164)

code structure

    * removed everything that concerned the 'memory double check',
      including doublecheck_memusage.sh script.
      (task-161)
    * in `pyproject.toml`, python = "^3.8" (task-162)
    * added `memoveruse_cpp/libmemoveruse_cpp.so`, a forgotten file
      (task-163)
    * modified `.gitignore` to include .so files (task-163)

version

    * set version to '0.1.2'

tasks

    * task(s): task-161, task-162, task-163, task-164

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
$ check_tools.sh

Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
pylint 2.11.1
astroid 2.8.2
Python 3.9.7 (default, Aug 31 2021, 13:28:12)
[GCC 11.1.0]
* about pipdeptree:
2.0.0
* about pimydoc:
Pimydoc v. 0.2.9
* about readmemd2txt:
readmemd2txt: 0.0.5
```

[DONE] task-164

Bug: in report_section_graphs(), msgdebug() is now called only in debug
     mode, if verbosity is set to VERBOSITY_DEBUG.

    * bug: in report_section_graphs(), msgdebug() is now called only in debug
      mode, if verbosity is set to VERBOSITY_DEBUG (task-164)

    * Pylint: 10/10

[DONE] task-163

Added `memoveruse_cpp/libmemoveruse_cpp.so`, a forgotten file.

    * added `memoveruse_cpp/libmemoveruse_cpp.so`, a forgotten file
      (task-163)
    * modified `.gitignore` to include .so files (task-163)

    * Pylint: 10/10

[DONE] task-162

In `pyproject.toml`, python = "^3.8".

    * in `pyproject.toml`, python = "^3.8" (task-162)

    * Pylint: 10/10

[DONE] task-161

Removed everything that concerned the 'memory double check'.

    * removed everything that concerned the 'memory double check',
      including doublecheck_memusage.sh script.
      (task-161)

    * Pylint: 10/10

[DONE] v. 0.1.1

'graphs' in reports.

bugs

    * Bug: report_section_graphs() has to stop if matplotlib package is
      not installed (task-157)

code structure

    * 'graphs' is now one of the REPORTS sections
      new report function: report_section_graphs() (task-154)
    * new file: wisteria/helpmsg.py and its unique function, help_graphsfilenames()
      (task-159)

code quality

    * Pylint: 10/10

interface

    * improved output message in partial_report__serializers(): removed useless
      blank line (task-154)
    * updated pimydoc: 'graphs' is now a report section (task-154)
    * checkup() now says if it's possible to draw graphs (task-154)
    * improved checkup() output: what would be the graphs filenames?
      (task-155)
    * added to report_section_graphs() debug message, namely graph filenames.
      (task-156)
    * improved error message in report_section_graphs() (task-157)
    * improved report_section_c2a() output: table title 'memory' > 'Memory'
      (task-158)
    * improved --help and --checkup messages by showing graphs filenames
      (task-159)
    * improved --memoveruse help message ('Python+C++' > 'Python/C++')
      (task-160)

tasks

    * task(s): task-154, task-155, task-156, task-157, task-158,
               task-159, task-160

version

    * set version to '0.1.1'

```
$ poetry show --tree

cppyy 2.1.0 Cling-based Python-C++ bindings
├── cppyy-backend 1.14.6
│   └── cppyy-cling >=6.25.1
├── cppyy-cling 6.25.1
└── cpycppyy 1.12.7
    ├── cppyy-backend >=1.14.6
    │   └── cppyy-cling >=6.25.1
    └── cppyy-cling >=6.25.1 (circular dependency aborted here)
psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.11.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
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

[DONE] task-160

Improved --memoveruse help message.

    * improved --memoveruse help message ('Python+C++' > 'Python/C++')
      (task-160)

    * Pylint: 10/10

[DONE] task-159

Improved --help and --checkup messages.

    * improved --help and --checkup messages by showing graphs filenames
      (task-159)
    * new file: wisteria/helpmsg.py and its unique function, help_graphsfilenames()
      (task-159)

    * Pylint: 10/10

[DONE] task-158

Improved report_section_c2a() output.

    * improved report_section_c2a() output: table title 'memory' > 'Memory'
      (task-158)

    * Pylint: 10/10

[DONE] task-157

Bug: report_section_graphs() has to stop if no matplotlib package.

    * Bug: report_section_graphs() has to stop if matplotlib package is
      not installed (task-157)
    * improved error message in report_section_graphs() (task-157)

    * Pylint: 10/10

[DONE] task-156

Added to report_section_graphs() debug message.

    * added to report_section_graphs() debug message, namely graph filenames.
      (task-156)

    * Pylint: 10/10

[DONE] task-155

Improved checkup() output.

    * improved checkup() output: what would be the graphs filenames?
      (task-155)

    * Pylint: 10/10

[DONE] task-154

'graphs' in reports.

    * 'graphs' is now one of the REPORTS sections
      new report function: report_section_graphs() (task-154)
    * improved output message in partial_report__serializers(): removed useless
      blank line (task-154)
    * updated pimydoc: 'graphs' is now a report section (task-154)
    * checkup() now says if it's possible to draw graphs (task-154)

    * Pylint: 10/10

[DONE] v. 0.1

--memoveruse command line argument
--mute command line argument; 'none' is a new --report shortcut;
Memory usage is now checked and displayed in reports.
New script (doublecheck_memusage.sh) used to check if memory allocation
is correctly detected by valgrind.


bugs

    * bugfix: if mem usage is 0, no more exception (ZeroDivisionError) in report.
      (task-146)

command line

    * --memoveruse command line argument; results func() knows how to alloc
      extra memory when "Python" is in --memoveruse (task-136)
    * --mute command line argumet; 'none' is a new --report shortcut;
      (task-138)
    * added default value to --checkup and --mymachine command line
      argument definitions (task-138)

code quality

    * Pylint: 10/10

code structure

    * add cppyy to projects' dependencies (task-137)
    * (--memoveruse); results' func() know how to alloc extra memory
      when "C++" is in --memoveruse (task-137)
    * new directory: memoverabuse_cpp/ (task-137)
    * new key in UNITS: UNITS['memory'] (task-142)
    * new function: aspect_mem_usage() (task-142)
    * split report_section_c2c() in 3 sub methods, namely
      report_section_c2c__allvsall, report_section_c2c__serializervsall,
      and report_section_c2c__serializervsserializer (task-142)
    * removed useless bunch of code (2x TODOs) (task-142)
    * new method: SerializationResults.total_mem_usage() (task-142)
    * memory usage is now checked and displayed in reports
      using the `resource.getrusage(resource.RUSAGE_SELF).ru_maxrss`
      mechanism (task-142)
    * new variable in globs.py: DEFAULT_LOGFILE_NAME, replacing
      old 'report.txt' occurences (task-143)
    * 'DEFAULT_LOGFILE_NAME' > 'LOGFILE_NAME' (task-145)
    * added a missing blank line in report.py (task-145)
    * added a shebang line to memoveruse_cpp/compile.sh (task-147)
    * improved humanratio() output: numbers that aren't a ratio may be
      formatted through the <numbersformat> argument (task-149)
    * new method: SerializationResults.get_serializers_whose_overallscore_is()
    * new aspect function: aspect_exaequowith() (task-150)
    * improved code in report_section_c2c__serializervsall() by replacing a
      call to `len(results.serializers)` by `results.serializers_number`, the
      result being already computed (task-151)
    * new script (doublecheck_memusage.sh) used to check if memory allocation
      is correctly detected by valgrind (task-153)
    * Python memoryoveruse is now 1 Mo (task-153)
    * C++ memoryoveruse is now 3 Mo (task-153)

documentation

    * improved documentation (task-136, task-137, task-138, task-142, task-144,
      task-150)
    * updated pimydoc (D1a and D1b titles) (task-148)

interface, output messages

    * if verbosity is set to minimal, no progress bar. It's important for scripts
      calling this project from the outside (task-135)
    * new debug message (displayed when verbosity is set to VERBOSITY_DEBUG)
      describing the content of --memoveruse. (task-136)
    * reports: no more base100 (task-140)
    * improved TextAndNotes.output() output message (task-142)
    * improved A1 report section: report_section_a1()
      now displays --cmp & --report content. (task-144)
    * improved output message from TextAndNotes.output()
    * improved titles in reports (D1a and D1b)
      (task-148)
    * improved message in report section C2c (report_section_c2c__serializervsall())
      by using the new aspect_exaequowith() function (task-150)
    * improved output messages: 'Encod.<>Decod.' > 'Reversibility' or 'Coverage rate'.
      (task-152)

tasks:

    * task(s) : task-135, task-136, task-137, task-138, task-139, task-140,
                task-141, task-142, task-143, task-144, task-145, task-146,
                task-147, task-148, task-149, task-150, task-151, task-152,
                task-153

version:

    * version set to '0.1'

```
$ poetry show --tree

cppyy 2.1.0 Cling-based Python-C++ bindings
├── cppyy-backend 1.14.6
│   └── cppyy-cling >=6.25.1
├── cppyy-cling 6.25.1
└── cpycppyy 1.12.7
    ├── cppyy-backend >=1.14.6
    │   └── cppyy-cling >=6.25.1
    └── cppyy-cling >=6.25.1 (circular dependency aborted here)
psutil 5.8.0 Cross-platform lib for process and system monitoring in Python.
py-cpuinfo 8.0.0 Get CPU info with pure Python 2 & 3
rich 10.11.0 Render rich text, tables, progress bars, syntax highlighting, markdown and more to the terminal
├── colorama >=0.4.0,<0.5.0
├── commonmark >=0.9.0,<0.10.0
└── pygments >=2.6.0,<3.0.0
```

```
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
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

[DONE] task-153

New script (doublecheck_memusage.sh) used to check if memory allocation
is correctly detected by valgrind.

    * new script (doublecheck_memusage.sh) used to check if memory allocation
      is correctly detected by valgrind (task-153)
    * Python memoryoveruse is now 1 Mo (task-153)
    * C++ memoryoveruse is now 3 Mo (task-153)

    * Pylint: 10/10

[DONE] task-152

Improved output messages: 'Encod.<>Decod.' > 'Reversibility' or 'Coverage rate'.

    * improved output messages: 'Encod.<>Decod.' > 'Reversibility' or 'Coverage rate'.
      (task-152)

    * Pylint: 10/10

[DONE] task-151

Improved code in report_section_c2c__serializervsall() by replacing a
call to `len(results.serializers)` by `results.serializers_number`, the
result being already computed.

    * improved code in report_section_c2c__serializervsall() by replacing a
      call to `len(results.serializers)` by `results.serializers_number`, the
      result being already computed (task-151)

    * Pylint: 10/10

[DONE] task-150

Improved message in report section C2c (report_section_c2c__serializervsall())
by using the new aspect_exaequowith() function.

    * improved message in report section C2c (report_section_c2c__serializervsall())
      by using the new aspect_exaequowith() function (task-150)
    * new method: SerializationResults.get_serializers_whose_overallscore_is()
    * new aspect function: aspect_exaequowith() (task-150)
    * improved documentation (task-150)

    * Pylint: 10/10

[DONE] task-149

Improved humanratio() output: numbers that aren't a ratio may be
formatted trough the <numbersformat> argument.

    * improved humanratio() output: numbers that aren't a ratio may be
      formatted through the <numbersformat> argument (task-149)

    * Pylint: 10/10

[DONE] task-148

Improved titles in reports (D1a and D1b).

    * improved titles in reports (D1a and D1b)
      (task-148)
    * updated pimydoc (D1a and D1b titles) (task-148)

    * Pylint: 10/10

[DONE] task-147

Added a shebang line to memoveruse_cpp/compile.sh.

    * added a shebang line to memoveruse_cpp/compile.sh (task-147)

    * Pylint 10/10

[DONE] task-146

Bugfix: if mem usage is 0, no more exception (ZeroDivisionError) in report.

    * bugfix: if mem usage is 0, no more exception (ZeroDivisionError) in report.
      (task-146)
    * improved output message from TextAndNotes.output()

    * Pylint 10/10

[DONE] task-145

'DEFAULT_LOGFILE_NAME' > 'LOGFILE_NAME'

    * 'DEFAULT_LOGFILE_NAME' > 'LOGFILE_NAME' (task-145)
    * added a missing blank line in report.py (task-145)

    * Pylint: 10/10

[DONE] task-144

Improved A1 report section.

    * improved A1 report section: report_section_a1()
      now displays --cmp & --report content. (task-144)
    * updated pimydoc (task-144)

    * Pylint: 10/10

[DONE] task-143

New variable in globs.py: DEFAULT_LOGFILE_NAME, replacing
old 'report.txt' occurences.

    * new variable in globs.py: DEFAULT_LOGFILE_NAME, replacing
      old 'report.txt' occurences (task-143)

    * Pylint (10/10)

[DONE] task-142

Memory usage is now checked and displayed in reports.

    * memory usage is now checked and displayed in reports
      using the `resource.getrusage(resource.RUSAGE_SELF).ru_maxrss`
      mechanism (task-142)
    * new method: SerializationResults.total_mem_usage() (task-142)
    * removed useless bunch of code (2x TODOs) (task-142)
    * split report_section_c2c() in 3 sub methods, namely
      report_section_c2c__allvsall, report_section_c2c__serializervsall,
      and report_section_c2c__serializervsserializer (task-142)
    * new function: aspect_mem_usage() (task-142)
    * new key in UNITS: UNITS['memory'] (task-142)
    * improved TextAndNotes.output() output message (task-142)
    * improved documentation (task-142)

    * Pylint (10/10)

[DONE] task-141

Renamed reports sections: ancient E* sections > D*, ancient D* sections > C* .

    * renamed reports sections: ancient E* sections > D*, ancient D*
      sections > C* (task-141)

    * Pylint (10/10)

[DONE] task-140

reports: no more base100

    * reports: no more base100 (task-140)

    * Pylint (10/10)

[DONE] task-139

Improved help message for --memoveruse.

    * improved help message for --memoveruse (task-139)

    * Pylint (10/10)

[DONE] task-138

--mute command line argument; 'none' is a new --report shortcut;

    * --mute command line argumet; 'none' is a new --report shortcut;
      (task-138)
    * added default value to --checkup and --mymachine command line
      argument definitions (task-138)
    * improved documentation (task-138)

    * Pylint (10/10)

[DONE] task-137

(--memoveruse); results' func() know how to alloc extra memory
when "C++" is in --memoveruse.

    * (--memoveruse); results' func() know how to alloc extra memory
      when "C++" is in --memoveruse (task-137)
    * add cppyy to projects' dependencies (task-137)
    * new directory: memoverabuse_cpp/ (task-137)
    * improved documentation (task-137)

    * Pylint (10/10)

[DONE] task-136

--memoveruse command line argument; results func() knows how to alloc
extra memory when "Python" is in --memoveruse.

    * --memoveruse command line argument; results func() knows how to alloc
      extra memory when "Python" is in --memoveruse (task-136)
    * new debug message (displayed when verbosity is set to VERBOSITY_DEBUG)
      describing the content of --memoveruse. (task-136)
    * improved documentation (task-136)

    * Pylint: 10/10

[DONE] task-135

If verbosity is set to minimal, no progress bar. It's important for scripts
calling this project from the outside.

    * if verbosity is set to minimal, no progress bar. It's important for scripts
      calling this project from the outside (task-135)

    * Pylint: 10/10

[DONE] v. 0.0.9

* --tolerateabsurdvalues
* 7 serializers: iaswn; json; jsonpickle; jsonpickle_keystrue; marshal; pickle; pyyaml
* documentation, bugfixes


command line

    * new command line argument: --tolerateabsurdvalues (task-124)

serializers

    * new serializers: jsonpickle_keystrue and pyyaml (task-124)

documentation

    * documentation (task-134)

interface

    * improved messages in compute_results() by adding a fingerprint of
      each (serializer, data object) computed (task-124)
    * in debug mode, serializer_xxx() displays a message saying if
      encoding/decoding has failed. (task-124)
    * in compute_results(), serializers and data objects are sorted so that
      every time the program is launched, the output is exactly the same
      (task-124)
    * Improved text displayed in checkup() and otherwise: serializers' version
      doesn't contain character \n anymore. (task-126)
    * improved messages readibility in report_section_d2c() by adding a missing
      space (task-127)
    * improved info message displayed if no argument is passed to the program.
      (task-128)
    * improved error messages in read_cmpstring(): check that serializer1 and
      serializer2 belong to UNAVAILABLE_SERIALIZERS (task-130)
    * improved tables in report.py (task-132)
    * added a column to some tables (B1a B2a C1a) to show fingerprint in debug
      mode (task-133)

bugs

    * fixed a bug in report_section_d2c(): a message couldn't be displayed
      (task-124)
    * bugfix: ERRORID032 was duplicated; in serializer_pyyaml()
      ERRORID032 > ERRORID044 (task-125)
    * fixed a bug in TextAndNotes.output(): notes number are now correct,
      even if the same note is used several times in the text. (task-127)
    * bugfix: report_section_d1a() and report_section_d1b() now strictly check
              that results[serializer][dataobj_name] is not None (task-129)
    * Bugfix: report_xxx() functions now strictly check
      that results[serializer][dataobj_name] is not None (task-131)

code structure

    * improved code structure in compute_results() by adding a subfunction
      named erase_progress_bar() (task-124)
    * in compute_results(), check if an absurd value is computed;
      the function stops if --tolerateabsurdvalues is False (task-124)
    * new exit code: -7 (error, an absurd value has been computed) (task-124)
    * serializer_xxx() functions have a third argument, fingerprint, to help
      debugging. (task-124)
    * new method: TextAndNotes.delete_duplicated_notes() (task-127)
    * new errors: ERRORID045 and ERRORID046 (task-130)
    * err_codes.sh: err_max set to 50 (task-130)

version

    * set version to '0.0.9'

Pylint

    * Pylint: 10/10

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
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
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


[DONE] task-134

Documentation.

    * documentation (task-134)

    * Pylint: 10/10

[DONE] task-133

Added a column to some tables (B1a B2a C1a) to show fingerprint in debug mode.

    * added a column to some tables (B1a B2a C1a) to show fingerprint in debug
      mode (task-133)

    * Pylint: 10/10

[DONE] task-132

Improved tables in report.py.

    * improved tables in report.py (task-132)

    * Pylint: 10/10

[DONE] task-131

Bugfix: report_xxx() functions now strictly check
        that results[serializer][dataobj_name] is not None

    * Bugfix: report_xxx() functions now strictly check
      that results[serializer][dataobj_name] is not None (task-131)

    * Pylint: 10/10

[DONE] task-130

Improved error messages in read_cmpstring(): check that serializer1 and
serializer2 belong to UNAVAILABLE_SERIALIZERS.

    * improved error messages in read_cmpstring(): check that serializer1 and
      serializer2 belong to UNAVAILABLE_SERIALIZERS (task-130)
    * new errors: ERRORID045 and ERRORID046 (task-130)
    * err_codes.sh: err_max set to 50 (task-130)

    * Pylint 10/10

[DONE] task-129

bugfix: report_section_d1a() and report_section_d1b() now strictly check
        that results[serializer][dataobj_name] is not None.

    * bugfix: report_section_d1a() and report_section_d1b() now strictly check
              that results[serializer][dataobj_name] is not None (task-129)

    * Pylint 10/10

[DONE] task-128

Improved info message displayed if no argument is passed to the program.

    * improved info message displayed if no argument is passed to the program.
      (task-128)

    * Pylint 10/10

[TODO] task-127

Fixed a bug in TextAndNotes.output(): notes' numbers are now correct,
even if the same note is used several times in the text.

    * fixed a bug in TextAndNotes.output(): notes number are now correct,
      even if the same note is used several times in the text. (task-127)
    * new method: TextAndNotes.delete_duplicated_notes() (task-127)
    * improved messages readibility in report_section_d2c() by adding a missing
      space (task-127)

    * Pylint 10/10

[DONE] task-126

Improved text displayed in checkup() and otherwise: serializers' version
doesn't contain character \n anymore.

    * Improved text displayed in checkup() and otherwise: serializers' version
      doesn't contain character \n anymore. (task-126)

    * Pylint 10/10

[TODO] task-125

bugfix: ERRORID032 was duplicated; in serializer_pyyaml() ERRORID032 > ERRORID044

    * bugfix: ERRORID032 was duplicated; in serializer_pyyaml()
      ERRORID032 > ERRORID044 (task-125)

    * Pylint 10/10

[DONE] task-124

new serializers: jsonpickle_keystrue and pyyaml; --tolerateabsurdvalues

    * new serializers: jsonpickle_keystrue and pyyaml (task-124)
    * in compute_results(), serializers and data objects are sorted so that
      every time the program is launched, the output is exactly the same
      (task-124)
    * fixed a bug in report_section_d2c(): a message couldn't be displayed
      (task-124)
    * improved messages in compute_results() by adding a fingerprint of
      each (serializer, data object) computed (task-124)
    * improved code structure in compute_results() by adding a subfunction
      named erase_progress_bar() (task-124)
    * in compute_results(), check if an absurd value is computed;
      the function stops if --tolerateabsurdvalues is False (task-124)
    * new command line argument: --tolerateabsurdvalues (task-124)
    * new exit code: -7 (error, an absurd value has been computed) (task-124)
    * serializer_xxx() functions have a third argument, fingerprint, to help
      debugging. (task-124)
    * in debug mode, serializer_xxx() displays a message saying if
      encoding/decoding has failed. (task-124)

    * Pylint 10/10

[DONE] v. 0.0.8

Improved data object support (113 data objects are now defined, see infra).
Unavailable data are now stored in globs.py:UNAVAILABLE_DATA variable.
Improved messages and documentation.

113 data objects are now defined:
```
array(b); array(b/empty); array(b_unsigned); array(b_unsigned/empty);
array(d); array(d/empty); array(f); array(f/empty); array(h);
array(h/empty); array(h_unsigned); array(h_unsigned/empty); array(i);
array(i/empty); array(i_unsigned); array(i_unsigned/empty); array(l);
array(l/empty); array(l_unsigned); array(l_unsigned/empty); array(q);
array(q/empty); array(q_unsigned); array(q_unsigned/empty); array(u);
array(u/empty); bool/false; bool/true; bytearray; bytearray(empty);
bytes; bytes(empty); calendar(calendar(3)); collections.chainmap;
collections.chainmap(empty); collections.counter;
collections.counter(empty); collections.defaultdict;
collections.defaultdict(empty); collections.deque;
collections.deque(empty); collections.ordereddict;
collections.ordereddict(empty); complex; datetime(datetime.datetime);
datetime(datetime.timedelta); dateutil(parser.parse);
decimal(+infinity); decimal(-infinity); decimal(0.5); decimal(1/7);
decimal(nan); dict(keys/bool); dict(keys/float); dict(keys/int);
dict(keys/str); dict(keys/str+subdicts); file descriptor; float;
float(nan); frozenset; frozenset(empty); function; function(python);
hashlib(hashlib.sha1); hashlib(hashlib.sha224);
hashlib(hashlib.sha256); hashlib(hashlib.sha384);
hashlib(hashlib.sha512); imported module; imported module(class);
imported module(function); int; io.string; io.string(empty); list;
list(+sublists); list(empty); memoryview; metaclass; none;
notimplemented; numbers(complex); numbers(integral); numbers(numbers);
numbers(real); pythonexception typeerror; range; range(empty);
re.match; re.match(+flags); re.pattern(bytes); re.pattern(str);
regularclass; regularclass(async_method); regularclass(class_method);
regularclass(generator); regularclass(method);
regularclass(static_method); regularclassinheriteddict;
regularclassinheritedlist; set; set(empty); str; str(empty);
str(long); str(non ascii characters); time(time.time); tuple;
tuple(+subtuples); tuple(empty); type(str); type(type(str))
```


data

    * added new data. (task-104)
    * improved data objects order in DATA (task-107)
    * bugfix: fixed data object "bool/false" definition in data.py (task-110)
    * check that DATA keys are written in lower case (task-113)
    * check that UNAVAILABLE_DATA keys are written in lower case (task-113)
    * new errors: ERRORID035, ERRORID036 (task-113)
    * fixed data objects names using upper letter case in DATA (task-114)
    * added checks to read_cfgfile(): are all DATA/UNAVAILABLE_DATA keys defined
      in the configuration file, and vice-versa ? (task-115)
    * fixed inconsistencies among data object names in data.py and in config
      file (task-119)
    * added numerous data objects. (task-120)
    * added numerous data objects (task-121)
    * check that there's no key defined DATA that is also defined in
      UNAVAILABLE_DATA, and vice-versa (task-123)

code structure

    * rewrote how checkup() displays the serializers and the data objects (task-91)
    * modified data.py:init_data() so that this functions stores in
      UNAVAILABLE_DATA the data objects that can't be used (task-91)
    * globs.py:UNAVAILABLE_DATA stores the data objects that can't be used (task-91)
    * .available is not an attribute of SerializerData anymore (task-93)
    * SerializerData has now a new attribute, .modulename (task-93)
    * modified init_serializers() so that serializers that can't be used
      are stored in globs.py:UNAVAILABLE_SERIALIZERS (task-93)
    * new aspect_xxx() method: aspect_serializer0(); aspect_serializer()
      is now based on it. (task-93)
    * globs.py:UNAVAILABLE_SERIALIZERS now contains serializers that can't be
      used. (task-93)
    * new aspect method: aspect_nounplural() (task-98)
    * replaced some doubloons in code by two fonctions, partial_report__data()
      and partial_report__serializers() (task-99)
    * err_codes.sh: max_index set to 45 (task-117)
    * new file: classesexamples/simpleclasses.py (task-121)

messages, interface

    * fixed a typo: 'extremly' > 'extremely' (task-92)
    * If no argument has been given on the command line, we modify the output
      to help the user (verbosity and report). (task-94)
    * fixed a color problem in report_section_d2c() (task-95)
    * improved the message displayed by checkup() : .internet string
      displayed for unavailable serializer (task-96)
    * improved error messages in read_cmpstring(); improved message in checkup()
      (task-97)
    * improved messages in read_cmpstring() and in checkup() (task-98)
    * improved checkup() display by adding project's name & version and the current
      timestamp. (task-102)
    * slightly improved messages displayed by the program: '}.' > '} .'
      (task-103)
    * improved msgerror(): error id is now displayed in red. (task-105)
    * modified checkup() so that, if verbosity==3, it displays all serializers and all
      data objects (unavailable+available). (data-106)
    * improved checkup() message by adding Python version (task-108)
    * improved debug message displayed by wisteria.py at the beginning of
      the program by adding Python version (task-109)
    * improved message display in partial_report__data(): we use '!'
      as prefix for unavailable serializers and data. (task-111)
    * improved messages in checkup() by adding colors and improving text
      (task-112)
    * improved message in report_section_d2c() (task-116)
    * removed useless duplicate ERRORID string in checkup() messages
      (task-118)
    * improved message in checkup(): total of serialiers/data objects
      is now displayed for debug message. (task-122)

documentation & code readibility

    * rewrote the sections' numbers of wisteria.py: no more '09bis' (task-91)
    * documentation in reportaspect.py  (task-100)
    * improved code readibility by adding a parameter to aspect_list(, func),
      func() being called on each item inserted in the result string. (task-101)
    * fix some glitches in ROADMAP.md
    * improved checkup doc. (data-106)
    * documentation in README.md (task-107)
    * added a blank line in report.py (task-107)
    * improved documentation (task-114)
    * improved comments in checkup() (task-115)
    * improved comments in read_cfgfile() (task-115)

Pylint

    * Pylint 10/10

tasks

    * task(s): task-91, task-92, task-93, task-94, task-95
               task-96, task-97, task-98, task-99, task-100,
               task-101, task-102, task-103, task-104, task-105,
               task-106, task-107, task-108, task-109, task-110

version

    * set version to 0.0.8

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
$ check_tools.sh

* about poetry:
Poetry version 1.1.11
* about shellcheck:
ShellCheck - shell script analysis tool
version: 0.7.2
license: GNU General Public License, version 3
website: https://www.shellcheck.net
* about pycodestyle:
2.7.0
* about pylint:
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


[DONE] task-123

Check that there's no key defined DATA that is also defined in
UNAVAILABLE_DATA, and vice-versa.

    * check that there's no key defined DATA that is also defined in
      UNAVAILABLE_DATA, and vice-versa (task-123)

    * Pylint 10/10

[DONE] task-122

Improved message in checkup().

    * improved message in checkup(): total of serialiers/data objects
      is now displayed for debug message. (task-122)

    * Pylint 10/10

[task-121]

Added numerous data objects.

113 data objects are now defined:
array(b); array(b/empty); array(b_unsigned); array(b_unsigned/empty);
array(d); array(d/empty); array(f); array(f/empty); array(h);
array(h/empty); array(h_unsigned); array(h_unsigned/empty); array(i);
array(i/empty); array(i_unsigned); array(i_unsigned/empty); array(l);
array(l/empty); array(l_unsigned); array(l_unsigned/empty); array(q);
array(q/empty); array(q_unsigned); array(q_unsigned/empty); array(u);
array(u/empty); bool/false; bool/true; bytearray; bytearray(empty);
bytes; bytes(empty); calendar(calendar(3)); collections.chainmap;
collections.chainmap(empty); collections.counter;
collections.counter(empty); collections.defaultdict;
collections.defaultdict(empty); collections.deque;
collections.deque(empty); collections.ordereddict;
collections.ordereddict(empty); complex; datetime(datetime.datetime);
datetime(datetime.timedelta); dateutil(parser.parse);
decimal(+infinity); decimal(-infinity); decimal(0.5); decimal(1/7);
decimal(nan); dict(keys/bool); dict(keys/float); dict(keys/int);
dict(keys/str); dict(keys/str+subdicts); file descriptor; float;
float(nan); frozenset; frozenset(empty); function; function(python);
hashlib(hashlib.sha1); hashlib(hashlib.sha224);
hashlib(hashlib.sha256); hashlib(hashlib.sha384);
hashlib(hashlib.sha512); imported module; imported module(class);
imported module(function); int; io.string; io.string(empty); list;
list(+sublists); list(empty); memoryview; metaclass; none;
notimplemented; numbers(complex); numbers(integral); numbers(numbers);
numbers(real); pythonexception typeerror; range; range(empty);
re.match; re.match(+flags); re.pattern(bytes); re.pattern(str);
regularclass; regularclass(async_method); regularclass(class_method);
regularclass(generator); regularclass(method);
regularclass(static_method); regularclassinheriteddict;
regularclassinheritedlist; set; set(empty); str; str(empty);
str(long); str(non ascii characters); time(time.time); tuple;
tuple(+subtuples); tuple(empty); type(str); type(type(str))

    * added numerous data objects (task-121)
    * new file: classesexamples/simpleclasses.py (task-121)

    * Pylint 10/10

[DONE] task-120

Added numerous data objects.

104 data objects are now defined, namely:
array(b); array(b/empty); array(b_unsigned); array(b_unsigned/empty);
array(d); array(d/empty); array(f); array(f/empty); array(h);
array(h/empty); array(h_unsigned); array(h_unsigned/empty); array(i);
array(i/empty); array(i_unsigned); array(i_unsigned/empty); array(l);
array(l/empty); array(l_unsigned); array(l_unsigned/empty); array(q);
array(q/empty); array(q_unsigned); array(q_unsigned/empty); array(u);
array(u/empty); bool/false; bool/true; bytearray; bytearray(empty);
bytes; bytes(empty); calendar(calendar(3)); collections.chainmap;
collections.chainmap(empty); collections.counter;
collections.counter(empty); collections.defaultdict;
collections.defaultdict(empty); collections.deque;
collections.deque(empty); collections.ordereddict;
collections.ordereddict(empty); complex; datetime(datetime.datetime);
datetime(datetime.timedelta); dateutil(parser.parse);
decimal(+infinity); decimal(-infinity); decimal(0.5); decimal(1/7);
decimal(nan); dict(keys/bool); dict(keys/float); dict(keys/int);
dict(keys/str); dict(keys/str+subdicts); file descriptor; float;
float(nan); frozenset; frozenset(empty); function; function(python);
hashlib(hashlib.sha1); hashlib(hashlib.sha224);
hashlib(hashlib.sha256); hashlib(hashlib.sha384);
hashlib(hashlib.sha512); imported module; imported module(class);
imported module(function); int; io.string; io.string(empty); list;
list(+sublists); list(empty); memoryview; none; notimplemented;
numbers(complex); numbers(integral); numbers(numbers); numbers(real);
pythonexception typeerror; range; range(empty); re.match;
re.match(+flags); re.pattern(bytes); re.pattern(str); set; set(empty);
str; str(empty); str(long); str(non ascii characters);
time(time.time); tuple; tuple(+subtuples); tuple(empty); type(str);
type(type(str))

    * added numerous data objects. (task-120)

    * Pylint 10/10

[DONE] task-119

Fixed inconsistencies among data object names in data.py and in config file.

    * fixed inconsistencies among data object names in data.py and in config
      file (task-119)

    * Pylint 10/10

[DONE] task-118

Removed useless duplicate ERRORID string in checkup() messages.

    * removed useless duplicate ERRORID string in checkup() messages
      (task-118)

    * Pylint 10/10

[DONE] task-117

err_codes.sh: max_index set to 45.

    * err_codes.sh: max_index set to 45 (task-117)

    * Pylint 10/10

[DONE] task-116

Improved message in report_section_d2c().

    * improved message in report_section_d2c() (task-116)

    * Pylint 10/10

[DONE] task-115

Added checks to read_cfgfile(): are all DATA/UNAVAILABLE_DATA keys defined
in the configuration file, and vice-versa ?

    * added checks to read_cfgfile(): are all DATA/UNAVAILABLE_DATA keys defined
      in the configuration file, and vice-versa ? (task-115)
    * improved comments in checkup() (task-115)
    * improved comments in read_cfgfile() (task-115)

    * Pylint 10/10

[DONE] task-114

Fixed data objects names using upper letter case in DATA.

    * fixed data objects names using upper letter case in DATA (task-114)
    * improved documentation (task-114)

    * Pylint 10/10

[DONE] task-113

Check that DATA and UNAVAILABLE_DATA keys are written in lower case.

    * check that DATA keys are written in lower case (task-113)
    * check that UNAVAILABLE_DATA keys are written in lower case (task-113)
    * new errors: ERRORID035, ERRORID036 (task-113)

    * pylint: 10/10

[DONE] task-112

Improved messages in checkup() by adding colors and improving text.

    * improved messages in checkup() by adding colors and improving text
      (task-112)

    * pylint: 10/10

[DONE] task-111

Improved message display in partial_report__data(): we use '!'
as prefix for unavailable serializers and data.

    * improved message display in partial_report__data(): we use '!'
      as prefix for unavailable serializers and data. (task-111)

[DONE] task-110

Bugfix: fixed data object "bool/false" definition in data.py .

    * bugfix: fixed data object "bool/false" definition in data.py (task-110)

    * pylint: 10/10

[DONE] task-109

Improved debug message displayed by wisteria.py at the beginning of
the program by adding Python version.

    * improved debug message displayed by wisteria.py at the beginning of
      the program by adding Python version (task-109)

    * pylint: 10/10

[DONE] task-108

Improved checkup() message by adding Python version.

    * improved checkup() message by adding Python version (task-108)

    * pylint: 10/10

[DONE] task-107

Documentation in README.md.

    * documentation in README.md (task-107)
    * added a blank line in report.py (task-107)
    * improved data objects order in DATA (task-107)

    * pylint: 10/10

[DONE] task-106

Modified checkup() so that, if verbosity==3 (debug), all serializers and all
data objects (unavailable+available) are displayed.

    * modified checkup() so that, if verbosity==3, it displays all serializers and all
      data objects (unavailable+available). (data-106)
    * improved checkup doc. (data-106)

    * pylint: 10/10

[DONE] task-105

Improved msgerror(): error id is now displayed in red.

    * improved msgerror(): error id is now displayed in red. (task-105)

    * pylint: 10/10

[DONE] task-104

Added new data.

    * added new data. (task-104)

    * pylint: 10/10

[DONE] task-103

Slightly improved messages displayed by the program.

    * slightly improved messages displayed by the program: '}.' > '} .'
      (task-103)

    * pylint: 10/10

[DONE] task-102

Improved checkup() display by adding project's name & version and the current
timestamp. (task-102)

    * improved checkup() display by adding project's name & version and the current
      timestamp. (task-102)

    * pylint: 10/10

[DONE] task-101

Improved code readibility by adding a parameter to aspect_list(, func),
func() being called on each item inserted in the result string.

    * improved code readibility by adding a parameter to aspect_list(, func),
      func() being called on each item inserted in the result string. (task-101)

    * pylint: 10/10

[DONE] task-100

Documentation in reportaspect.py.

    * documentation in reportaspect.py  (task-100)

    * pylint: 10/10

[DONE] task-99

Replaced some duplicates in code by two fonctions, partial_report__data()
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
    * improved the content of main() and of bin/wisteria so that the
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

     * improved the content of main() and of bin/wisteria so that the
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

    * improved help message..
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
