# web scrape logic for getting the statistic data
# run this file to initiate a web scrape to fill the tables with data

import requests
import pymysql.cursors
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

assert(os.getenv('WORKER_USERNAME') and os.getenv('WORKER_PASSWORD') and os.getenv('DB_URL'))

index = [
            {   
                'table':"passing", #0
                'cols':[0, 1, 3, 4, 5, 6, 7, 8, 14], 
                'url':"/stats/player-stats/category/passing/2023/reg/all/passingyards/desc"
            },
            {
                'table':"rushing", #1
                'cols':[0, 1, 2, 3, 6, 9], 
                'url':"/stats/player-stats/category/rushing/2023/reg/all/rushingyards/desc"
            },
            {
                'table':"receiving", #2
                'cols':[0, 1, 2, 3, 6, 9, 11], 
                'url':"/stats/player-stats/category/receiving/2023/reg/all/receivingreceptions/desc"
            },
            {
                'table':"tackles", #3
                'cols':[0, 1, 2, 3, 4], 
                'url':"/stats/player-stats/category/tackles/2023/post/all/defensivecombinetackles/desc"
            },
            {
                'table':"interceptions", #4
                'cols':[0, 1, 2, 3, 4], 
                'url':"/stats/player-stats/category/interceptions/2023/reg/all/defensiveinterceptions/desc"
            },
            {
                'table':"field_goals", #5
                'cols':[0, 1, 2, 3, 10, 11], 
                'url':"/stats/player-stats/category/field-goals/2023/post/all/kickingfgmade/desc"
            },
            {
                'table':"team_passing", #6
                'cols':[0, 1, 2, 3, 5, 6, 7, 8, 14, 15], 
                'url':"/stats/team-stats/offense/passing/2023/reg/all"
            },
            {
                'table':"team_rushing", #7
                'cols':[0, 1, 2, 3, 4, 10], 
                'url':"/stats/team-stats/offense/rushing/2023/reg/all"
            },
            {
                'table':"team_receiving", #8
                'cols':[0, 1, 2, 4, 10], 
                'url':"/stats/team-stats/offense/receiving/2023/reg/all"
            },
            {
                'table':"team_defense_passing", #9
                'cols':[0, 1, 2, 3, 5, 6, 7, 8, 14], 
                'url':"/stats/team-stats/defense/passing/2023/reg/all"
            },
            {
                'table':"team_defense_rushing", #10
                'cols':[0, 1, 2, 3, 4, 10], 
                'url':"/stats/team-stats/defense/rushing/2023/reg/all"
            },
            {
                'table':"team_defense_receiving", #11
                'cols':[0, 1, 2, 4, 10, 11], 
                'url':"/stats/team-stats/defense/receiving/2023/reg/all"
            }
        ]

def make_snapshot(cursor):
    tsql = 'INSERT INTO snapshots (timestamp) VALUES(CURRENT_TIMESTAMP)'
    cursor.execute(tsql)
    sid = cursor.lastrowid
    return sid

#recursive FX that takes a url, and sid
# def go(table="passing", columns=["player", "yards", "attempts", "completions"], url="/stats/player-stats/category/passing/2023/reg/all/passingyards/desc", sid=None):
def go(tablename, cols, url, sid=None):
    db_url = str(os.getenv('DB_URL'))
    db_host, db_name = db_url.split('/', 2)
    conn = pymysql.connect(host=db_host, user=os.getenv('WORKER_USERNAME'), password=os.getenv('WORKER_PASSWORD'), database=db_name, cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        try:
            # Scraping data from the URL
            url = f'https://www.nfl.com{url}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            next_page = soup.find('a', attrs={"class":"nfl-o-table-pagination__next"})
            next_url = None
            if next_page:
                next_url = next_page.attrs['href']
                
            # Extracting data from the table and storing it in the database
            table = soup.find('table')
            all_rows = table.find_all('tr')

            # teamName = soup.find('div', attrs={"class":"d3-o-club-shortname"})
   
            header_html = all_rows[0]
            rows = all_rows[1:]  # Skip the header row
            headers = []
            for header in header_html.find_all('th'):
                hn = header.text.strip() 
                hn = hn.replace(' %', "_percent", 1)
                hn = hn.replace(' ', "_", 1)
                hn = hn.replace('+', "Plus", 1)
                headers.append(f'`{hn}`')

            header_list = []
            for i in cols:
                header_list.append(headers[i])
          
            # Enter a new Timestamp record.
            if not sid:
                sid = make_snapshot(cursor)

            for row in rows:
                columns = row.find_all('td')
                values = []
                for i in cols:
                    data = None
                    if 'tabindex' in columns[i].attrs:
                        div = columns[i].find('div', attrs={'class':'d3-o-club-fullname'})
                        if(div != None):
                            data = str(div.text.strip())
                        else:
                            div = columns[i].find('div', attrs={'class':'d3-o-media-object__body'})
                            if (div != None):
                                data = str(div.text.strip())
                            else:
                                raise Exception("HTML_CLASS_NOT_FOUND")

                    else:
                        data = str(columns[i].text.strip())
                    if i == 0:
                        values.append(data)
                    elif data.__contains__('.'):
                        values.append(float(data))
                    else:
                        values.append(int(data))

                sql = f'INSERT INTO {tablename} ({", ".join(header_list)}, snapshot_id) VALUES({"%s, " * len(header_list)}%s)'
                print(sql)
            
                values.append(sid)
                cursor.execute(sql, values)
                conn.commit()
            
            if next_url:
                go(tablename=tablename, cols=cols, url=next_url, sid=sid)

        except Exception as e:
            # Log the error
            print(f'Error fetching and storing data: {e}')
        finally:
            conn.close()

        return sid

if __name__ == '__main__': # If im the real file being called we do this, however if someone just wants an import we allow that too.
    sid = None
    for page in index:
        sid = go(page['table'], page['cols'], page['url'], sid)
    # go(index[0]['table'], index[0]['cols'], index[0]['url'])

