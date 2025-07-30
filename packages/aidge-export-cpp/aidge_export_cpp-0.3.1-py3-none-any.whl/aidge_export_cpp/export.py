import os
import shutil
import numpy as np
from pathlib import Path
from typing import List, Union

import aidge_core
from aidge_core.mem_info import generate_optimized_memory_info
from aidge_core.export_utils import scheduler_export, generate_main_cpp, aidge2c, generate_file

from aidge_export_cpp import ExportLibCpp, ROOT
from aidge_export_cpp.export_utils import read_log_file


def export(export_folder_name: str,
           graphview: aidge_core.GraphView,
           scheduler: Union[List[aidge_core.Node],
                            aidge_core.Scheduler],
           inputs_tensor: aidge_core.Tensor = None,
           labels: aidge_core.Tensor = None,
           dev_mode: bool = False,
           aidge_cmp: bool = False):
    
    """ Export an aidge_core.Scheduler to C++ code
    
    :param export_folder_name: Export folder name
    :type export_folder_name: str
    :param graph_view: An instance of :py:class:`aidge_core.graph_view`, providing access to nodes and
                       ordered input/output data within the computational graph.
    :type graph_view: aidge_core.GraphView
    :param scheduler: Scheduler instance managing the computation graph.
                      Uses `graph_view` and `get_sequential_static_scheduling` methods
    :param inputs_tensor: **For future** argument to provide tensor to use in the main function, not implemented yet!
                          By default, the input of the given graph will be exported.
    :type input_tensor: aidge_core.Tensor
                    to retrieve the computation graph layout and ordered nodes.
    :type scheduler: aidge_core.Scheduler
    :param labels: Argument to provide labels tensor to generate and use in the main function. 
    :type labels: aidge_core.Tensor
    :param dev_mode: Wether or not the developer mode is enabled. If enabled, the export files
                     will be symlinks from the aidge_export_cpp module. Therefore, modifying
                     a file within the export will change the module as well. 
    :type dev_mode: boolean
    """

    export_folder_name = Path(export_folder_name)

    # Remove existing export
    if os.path.isdir(export_folder_name):
        print("Removing existing export directory...")
        shutil.rmtree(export_folder_name)

    # Generate Model Files
    """
    Perform the following tasks :
    - Generate the parameters and layers config files
    - Generate the forward.cpp file
    - Copy all needed kernels
    """

    scheduler_export(scheduler,
                     export_folder_name,
                     ExportLibCpp,
                     memory_manager=generate_optimized_memory_info,
                     memory_manager_args={
                         "stats_folder": f"{export_folder_name}/stats"},
                     dev_mode=dev_mode)
    
    # Generate main file
    generate_main_cpp(export_folder_name, graphview, labels=labels, inputs_tensor=inputs_tensor)

    # Generate log files (aidge_cmp option)
    """
    If the aidge_cmp option has been enabled, the generated log_outputs will
    be copied into the generated export in order to be used as reference. 
    """
    if aidge_cmp:
        ranked_nodes = graphview.get_ranked_nodes_name("{0}[{1}#{3}]")
        os.makedirs(export_folder_name / "data" / "aidge_outputs")
        os.makedirs(export_folder_name / "data" / "export_outputs")
        for node in graphview.get_nodes():
            if node.type() != "Producer":
                file_path = 'log_outputs/' + ranked_nodes[node] + '/output_0.log'
                data_t = aidge2c(node.get_operator().get_output(0).dtype())
                name = node.name() + '_output_0_aidge'
                dims = node.get_operator().get_output(0).dims()
                values = read_log_file(file_path)

                generate_file(export_folder_name / "data" / "aidge_outputs" / (node.name() + ".hpp"),
                              ROOT / "templates" / "data" / "aidge_tensor.jinja",
                              data_t=data_t,
                              name=name,
                              dims=dims,
                              values=values)
