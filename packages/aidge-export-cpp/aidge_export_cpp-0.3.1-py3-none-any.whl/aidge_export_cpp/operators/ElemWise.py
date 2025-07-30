import aidge_core
from aidge_core.export_utils import ExportNodeCpp, get_node_from_metaop
from aidge_export_cpp import ROOT, ExportLibCpp, set_scaling_attributes

class ElemWise(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Initialize kernel attributes
        self.attributes["activation"] = "Linear"
        self.attributes["aidge_cmp"] = node.attributes().has_attr("aidge_cmp")

        ## Scaling
        self.attributes["rescaling"] = "NoScaling"
        self.attributes["shift_value"] = 0
        self.attributes["coef_value"] = 1

        # Template for layer configutation file generation
        self.config_template = str(ROOT / "templates" / "configuration" / "elemwise_config.jinja")

        # Template layer call function generation within the forward file
        self.forward_template = str(ROOT / "templates" / "kernel_forward" / "elemwise_forward.jinja")

        # Files to include within the generated forward.cpp file
        self.include_list = []

        # Path to the kernel(s) files to copy
        self.add_kernel_to_copy(ROOT / "kernels" / "elemwise.hpp")
        
        # Include aidge outputs within the fwd file
        if self.attributes["aidge_cmp"]:
            self.include_list.append("network/utils.hpp")   # aidge_cmp function
            self.include_list.append("data/aidge_outputs/" + node.name() + ".hpp")


class QElemWise(ElemWise):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        set_scaling_attributes(self, node)

        ## Set the scaling type
        if self.attributes["coef_value"] != 1:
            self.attributes["rescaling"] = "FixedPointScaling"
        elif self.attributes["shift_value"] != 0:
            self.attributes["rescaling"] = "SingleShiftScaling"


@ExportLibCpp.register("Add", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class Add(ElemWise):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["elemwise_op"] = "Add"


@ExportLibCpp.register_metaop("QAdd", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class QAdd(QElemWise, Add):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register_metaop("AddAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class AddAct(QAdd):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        if get_node_from_metaop(node, "ReLU"):
            self.attributes["activation"] = "Rectifier"
        else:
            aidge_core.Log.error(f"{node.type()} activation is not yet supported.") 


@ExportLibCpp.register("Sub", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class Sub(ElemWise):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["elemwise_op"] = "Sub"


@ExportLibCpp.register_metaop("QSub", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class QSub(QElemWise, Sub):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register_metaop("SubAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class SubAct(QSub):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        if get_node_from_metaop(node, "ReLU"):
            self.attributes["activation"] = "Rectifier"
        else:
            aidge_core.Log.error(f"{node.type()} activation is not yet supported.") 


@ExportLibCpp.register("Mul", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class Mul(QElemWise):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["elemwise_op"] = "Mul"


@ExportLibCpp.register_metaop("MulAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class MulAct(Mul):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        if get_node_from_metaop(node, "ReLU"):
            self.attributes["activation"] = "Rectifier"
        else:
            aidge_core.Log.error(f"{node.type()} activation is not yet supported.")