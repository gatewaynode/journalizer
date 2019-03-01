#!/usr/bin/env python3

#
#
#

import os
import sys
import tempfile
import subprocess

def main():
    EDITOR = os.environ.get('EDITOR', 'vim')
    
    initial_message = "Testing {}".format("test")
    journal_entry = ""

    with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
        tf.write(initial_message.encode('utf-8'))
        tf.flush
        subprocess.call([EDITOR, tf.name])
        
        # Read the temp file
        tf.seek(0)
        journal_entry = tf.read()

    print(journal_entry.decode('utf-8'))

if __name__ == '__main__':
    main()
