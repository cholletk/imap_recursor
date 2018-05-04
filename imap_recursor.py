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

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        print('Message %s: %s' % (num, subject))
        print('Raw Date:', msg['Date'])
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print("Local Date:",
                local_date.strftime("%a, %d %b %Y %H:%M:%S"))


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
    process_mailbox(M)
    imap_ressource.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

imap_ressource.logout()
