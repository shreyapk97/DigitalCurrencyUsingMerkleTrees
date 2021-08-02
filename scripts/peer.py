'''On first terminal:  sudo python3 peer.py 8000 a abcdefgh lmnopqrs
where abcdefgh and lmnopqrs are the IDs

On another terminal : sudo python3 peer.py 8001 b abcdefgh lmnopqrs
Third terminal : sudo python3 query.py abcdefgh 8000 8001'''

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from generate_random_id import generate_id
import json
import sys
import hashlib
from datetime import datetime
import uuid 
import sqlite3

leafHash = []

port_number = int(sys.argv[1])
choice=sys.argv[2]

list_id_for_peers=sys.argv[3:]
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(('localhost', port_number),requestHandler=RequestHandler)
server.register_introspection_functions()

def doubleSha256(input):
	
	json_input=json.dumps(input)
	json_input2=json_input.encode('utf-8')
	return hashlib.sha256(json_input2).hexdigest() 
server.register_function(doubleSha256, 'doubleSha256')
	
    
def findMerkleRoot(leafHash):
	hash = []
	hash2 = []
	if len(leafHash) % 2 != 0:                            
		leafHash.extend(leafHash[-1:])
        
	for leaf in sorted(leafHash):                        
		hash.append(leaf)
		if len(hash) % 2 == 0:                          
			hash2.append(doubleSha256(hash[0]+hash[1]))   
			hash == []                                    
	if len(hash2) == 1:                                   
		return hash2
	else:
		return findMerkleRoot(hash2)  
server.register_function(findMerkleRoot,'root')


class MyFuncs:
	def mul(self, x, y):
		return x * y
server.register_instance(MyFuncs())
	
#server.register_function(encode_id_for_peer,'encode')

def authenticate(encoded_id):
	#des = DES.new('01234567', DES.MODE_ECB)
	#print("about to decrypt")
	plain_text=encoded_id
	if(plain_text not in list_id_for_peers):
		print("client not authenticated")
		return 0
	return 1	
server.register_function(authenticate,'authenticate')
	
def select_table():
	with sqlite3.connect('participants_db.db') as conn :
		cur=conn.cursor()
		c=cur.execute("SELECT * FROM PARTICIPANT_BALANCE")
		data=c.fetchall()
	return data
			
server.register_function(select_table,'select_table')

def read_db(p):
	COLUMN='BALANCE'
	COLUMN2='NAME'
	#p='a'
	with sqlite3.connect('participants_db.db') as conn :
		cur=conn.cursor()
		#c=cur.execute("SELECT" + COLUMN + "from PARTICIPANT_BALANCE where" + COLUMN2 +"=?",(p,))
		c=cur.execute("SELECT "+COLUMN+" FROM PARTICIPANT_BALANCE where "+COLUMN2+"=?", (p,))
		data=c.fetchone()
	return int(data[0])
server.register_function(read_db,'read')
	
def update_db(bal,p):
	COLUMN='BALANCE'
	COLUMN2='NAME'
	with sqlite3.connect('participants_db.db') as conn :
		cur=conn.cursor()
		#cur.execute("UPDATE PARTICIPANT_BALANCE SET BALANCE=? where NAME=?",(bal,p))
		cur.execute("UPDATE PARTICIPANT_BALANCE SET BALANCE=? WHERE NAME=?", (bal,p))
		c=cur.execute("SELECT "+COLUMN+" FROM PARTICIPANT_BALANCE where "+COLUMN2+"=?", (p,))
		data=c.fetchone()
	return int(data[0])
server.register_function(update_db,'update')

def build_tree():	
	directory = "/home/pr/Documents/final_project/Input"
	new_f_1=directory+"/"+"dict_input_" + choice + ".txt"
	with open(new_f_1) as file:
		lines = [line.strip() for line in file]
		print("\n")
		print("File is",lines)
		print("\n")
		print("#################################################################################################################################")
		print("\n")
	total=0
	list_of_transactions=[]
	for line in lines :
		input1=line.split()
		print("Input is:",input1)
		print("\n")
		involved=input1[0]
		if(choice!=involved[0]):
			print("Wrong file opened")
		s_bal=int(input1[1])
		p_bal=int(input1[2])
		amount =int(input1[3])
		action=input1[4] #i want to purchase
		if("purchase" in action and choice in action):
			purchaser=choice
			seller=involved[1]
			print("Purchaser is",purchaser)
			print("\n")
			print("Seller is",seller)
			print("\n")
			s_bal=read_db(seller)
			p_bal=read_db(purchaser)
			
			new_p_bal=p_bal-amount
			new_s_bal=s_bal+amount
			total=total+amount
			update_db(new_s_bal,seller)
			update_db(new_p_bal,purchaser)
		elif("sell" in action and choice in action):
			seller=choice
			purchaser=involved[1]
			print("Seller is",seller)
			print("\n")
			print("Purchaser is",purchaser)
			print("\n")
			
			s_bal=read_db(seller)
			p_bal=read_db(purchaser)
			new_p_bal=p_bal-amount
			new_s_bal=s_bal+amount
			update_db(new_s_bal,seller)
			update_db(new_p_bal,purchaser)
		elif("sell" in action and choice not in action):
			purchaser=choice
			seller=involved[1]
			print("Purchaser is",purchaser)
			print("\n")
			print("Seller is",seller)
			print("\n")
				
			s_bal=read_db(seller)
			p_bal=read_db(purchaser)
			new_p_bal=p_bal-amount
			new_s_bal=s_bal+amount
			total=total+amount
			update_db(new_s_bal,seller)
			update_db(new_p_bal,purchaser)
				
		elif("purchase" in action and choice not in action):
			seller=choice
			purchaser=involved[1]
			print("Seller is",seller)
			print("\n")
			print("Purchaser is",purchaser)
			print("\n")
				
			s_bal=read_db(seller)
			p_bal=read_db(purchaser)
			new_p_bal=p_bal-amount
			new_s_bal=s_bal+amount
			update_db(new_s_bal,seller)
			update_db(new_p_bal,purchaser)
			
		x=read_db(seller)
		y=read_db(purchaser)
		
				
		t = {}
	

		tid = generate_id()
		print("Transaction ID:",tid)
		pid = generate_id()
		print("Purchaser ID:",pid)
		sid = generate_id()
		print("Seller ID:",sid)
		print("\n")

		t['involved'] = involved
		t['transaction_id'] = tid
		t['purchaser_id'] = pid
		t['seller_id'] = sid
		t['amount'] = amount
		t['action'] = action
	

		t['new_purchaser_balance'] = y
		print("\n")
		print("New_Purchaser_Balance:",y)
		print("\n")
		t['new_seller_balance'] = x
		print("New_Seller_Balance:",x)
		print("\n")
		print("transaction dictionary is",t)
		print("\n")
		print("total amount spent by"+' '+choice+' '+"is"+' '+str(total))
		print("\n")
		now = datetime.now()

		timestamp = datetime.timestamp(now)
		
		t['timestamp']=timestamp
			
		list_of_transactions.append(t)
		print("list of transactions is",list_of_transactions)
		print("\n")
		print("#########################################################################################################################")
		print("\n")
	return list_of_transactions
server.register_function(build_tree,"build")

def create_list_of_hashes(l_transactions):
	for trans in l_transactions:
		leafHash.append(doubleSha256(trans))
	return leafHash
server.register_function(create_list_of_hashes,"create")


	
server.serve_forever()

			

				
			
				
				
			

		
