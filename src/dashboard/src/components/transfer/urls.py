# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
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

from django.conf.urls.defaults import patterns

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('components.transfer.views',
    (r'^$', 'transfer_grid'),
    (r'(?P<uuid>' + UUID_REGEX + ')/$', 'transfer_detail'),
    (r'(?P<uuid>' + UUID_REGEX + ')/delete/$', 'transfer_delete'),
    (r'(?P<uuid>' + UUID_REGEX + ')/microservices/$', 'transfer_microservices'),
    (r'status/$', 'transfer_status'),
    (r'status/(?P<uuid>' + UUID_REGEX + ')/$', 'transfer_status'),
    (r'browser/$', 'transfer_browser')
)