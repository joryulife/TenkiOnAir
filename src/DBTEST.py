from MysqlManager import MysqlConnectorManager
sqladdmin = open('../lib/sqladdmin.json','r')
sqladdmin = json.load(sqladdmin)
CM = MysqlConnectorManager(user=sqladdmin['user'],
    password=sqladdmin['password'],
    host=sqladdmin['host'],
    database_name=sqladdmin['database'])
CM.start_connection()

from datetime import datetime as dt
time = "22:22"
RT = dt.strptime(time,'%H:%M')
CM.update_delete_contents(("UPDATE USER SET flag=%s remindTime=%s where UserId = %s"),("FLAT",RT,result["UserId"]))