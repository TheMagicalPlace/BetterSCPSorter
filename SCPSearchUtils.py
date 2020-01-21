
import sqlite3

def open_connection(func):
    pass

def by_rating(min_rating,number_to_return=10):
    with sqlite3.connect('scps.db') as scpdb:
        cur = scpdb.cursor()
        results = list(cur.execute(f'SELECT link FROM scp_main WHERE scp_main.rating >=:min_rating ORDER BY scp_main.rating DESC' ,{'min_rating':min_rating}))
        if len(results) > number_to_return:
            results = results[:number_to_return]
        return results

def by_tag(tag,number_to_return=10,min_rating=None):

    with sqlite3.connect('scps.db') as scpdb:
        cur = scpdb.cursor()
        try:
            if min_rating is None:
                results = list(cur.execute(f'SELECT link from scp_main INNER JOIN {tag} on {tag}.number = scp_main.number'))
            else:
                results = list(cur.execute(f'SELECT link from scp_main INNER JOIN {tag} on {tag}.number = scp_main.number WHERE scp_main.rating >=:min_rating',{'min_rating':min_rating}))
        except sqlite3.OperationalError:
            return 'NON-VALID TAG'
        else:
            if len(results) > number_to_return:
                results = results[:number_to_return]
            print(results)
            return results

def by_tags(tags,number_to_return=10,min_rating=None):
    with sqlite3.connect('scps.db') as scpdb:
        cur = scpdb.cursor()
        common_articles = {}
        for tag in tags:
            try:
                if min_rating is None:

                    results = list(cur.execute(f'SELECT link,scp_main.rating FROM scp_main INNER JOIN {tag} on {tag}.number = scp_main.number ORDER BY scp_main.rating DESC'))
                else:
                    results = list(cur.execute(f'SELECT link,scp_main.rating FROM scp_main INNER JOIN {tag} on {tag}.number = scp_main.number WHERE scp_main.rating >=:min_rating ORDER BY rating DESC',{'min_rating':min_rating}))
            except sqlite3.OperationalError:
                common_articles[tag] = {'NON-VALID Tag':'NON-VALID TAG'}
            else:
                results = {l[0]:l[1] for l in results}
                common_articles[tag] = results
    lset = None
    for resultdict in common_articles.values():
            rset = set([lnk for lnk in resultdict.keys()])
            if lset is None:
                lset=rset
            else:
                lset = lset.intersection(rset)

    resdict = {}
    for resultdict in common_articles.values():
        for lnk in lset:
            try:
                resdict[lnk] = resultdict[lnk]
            except KeyError:
                continue

    results = [lnk for lnk,_ in sorted(resdict.items(),reverse=True)]
    if len(results) > number_to_return:
        results = results[:number_to_return]
    return results

def by_author(author):
    pass

if __name__ == '__main__':
    by_rating(10000,10)
    by_tag('sculpture',min_rating=1020)
    print(by_tags(['sculpture','euclid']))