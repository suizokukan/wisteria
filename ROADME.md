Linden's roadmap & todos
========================

See TODOs at the end of this file.

[CURRENT] v. 0.0.1
------------------

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

task-9:
(1) [empty string] --cmp="" > all vs|versus|against all ""=(A)
(2)                --cmp="jsonpickle vs|versus|against json(A)" / ""=(A) (CWC) (INI)
(3)                --cmp="jsonpickle(A)" / "" (A) (CWC) (INI)
(3')               --cmp="jsonpickle vs|versus|against others|all(A)" / ""=(A) (CWC) (INI)

    cmpsyntax = (None i.e all | "jsonpickle",
                 None i.e all | "jsonpickle",
                 "all"/"cwc"/"ini")


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
