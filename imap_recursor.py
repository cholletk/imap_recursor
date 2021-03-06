#!/usr/bin/env python
#
'''
    File name: imap_recursor.py
    License: GNU LESSER GENERAL PUBLIC LICENSE
    Author: Kevin Chollet
    Date created: 04/05/2018
    Date last modified: 04/05/2018
    Python Version: 3.2.3
    Sources : sample used : http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
'''

import sys
import imaplib
import email
import argparse
import subprocess

def process_mailbox(imap_ressource, command, delete="false", mar="false"):

    if mar == "true" :
        # If MarkAsRead is setted, we will manage only the unread messages
        result, data = imap_ressource.search(None, "ALL", "(UNSEEN)")
    else :
        result, data = imap_ressource.search(None, "ALL")

    if result != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        result, data = imap_ressource.fetch(num, '(RFC822)')
        if result != 'OK':
            print("ERROR getting message", num)
            return

        # Launching subprocess
        
        proc = subprocess.Popen(command.split(' '), stdin=subprocess.PIPE)
        proc.stdin.write(data[0][1])
        proc.communicate()

        if proc.returncode == 0:
            if mar == "true" :
                imap_ressource.store(num, '+FLAGS', '\Seen')
            if delete == "true" :
                imap_ressource.store(num, '+FLAGS', '\Deleted')

    imap_ressource.expunge()




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

parser.add_argument('-e', '--exec',
    action="store", dest="execute",
help="Command to execute" )

parser.add_argument('-d', '--delete',
    action="store", dest="delete",
help="delete email after processing", default="false", choices=['false', 'true'])

parser.add_argument('-r', '--markasread',
    action="store", dest="mar",
help="mark email as readen after processing", default="true", choices=['false', 'true'])


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
    process_mailbox(imap_ressource, options.execute, mar = options.mar, delete=options.delete)
    imap_ressource.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

imap_ressource.logout()
