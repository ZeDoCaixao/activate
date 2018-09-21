#!/usr/bin/python3

# Copyright (C) 2017 Зека-из-Гроба
# Thanks to hypermozg for <https://rutracker.org/forum/viewtopic.php?p=68143490>
#
# License WTFPL
#
# This program is free software. It comes without any warranty, to the extent
# permitted by applicable law.
# You can redistribute it and/or modify it under the terms of the Do What The
# Fuck You Want To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.


# WARNING! #####################################################################
# To make it work put your latest ACTiVATED libsteam_api.so files to:
#  *  $HOME/.local/share/activate/x86/libsteam_api.so
#  *  $HOME/.local/share/activate/x86_64/libsteam_api.so
#
# (Respects your redefined $XDG_DATA_HOME too)
################################################################################

import os
import json
from shutil import copyfile
from hashlib import sha1


def get_crack_path():
    dir = os.getenv("XDG_DATA_HOME")
    if not dir:
        dir = os.path.join(os.getenv("HOME"), ".local", "share")
    return os.path.join(dir, "activate")


def read_config():
    dir = os.getenv("XDG_CONFIG_HOME")
    if not dir:
        dir = os.path.join(os.getenv("HOME"), ".config")
    try:
        with open(os.path.join(dir, "activate.json")) as f:
            return json.load(f)
    except:
        return {}


def get_file_sha1(path):
    with open(path, 'rb') as f:
        data = f.read()
    return sha1(data).hexdigest()


def get_version_from_lib(path):
    checksum = get_file_sha1(path)
    if checksum not in SUMS:
        print("No libsteam_api.so version found. Assuming {} (latest)".format(
            max(SUMS.values())))
        return max(SUMS.values())
    return SUMS[checksum]


def get_lib_arch(path):
    with open(path, "rb") as f:
        data = f.read(5)
    if data[4] == 1:
        return "x86"
    elif data[4] == 2:
        return "x86_64"
    return None


def get_steamapi_version_replace_libs(path):
    versions = []
    for dirpath, _, files in os.walk(path, topdown=False):
        for name in sorted(files):
            libpath = os.path.join(dirpath, name)
            if name.startswith('libsteam_api.so'):
                print(libpath)
                versions.append(get_version_from_lib(libpath))
                if name == "libsteam_api.so":
                    arch = get_lib_arch(libpath)
                    if not arch:
                        continue
                    os.rename(libpath, libpath+".orig")
                    copyfile(
                        os.path.join(get_crack_path(), arch, "libsteam_api.so"),
                        libpath)
    if not versions:
        return None
    return sorted(versions)[-1]


def ask_number(mes):
    r = input(mes)
    try:
        int(r)
    except:
        print("Invalid number. Please input an integer.")
        return ask_number(mes)
    return r


def get_appid(path):
    try:
        for dirpath, _, files in os.walk(path, topdown=False):
            for name in sorted(files):
                if name == "steam_appid.txt":
                    with open(os.path.join(dirpath, name)) as f:
                        data = f.read()
                    return data.strip()
    except:
        pass
    print("No steam_appid.txt found. Please enter game's steam appID.")
    print("It can be found in game page URL, it's numbers")
    print("Search: http://store.steampowered.com/search/?term={}".format(
        "%20".join(os.path.basename(os.path.abspath(path)).split())))
    return ask_number("Input appID: ")


def main():
    config = read_config()
    version = get_steamapi_version_replace_libs('.')
    if version is None:
        print("No libsteam_api.so found. Isn't game DRM-free")
        return
    print(version)
    interfaces = INTERFACES[version]
    appid = get_appid(".")
    ini = INI_TEMPLATE.format(
        interfaces=interfaces,
        appid=appid,
        username=config.get("username", "Cracked")
    )
    with open("activated.ini", "w") as f:
        f.write(ini)


