import MySQLdb

class IngatlanPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='root', db='ingatlan', host='localhost', port=8889, charset="utf8",
                                    unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT INTO entry
                            (id, cim, terulet, szoba_egesz, szoba_fel, ar, tipus, allapot, komfort, emelet, szintek,
                            lift, belmagassag, futes, legkondi, akadaly, wc, tajolas, kilatas, kert, tetoter, parkolas,
                            erkely) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (item['id'],
                                 item['cim'].encode('utf-8'),
                                 item['terulet'],
                                 item['szobak'][0],
                                 item['szobak'][1],
                                 item['ar'],
                                 item['tipus'].encode('utf-8'),
                                 item['allapot'].encode('utf-8'),
                                 item['komfort'].encode('utf-8'),
                                 self.to_unicode(item['emelet']),
                                 self.to_unicode(item['szintek']),
                                 item['lift'].encode('utf-8'),
                                 item['belmagassag'].encode('utf-8'),
                                 item['futes'].encode('utf-8'),
                                 item['legkondi'].encode('utf-8'),
                                 item['akadaly'].encode('utf-8'),
                                 item['wc'].encode('utf-8'),
                                 item['tajolas'].encode('utf-8'),
                                 item['kilatas'].encode('utf-8'),
                                 item['kert'].encode('utf-8'),
                                 item['tetoter'].encode('utf-8'),
                                 item['parkolas'].encode('utf-8'),
                                 item['erkely']))

            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item

    def to_unicode(self, target):
        if isinstance(target, unicode):
            return target
        elif isinstance(target, int):
            return unicode(target)