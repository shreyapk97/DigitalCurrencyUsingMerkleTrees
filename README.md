# DigitalCurrencyUsingMerkleTrees
Python POC of Digital Currency using Merkle Trees. We have implemented a distributed expense tracking system for digital currency using
Merkle Trees. RPC (Remote Procedural Calls) are used to exchange data between peers and the query
program.

peer.py is the main file which we run for every participant.
query.py is the program we run to authenticate the participants and finally create the master
Merkle Tree

Implementation
To Run:
On first terminal: python3 peer.py 8000 a abcdefgh lmnopqrs aaaaaaaa
On second terminal : python3 peer.py 8001 b abcdefgh lmnopqrs aaaaaaaa
On third terminal : python3 peer.py 8002 c abcdefgh lmnopqrs aaaaaaaa
Fourth terminal (query program) : python3 query.py abcdefgh 8000 8001 8002 --&gt;
Authentication is successful in this case

Different Authentication Failure cases:
1) python3 peer.py 8000 a abcdefgh lmnopqrs aaaaaaaa
python3 peer.py 8001 b abcdefgh lmnopqrs aaaaaaaa
python3 peer.py 8002 c abcdefgh lmnopqrs aaaaaaaa
python3 query.py aaaa 8000 8001 8002 (Passing a key which is not in the list)

2) python3 peer.py 8000 a abcdefgh
python3 peer.py 8001 b abcdefgh lmnopqrs
python3 query.py lmnopqrs 8000 8001 (Passing different number of keys)

3) python3 peer.py 8000 a abcdefgh lmnopqrs aaaaaaaa
python3 peer.py 8001 b lmnopqrs aaaaaaaa abcdefgh
python3 peer.py 8002 c abcdefgh lmnopqrs aaaaaaaa
python3 query.py abcdefgh 8000 8001 8002
Fails because the order of the list of query Ids passed is different for the participant at port
number 8001.
