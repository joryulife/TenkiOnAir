from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import mysql.connector


@dataclass
class MysqlConnectorManager():
    user: str = ""
    password: str = ""
    host: str = ""
    database_name: str = ""
    cur: Optional[Any] = None
    conn: Optional[Any] = None

    @classmethod
    def create(cls,
                user: str,
                password: str,
                host: str,
                database_name: str,
            ) -> 'MysqlConnectorManager':
        return MysqlConnectorManager(user=user, password=password, host=host, database_name=database_name)

    def __del__(self):
        self._close_connection()

    def start_connection(self) -> None:
        """DBに接続する"""
        self.conn = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database_name
        )

        # DB接続の確認
        if not self.conn.is_connected():
            raise Exception("MySQLサーバへの接続に失敗しました")

        self.cur = self.conn.cursor(dictionary=True)

    def _close_connection(self) -> None:
        """DBの接続を切る
        """
        self.cur.close
        self.conn.close
        self.cur = None
        self.conn = None

    def fetch_contents(self, query: str,ps: str) -> List[Dict[str, Any]]:
        """DBから情報を取得する
        """
        #print(query)
        self.cur.execute(query,ps)
        fetched_contents: List[Dict[str, Any]] = self.cur.fetchall()
        return fetched_contents
    
    def update_delete_contents(self, query: str,ps: str):
        """データを更新する
        """
        self.cur.execute(query,ps)
        self.conn.commit()

    def insert_contents(self, query: str,ps: str):
        """データを追加する
        """
        self.cur.execute(query,ps)
        self.conn.commit()