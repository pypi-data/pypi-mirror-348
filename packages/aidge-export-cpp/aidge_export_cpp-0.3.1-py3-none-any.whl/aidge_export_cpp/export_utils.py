import os
from collections import OrderedDict

import aidge_core
from aidge_core.export_utils import get_node_from_metaop

def cpp_fuse_to_metaops(graph_view: aidge_core.GraphView):
    """ 
    Fuse nodes into metaops adapted for the CPP Export
    TODO: These recipes should be into aidge_core

    :param graph_view: An instance of :py:class:`aidge_core.GraphView`, providing access to nodes and
                       ordered input/output data within the computational graph.
    """

    cpp_recipes = OrderedDict({
        # Quantization
        "QMul":           "Mul->Quantizer",     # Fixed Point Scaling

        # FC
        "QFC":            "FC->(Quantizer|QMul)",
        "FCAct":          "(FC|QFC)->ReLU",

        # Conv
        "QConv":          "Conv2D->(Quantizer|QMul)",
        "PadConv":        "(QConv|Conv2D)<-Pad2D",
        "ConvAct":        "(QConv|Conv2D)->ReLU",
        "PadConvAct":     "PadConv->ReLU",

        # ConvDw
        "QConvDw":          "ConvDepthWise2D->(Quantizer|QMul)",
        "ConvDwPad":        "(QConvDw|ConvDepthWise2D)->Pad2D",
        "ConvDwAct":        "(QConvDw|ConvConvDepthWise2D2D)->ReLU",
        "ConvDwActPad":     "ConvDwAct->Pad2D",

        # Max Pooling
        "PadMaxPool":     "MaxPooling2D<-Pad2D",
        "MaxPoolAct":     "MaxPooling2D->ReLU",
        "PadMaxPoolAct":  "PadMaxPool->ReLU",

        # Average Pooling
        "PadAvgPool":     "AvgPooling2D<-Pad2D",
        "AvgPoolAct":     "AvgPooling2D->ReLU",
        "PadAvgPoolAct":  "PadAvgPool->ReLU",

        # Global Average Pooling
        "PadGlobalAvgPool":     "GlobalAveragePooling2D<-Pad2D",
        "GlobalAvgPoolAct":     "GlobalAveragePooling2D->ReLU",
        "PadGlobalAvgPoolAct":  "PadGlobalAveragePool->ReLU",

        # ElemWise
        "QAdd":      "Add->(Quantizer|QMul)",
        "QSub":      "Sub->(Quantizer|QMul)",
        # "QMul":    "Mul->Quantizer",      # Already defined
        "AddAct":    "(QAdd|Add)->ReLU",
        "SubAct":    "(QSub|Sub)->ReLU",
        "MulAct":    "(QMul|Mul)->ReLU",

        # Activation
        "QReLU":        "ReLU->(Quantizer|QMul)",
    })

    for node, recipe in cpp_recipes.items():
        aidge_core.fuse_to_metaops(graph_view, recipe, node)



def set_nodes_names(scheduler):
    """
    Set the CPP nodes names as well as their producers. 
    The producers naming is handled from their child node.
    
    [TODO] Fc and Conv layers will always have weights as parent 1 and 
    possibly biases as parent 2. It may be better to previously label the 
    producers. 

    :param scheduler: Scheduler instance managing the computation graph.
                      Uses `graph_view` and `get_sequential_static_scheduling` methods
                      to retrieve the computation graph layout and ordered nodes.
    :type scheduler: aidge_core.Scheduler
    """

    node_ids = {}   # Dict holding the node type along with a counter
    node_it = 0     # Node Iterator

    ## MetaOps
    for node in scheduler.get_sequential_static_scheduling():
        node_type = node.type()

        if node_type != "Producer":
            if node.type() not in node_ids:
                node_ids[node_type] = 0

            # Set node name
            node.set_name("_" + str(node_it) + "_" +
                            str(node_type) + "_" + str(node_ids[node_type]))
            node_ids[node_type] += 1
            node_it += 1

            # Set producers names
            ## Weights & Biases producers
            if get_node_from_metaop(node, "FC") or \
               get_node_from_metaop(node, "Conv2D") or \
               get_node_from_metaop(node, "ConvDepthWise2D"):
                
                node.get_parent(1).set_name(node.name() + "_weights")
                if node.get_parent(2) is not None:
                    node.get_parent(2).set_name(node.name() + "_biases")  

    ## Scaling Producers
    for node in scheduler.get_sequential_static_scheduling():
        """
        TODO: If multiple quantizer nodes are found, the producers will
        all have the same name and this will not work properly. 
        """
        if node.type() == "Producer":
            child_node = node.output(0)[0][0]
            if node.attributes().has_attr("shift_prod"):
                node.set_name(child_node.name() + "_shift")
            if node.attributes().has_attr("coef_prod"):
                node.set_name(child_node.name() + "_coef")



