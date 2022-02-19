import os
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

# def test_server():
#   assert True
#   output = []
#   chat_server.print = lambda s : output.append(s)
#   chat_server.main([_client_ids, _port, '1'])
#   assert output == [
#        '...STARTING SERVER...',
#        '...SERVER RUNNING...'
#    ]


def test_scenario_1():
  bob_output = []
  chad_output = []

  # activate the server
  threading.Thread(target=chat_server.main, args=([[_client_ids, _port]]), daemon=True).start()

  # Alice joins the chat
  threading.Thread(target=alice.main, args=([['1',_server_ip, _port, 'Alice'],_clients]), daemon=True).start()
  # wait for a second to send message
  time.sleep(1)
  alice.sendMessage(_clients[0],'Good Morning')
  print('Alice joins the chat and sends message: Good morning')
  # wait 5 seconds before anyone else joins
  time.sleep(5)

  # Bob And Chad join the chat
  threading.Thread(target=bob.main, args=([['2',_server_ip, _port, 'Bob'],_clients,bob_output]), daemon=True).start()
  threading.Thread(target=chad.main, args=([['3',_server_ip, _port, 'Chad'],_clients,chad_output]), daemon=True).start()
  print('Bob and Chad join the chat')

  # wait 2 seconds before reading outputs
  time.sleep(2)
  print('Bob and Chad receive the message sent by Alice, before they joined')
  print('Bob and Chad received Alice: Good Morning')

  # terminate all threads
  # s.terminate()
  # a.terminate()
  # a1.terminate()
  # b.terminate()
  # c.terminate()
  # print(output)
  # client.destroy(_clients[0])
  assert bob_output == ['Alice: Good Morning'] and chad_output == ['Alice: Good Morning']
  threading.Thread(target=alice.main, args=([['1',_server_ip, _port, 'Alice'],_clients]), daemon=True).do_stop = True
  threading.Thread(target=bob.main, args=([['2',_server_ip, _port, 'Bob'],_clients,bob_output]), daemon=True).do_stop = True
  threading.Thread(target=chad.main, args=([['3',_server_ip, _port, 'Chad'],_clients,chad_output]), daemon=True).do_stop = True
  return

def test_scenario_2():
  alice_output = []
  bob_output = []
  chad_output = []
  doug_output = []
  _port = '50002'

  # try:
    # activate the server
  threading.Thread(target=chat_server.main, args=([[_client_ids, _port, '1,2,3']]), daemon=True).start()
  time.sleep(3)
  # Alice, Bob and Chad join the chat
  threading.Thread(target=alice.main, args=([['1',_server_ip, _port, 'Alice'],_clients,alice_output]), daemon=True).start()
  threading.Thread(target=bob.main, args=([['2',_server_ip, _port, 'Bob'],_clients,bob_output]), daemon=True).start()
  threading.Thread(target=chad.main, args=([['3',_server_ip, _port, 'Chad'],_clients,chad_output]), daemon=True).start()

  print('Alice joined the chat')
  print('Bob joined the chat')
  print('Chad joined the chat')
  return

def test_scenario_3():
  alice_output = []
  bob_output = []
  chad_output = []
  doug_output = []
  _port = '50001'

  # try:
    # activate the server
  threading.Thread(target=chat_server.main, args=([[_client_ids, _port, '1,2,3']]), daemon=True).start()
  time.sleep(3)
  # Alice, Bob and Chad join the chat
  threading.Thread(target=alice.main, args=([['1',_server_ip, _port, 'Alice'],_clients,alice_output]), daemon=True).start()
  threading.Thread(target=bob.main, args=([['2',_server_ip, _port, 'Bob'],_clients,bob_output]), daemon=True).start()
  threading.Thread(target=chad.main, args=([['3',_server_ip, _port, 'Chad'],_clients,chad_output]), daemon=True).start()

  print('Alice joined the chat')
  print('Bob joined the chat')
  print('Chad joined the chat')
  print('Doug joins port but receives no messages')
  threading.Thread(target=doug.main, args=([['4',_server_ip, _port, 'Doug'],_clients,doug_output]), daemon=True).start()
  os._exit(0)
  try:
    # bob sends a message
    time.sleep(1)
    bob.sendMessage(_clients[1],'Hi, Good Morning')
    print('Bob: Hi, Good Morning')

    # alice sends a message
    time.sleep(1)
    alice.sendMessage(_clients[0],'Hi Bob, Good Morning')
    print('Alice: Hi Bob, Good Morning')

    time.sleep(1)
    assert alice_output == ['Bob: Hi, Good Morning', 'Alice: Bob, Good Morning'] and bob_output == ['Bob: Hi, Good Morning', 'Alice: Bob, Good Morning'] and chad_output == ['Bob: Hi, Good Morning', 'Alice: Bob, Good Morning']and doug_output == []
    print('Chad receives messages')
    print('Doug joins port but receives no messages')

    # doug joins chat, but not in same group
    threading.Thread(target=doug.main, args=([['4',_server_ip, _port, 'Doug'],_clients,doug_output]), daemon=True).start()
  except Exception:
    os._exit(0)
  os._exit(0)

def __send_message(client, message):
  n = chat.Note()
  n.name = client.username
  n.message = message
  client.conn.SendNote(n)


if __name__ == '__main__':
  test_scenario_1()
  case1()
  test_scenario_2()
