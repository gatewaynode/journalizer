#!/usr/bin/env python3

#
# This will be a simple script to open vim for a journal entry and write it to an organized journal directory.
#

import os
import sys
import tempfile
import subprocess
import datetime

journal_path = os.path.join(os.path.expanduser('~'), '.journal')
journal_date = datetime.datetime.today()
journal_dir = os.path.join(journal_path, journal_path.year, journal_date.month)

def upsert_dir():
    if os.path.isdir(journal_dir) and os.path.isfile(os.path.join(journal_dir, journal_date.day)):
        print("Update")
    else:
        os.makedirs(journal_dir)

def edit_journal():
    # stamp = datetime.datetime()
    EDITOR = os.environ.get('EDITOR', 'vim')
    
    journal_entry = ""

    with tempfile.NamedTemporaryFile(suffix = '.tmp') as tf:
        subprocess.call([EDITOR, tf.name])
        
        # Read the temp file
        tf.seek(0)
        journal_entry = tf.read()

    print(journal_entry.decode('utf-8'))
    return(journal_entry.decode('utf-8'))

def main():
    # Check that our jornal dir exists
    if os.path.isdir(journal_path):
        journal_entry = edit_journal()
    else:
        setup = input("Journal files not found, do you want to create them? (Y/N): ")
        
        if setup == 'y' or setup == 'Y':
            os.makedirs(journal_path)
            print("Journal entrie will be stored in: {}".format(journal_path))
            journal_entry = edit_journal()
        else:
            print("Nothing else to do.  Exiting")
            sys.exit(0)
if __name__ == '__main__':
    main()
