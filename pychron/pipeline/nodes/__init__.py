# ===============================================================================
# Copyright 2015 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
# ============= standard library imports ========================
# ============= local library imports  ==========================

from pychron.pipeline.nodes.audit import AuditNode
from pychron.pipeline.nodes.bulk_edit import BulkEditNode
from pychron.pipeline.nodes.correction_factors import CorrectionFactorsNode
from pychron.pipeline.nodes.data import UnknownNode, ReferenceNode, FluxMonitorsNode, ListenUnknownNode, CSVNode, \
    InterpretedAgeNode, CalendarUnknownNode
from pychron.pipeline.nodes.detector_yield import YieldNode
from pychron.pipeline.nodes.diff import DiffNode
from pychron.pipeline.nodes.dvc_history import DVCHistoryNode
from pychron.pipeline.nodes.email_node import EmailNode
from pychron.pipeline.nodes.figure import IdeogramNode, SpectrumNode, SeriesNode, InverseIsochronNode, \
    VerticalFluxNode, XYScatterNode, RadialNode, RegressionSeriesNode, HistoryIdeogramNode
from pychron.pipeline.nodes.filter import FilterNode
from pychron.pipeline.nodes.find import FindReferencesNode, FindFluxMonitorsNode, FindVerticalFluxNode, \
    FindBlanksNode, FindRepositoryAnalysesNode
from pychron.pipeline.nodes.fit import FitIsotopeEvolutionNode, FitBlanksNode, FitICFactorNode, FitFluxNode
from pychron.pipeline.nodes.gain import GainCalibrationNode
from pychron.pipeline.nodes.group_age import GroupAgeNode
from pychron.pipeline.nodes.grouping import GroupingNode, GraphGroupingNode, SubGroupingNode
from pychron.pipeline.nodes.ia import SetInterpretedAgeNode
from pychron.pipeline.nodes.mass_spec_reduced import MassSpecReducedNode
from pychron.pipeline.nodes.ml import MLDataNode, MLRegressionNode
from pychron.pipeline.nodes.persist import DVCPersistNode, PDFFigureNode, \
    BlanksPersistNode, IsotopeEvolutionPersistNode, ICFactorPersistNode, FluxPersistNode, XLSXAnalysisTablePersistNode, \
    InterpretedAgePersistNode, CSVAnalysesExportNode
from pychron.pipeline.nodes.push import PushNode
from pychron.pipeline.nodes.report import ReportNode
from pychron.pipeline.nodes.review import ReviewNode
from pychron.pipeline.nodes.table import AnalysisTableNode, InterpretedAgeTableNode



class NodeFactory:
    def __init__(self, name, factory):
        self.name = name
        self.factory = factory
# ============= EOF =============================================
