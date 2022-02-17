import sys
import chat_server
# python uses the same instance to import the same module, importing multiple times for readability
import client as alice
import client as bob
import client as chad
import client as doug
import proto.chat_pb2 as chat
import threading
import time

_client_ids = '1,2,3'
_port = '5000'
_server_ip = '127.0.0.1'
_clients = []


def test_scenario_2():
  alice_output = []
  bob_output = []
  chad_output = []
  doug_output = []

  # activate the server
  threading.Thread(target=chat_server.main, args=([[_client_ids, _port, '1,2,3']]), daemon=True).start()

  # Alice, Bob and Chad join the chat
  threading.Thread(target=alice.main, args=([['1',_server_ip, _port, 'Alice'],_clients,alice_output]), daemon=True).start()
  threading.Thread(target=bob.main, args=([['2',_server_ip, _port, 'Bob'],_clients,bob_output]), daemon=True).start()
  threading.Thread(target=chad.main, args=([['3',_server_ip, _port, 'Chad'],_clients,chad_output]), daemon=True).start()
  print('Alice joined the chat')
  print('Bob joined the chat')
  print('Chad joined the chat')


  # bob sends a message
  time.sleep(1)
  bob.sendMessage(_clients[1],'Hi, Good Morning')
  print('Bob: Hi, Good Morning')

  # alice sends a message
  time.sleep(1)
  alice.sendMessage(_clients[0],'Hi Bob, Good Morning')
  print('Alice: Hi Bob, Good Morning')

  # doug joins chat, but not same group
  threading.Thread(target=doug.main, args=([['4',_server_ip, _port, 'Doug'],_clients,doug_output]), daemon=True).start()

  # reaed all outputs
  time.sleep(1)
  assert alice_output == ['Bob: Hi, Good Morning', 'Alice: Bob, Good Morning'] and bob_output == ['Bob: Hi, Good Morning', 'Alice: Bob, Good Morning'] and chad_output == ['Bob: Hi, Good Morning', 'Alice: Bob, Good Morning']and doug_output == []
  print('Chad receives messages')
  print('Doug joins port but receives no messages')
  return

def __send_message(client, message):
  n = chat.Note()
  n.name = client.username
  n.message = message
  client.conn.SendNote(n)
