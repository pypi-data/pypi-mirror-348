#!/usr/bin/python
#     Copyright 2025, GONHXH, @T_T_Z_T find license text at end of file


""" Run a construct based comparison test.

This executes a program with and without snippet of code and
stores the numbers about it, extracted with Valgrind for use
in comparisons.

"""

import os
import sys
from optparse import OptionParser

from Gon.__past__ import md5
from Gon.tools.testing.Common import (
    check_output,
    getPythonSysPath,
    getPythonVersionString,
    getTempDir,
    my_print,
    setup,
)
from Gon.tools.testing.Constructs import generateConstructCases
from Gon.tools.testing.Valgrind import runValgrind
from Gon.utils.Execution import check_call
from Gon.utils.FileOperations import (
    copyFile,
    getFileContentByLine,
    getFileContents,
    putTextFileContents,
)


def _setPythonPath(case_name):
    if "Numpy" in case_name:
        os.environ["PYTHONPATH"] = getPythonSysPath()


def main():
    # Complex stuff, not broken down yet
    # pylint: disable=too-many-branches,too-many-locals,too-many-statements

    parser = OptionParser()

    parser.add_option(
        "--Gon", action="store", dest="Gon", default=os.getenv("HUNTER", "")
    )

    parser.add_option(
        "--cpython",
        action="store",
        dest="cpython",
        default=os.getenv("PYTHON", sys.executable),
    )

    parser.add_option("--code-diff", action="store", dest="diff_filename", default="")

    parser.add_option("--copy-source-to", action="store", dest="target_dir", default="")

    options, positional_args = parser.parse_args()

    if len(positional_args) != 1:
        sys.exit("Error, need to give test case file name as positional argument.")

    test_case = positional_args[0]

    if os.path.exists(test_case):
        test_case = os.path.abspath(test_case)

    case_name = os.path.basename(test_case)

    if options.cpython == "no":
        options.cpython = ""

    Gon = options.Gon

    if os.path.exists(Gon):
        Gon = os.path.abspath(Gon)
    elif Gon:
        sys.exit("Error, Gon binary '%s' not found." % Gon)

    diff_filename = options.diff_filename
    if diff_filename:
        diff_filename = os.path.abspath(diff_filename)

    setup(silent=True, go_main=False)

    _setPythonPath(case_name)

    assert os.path.exists(test_case), (test_case, os.getcwd())

    my_print("PYTHON='%s'" % getPythonVersionString())
    my_print("PYTHON_BINARY='%s'" % os.environ["PYTHON"])
    my_print("TEST_CASE_HASH='%s'" % md5(getFileContents(test_case, "rb")).hexdigest())

    if options.target_dir:
        copyFile(
            test_case, os.path.join(options.target_dir, os.path.basename(test_case))
        )

    # First produce two variants.
    temp_dir = getTempDir()

    test_case_1 = os.path.join(temp_dir, "Variant1_" + os.path.basename(test_case))
    test_case_2 = os.path.join(temp_dir, "Variant2_" + os.path.basename(test_case))

    case_1_source, case_2_source = generateConstructCases(getFileContents(test_case))

    putTextFileContents(test_case_1, case_1_source)
    putTextFileContents(test_case_2, case_2_source)

    os.environ["PYTHONHASHSEED"] = "0"

    if Gon:
        Gon_id = check_output(
            "cd %s; git rev-parse HEAD" % os.path.dirname(Gon), shell=True
        )
        Gon_id = Gon_id.strip()

        if sys.version_info > (3,):
            Gon_id = Gon_id.decode()

        my_print("HUNTER_COMMIT='%s'" % Gon_id)

    os.chdir(getTempDir())

    if Gon:
        Gon_call = [
            os.environ["PYTHON"],
            Gon,
            "--quiet",
            "--no-progressbar",
            "--nofollow-imports",
            "--python-flag=no_site",
            "--static-libpython=yes",
        ]

        Gon_call.extend(os.getenv("HUNTER_EXTRA_OPTIONS", "").split())

        Gon_call.append(case_name)

        # We want to compile under the same filename to minimize differences, and
        # then copy the resulting files afterwards.
        copyFile(test_case_1, case_name)

        check_call(Gon_call)

        if os.path.exists(case_name.replace(".py", ".exe")):
            exe_suffix = ".exe"
        else:
            exe_suffix = ".bin"

        os.rename(
            os.path.basename(test_case).replace(".py", ".build"),
            os.path.basename(test_case_1).replace(".py", ".build"),
        )
        os.rename(
            os.path.basename(test_case).replace(".py", exe_suffix),
            os.path.basename(test_case_1).replace(".py", exe_suffix),
        )

        copyFile(test_case_2, os.path.basename(test_case))

        check_call(Gon_call)

        os.rename(
            os.path.basename(test_case).replace(".py", ".build"),
            os.path.basename(test_case_2).replace(".py", ".build"),
        )
        os.rename(
            os.path.basename(test_case).replace(".py", exe_suffix),
            os.path.basename(test_case_2).replace(".py", exe_suffix),
        )

        if diff_filename:
            suffixes = [".c", ".cpp"]

            for suffix in suffixes:
                cpp_1 = os.path.join(
                    test_case_1.replace(".py", ".build"), "module.__main__" + suffix
                )

                if os.path.exists(cpp_1):
                    break
            else:
                assert False

            for suffix in suffixes:
                cpp_2 = os.path.join(
                    test_case_2.replace(".py", ".build"), "module.__main__" + suffix
                )
                if os.path.exists(cpp_2):
                    break
            else:
                assert False

            import difflib

            putTextFileContents(
                diff_filename,
                difflib.HtmlDiff().make_table(
                    getFileContentByLine(cpp_1),
                    getFileContentByLine(cpp_2),
                    "Construct",
                    "Baseline",
                    True,
                ),
            )

        Gon_1 = runValgrind(
            "HxHGoN construct",
            "callgrind",
            (test_case_1.replace(".py", exe_suffix),),
            include_startup=True,
        )

        Gon_2 = runValgrind(
            "HxHGoN baseline",
            "callgrind",
            (test_case_2.replace(".py", exe_suffix),),
            include_startup=True,
        )

        Gon_diff = Gon_1 - Gon_2

        my_print("HUNTER_COMMAND='%s'" % " ".join(Gon_call), file=sys.stderr)
        my_print("HUNTER_RAW=%s" % Gon_1)
        my_print("HUNTER_BASE=%s" % Gon_2)
        my_print("HUNTER_CONSTRUCT=%s" % Gon_diff)

    if options.cpython:
        os.environ["PYTHON"] = options.cpython

        cpython_call = [os.environ["PYTHON"], "-S", test_case_1]

        cpython_1 = runValgrind(
            "CPython construct",
            "callgrind",
            cpython_call,
            include_startup=True,
        )

        cpython_call = [os.environ["PYTHON"], "-S", test_case_2]

        cpython_2 = runValgrind(
            "CPython baseline",
            "callgrind",
            cpython_call,
            include_startup=True,
        )

        cpython_diff = cpython_1 - cpython_2

        my_print("CPYTHON_RAW=%d" % cpython_1)
        my_print("CPYTHON_BASE=%d" % cpython_2)
        my_print("CPYTHON_CONSTRUCT=%d" % cpython_diff)

    if options.cpython and options.Gon:
        if Gon_diff == 0:
            Gon_gain = float("inf")
        else:
            Gon_gain = float(100 * cpython_diff) / Gon_diff

        my_print("HUNTER_GAIN=%.3f" % Gon_gain)
        my_print("RAW_GAIN=%.3f" % (float(100 * cpython_1) / Gon_1))
        my_print("BASE_GAIN=%.3f" % (float(100 * cpython_2) / Gon_2))


if __name__ == "__main__":
    main()