def set_nodes_datatypes(graph_view: aidge_core.GraphView):
    """ Set the nodes' datatypes

    The set_datatype function can't be used on Conv2D and FC nodes directly
    as the biases datatype is different from the other inputs. 
    TODO: Should be using forward_datatype()

    :param graph_view: An instance of :py:class:`aidge_core.graph_view`, providing access to nodes and
                       ordered input/output data within the computational graph.
    """
    for node in graph_view.get_nodes():
        if node.type() != "Producer":
            if get_node_from_metaop(node, "FC") or \
               get_node_from_metaop(node, "Conv2D") or \
               get_node_from_metaop(node, "ConvDepthWise2D"):

                node.get_operator().get_input(0).set_datatype(aidge_core.dtype.int8)    # Input
                node.get_operator().get_input(1).set_datatype(aidge_core.dtype.int8)    # Weights
                if node.get_parent(2) is not None:
                    node.get_operator().get_input(2).set_datatype(aidge_core.dtype.int32)   # Biases
                node.get_operator().get_output(0).set_datatype(aidge_core.dtype.int8)       # Output
            else:
                node.get_operator().set_datatype(aidge_core.dtype.int8)

    # Set input node's datatype
    for n in graph_view.get_input_nodes():
        n.get_operator().get_input(0).set_datatype(aidge_core.dtype.int8)



def read_log_file(file_path: str):
    """ Read log file
    Used to read the aidge generated log files containing the intermediate
    tensors of the exported model. 

    :param file_path: Path to the file to read. 
    :type file_path: str
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return None

    with open(file_path, 'r') as file:
        content = file.read()
    return content



def exclude_unwanted_producers(model):
    """ Exclude some producers not needed for the export

    Currently excludes the producers attached to the Mul and BitShift nodes, as they are
    tensors holding a single data. This data is retrieved during the export
    generation process and passed as argument directly within the Mul layer
    configuration. 
    """

    nodes_to_ignore = ["Mul", "BitShift", "Clip"]

    for node in model.get_nodes():
        if node.type() == "Producer":
            children_nodes = [n.type() for n in node.get_children()]
            for node_type in nodes_to_ignore:
                if node_type in children_nodes:
                    node.attributes().ignore = True
                    break



def set_scaling_attributes(export_node: aidge_core.export_utils.ExportNode, node: aidge_core.Node):
    """
    Look recursively for a Quantizer node inside of the given node, 
    then set shift and coef attributes of the given export node.
    [TODO] Should be moved into aidge_core.ExportNode

    :param export_node: An instance of :py:class:`aidge_core.export_utils.ExportNode` to set the scaling
                        attributes needed for a quantized export. 
    :type export_node: aidge_core.export_utils.ExportNode
    :param node: Node which may hold a Quantizer node. 
    :type node: aidge_core.Node
    """

    QNode = get_node_from_metaop(node, "Quantizer")
    if QNode:
        BNode = get_node_from_metaop(QNode[0], "BitShift")
        export_node.attributes["shift_value"] = BNode[0].get_operator().get_input(1)[0]

    QMulNode = get_node_from_metaop(node, "QMul")
    if QMulNode:
        CNode = get_node_from_metaop(QMulNode[0], "Mul")
        export_node.attributes["coef_value"] = CNode[0].get_operator().get_input(1)[0]

      
            
def normalize(array):
    """
    Normalize an input image between -1 and 1
    """
    if array.max() == array.min():
        return array/array.max()
    array = (array - array.min()) / (array.max() - array.min())
    return 2 * array - 1

