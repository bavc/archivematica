#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2013 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage FPRClient
# @author Joseph Perry <joseph@artefactual.com>
from addLinks import addLinks
from optparse import OptionParser
from getFromRestAPI import getFromRestAPI
import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface

databaseInterface.printSQL = True


def create(table, entry):
    global maxLastUpdate
    sets = []
    for key, value in entry.iteritems():
        if key == "resource_uri":
            continue
        if key == "uuid":
            key = "pk"
        if key == "lastmodified" and value > maxLastUpdate:
            maxLastUpdate = value
        #print type(value)
        if value == None:
            sets.append("%s=NULL" % (key))
        elif isinstance(value, int):
            sets.append("%s=%s" % (key, value))
        elif isinstance(value, unicode):
            sets.append("%s='%s'" % (key, databaseInterface.MySQLdb.escape_string(value)))
        elif isinstance(value, str):
            sets.append("%s='%s'" % (key, databaseInterface.MySQLdb.escape_string(value)))
            
    sets = ", ".join(sets)
    sql = """INSERT INTO %s SET %s;""" % (table, sets)
    #print sql
    databaseInterface.runSQL(sql)
    
             




if __name__ == '__main__':
    global maxLastUpdate
    maxLastUpdate = "2000-01-01T00:00:00"
    maxLastUpdateAtStart = maxLastUpdate
    databaseInterface.runSQL("SET foreign_key_checks = 0;")
    for x in [
        ("CommandRelationships", "http://fprserver/api/fpr/v1/FPRCommandRelationships/"),
        ("FileIDsBySingleID", "http://fprserver/api/fpr/v1/FPRFileIDsBySingleID/"),
        ("FileIDs", "http://fprserver/api/fpr/v1/FPRFileIDs/"),
        ("Commands", "http://fprserver/api/fpr/v1/FPRCommands/"),
        ("CommandTypes", "http://fprserver/api/fpr/v1/FPRCommandTypes/"),
        ("CommandClassifications", "http://fprserver/api/fpr/v1/FPRCommandClassifications/"),
        ("CommandsSupportedBy", "http://fprserver/api/fpr/v1/FPRCommandsSupportedBy/"),
        ("FileIDTypes", "http://fprserver/api/fpr/v1/FPRFileIDTypes/"),
        ("Groups", "http://fprserver/api/fpr/v1/FPRGroups/"),
        ("FileIDGroupMembers", "http://fprserver/api/fpr/v1/FPRFileIDGroupMembers/"),
        ("SubGroups", "http://fprserver/api/fpr/v1/FPRSubGroups/"),
        ("DefaultCommandsForClassifications", "http://fprserver/api/fpr/v1/FPRDefaultCommandsForClassifications/")
    ]:
        table, url = x
        params = {"format":"json", "order_by":"lastmodified", "lastmodified__gte":maxLastUpdateAtStart, "limit":"0"}
        entries = getFromRestAPI(url, params, verbose=False, auth=None)
        #print "test", entries
        for entry in entries:
            #print table, entry
            
            #check if it already exists
            sql = """SELECT pk FROM %s WHERE pk = '%s'""" % (table, entry['uuid'])
            if databaseInterface.queryAllSQL(sql):
                #pass
                continue
            
            #If updating a disabled entry, it will continue to be disabled.
            if entry['replaces'] != None:
                 sql = """SELECT enabled FROM %s WHERE pk = '%s';""" % (table, entry['uuid'])
                 enabled=databaseInterface.queryAllSQL(sql)[0][0]
                 if not enabled:
                     entry['enabled'] = 0
            create(table, entry) 
            
                
            
    #createLinks()
    #update last modified time
    addLinks()
    databaseInterface.runSQL("SET foreign_key_checks = 1;")
    print maxLastUpdate