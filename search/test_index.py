import whoosh.index as index
from whoosh.qparser import QueryParser


indexdir = "/Users/kevindunn/ConnectMV/pid-book/_build/whoosh"
myindex = index.open_dir(indexdir)
assert(index.exists_in(indexdir))


searcher = myindex.searcher()

with myindex.searcher() as searcher:
    
    # Show all the search terms in the index
    #list(searcher.lexicon("body"))

    qp = QueryParser("body", schema=myindex.schema)
    q = qp.parse(u"qqplot")
    results = searcher.search(q, limit=10)
    results.fragmenter.charlimit = None    


    for hit in results:
        print(hit["title"])
        print(hit.highlights("body"))
        print('----')