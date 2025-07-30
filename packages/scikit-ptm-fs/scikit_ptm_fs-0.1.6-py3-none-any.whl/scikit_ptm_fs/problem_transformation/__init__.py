"""

The problem transformation approach to single-label problems: single-class or multi-class.

"""
from .utils import get_matrix_in_format, matrix_creation_function_for_format

from .BR import BinaryRelevance
from .ELA import Entropy_Label_Assignment
from .LP import LabelPowerset
from .PPT import Pruned_Problem_Transformation
from .PW import PairwiseComparsion

__all__ = ["BinaryRelevance", "Entropy_Label_Assignment", "LabelPowerset", "Pruned_Problem_Transformation","PairwiseComparsion" ]