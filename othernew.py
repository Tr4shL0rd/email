#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import imaplib2 as imaplib
from email import Header
from email.parser import Parser

##USER CONFIG
HOST = 'imap.gmail.com'
PORT = '993'
USER = 'm4mebox@gmail.com'
PAWD = '22Nisser'
HAM_F  = 'INBOX'

SPAM_F = '0_learn_spam' #'[Gmail]/Spam' by default
LIMIT = 1  #howmany mails to read each time.

##Filter config. you need to know some regex
filters = {
    "Subject": re.compile(r"""(?x)
                              （AD）|
                              \(AD\)|
                              ^\.$
                           """),
    }

## system config


def GetUID(s):
    """the global ID for emails"""
    pattern_uid = re.compile(r'(?<=UID )(\d+)')
    try:
        return pattern_uid.findall(s)[0]
    except Exception, e:
        print "Error!", str(e)
        return ""
    

def Filter(headers):
    """to detect if it is spam
    if any of the filters matches, the message is considered spammy.
    aggressive, but simple to handle.
    """
    for header_name, header_value in headers.items():
        if filters[header_name].search(header_value):
            #print "Match!", header_name, header_value, headers
            return True

    return False       
        
def DecodeSingleHeader(s):
    """
    decode headers to UTF-8
    """
    parts = Header.decode_header(s)
    header = []
    for part in parts:
        s, enc=part
        if enc:
            s = unicode(s , enc).encode('utf8', 'replace')
        header.append(s)
        
    h= " ".join(header)
    return h

def StringToHeaders(s):
    return Parser().parsestr(s)



def MarkUnread(imap, uids):
    """
    mark a list of uids as Read. Implementation: remove the SEEN flag.
    """
    if not uids:
        return
        
    uids=','.join(uids)
    print "marking unread", uids
    typ, data = imap.uid('STORE', uids, '-FLAGS', "\SEEN")
    print typ, data
    

        
g = imaplib.IMAP4_SSL(HOST) 

try:
    r, info=g.login(USER, PAWD)
except Exception, e:
    print str(e)

g.select(HAM_F)
#typ, msg_ids = g.search(None, ('UNSEEN'))
typ, msg_ids = g.search(None, ('ALL'))

ham=[]

if typ=='OK':
    ids= msg_ids[0].split(' ')
    for id in ids[:LIMIT]:

        (r,msg)=g.fetch(id, '(UID BODY[HEADER.FIELDS (SUBJECT FROM TO MESSAGE-ID)])')

        header=msg[0][1]
        uid= GetUID(msg[0][0])

        h=StringToHeaders(header)
                        
        header={}
        for i in ['Subject' ]:
            if h.has_key(i):

                v=h[i]
                if i.lower() == 'from':
                    v=TrimFrom(v)                 

                header[i]=DecodeSingleHeader(v)

        
        for k, v in header.items():
            print k, ": ", v
        print




MarkUnread(g, ham)
g.logout()