SUMS = {
    "020fcb7ec7dbdfa70a0ad0a70bc19f388563fc23": "1.37",
    "02a9e6ebd01d196e2bd86fb1eff89d47d080314e": "1.37",
    "0669efd72c969bfb101a8b7435a7575a498f073e": "1.38",  # +1.38a
    "0b3343b0a0d0c1d2f0d1457608f480602b32bdf3": "1.35a",
    "0f5b86c1552b1713b3fc9cce8f439f7fcbcbad3f": "1.27",
    "1090a8ffd56cbdafb6a934a6a17bb9d8b415c31d": "1.21",
    "29489b12c24565f2e27c2fbae852957088c90f02": "1.11",
    "3452ef6344c950942f53a28c732873ae329875b6": "1.14",
    "351e7493091df11b73697a91f1cf337f64660104": "1.15",
    "3847e8e66fa1408dac70c05ea8bc56e63c61401a": "1.26a",
    "3ba9e67e5e858980134f42718187287a1f0616a3": "1.17",
    "41effbf1808b75637bb45e8f2e5d1ba74d50fbd1": "1.29a",
    "4263ec03912b0980a6b2fbdc991416aafef99061": "1.30",
    "52fb617c961142207bf8954a71673352eecafc39": "1.35",
    "54ca9f55a6f1c8086f90ebad0d84f173936fbb49": "1.33b",
    "5c6ed1feae178ea985f9a5e52e16bc826e7cd492": "1.27",
    "5ed9e34305f20810e4ddea1ba6d112eeb5343c1f": "1.12",
    "60e67e4b01a8ddc72bdb9b971ba9b283c8398972": "1.06",  # +1.07
    "60e72d4cf29e7beb7fc3312e5491a87ec73c2207": "1.30",
    "660d6f5242b9da8a5d303e31fad80752c250f394": "1.08",
    "67404e25c6d17f747781520565d18625f734ea02": "1.33b",
    "67958100f70696d2fd36ccfc03c51ecd04002ccc": "1.31",
    "7208d97d811eee4926693e1adc5898589f9daa64": "1.31",
    "7c8db70cc15351cff3b100cd7089b59ee0f388f6": "1.13",
    "81d6fa45779ac5a1754285f28e1f58e455896b4c": "1.40",
    "823aecb0337430f5aba824e9e3a87d33643da31e": "1.36",
    "831666ad7435503b46243299289bd6176b556882": "1.34",
    "83419d084c5831a2c789b8733e13f98495a00e99": "1.35a",
    "87ffc5d98cb98f50bc205aaad7970adab7d0e03c": "1.16",
    "8a5628f5ef39cb3589495eb5cfcbf21314780ce2": "1.32",
    "901c13bef70b4b22d16d88708116a5e4501899ff": "1.29a",
    "904fae845b346aba231852bf1bebb306d74a3d8f": "1.38",  # +1.38a
    "9a762eed0eea49fd9068d3515da29001ee4a11e2": "1.39",
    "9a7d04d0b23a148af77cd005b61cd8e730e67c0c": "1.23a",
    "a1820b78cc9feb557b9a2d4b69d04c222af00ef1": "1.40",
    "a887011e976c19f4595ce600dc8195d3d31acd08": "1.10",
    "af65a12a194bb4e770b4e767ef3e0c9eb50e1f78": "1.20",
    "b1c7d8f0734326fe302f42df303e191ebb403548": "1.32",
    "c8be8b6ce69c4b35a4cf7723fb6dd7fee4e872e0": "1.39",
    "c9df74be1fb3cdb6a87c3be7fa90cc9943773ac3": "1.19",
    "ccbd76d92c77d23b7602406bec965b2b6a9abf0c": "1.35",
    "d4c222e1e6086cb134d3e12e2175cb72ba8a87d0": "1.34",
    "d545ebfed842359bc17fcba5df9b6c129598dbe0": "1.09",
    "e4b45a97cfaf1a5be418f665afa55177625bbd26": "1.25",
    "eb89fd00efdc1c5f6f408d2638ce2d32d2301c95": "1.18",
    "ee019e3304fc71bfacf495b3bf87c5a2662cb422": "1.22",
    "f375c0c391efbfbbfb2f5a5b69305a85e842be28": "1.26a",
    "f788ceb733b3f7c490a049544d1f9ca5ce97a2a4": "1.28",
    "fc5644155f4f642efdc2efcafddadf9948072248": "1.28",
    "fe0a15e6596f9ae9bca63f8d8d460888fc90d7f8": "1.36",
}
INTERFACES = {}
INTERFACES["1.00"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION001
SteamClient=SteamClient007
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends003
SteamGameServer=SteamGameServer004
SteamGameServerStats=0
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking002
SteamMatchMakingServers=SteamMatchMakingServers001
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking001
SteamRemoteStorage=0
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser009
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION003
SteamUtils=SteamUtils002
SteamVideo=0"""
INTERFACES["1.01"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION002
SteamClient=SteamClient007
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends003
SteamGameServer=SteamGameServer005
SteamGameServerStats=0
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking002
SteamMatchMakingServers=SteamMatchMakingServers001
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking001
SteamRemoteStorage=0
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser010
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION003
SteamUtils=SteamUtils002
SteamVideo=0"""
INTERFACES["1.02"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION001
SteamClient=SteamClient007
SteamContentServer=SteamContentServer001
SteamController=0
SteamFriends=SteamFriends003
SteamGameServer=SteamGameServer003
SteamGameServerStats=0
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking001
SteamMatchMakingServers=SteamMatchMakingServers001
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=0
SteamRemoteStorage=0
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser008
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION002
SteamUtils=SteamUtils002
SteamVideo=0"""
INTERFACES["1.03"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION002
SteamClient=SteamClient007
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends005
SteamGameServer=SteamGameServer008
SteamGameServerStats=0
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking006
SteamMatchMakingServers=SteamMatchMakingServers001
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking002
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser011
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION004
SteamUtils=SteamUtils002
SteamVideo=0"""
INTERFACES["1.04"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION003
SteamClient=SteamClient008
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends005
SteamGameServer=SteamGameServer008
SteamGameServerStats=0
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking006
SteamMatchMakingServers=SteamMatchMakingServers001
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking002
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser012
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION005
SteamUtils=SteamUtils004
SteamVideo=0"""
INTERFACES["1.05"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION003
SteamClient=SteamClient008
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends005
SteamGameServer=SteamGameServer009
SteamGameServerStats=0
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking007
SteamMatchMakingServers=SteamMatchMakingServers001
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking003
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser012
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION006
SteamUtils=SteamUtils004
SteamVideo=0"""
INTERFACES["1.06"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION003
SteamClient=SteamClient008
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends005
SteamGameServer=SteamGameServer009
SteamGameServerStats=0
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking007
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking003
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser013
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION006
SteamUtils=SteamUtils004
SteamVideo=0"""
INTERFACES["1.07"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION003
SteamClient=SteamClient008
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends005
SteamGameServer=SteamGameServer009
SteamGameServerStats=0
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking007
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking003
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser013
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION006
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.08"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION003
SteamClient=SteamClient009
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends005
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking003
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser013
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION007
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.09"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION003
SteamClient=SteamClient009
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends005
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking003
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser013
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION007
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.10"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION003
SteamClient=SteamClient009
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends006
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking003
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser013
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION007
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.11"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION003
SteamClient=SteamClient009
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends007
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking004
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION002
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser014
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION007
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.12"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION004
SteamClient=SteamClient010
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends008
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking004
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION004
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser014
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION009
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.13"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION004
SteamClient=SteamClient010
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends009
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION004
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION009
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.14"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION004
SteamClient=SteamClient010
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends009
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=0
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION004
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION010
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.15"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION004
SteamClient=SteamClient010
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends009
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION001
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION004
SteamScreenshots=0
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION010
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.16"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION004
SteamClient=SteamClient011
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends009
SteamGameServer=SteamGameServer010
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION001
SteamInventory=0
SteamMasterServerUpdater=SteamMasterServerUpdater001
SteamMatchMaking=SteamMatchMaking008
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION004
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION001
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION010
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.17"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION004
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends011
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION001
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION005
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION001
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION010
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.18"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION005
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends011
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION001
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION006
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION001
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION010
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.19"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION005
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends011
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION001
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION006
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION001
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION010
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.20"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION005
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends013
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION001
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION008
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION001
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.21"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION005
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends013
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION001
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION008
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION001
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.22"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION005
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends013
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION010
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION001
SteamUGC=0
SteamUnifiedMessages=0
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.23a"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION005
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends013
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION010
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=0
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser016
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils005
SteamVideo=0"""
INTERFACES["1.25"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION005
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=0
SteamFriends=SteamFriends013
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION011
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=0
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser017
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils006
SteamVideo=0"""
INTERFACES["1.26a"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION006
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends014
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION001
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser017
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils006
SteamVideo=0"""
INTERFACES["1.27"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION006
SteamClient=SteamClient012
SteamContentServer=SteamContentServer002
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends014
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION001
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser017
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils006
SteamVideo=0"""
INTERFACES["1.28"] = """SteamAppList=0
SteamApps=STEAMAPPS_INTERFACE_VERSION006
SteamClient=SteamClient012
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends014
SteamGameServer=SteamGameServer011
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=0
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION001
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser017
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils006
SteamVideo=0"""
INTERFACES["1.29a"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION006
SteamClient=SteamClient014
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends014
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=0
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION002
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser017
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=0"""
INTERFACES["1.30"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION006
SteamClient=SteamClient015
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends014
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=0
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION002
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser017
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=0"""
INTERFACES["1.31"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION006
SteamClient=SteamClient016
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends014
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_002
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=0
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION003
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser017
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=0"""
INTERFACES["1.32"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION007
SteamClient=SteamClient017
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends015
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_002
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION003
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser018
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.33b"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION007
SteamClient=SteamClient017
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends015
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION005
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser018
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.34"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION007
SteamClient=SteamClient017
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends015
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION012
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION007
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser018
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.35"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION007
SteamClient=SteamClient017
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends015
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION013
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION007
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser018
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.35a"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION007
SteamClient=SteamClient017
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends015
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION013
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION007
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser018
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.36"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION007
SteamClient=SteamClient017
SteamContentServer=0
SteamController=STEAMCONTROLLER_INTERFACE_VERSION
SteamFriends=SteamFriends015
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMasterServerUpdater=0
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION013
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION007
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser018
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils007
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.37"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION008
SteamAppTicket=STEAMAPPTICKET_INTERFACE_VERSION001
SteamClient=SteamClient017
SteamController=SteamController003
SteamFriends=SteamFriends015
SteamGameCoordinator=SteamGameCoordinator001
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION013
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION002
SteamUGC=STEAMUGC_INTERFACE_VERSION008
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser019
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils008
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.38"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION008
SteamAppTicket=STEAMAPPTICKET_INTERFACE_VERSION001
SteamClient=SteamClient017
SteamController=SteamController004
SteamFriends=SteamFriends015
SteamGameCoordinator=SteamGameCoordinator001
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION014
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION003
SteamUGC=STEAMUGC_INTERFACE_VERSION009
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser019
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils008
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.38a"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION008
SteamAppTicket=STEAMAPPTICKET_INTERFACE_VERSION001
SteamClient=SteamClient017
SteamController=SteamController004
SteamFriends=SteamFriends015
SteamGameCoordinator=SteamGameCoordinator001
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION014
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION003
SteamUGC=STEAMUGC_INTERFACE_VERSION009
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser019
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils008
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.39"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION008
SteamAppTicket=STEAMAPPTICKET_INTERFACE_VERSION001
SteamClient=SteamClient017
SteamController=SteamController005
SteamFriends=SteamFriends015
SteamGameCoordinator=SteamGameCoordinator001
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V001
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION014
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION003
SteamUGC=STEAMUGC_INTERFACE_VERSION009
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser019
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils008
SteamVideo=STEAMVIDEO_INTERFACE_V001"""
INTERFACES["1.40"] = """SteamAppList=STEAMAPPLIST_INTERFACE_VERSION001
SteamApps=STEAMAPPS_INTERFACE_VERSION008
SteamAppTicket=STEAMAPPTICKET_INTERFACE_VERSION001
SteamClient=SteamClient017
SteamController=SteamController005
SteamFriends=SteamFriends015
SteamGameCoordinator=SteamGameCoordinator001
SteamGameServer=SteamGameServer012
SteamGameServerStats=SteamGameServerStats001
SteamHTMLSurface=STEAMHTMLSURFACE_INTERFACE_VERSION_003
SteamHTTP=STEAMHTTP_INTERFACE_VERSION002
SteamInventory=STEAMINVENTORY_INTERFACE_V002
SteamMatchMaking=SteamMatchMaking009
SteamMatchMakingServers=SteamMatchMakingServers002
SteamMusic=STEAMMUSIC_INTERFACE_VERSION001
SteamMusicRemote=STEAMMUSICREMOTE_INTERFACE_VERSION001
SteamNetworking=SteamNetworking005
SteamRemoteStorage=STEAMREMOTESTORAGE_INTERFACE_VERSION014
SteamScreenshots=STEAMSCREENSHOTS_INTERFACE_VERSION003
SteamUGC=STEAMUGC_INTERFACE_VERSION010
SteamUnifiedMessages=STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamUser=SteamUser019
SteamUserStats=STEAMUSERSTATS_INTERFACE_VERSION011
SteamUtils=SteamUtils009
SteamVideo=STEAMVIDEO_INTERFACE_V002"""

INI_TEMPLATE = """[Settings]
### Game identifier - http://store.steampowered.com/app/{appid}
### Game data is stored at ~/.local/share/Steam/ACTiVATED/{appid}
AppId={appid}
UserName={username}
Language=english

[Interfaces]
{interfaces}

[DLC]
DLCUnlockall=1
### Identifiers for DLCs
#ID=Name
"""

if __name__ == "__main__":
    main()
