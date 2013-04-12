#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
#
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.    If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage Dashboard
# @author Joseph Perry <joseph@artefactual.com>

def getNormalizationReportQuery():
    return """
select
    CONCAT(f.fileUUID,' ', fid.pk) AS fileName, f.fileUUID, f.currentLocation , fid.description, fid.validAccessFormat AS 'already_in_access_format', fid.validPreservationFormat AS 'already_in_preservation_format',
    max(if(cc.classification = 'access', t.taskUUID, null)) IS NOT NULL as access_normalization_attempted,
    max(if(cc.classification = 'preservation', t.taskUUID, null)) IS NOT NULL as preservation_normalization_attempted,
    max(if(cc.classification = 'access', t.taskUUID, null)) as access_normalization_task_uuid,
    max(if(cc.classification = 'preservation', t.taskUUID, null)) as preservation_normalization_task_uuid,
    max(if(cc.classification = 'access', t.exitCode, null)) != 0 AS access_normalization_failed,
    max(if(cc.classification = 'preservation', t.exitCode, null)) != 0 AS preservation_normalization_failed,
    max(if(cc.classification = 'access', t.exitCode, null)) as access_task_exitCode,
    max(if(cc.classification = 'preservation', t.exitCode, null)) as preservation_task_exitCode
from
    Files f
    Join
    FilesIdentifiedIDs fii on f.fileUUID = fii.fileUUID
    Join
    FileIDs fid on fii.fileID = fid.pk 
    Join
    CommandRelationships cr on cr.fileID = fid.pk
    Join
    CommandClassifications cc on cr.commandClassification  = cc.pk
    join
    TasksConfigs tc on tc.taskTypePKReference = cr.pk
    join
    MicroServiceChainLinks ml on tc.pk = ml.currentTask
    join
    Jobs j on j.MicroServiceChainLinksPK = ml.pk and j.sipUUID = f.sipUUID
    join
    Tasks t on t.jobUUID = j.jobUUID
where
    f.sipUUId = %s and f.fileGrpUse in ('original', 'service')
    and cc.classification in ('preservation', 'access')
    AND ml.pk NOT IN (SELECT MicroserviceChainLink FROM DefaultCommandsForClassifications)
group by
    fid.pk;"""

#TODO and fid.fileIDType like '16ae%'
#variableValue FROM UnitVariables WHERE unitType = 'SIP' AND variable = 'normalizationFileIdentificationToolIdentifierTypes' AND unitUUID = '';

if __name__ == '__main__':
    import sys
    uuid = "'%s'" % (sys.argv[1])
    sys.path.append("/usr/lib/archivematica/archivematicaCommon")
    import databaseInterface
    print "testing normalization report"
    sql = getNormalizationReportQuery()
    sql = sql % ( uuid)
    rows = databaseInterface.queryAllSQL(sql)
    for row in rows:
        print row
        print
