import MySQLdb
import simplejson as simplejson
from dbconnect import connection
from flask import json

c, conn = connection()


c.execute("DELETE FROM users WHERE uid > 10060;")
conn.commit()

c.close()
conn.close()






