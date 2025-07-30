"""
slide/_slide
~~~~~~~~~~~~
"""

from ._analysis import AnalysisLoader
from ._annotation import AnnotationIO
from ._input import InputIO
from ._log import params, set_global_verbosity
from ._plot import PlotterAPI


class SLIDE:
    """
    SLIDE: A framework for local enrichment analysis on ranked label datasets.

    SLIDE enables systematic detection of enriched annotation terms along a ranked axis,
    such as genes sorted by correlation or phenotype. It applies a sliding window across
    the ranked input to compute statistical overrepresentation using various tests,
    supporting modular input loading, annotation parsing, and result visualization.
    """

    def __init__(self, verbose: bool = True) -> None:
        """
        Initialize the SLIDE framework with logging and modular interfaces.

        Args:
            verbose (bool): If False, suppresses all log messages to the console. Defaults to True.
        """
        # Set global logging verbosity
        set_global_verbosity(verbose)
        # Provide public access to parameter state
        self.params = params
        # Initialize submodules for I/O, analysis, and plotting
        self._input = InputIO()
        self._annotation = AnnotationIO()
        self._analysis = AnalysisLoader()
        self._plot = PlotterAPI()

    @property
    def input(self) -> InputIO:
        """
        Provides access to input data loaders.

        Returns:
            InputIO: Module for loading ranked labels, paired relationships, or matrices
            from CSV, TSV, Excel, or other formats for downstream analysis.
        """
        return self._input

    @property
    def annotation(self) -> AnnotationIO:
        """
        Provides access to annotation data loaders.

        Returns:
            AnnotationIO: Module for loading and filtering annotation term-to-label
            mappings, including gene ontology terms or functional sets.
        """
        return self._annotation

    @property
    def analysis(self) -> AnalysisLoader:
        """
        Provides access to the statistical enrichment engine.

        Returns:
            AnalysisLoader: Constructor for creating an Analysis object that applies
            sliding windows and computes enrichment using statistical tests.
        """
        return self._analysis

    @property
    def plot(self) -> PlotterAPI:
        """
        Provides access to SLIDE visualizations.

        Returns:
            PlotterAPI: Interface for plotting local enrichment results, label-level
            scores, and other outputs from SLIDE analyses.
        """
        return self._plot
