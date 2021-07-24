import json
#from ..lib import sqladdmin
from MysqlManager import MysqlConnectorManager
sqladdmin = open('../lib/sqladdmin.json','r')
sqladdmin = json.load(sqladdmin)
CM = MysqlConnectorManager(user=sqladdmin['user'],
    password=sqladdmin['password'],
    host=sqladdmin['host'],
    database_name=sqladdmin['database'])
CM.start_connection()
q = ("insert into TESTTABLE value(%s,%s)")
ps =(2, 'TEST2')
ans =CM.insert_contents(q,ps)
print(ans)