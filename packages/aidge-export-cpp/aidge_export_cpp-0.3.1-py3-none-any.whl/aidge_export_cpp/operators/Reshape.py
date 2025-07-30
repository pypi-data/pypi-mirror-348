import aidge_core
from aidge_core.export_utils import ExportNodeCpp
from aidge_export_cpp import ROOT
from aidge_export_cpp import ExportLibCpp

@ExportLibCpp.register("Reshape", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class ReshapeCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.config_template = str(
            ROOT / "templates" / "configuration" / "reshape_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "reshape_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "reshape.hpp"),
        ]
