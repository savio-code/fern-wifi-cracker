#-------------------------------------------------------------------------------
# Name:        Mozilla Cookies Engine
# Purpose:     Mozilla Firefox Cookie Engine
#
# Author:      Saviour Emmanuel Ekiko
#
# Created:     20/07/2012
# Copyright:   (c) Fern Wifi Cracker 2012
# Licence:     <GNU GPL v3>
#
#
#-------------------------------------------------------------------------------
# GNU GPL v3 Licence Summary:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


# PURPOSE:
#-------------------------------------------------------------------------------
# This API was written by reverse engineering the mozilla firefox program using
# IDA Pro and OllyDBG,This platform independent api allows commuication with mozillas
# Sqlite databases by hooking into its DLL or SO objects (libmozsqlite3.so  | mozsqlite3.dll)
# Hooking and using the DLL is important because using the python's sqlite3 library
# fails to communicate with the cookie database, and also firefox changes its database
# format on each release. This api communicates with the cookie database no matter
# what changes are made.
#
# Offset 0x00F25210 of xull.dll (windows) <- OllyDBG
#-------------------------------------------------------------------------------

import os
import time
from ctypes import *

# int __cdecl sqlite3_open(const char *filename, sqlite3 **ppDb)
# sqlite3_mutex *__cdecl sqlite3_db_mutex(sqlite3 *db)
# int __cdecl sqlite3_prepare_v2(sqlite3 *db, const char *zSql, int nBytes, sqlite3_stmt **ppStmt, const char **pzTail)

# CREATE TABLE moz_cookies (id INTEGER PRIMARY KEY, baseDomain TEXT, name TEXT, value TEXT, host TEXT, path TEXT, expiry INTEGER, lastAccessed INTEGER, creationTime INTEGER, isSecure INTEGER, isHttpOnly INTEGER, CONSTRAINT moz_uniqueid UNIQUE (name, host, path))

