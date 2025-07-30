import aidge_core
from aidge_core.export_utils import ExportNodeCpp
from aidge_export_cpp import ROOT
from aidge_export_cpp import ExportLibCpp

@ExportLibCpp.register("Pad2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class CppPad(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Initialize kernel attributes
        self.attributes["padding"] = node.get_operator().attr.begin_end_borders
        self.attributes["border_type"] = node.get_operator().attr.border_type
        self.attributes["border_value"] = node.get_operator().attr.border_value
        self.attributes["aidge_cmp"] = node.attributes().has_attr("aidge_cmp")

        assert self.attributes["border_type"] == aidge_core.pad_border_type.Constant, (
            f"export Pad2d: border_type == {node.get_operator().attr.border_type} not implemented"
        )

        # Template for layer configutation file generation
        self.config_template = str(ROOT / "templates" / "configuration" / "pad_config.jinja")

        # Template layer call function generation within the forward file
        self.forward_template = str(ROOT / "templates" / "kernel_forward" / "pad_forward.jinja")
        
        # Files to include within the generated forward.cpp file
        self.include_list = []

        # Path to the kernel(s) files to copy
        self.add_kernel_to_copy(ROOT / "kernels" / "pad.hpp")

        # Include aidge outputs within the fwd file
        if self.attributes["aidge_cmp"]:
            self.include_list.append("network/utils.hpp")   # aidge_cmp function
            self.include_list.append("data/aidge_outputs/" + node.name() + ".hpp")