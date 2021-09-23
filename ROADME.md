Linden's roadmap & todos
========================

See TODOs at the end of this file.

[CURRENT] v. 0.0.1
------------------


Conclusion:
According to the tests conducted on all data...
According to the tests conducted on the data of the "comparing what is comparable" type
According to the tests conducted on the data read in the %%% file
Iaswn is much much faster than jsonpickle (Iaswn/jsonpicle: 23.3) to encode/decode; Iaswn's encoded strings are slightly shorter than jsonpickle one's (Iaswn/jsonpickle: 0.9); Iaswn's coverage rate is lower than jsonpickle's (Iaswn/jsonpicle: 0.5).

* --downloaddfltini
* i18n() + --i18n=en|fr|de|it|es|ru (ou plutôt FR_fr ???, important pour le mandarin)
* linden > wisteria (https://en.wikipedia.org/wiki/Wisteria : image!)
* progress bar : calcul
  en profiter pour proposer plusieurs méthodes : 1.1, 1.2, ... 1.9, 2.1, 2.2 ... 2.9, ...
                                                 1.1, 2.1, 3.1, ... 1.2, 2.2, 3.2, ...
* --lenmethod + modifier les en-têtes des tableaux
* --meta: comparer avec les différentes versions de _len, graphique montrant ce qui se passe qd on augmente TIMEITNUMBER

task-24: TIMEITNUMBER > --timeitnumber=

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
