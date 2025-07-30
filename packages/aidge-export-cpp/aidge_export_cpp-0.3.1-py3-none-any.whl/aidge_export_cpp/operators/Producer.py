import os
from pathlib import Path
import numpy as np
import aidge_core
from aidge_core.export_utils import ExportNode, generate_file
from aidge_export_cpp import ROOT
from aidge_export_cpp import ExportLibCpp

def numpy_dtype2ctype(dtype):
    if dtype == np.int8:
        return "int8_t"
    elif dtype == np.int16:
        return "int16_t"
    elif dtype == np.int32:
        return "int32_t"
    elif dtype == np.int64:
        return "int64_t"
    elif dtype == np.float32:
        return "float"
    elif dtype == np.float64:
        return "double"
    # Add more dtype mappings as needed
    else:
        raise ValueError(f"Unsupported {dtype} dtype")

def export_params(name: str,
                  array: np.ndarray,
                  filepath: str):

    # Get directory name of the file
    dirname = os.path.dirname(filepath)

    # If directory doesn't exist, create it
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    generate_file(
        filepath,
        str(ROOT / "templates" / "data" / "parameters.jinja"),
        name=name,
        data_t=numpy_dtype2ctype(array.dtype),
        values=array.tolist()
    )

@ExportLibCpp.register("Producer", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class ProducerCPP(ExportNode):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.values = np.array(self.operator.get_output(0))
        self.ignore = node.attributes().has_attr("ignore")

        if len(self.values.shape) == 4:  # Note: export in HWC
            self.values = np.transpose(self.values, (0, 2, 3, 1))

    def export(self, export_folder: Path):
        if not self.ignore :
            header_path = f"include/parameters/{self.attributes['name']}.h"
            export_params(
                self.attributes['out_name'][0],
                self.values.reshape(-1),
                str(export_folder / header_path))
            return [header_path]
        return []

    def forward(self):
        # A Producer does nothing during forward
        return []