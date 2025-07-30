import aidge_core
from aidge_core.export_utils import ExportNodeCpp, get_node_from_metaop
from aidge_export_cpp import ROOT, ExportLibCpp, set_scaling_attributes

@ExportLibCpp.register_metaop("Quantizer", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class Quantizer(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Initialize kernel attributes
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.attributes["shift_value"] = 0
        self.attributes["coef_value"] = 1
        self.attributes["aidge_cmp"] = node.attributes().has_attr("aidge_cmp")

        # Browse the metaop to update kernel attributes
        if get_node_from_metaop(node, "ReLU"):
            self.attributes["activation"] = "Rectifier"
        
        # Set scaling attributes
        set_scaling_attributes(self, node)

        ## Set the scaling type
        if self.attributes["coef_value"] != 1:
            self.attributes["rescaling"] = "FixedPointScaling"
        elif self.attributes["shift_value"] != 0:
            self.attributes["rescaling"] = "SingleShiftScaling"

        # Template for layer configutation file generation
        self.config_template = str(ROOT / "templates" / "configuration" / "rescaling_config.jinja")

        # Template layer call function generation within the forward file
        self.forward_template = str(ROOT / "templates" / "kernel_forward" / "rescaling_forward.jinja")

        # Files to include within the generated forward.cpp file
        self.include_list = []

        # Path to the kernel(s) files to copy
        self.add_kernel_to_copy(ROOT / "kernels" / "rescaling.hpp")
        
        # Include aidge outputs within the fwd file
        if self.attributes["aidge_cmp"]:
            self.include_list.append("network/utils.hpp")   # aidge_cmp function
            self.include_list.append("data/aidge_outputs/" + node.name() + ".hpp")

@ExportLibCpp.register_metaop("QMul", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class QMul(Quantizer):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
