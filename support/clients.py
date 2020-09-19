"""Возаимодействия с клиентами"""
import json
from pathlib import Path

# file = Path(__file__).parents[1] / "database" / "clientBase.json"


def add_client(info):
    with open('database\\clientBase.json', 'r') as f:
        list_of_clients = json.loads(f.read())
    list_of_clients.append(info)
    with open('database\\clientBase.json', 'w') as f:
        f.write(json.dumps(list_of_clients))


def add_client_req(info):
    with open('database\\clientsRequests.json', 'r') as f:
        list_of_requests = json.loads(f.read())
    list_of_requests.append(info)
    with open('database\\clientsRequests.json', 'w') as f:
        f.write(json.dumps(list_of_requests))


def change_status(id, weekDay, time):
    with open('database\\teachers_data.json', 'r') as f:          # Меняет статус записи у преподавателя
        teachers_data = json.loads(f.read())
    teachers_data[id]['free'][weekDay][time] = False
    with open('database\\teachers_data.json', 'w') as f:
        f.write(json.dumps(teachers_data))
