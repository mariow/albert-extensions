# -*- coding: utf-8 -*-

"""Copy a new jitsi link into the clipboard

The base url (aka your jisti host) can be configured in ~/.config/albert/jitsi-link/jitsi-link.json

Synopsis: <trigger>""" 
import json
import os
import coolname
from albert import *

__title__ = "jitsi-link"
__version__ = "0.0.1"
__triggers__ = "meet"
__authors__ = "Mario Witte"
__py_deps__ = ["json","coolname"]

iconPath = iconLookup("camera-web")

cfg_fname = "jitsi_link.json"
cfg_dir = os.path.join(configLocation(), __title__)
cfg_file = os.path.join(cfg_dir, cfg_fname)
jitsiBaseUrl = "https://meet.jit.si/"

def initialize():
    global jitsiBaseUrl
    if os.path.exists(cfg_file):
        with open(cfg_file) as json_config:
            jitsiBaseUrl = json.load(json_config)["base_url"]
            print(jitsiBaseUrl)
    else:
        try:
            os.makedirs(cfg_dir, exist_ok=True)
            try:
                with open(cfg_file, "w") as output_file:
                    json.dump({"base_url": jitsiBaseUrl}, output_file)
            except OSError:
                print("There was an error opening the cfgfile: %s" % cfg_file)
        except OSError:
            print("There was an error making the directory: %s" % cfg_dir)

def handleQuery(query):
    if query.isTriggered:
        jitsiLink = generateJitsiLink()
        if jitsiLink is not None:
            jitsiLink = jitsiBaseUrl + jitsiLink
            return getJitsiItem(query, jitsiLink)


def generateJitsiLink():
    return ''.join(x.capitalize() for x in coolname.generate())
        


def getJitsiItem(query, jitsiLink):
    return Item(
        id=__title__,
        icon=iconPath,
        text=jitsiLink,
        subtext="Copy new jitsi link to clipboard",
        actions=[ClipAction("Copy to clipboard", jitsiLink)]
    )
