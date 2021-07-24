import mysql.connector
from ..lib import sqladdmin


# DBへ接続
conn = mysql.connector.connect(
    user=sqladdmin.user,
    password=sqladdmin.password,
    host=sqladdmin.host,
    database_name=sqladdmin.database
)

# DBの接続確認
if not conn.is_connected():
    raise Exception("MySQLサーバへの接続に失敗しました")

cur = conn.cursor(dictionary=True)

query__for_fetching = """
SELECT
    sample_table.sample_id   AS id,
    sample_table.sample_name AS name
FROM sample_table
ORDER BY sample_table.sample_id
;
"""

cur.execute(query__for_fetching)

for fetched_line in cur.fetchall():
    id = fetched_line['id']
    name = fetched_line['name']
    print(f'{id}: {name}')