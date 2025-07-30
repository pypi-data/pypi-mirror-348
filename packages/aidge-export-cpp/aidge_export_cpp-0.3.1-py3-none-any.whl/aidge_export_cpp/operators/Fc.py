import aidge_core
from aidge_core.export_utils import ExportNodeCpp, get_node_from_metaop
from aidge_export_cpp import ROOT, ExportLibCpp, set_scaling_attributes

@ExportLibCpp.register("FC", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class FC(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Initialize kernel attributes
        self.attributes["activation"] = "Linear"
        self.attributes["aidge_cmp"] = node.attributes().has_attr("aidge_cmp")

        ## Scaling
        self.attributes["rescaling"] = "NoScaling"
        self.attributes["shift_value"] = 0

        # Template for layer configutation file generation
        self.config_template = str(ROOT / "templates" / "configuration" / "fullyconnected_config.jinja")
        
        # Template layer call function generation within the forward file
        self.forward_template = str(ROOT / "templates" / "kernel_forward" / "fullyconnected_forward.jinja")
        
        # Files to include within the generated forward.cpp file
        self.include_list = []
        
        # Path to the kernel(s) files to copy
        self.add_kernel_to_copy(ROOT / "kernels" / "fullyconnected.hpp")
        self.add_kernel_to_copy(ROOT / "static" / "macs.hpp", "include/network", fwd_include=False)

        # Include aidge outputs within the fwd file
        if self.attributes["aidge_cmp"]:
            self.include_list.append("network/utils.hpp")   # aidge_cmp function
            self.include_list.append("data/aidge_outputs/" + node.name() + ".hpp")


@ExportLibCpp.register_metaop("QFC", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class QFC(FC):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        set_scaling_attributes(self, node)

        ## Set the scaling type
        if self.attributes["shift_value"] != 0:
            self.attributes["rescaling"] = "SingleShiftScaling"


@ExportLibCpp.register_metaop("FCAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class FCAct(QFC):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        if get_node_from_metaop(node, "ReLU"):
            self.attributes["activation"] = "Rectifier"
        else:
            aidge_core.Log.error(f"{node.type()} activation is not yet supported.")
