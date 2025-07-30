import os

import h5py
import numpy as np
from solidipes.loaders.sequence import Sequence
from solidipes_core_plugin.loaders.xml import XML


class XDMF(Sequence, XML):
    supported_mime_types = {"mesh/XDMF": "xdmf"}

    def __init__(self, **kwargs):
        from ..viewers.pyvista_plotter import PyvistaPlotter

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [PyvistaPlotter]

    def _load_hdf5_data_item(self, item):
        if item["@Format"] == "HDF":
            dimensions = item["@Dimensions"]
            dimensions = [int(e) for e in dimensions.split(" ")]
            path, hdf5_path = item["#text"].split(":")
            path = os.path.join(os.path.dirname(self.path), path)
            h5 = h5py.File(path)
            h5 = h5[hdf5_path]
            h5 = np.array(h5).reshape(dimensions)
            return h5
        if item["@Format"] == "XML":
            return [float(e) for e in item["#text"].split(" ")]
        return item

    def _load_xdmf_data_item(self, item):
        if isinstance(item, dict):
            res = {}
            for k, v in item.items():
                if k == "DataItem":
                    # print(f'LoadasDataItem: {k} {v}\n')
                    res[k] = self._load_hdf5_data_item(v)
                else:
                    res[k] = self._load_xdmf_data_item(v)
            return res
        if isinstance(item, list) and not isinstance(item, str):
            return [self._load_xdmf_data_item(e) for e in item]
        return item

    def find_dataitem_from_ref(self, ref):
        ref = [e for e in ref.split("/") if e != "" and e != "Xdmf"]
        print(ref)

        def extract_label(r):
            try:
                name, label = r.split("[")
                label = label[:-1]
                label = label.replace(r'"', "")
                label = label.split("=")
                return name, label
            except ValueError:
                return r, None

        res = self.xdmf
        for r in ref:
            name, label = extract_label(r)
            # print(name, label)
            res = res[name]
            if isinstance(res, list):
                for r in res:
                    if r[label[0]] != label[1]:
                        continue
                    res = r
                    break
            # print(res.keys())
            if label is None:
                # print(res)
                continue

            if label[0] not in res:
                raise RuntimeError(f"Cannot find {name} {label} in {ref}")
            if res[label[0]] != label[1]:
                raise RuntimeError(f"Cannot find {name} {label} in {ref}")
        return res

    def _load_element(self, n):
        """Load a single frame"""

        grids = self.grids[n]
        geometry = grids["Geometry"]
        topology = grids["Topology"]

        if "DataItem" in geometry:
            geometry = geometry["DataItem"]
        elif "@Reference" in geometry:
            ref = geometry["#text"]
            geometry = self.find_dataitem_from_ref(ref)["DataItem"]

        points = np.array(geometry)

        if "DataItem" in topology:
            conn = topology["DataItem"]
        elif "@Reference" in topology:
            ref = topology["#text"]
            conn = self.find_dataitem_from_ref(ref)["DataItem"]

        cells = [(topology["@TopologyType"].lower(), np.array(conn))]

        point_data = {}
        cell_data = {}

        if "Attribute" in grids:
            for a in grids["Attribute"]:
                # _type = a['@AttributeType']
                _center = a["@Center"]
                _name = a["@Name"]
                _data = a["DataItem"]
                if _center == "Node":
                    point_data[_name] = np.array(_data)
                if _center == "Cell":
                    cell_data[_name] = np.array([_data])
        import meshio

        mesh = meshio.Mesh(points, cells, point_data=point_data, cell_data=cell_data)
        import pyvista as pv

        mesh = pv.from_meshio(mesh)
        return mesh

    def select_frame(self, frame):
        self.select_element(frame)

    # cannot be defined with pre_loaded because it changes on demand
    @property
    def mesh(self):
        return self._current_element

    @XML.loadable
    def xdmf(self):
        return self._load_xdmf_data_item(self.xml["Xdmf"])

    @XML.loadable
    def version(self):
        return self.xdmf["@Version"]

    @XML.loadable
    def mesh_name(self):
        return self.domain["@Name"]

    @XML.loadable
    def domain(self):
        return self.xdmf["Domain"]

    @XML.loadable
    def grid(self):
        _grid = self.domain["Grid"]
        keys = [e for e in _grid.keys() if e != "Grid"]
        grid = {}
        for e in keys:
            grid[e] = _grid[e]
        return grid

    @XML.loadable
    def n_frames(self):
        return len(self.grid["Time"]["DataItem"])

    @property
    def _element_count(self):
        return self.n_frames

    @XML.loadable
    def grids(self):
        _grid = self.domain["Grid"]["Grid"]
        return _grid
