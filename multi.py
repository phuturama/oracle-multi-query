###################################################################
# Purpose:  execute queries against multiple databases            #   
# Version:  0.0.2                                                 #   
# Author:   phuturama                                             #   
# Requires: Python 3.x, pykeepass                                 #   
# Params:   multi.py <KeePassMasterPassphrase>                    #
###################################################################

from __future__ import print_function
from pykeepass import PyKeePass            
import cx_Oracle
import json
import sys

keefile = '/path/to/credentials.kdbx' 
if (len (sys.argv) == 1): print('Missing parameter KeePass master password'); exit (1)
kp = PyKeePass(keefile, password = sys.argv[1])
ora = ''
res = ''
qry = 'select * from v$version'

# KeePass connections 
# Positions 
# 0           1               2           3           4           5           6           7                   8
# Format   
# 'user',     'kp-entry',     'fqdn',     'port',     'sid name', 'env',      'stream',   'database name',    'literal sid or DSN/TNS string'  

conns = [
('APP_DBA', 'dev.db.orac.dba', 'orac-db-dev.db.com',  '1521', 'ORAC', 'DEV', 'MANDANT', 'ORAC', 'sid' ), 
('APP_DBA', 'prd.db.orac.dba', '0', '0', '0',                         'PRD', 'MANDANT', 'ORAC', '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=orac-db-prd1.db.com)(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST=orac-db-prd2.db.com)(PORT=6777)))(CONNECT_DATA=(SERVICE_NAME=orac_primary.prd.db.de)))'), 
# add connections here
]

for conn in conns:    
    print ('\n►  Connection: ' + conn[5] + '-' + conn[6] + '-' + conn[7] + '-' + conn[0] )

    # Get KeePass password
    entry = kp.find_entries(title = conn[1], first = True)

    # Setup connection   
    ora = conn[2] + ":" + conn[3] + "/" + conn[4] 
    if (conn[8] == 'sid' ):
        dsnStr = cx_Oracle.makedsn(conn[2], conn[3], conn[4])
    else:
        dsnStr = conn[8]
    connection = cx_Oracle.connect(user = conn[0], password = entry.password, dsn = dsnStr)      
    cursor = connection.cursor()

    # Execute query
    if True:
        cursor.execute(qry)
        for row in cursor.fetchall():
            # beautify
            res = str(row)
            res = res.replace("',)" , "")
            res = res.replace(")"   , "")
            res = res.replace("('"  , "")
            print (res) 
    connection.close()