class Mozilla_Cookie_Core(object):
    def __init__(self):
        self.shared_library = "libmozsqlite3.so"                        # Firefox SQlite 3 Database library (Linux = ibmozsqlite3.so || Windows = mozsqlite3.dll)
        self.cookie_database = str()                                    # /root/.mozilla/firefox/nq474mcm.default/cookies.sqlite (Use self.get_Cookie_Path() to file path)
        self.mozilla_install_path = "/opt/firefox/"                     # Linux = /opt/firefox/  || Windows = C:\Program Files\Mozilla Firefox\
        self._library = object()                                        # LoadLibrary("libmozsqlite.so")


    def _get_Database_Pointer(self):
        '''Returns Database pointer to functions'''
        return_code = c_int()
        database_ptr = pointer(c_int())
        filename = c_char_p(self.cookie_database)
        self._library = cdll.LoadLibrary(self.mozilla_install_path + self.shared_library)   # LoadLibrary("libmozsqlite.so")
        return_code = self._library.sqlite3_open(filename,addressof(database_ptr))          # Mozilla Firefox offset 0x00F25210 from xul.dll (firefox uses sqlite3_open_v2())
        if(return_code):
            error = cast(self._library.sqlite3_errmsg(database_ptr),c_char_p)
            raise Fern_Mozilla_Exception(error.value)                                       # (char*)(sqlite_errmsg(database_ptr))
        return(database_ptr)                                                                # return();  Return pointer to database


    def execute_query(self,sql_statement):
        '''Executes raw query into database and returns entry
            list() if any'''
        database_ptr = self._get_Database_Pointer()
        ppStmt = pointer(c_buffer(0x512))
        sql_code = c_char_p()
        sql_code.value = sql_statement
        return_code = self._library.sqlite3_prepare_v2(database_ptr,sql_code,0xFFFFFFFF,addressof(ppStmt),0x0)   # Mozilla Firefox offset 0x00F1E106 from xul.dll
        if(return_code == 0):
            return_list = []
            while(self._library.sqlite3_step(ppStmt) == 100):                                  # 100 = SQLITE_OK ; sqlite3_step(mem_hash)
                row_count = self._library.sqlite3_column_count(ppStmt)

                temp = []
                for row in xrange(row_count):
                    row_data = (cast(self._library.sqlite3_column_text(ppStmt, row),c_char_p)) # char* _cdecl sqlite3_column_text(sqlite3_strp** obj,int row)
                    temp.append(row_data.value)
                return_list.append(tuple(temp))
                temp = []

            return(return_list)
            self._library.sqlite3_finalize(ppStmt)
        else:
            error = cast(self._library.sqlite3_errmsg(database_ptr),c_char_p)
            raise Fern_Mozilla_Exception(error.value)                                 # (char*)(sqlite_errmsg(database_ptr))
        self._library.sqlite3_close(addressof(database_ptr))


    # Mozilla Cookie entry format
    #
    # ('14', 'scorecardresearch.com', 'UID', '2baec64d-23.63.99.90-1342553308', '.scorecardresearch.com', '/', '1404761306', '1342815702910000', '1342553306190000', '0', '0')
    # (id_number,baseDomain,name,value,host,path,expiry,lastAccessed,creationTime,isSecure,isHttpOnly)
    #


    def calculate_mozilla_creationTime(self):
        crude_index = "0123456789"
        creation_time = str(int(time.time()))
        for add in xrange(16 - (len(creation_time) + 3)):
            creation_time += crude_index[add]
        creation_time += "000"
        return(creation_time)



    def insert_Cookie_Values(self,baseDomain,name,value,host,path,isSecure,isHttpOnly):
        '''Stores cookies into the moz_cookies table
        e.g "foobar.com","UID","1235423HYFFDTWB=YTER",".foobar.com","/","0","0"
        '''
        sql_code_a = "select max(id) from moz_cookies"

        response = self.execute_query(sql_code_a)[0][0]
        if(response):
            id_number = str(int(response) + 1)                           # calculates the next id number
        else:
            id_number = str(1)

        creationTime = self.calculate_mozilla_creationTime()    # 1342948082 + 023 + 0000 = (length == 16)
        lastAccessed = creationTime

        expiry = str(int(time.time()) + 1065600)                # (Sun Jul 22 09:08:42 2012) -> (Fri Aug 3 17:45:51 2012) 12 days

        sql_code_b = "insert into moz_cookies values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        sql_code_b = sql_code_b % (id_number,baseDomain,name,value,host,path,expiry,lastAccessed,creationTime,isSecure,isHttpOnly)
        self.execute_query(sql_code_b)



    def get_Cookie_Path(self,cookie_name):
        '''Finds the cookie path from user's profile
           sets cookie_database variable to cookie path'''
        cookie_path = str()
        userprofile = os.path.expanduser("~")
        for root,direc,files in os.walk(userprofile,True):
            if((cookie_name in files) and ("firefox" in root.lower())):
                cookie_path = root + os.sep + cookie_name
                self.cookie_database = cookie_path
                return(cookie_path)


    def find_mozilla_lib_path(self):
        '''Finds the path to the dll or shared object'''
        shared_object_path = str()
        for root,direc,files in os.walk(os.sep,True):
            if((self.shared_library in files) and ("firefox" in root.lower())):
                shared_object_path = root + os.sep
                self.mozilla_install_path = shared_object_path
                return(shared_object_path)


class Fern_Mozilla_Exception(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return(self.value)


# USAGE:

# cookie = Mozilla_Cookie_Core()
#
# cookie.shared_library = "mozsqlite3.dll"
# cookie.get_Cookie_Path("cookies.sqlite")  | cookie.cookie_database = "D:\\cookies.sqlite"
# cookie.find_mozilla_lib_path()            # its best to cache once path is found, might take time to load
# cookie.mozilla_install_path = "C:\\Program Files (x86)\\Mozilla Firefox\\"
#
# retrun_list = cookie.execute_query("select * from moz_cookies")
# for entries in retrun_list:
#    print(entries)



