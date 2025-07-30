from aidge_core.export_utils import ExportLib
from aidge_export_cpp import ROOT

class ExportLibCpp(ExportLib):
    _name="export_cpp"
    static_files={
        str(ROOT / "static" / "Makefile"): "",
        str(ROOT / "static" / "typedefs.hpp"): "dnn/include/network",
        str(ROOT / "static" / "utils.hpp"): "dnn/include/network",
        str(ROOT / "static" / "rescaling_utils.hpp"): "dnn/include/network",
        str(ROOT / "static" / "activation_utils.hpp"): "dnn/include/network",
    }
