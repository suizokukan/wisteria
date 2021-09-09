Linden's roadmap & todos
========================

See TODOs at the end of this file.

[CURRENT] v. 0.0.1
------------------

rm .tmp
fullpath() pour les print
--downloaddfltini
--inifile
i18n=en|fr|de|it|es|ru (ou plutôt FR_fr ???, important pour le mandarin)

--cmp="iaswn vs others(A)"  (A) (CWC) (INI)
--cmp="iaswn vs jsonpickle;json(A)"  (A) (CWC) (INI)

Conclusion:
According to the tests conducted on all data...
According to the tests conducted on the data of the "comparing what is comparable" type
According to the tests conducted on the data read in the %%% file
Iaswn is much much faster than jsonpickle (Iaswn/jsonpicle: 23.3) to encode/decode; Iaswn's encoded strings are slightly shorter than jsonpickle one's (Iaswn/jsonpickle: 0.9); Iaswn's coverage rate is lower than jsonpickle's (Iaswn/jsonpicle: 0.5).

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
