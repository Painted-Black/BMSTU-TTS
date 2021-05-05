from modules.database.db_access_manager import db_access_manager
import logging
import pickle
from confg import *


def parse_consonants_pronunciation(string: str) -> (str, []):
    buffer = string.split(':')
    if len(buffer) != 2:
        return None, None
    buffer[1] = buffer[1].strip('\n')
    key = buffer[0]
    values = buffer[1].split(',')
    if len(values) < 1:
        return None, None
    return key, [values]


def parse_ph_exc_string(string: str) -> (str, str):
    string = string.rstrip('\n')
    buffer = string.split(' ')
    if len(buffer) != 2:
        return None, None
    key = buffer[0]
    value = buffer[1]
    key = key.strip()
    value = value.strip()
    return key, value


def parse_jo_string(string: str) -> (str, []):
    string = string.rstrip('\n')
    buffer = string.split('#')
    if len(buffer) != 2:
        return None, None
    buffer[1] = buffer[1].strip('\n')
    key = buffer[0]
    value_buff = buffer[1]
    values = value_buff.split(',')
    for i in range(len(values)):
        values[i] = values[i].strip()
    return key, values


def parse_stress_string(string: str) -> (str, []):
    string = string.rstrip('\n')
    buffer = string.split('#')
    if len(buffer) != 2:
        return None, None
    buffer[1] = buffer[1].strip('\n')
    key = buffer[0]
    value_buff = buffer[1]
    values = value_buff.split(',')
    for i in range(len(values)):
        values[i] = values[i].strip()
    return key, [values]


def parse_abbrev_string(string: str) -> (str, []):
    buffer = string.split('><')
    if len(buffer) < 2:
        return None, None
    for i in range(len(buffer)):
        buffer[i] = buffer[i].strip('<').strip('\n').strip('>')

    key = buffer[0]
    values = []
    for i in range(1, len(buffer)):
        definition_buffer = buffer[i].split(',')
        if len(definition_buffer) < 1 or len(definition_buffer) > 4:
            return None, None
        pronunciation = definition_buffer[0].rstrip(']').lstrip('[')
        declination = definition_buffer[1]
        genus = definition_buffer[2]
        if Genus().build(genus) is None:
            return None, None
        definition = definition_buffer[3]
        values.append([pronunciation, declination, genus, definition])
    return key, values


def fill_db(filename: str, dbname: str, db_path: str, parse_func) -> bool:
    database = db_access_manager.create_db(db_path=db_path, name=dbname)
    if database is None:
        logging.error('fill_db(): Cannot create ', dbname, 'database at ', db_path)
        return False
    with open(filename) as source_file:
        if source_file is None:
            logging.error('fill_db(): Cannot open file ', filename)
            return False
        line = source_file.readline()
        idx = 1
        while line != '':
            key, value = parse_func(line)
            if key is None or value is None:
                logging.error('fill_db(): Cannot parse string {0} from file {1}'.format(idx, filename))
                return False
            db_contains = database.read(pickle.dumps(key))
            if db_contains is not None:
                old_value = pickle.loads(db_contains)
                if isinstance(old_value, list):
                    old_value.append(value[0])
                    value = old_value
            database.write(pickle.dumps(key), pickle.dumps(value))
            line = source_file.readline()
            idx += 1
    database.close()
    return False
