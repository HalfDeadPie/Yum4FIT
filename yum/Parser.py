import configparser
import json
import sys

import os

from yum import CONSTANTS


def parse(file):
    """
    Parse the file
    :param file: path to file
    :return: fulfilled parser
    """
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(file,encoding='utf8')
    return parser

def getUsername(username, config):
    """
    Username for instagram
    :param username: Username from previous functions
    :param config: config file
    :return: Username
    """
    if(username == None):
        parser = parse(config)
        if(parser.has_section('instagram')):
            return parser['instagram']['username']
    else:
        return username

def getPassword(password, config):
    """
    Get password from config file
    :param password: Pre-filled password from CLI
    :param config: config file
    :return: str
    """
    if(password == None):
        parser = parse(config)
        if(parser.has_section('instagram')):
            return parser['instagram']['password']
    else:
        return password

def exitBadConfig():
    """
    Exit application because of error with config
    """
    sys.exit("Something is wrong with the configuration file")

def get(config, section, field):
    """
    Get value from section and field in .cfg file
    :param config: file
    :param section: section
    :param field: field
    :return: value as String
    """
    if(field != None):
        parser = parse(config)
        if(len(parser.sections()) == 0 and config!=CONSTANTS.FRIENDS_FILE):
            exitBadConfig()
        if(parser.has_section(section) and parser.has_option(section,field)):
            return parser[section][field]
        else:
            return None
    else:
        raise IndexError('Field does not exists in config file!')

def exists(file):
    parser = parse(file)
    if (len(parser.sections()) == 0):
        return False
    else:
        return True

def getParameter(config, field):
    """
    Special function to get parameter
    :param config: config file
    :param field: field in config file
    :return:
    """
    parser = parse(config)
    if(parser.has_section('parameters')):
        try:
            return parser['parameters'][field]
        except:
            return None

def updateSave(file, section, fields, value):
    """
    Update save file
    :param file: file for save (default=savegame.cfg)
    :param section: sections of the file
    :param fields: fields of the file
    :param value: values of the file
    """

    # lets create that config file for next time...

    cfgfile = open(file, 'w+', encoding="utf8")

    Config = configparser.ConfigParser()
    # add the settings to the structure of the file, and lets write it out...
    Config.add_section(section)
    for i in range(0, len(fields)):
        Config.set(section, fields[i], value[i])
    Config.write(cfgfile)
    cfgfile.close()

def updateSection(file, section, fields, value):
    """
    Update section in file
    :param file: target file
    :param section: updating sectiong
    :param fields: all fields for section
    :param value: all values for fields
    """
    readed = parse(file)
    if section in readed.sections():
        sections = readed.sections()
        options = []
        i = 0
        dict = {}
        for s in sections:
            options.append(readed.options(s))
            dict[s] = {}
            for o in options[i]:
                dict[s][o] = readed[s][o]
            i+=1

        j = 0
        dict[section][fields] = value
        refresh(file,dict)
    else:
        cfgfile = open(file, 'a')
        Config = configparser.ConfigParser()
        # add the settings to the structure of the file, and lets write it out...
        Config.add_section(section)
        Config.set(section, fields, value)
        Config.write(cfgfile)
        cfgfile.close()

def refresh(file, dict):
    """
    Refreshes file using dictionary
    :param file: target file
    :param dict: source dictionary
    """
    cfgfile = open(file, 'w')
    Config = configparser.ConfigParser()

    for key, value in dict.items():
        Config.add_section(key)
        for innerKey, innerValue in dict[key].items():
            Config.set(key, innerKey, innerValue)

    Config.write(cfgfile)
    cfgfile.close()

def has_field(file, section, field):
    """
    Check if file has field
    :param file: target file
    :param section: section of the file
    :param field: target field
    :return: True or False
    """
    reader = parse(file)
    if (reader.has_section(section) and reader.has_option(section, field)):
        return True
    else:
        return False

def getConfirmated(friendsFile):
    parser = parse(friendsFile)
    sections = parser.sections()
    confirmated = []
    if (len(sections) == 0):
        return None
    else:
        for friend in sections:
            for food in parser.options(friend):
                if parser[friend][food] == 'yes':
                    confirmated.append(friend +" "+ food)
        return confirmated

def buildJson(self, fields, values):
    """
    Builds json
    :param fields: fields for json
    :param values: values for fields in json
    :return: json
    """
    i = 0
    data = {}
    for field in fields:
        data[field] = values[i]
        i += 1

    json_data = json.dumps(data)
    return json_data