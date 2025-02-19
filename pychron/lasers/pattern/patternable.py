# ===============================================================================
# Copyright 2012 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
from __future__ import absolute_import
from traits.api import Instance, DelegatesTo, List, Str

# import apptools.sweet_pickle as pickle
import six.moves.cPickle as pickle

# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.lasers.pattern.patterns import Pattern
from pychron.managers.manager import Manager


class Patternable(Manager):
    pattern = Instance(Pattern)
    pattern_name = DelegatesTo("pattern", prefix="name")
    selected_pattern_name = Str
    patterns = List

    def _load_pattern(self, fileobj, path):
        """
        unpickle fileobj as a pattern
        """
        try:
            obj = pickle.load(fileobj)
            self.pattern = obj
            self.pattern.path = path
            self.selected_pattern_name = self.pattern_name
            return obj
        except (pickle.PickleError, Exception) as e:
            import traceback

            traceback.print_exc()
            self.debug("load pattern:{}".format(e))
        finally:
            fileobj.close()


# ============= EOF =============================================
