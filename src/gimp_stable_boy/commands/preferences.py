#!/usr/bin/env python
#
# Stable Boy
# Copyright (C) 2022 Torben Giesselmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gimpfu
import gimp_stable_boy as sb
from _command import PluginCommand


class PreferencesCommand(PluginCommand):
    metadata = PluginCommand.CommandMetadata(
        sb.__prefix__ + "-prefs",
        sb.__name__ + sb.__version__ + " - Preferences",
        sb.__description__,
        sb.__author__,
        sb.__author__,
        sb.__year__,
        sb.__menu__ + "/Preferences",
        "*",
        [(gimpfu.PF_STRING, 'api_base_url',
            'API URL', sb.config.DEFAULT_API_URL)],
        [],)

    def __init__(self, **kwargs):
        PluginCommand.__init__(self, **kwargs)
        self.prefs = kwargs

    def run(self):
        sb.gimp.save_prefs(sb.config.PREFERENCES_SHELF_GROUP, **self.prefs)
