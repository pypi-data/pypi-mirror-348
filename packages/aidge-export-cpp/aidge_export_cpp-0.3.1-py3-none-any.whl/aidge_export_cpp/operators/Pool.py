import aidge_core
from aidge_core.export_utils import ExportNodeCpp, get_node_from_metaop
from aidge_export_cpp import ROOT
from aidge_export_cpp import ExportLibCpp

class Pool(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Initialize kernel attributes
        self.attributes["stride_dims"] = [1, 1]
        self.attributes["padding"] = [0, 0, 0, 0]
        self.attributes["pool_type"] = "Max"
        self.attributes["activation"] = "Linear"
        self.attributes["aidge_cmp"] = node.attributes().has_attr("aidge_cmp")

        # Template for layer configutation file generation
        self.config_template = str(ROOT / "templates" / "configuration" / "pooling_config.jinja")
        
        # Template layer call function generation within the forward file
        self.forward_template = str(ROOT / "templates" / "kernel_forward" / "pooling_forward.jinja")
        
        # Files to include within the generated forward.cpp file
        self.include_list = []
        
        # Path to the kernel(s) files to copy
        self.add_kernel_to_copy(ROOT / "kernels" / "pooling.hpp")

        # Include aidge outputs within the fwd file
        if self.attributes["aidge_cmp"]:
            self.include_list.append("network/utils.hpp")   # aidge_cmp function
            self.include_list.append("data/aidge_outputs/" + node.name() + ".hpp")


class PadPool(Pool):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        PadNode = get_node_from_metaop(node, "Pad2D")
        self.attributes["padding"] = PadNode[0].get_operator().attr.begin_end_borders


class PoolAct(Pool):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        if get_node_from_metaop(node, "ReLU"):
            self.attributes["activation"] = "Rectifier"
        else:
            aidge_core.Log.error(f"{node.type()} activation is not yet supported.")  


@ExportLibCpp.register("MaxPooling2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class MaxPool(Pool):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        PoolNode = get_node_from_metaop(node, "MaxPooling2D")
        self.attributes["pool_type"] = "Max"
        self.attributes["kernel_dims"] = PoolNode[0].get_operator().attr.kernel_dims
        self.attributes["stride_dims"] = PoolNode[0].get_operator().attr.stride_dims


@ExportLibCpp.register_metaop("PadMaxPool", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class PadMaxPool(MaxPool, PadPool):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register_metaop("MaxPoolAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class MaxPoolAct(MaxPool, PoolAct):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register_metaop("PadMaxPoolAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class PadMaxPoolAct(PadMaxPool, MaxPoolAct):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register("AvgPooling2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class AvgPool(Pool):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # Browse the metaop to update kernel attributes
        PoolNode = get_node_from_metaop(node, "AvgPooling2D")
        self.attributes["pool_type"] = "Average"
        self.attributes["kernel_dims"] = PoolNode[0].get_operator().attr.kernel_dims
        self.attributes["stride_dims"] = PoolNode[0].get_operator().attr.stride_dims


@ExportLibCpp.register_metaop("PadAvgPool", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class PadAvgPool(AvgPool, PadPool):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register_metaop("AvgPoolAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class AvgPoolAct(AvgPool, PoolAct):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register_metaop("PadAvgPoolAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class PadAvgPoolAct(PadAvgPool, AvgPoolAct):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register("GlobalAveragePooling", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class GlobalAvgPool(Pool):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        self.attributes["pool_type"] = "Average"
        self.attributes["kernel_dims"] = [self.attributes["in_width"][0], self.attributes["in_height"][0]]


@ExportLibCpp.register_metaop("PadGlobalAvgPool", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class PadGlobalAvgPool(GlobalAvgPool, PadPool):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register_metaop("GlobalAvgPoolAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class GlobalAvgPoolAct(GlobalAvgPool, PoolAct):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)


@ExportLibCpp.register_metaop("PadGlobalAvgPoolAct", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class PadGlobalAvgPoolAct(PadGlobalAvgPool, GlobalAvgPoolAct):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)