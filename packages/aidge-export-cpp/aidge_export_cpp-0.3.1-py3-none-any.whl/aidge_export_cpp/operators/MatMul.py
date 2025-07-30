import aidge_core
from aidge_core.export_utils import ExportNodeCpp
from aidge_export_cpp import ROOT
from aidge_export_cpp import ExportLibCpp

@ExportLibCpp.register("MatMul", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class MatMulCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "matmul_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "matmul_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "matmul.hpp"),
        ]
