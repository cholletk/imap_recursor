#!/usr/bin/env python
#
# Very basic example of using Python and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
import sys
import imaplib
import getpass
import email
import email.header
import datetime
import argparse


def process_mailbox(M):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        print(data[0][1].decode("utf-8"))
        """msg = email.message_from_bytes(data[0][1])"""


#Parsing arguments
parser = argparse.ArgumentParser(description='Recurse over each email of imap directory')

parser.add_argument('-u', '--username',
    action="store", dest="username",
help="Username", required=True)

parser.add_argument('-p', '--password',
    action="store", dest="password",
help="Password", required=True)

parser.add_argument('-s', '--server',
    action="store", dest="server",
help="Imap server", required=True)

parser.add_argument('-S', '--ssl',
    action="store", dest="ssl",
help="using ssl or not (imaps vs imap)", default="true", choices=['false', 'true'])

parser.add_argument('-f', '--folder',
    action="store", dest="folder",
help="Folder to explore", default="INBOX")


options = parser.parse_args()

if options.ssl == "true" :
    imap_ressource = imaplib.IMAP4_SSL(options.server)
else :
    imap_ressource = imaplib.IMAP4(options.server)

try:
    result, data = imap_ressource.login(options.username, options.password)
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ")
    sys.exit(1)

print(result, data)

result, mailboxes = imap_ressource.list()
if result == 'OK':
    print("Mailboxes:")
    print(mailboxes)

result, data = imap_ressource.select(options.folder)
if result == 'OK':
    print("Processing mailbox...\n")
    process_mailbox(imap_ressource)
    imap_ressource.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

imap_ressource.logout()
