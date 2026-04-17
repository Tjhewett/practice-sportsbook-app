# This file is responsible for truncating the tables and reapplying the foreign keys for speed purposes. 

import pymysql.cursors
import os
from dotenv import load_dotenv

def trunc(table_names, cursor=None):
    if(cursor == None):
        load_dotenv()
        assert(os.getenv('WORKER_USERNAME') and os.getenv('WORKER_PASSWORD') and os.getenv('DB_URL')) # quits if those arent in env.
        db_url = str(os.getenv('DB_URL'))
        db_host, db_name = db_url.split('/', 2)
        conn = pymysql.connect(host=db_host, user=os.getenv('WORKER_USERNAME'), password=os.getenv('WORKER_PASSWORD'), database=db_name, cursorclass=pymysql.cursors.DictCursor, client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)

        with conn.cursor() as cursor, open('un_fk.sql') as un_fk, open('re_fk.sql') as re_fk:
            un_fk_sql = "".join([line for line in un_fk.readlines()])
            re_fk_sql = "".join([line for line in re_fk.readlines()])


            for table_name in table_names:
                trunc_sql = f'TRUNCATE`gridiron_wager`.`{table_name}`;'
                cursor.execute(trunc_sql)

            for table_name in table_names:
                try:
                    temp_un_fk_sql = un_fk_sql.replace('%s', table_name)
                    cursor.execute(temp_un_fk_sql)
                except:
                    pass

            cursor.execute('TRUNCATE`gridiron_wager`.`snapshots`;')

            for table_name in table_names:
                try:
                    temp_re_fk_sql = re_fk_sql.replace('%s', table_name)
                    cursor.execute(temp_re_fk_sql)
                except:
                    pass
            
         
    else: # If there is a safe pre-existing cursor.
        pass



if __name__ == '__main__':
    trunc(["field_goals", "interceptions", "passing", "receiving", "rushing", "tackles", "team_passing", "team_receiving", "team_rushing","team_defense_passing", "team_defense_receiving", "team_defense_rushing"])