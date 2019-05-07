import psycopg2

from model import PriceOverTime, PriceStats
from api import ApiGateway

class Repository:

    conn = psycopg2.connect("dbname=db user=user password=xxxxx")

    def __init__ (self):
        pass

    def update_auction_data(self):

        gateway = ApiGateway()
        auction_data = gateway.get_auction_data()

        c = self.conn.cursor()

        for row in auction_data:

            c.execute('INSERT INTO auctions(auction_id, item_id, owner, bid, ' +
                    'buyout, quantity, date) VALUES (%s, %s, %s, %s, %s, %s, ' +
                    "CURRENT_DATE) " +
                    'ON CONFLICT (auction_id) DO NOTHING',
                    (row['auction_id'], row['item_id'], row['owner'], row['bid'],
                        row['buyout'], row['quantity'])
                    )

        self.conn.commit()
        c.close()
        self.conn.close()


    def get_historical_prices(self):
        results = []

        sql = '''
                SELECT 
                    items.name AS name,
                    items.category AS category,
                    auctions.date AS date,
                    ROUND(SUM(auctions.buyout)/SUM(auctions.quantity)/10000)::integer AS price
                FROM auctions 
                LEFT JOIN items ON auctions.item_id = items.id 
                WHERE items.category IS NOT NULL
                    AND auctions.date > (CURRENT_DATE - INTERVAL '14' DAY)
                GROUP BY items.name, items.category, auctions.date
                ORDER BY auctions.date ASC
                ;
            '''

        c = self.conn.cursor()
        c.execute(sql)

        for row in c.fetchall():
            auction = PriceOverTime(*row)
            results.append(auction)

        for auction in results:
            auction.date = auction.date.strftime('%m/%d/%Y')


        return results

if __name__ == "__main__":
    repo = Repository()
    repo.update_auction_data()
