Linden's roadmap & todos
========================

See TODOs at the end of this file.

[CURRENT] v. 0.0.1
------------------

--showserializers: show installed serializers and stop (arrêter avant que le .tmp ne soit créé)
--downloaddfltini
i18n() + --i18n=en|fr|de|it|es|ru (ou plutôt FR_fr ???, important pour le mandarin)

Conclusion:
According to the tests conducted on all data...
According to the tests conducted on the data of the "comparing what is comparable" type
According to the tests conducted on the data read in the %%% file
Iaswn is much much faster than jsonpickle (Iaswn/jsonpicle: 23.3) to encode/decode; Iaswn's encoded strings are slightly shorter than jsonpickle one's (Iaswn/jsonpickle: 0.9); Iaswn's coverage rate is lower than jsonpickle's (Iaswn/jsonpicle: 0.5).
                                  
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
