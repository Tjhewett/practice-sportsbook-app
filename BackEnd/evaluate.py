# evaluation script to run after bets have been evaluated manually 

import pymysql.cursors
import os
from dotenv import load_dotenv

def eval_bets():
    load_dotenv()
    assert(os.getenv('WORKER_USERNAME') and os.getenv('WORKER_PASSWORD') and os.getenv('DB_URL'))
    db_url = str(os.getenv('DB_URL'))
    db_host, db_name = db_url.split('/', 2)
    conn = pymysql.connect(host=db_host, user=os.getenv('WORKER_USERNAME'), password=os.getenv('WORKER_PASSWORD'), database=db_name, cursorclass=pymysql.cursors.DictCursor, client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)

    try:
        with conn.cursor() as cursor:
            # List of tables and their respective payout columns
            bet_tables = [
                ('bets_draft', 'potential_payout'),
                ('bets_week1', 'potential_payout'),
                ('bets_superbowl', 'potential_payout')
            ]
            
            for table_name, payout_column in bet_tables:
                # Update currency for users whose bets have won in each table
                sql = f'''
                    UPDATE user u JOIN {table_name} b ON u.id = b.user_id
                    SET u.currency = u.currency + b.{payout_column}
                    WHERE b.is_won = 1;
                '''
                cursor.execute(sql)
                conn.commit()

                # Optionally fetch and print updated balances for confirmation/logging
                cursor.execute('SELECT username, currency FROM user')
                users = cursor.fetchall()
                for user in users:
                    print(f"User: {user['username']}, New Currency: {user['currency']}")

    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    eval_bets()
