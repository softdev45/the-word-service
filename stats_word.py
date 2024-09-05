from bible import root_pl, root_en

from re import findall

verses = root_pl.xpath('.//verse')

wstat = dict()

for v in verses:
    v = v.text
    words = findall(r'\w+', v)
    for w in words:
        wstat[w] = wstat.get(w, 0) + 1

stat = sorted(wstat.items(), key= lambda i: i[1], reverse=True)
with open('stats.txt','w') as sf:
    for s in stat:
        sf.write(f'{s[1]} {s[0]}\n')



