#!/usr/bin/env python3

"""This will be a simple script to open vim for a journal entry and write it to an organized journal directory.  Entries will be stored in JSON format so we can more easily analyze them with a reader later."""

import os
import sys
import tempfile
import subprocess
import json
import datetime
import traceback
import logging
from pprint import pprint

"""Kind of a proto-consructor here"""


def init():
    journal_path = os.path.join(os.path.expanduser("~"), ".journal")
    journal_date = datetime.datetime.today()
    journal_dir = os.path.join(
        journal_path, str(journal_date.year), str(journal_date.month)
    )
    return {
        "journal_path": journal_path,
        "journal_date": journal_date,
        "journal_dir": journal_dir,
    }


"""Keep things organized by directory"""


def upsert_dir(state):
    if os.path.isdir(state["journal_dir"]) and os.path.isfile(
        os.path.join(state["journal_dir"], str(state["journal_date"].day))
    ):
        append_state = True
        return append_state
    elif os.path.isdir(state["journal_dir"]):
        append_state = False
        return append_state
    else:
        try:
            os.makedirs(state["journal_dir"])
            append_state = False
            return append_state
        except Exception as e:
            logging.error(traceback.format_exc())


"""Use VIM as the text entry editor"""


def edit_journal():
    # stamp = datetime.datetime()
    EDITOR = os.environ.get("EDITOR", "vim")

    journal_entry = ""

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        subprocess.call([EDITOR, tf.name])

        # Read the temp file
        tf.seek(0)
        journal_entry = tf.read()
    if journal_entry:
        return journal_entry.decode("utf-8")
    else:
        sys.exit(0)


"""Write the entry back to journal file with timestamp in JSON format"""


def write_journal(state, journal_entry, append_state):
    final_write_state = []
    if append_state:
        try:
            with open(
                os.path.join(state["journal_dir"], str(state["journal_date"].day)), "r"
            ) as file:
                final_write_state = json.loads(file.read())
        except Exception as e:
            logging.error(traceback.format_exc())

    # Always append to the list for final write state
    final_write_state.append(
        {"timestamp": str(state["journal_date"].time()), "content": journal_entry}
    )

    try:
        with open(
            os.path.join(state["journal_dir"], str(state["journal_date"].day)), "w"
        ) as file:
            file.write(json.dumps(final_write_state))
    except Exception as e:
        logging.error(traceback.format_exc())


"""Main sequence"""


def main():
    state = init()
    # Check that our journal dir exists
    if os.path.isdir(state["journal_path"]):
        append_state = upsert_dir(state)
        journal_entry = edit_journal()
        write_journal(state, journal_entry, append_state)
    else:
        setup = input("Journal files not found, do you want to create them? (Y/N): ")

        if setup == "y" or setup == "Y":
            print("Journal entry will be stored in: {}".format(state["journal_path"]))
            _ = input("Press any key to continue.")
            os.makedirs(state["journal_path"])
            append_state = upsert_dir(state)
            journal_entry = edit_journal()
            write_journal(state, journal_entry, append_state)
        else:
            print("Nothing else to do.  Exiting")
            sys.exit(0)


if __name__ == "__main__":
    main()
