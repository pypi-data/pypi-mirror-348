from io import StringIO

import mergedeep
import numpy as np
import pandas as pd
import pyparsing as pp
from solidipes_core_plugin.loaders.code_snippet import CodeSnippet


class ParseAbaqus:
    _valid_characters = " " + pp.printables
    _valid_characters = _valid_characters.replace("*", "")
    ppText = pp.Word(_valid_characters + "\n")
    ppHead = pp.Word(_valid_characters.replace(",", ""))

    def parseComments(self, toks):
        cs = [e.strip() for e in toks if e.strip() != ""]
        if cs:
            return {"Comment": cs}
        return None

    comments = pp.OneOrMore(pp.Suppress(pp.Literal("**")) + ppText).addParseAction(parseComments)

    def parseData(self, toks):
        name = toks[0]
        data = toks[2].strip()
        params = [e.strip() for e in toks[1]]
        res = {}
        if params:
            res[":".join(params)] = {"data": data, "@params": params}
        else:
            res["data"] = data

        return {name: res}

    def _tag(self, name):
        return (
            pp.Suppress(pp.Literal("*"))
            + name
            + pp.Group(pp.ZeroOrMore(pp.Suppress(pp.Literal(",")) + self.ppHead))
            + pp.Suppress(pp.Optional(pp.Literal("\n")))
        )

    def _data(self, name):
        return (self._tag(name) + pp.Combine(pp.ZeroOrMore(self.ppText))).addParseAction(self.parseData)

    def parseTag(self, toks):
        name = toks[0]
        params = [e.strip() for e in toks[1]]
        res = {}
        res[name] = {}
        for e in toks[2:]:
            if isinstance(e, str):
                e = e.strip()
                if e == "":
                    continue
            if isinstance(e, dict):
                res[name] = mergedeep.merge(res[name], e)
        # print('aaa', res, conv)
        if params:
            res[name]["@params"] = params

        return res

    def _heading(self):
        _heading = self._tag("Heading") + self.comments()
        return _heading.addParseAction(self.parseTag)

    def _paragraph(self, name):
        return self._tag(name) + pp.ZeroOrMore(self.ppText | self.comments())

    def _block(self, name):
        stag = name
        etag = "End " + stag

        _block_start = self._tag(stag)
        _block_content = pp.Forward()
        _block_end = self._tag(etag)
        _block = _block_start + _block_content + pp.Suppress(_block_end)
        _block_content << pp.ZeroOrMore(
            self._data("Node")
            | self._data("Element")
            | self._data("Nset")
            | self._data("Elset")
            | self._data("Equation")
            | self._data("Surface")
            | self._data("Solid Section")
            | self._data("Section")
            | self._data("Shell Section")
            | self.comments()
        )
        return _block.addParseAction(self.parseTag)

    def inp_file(self):
        _file = (
            self._heading()
            + pp.Optional(self._tag("Preprint").addParseAction(self.parseTag))
            + pp.ZeroOrMore(self.comments | self._block("Part"))
        )
        _file = _file.leaveWhitespace().addParseAction(
            lambda toks: {"main": [e for e in toks if (not isinstance(e, str) or e.strip() != "")]}
        )
        return _file

    def parse(self, filename):
        to_parse = open(filename).read()
        ret = self.inp_file().parseString(to_parse)
        return ret


################################################################


class Abaqus(CodeSnippet):
    supported_mime_types = {"application/fem/abaqus": "inp"}

    def __init__(self, **kwargs):
        from solidipes_core_plugin.viewers.xml import XML

        from ..viewers.pyvista_plotter import PyvistaPlotter

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [PyvistaPlotter, XML]

    @CodeSnippet.loadable
    def structure(self):
        try:
            parser = ParseAbaqus()
            ret = parser.parse(self.file_info.path)
            return ret[0]
        except Exception as e:
            print(e)

    @property
    def xml(self):
        return self.structure

    @property
    def parts(self):
        return [e["Part"] for e in self.xml["main"] if "Part" in e]

    def nodes(self, part):
        p = self.parts[part]
        if "Node" in p:
            df = pd.read_csv(StringIO(p["Node"]["data"]), sep=",", header=None)
            return df.to_numpy()[:, 1:]
        return []

    def elements(self, part):
        p = self.parts[part]
        cells = []
        if "Element" in p:
            for _type, v in p["Element"].items():
                if _type.startswith("type="):
                    _type = _type[5:]
                if _type == "CPE4":
                    _type = "quad"
                elif _type == "CPE3":
                    _type = "triangle"
                else:
                    print(f"Do not know element type {_type}")
                    raise RuntimeError(f"Do not know element type {_type}")
                conn = pd.read_csv(StringIO(v["data"]), sep=",", header=None).to_numpy()[:, 1:] - 1
                cells.append((_type, np.array(conn)))
            return cells
        return []

    @CodeSnippet.loadable
    def meshes(self):
        import pyvista as pv

        try:
            import meshio

            fname = self.file_info.path
            from pyvista.core.utilities import from_meshio

            return {"meshio_reader": from_meshio(meshio.read(fname))}
        except Exception:
            pass

        meshes = {}
        for p, part in enumerate(self.parts):
            mesh = meshio.Mesh(self.nodes(p), self.elements(p))
            mesh = pv.from_meshio(mesh)
            params = part["@params"]
            for param in params:
                if param.startswith("name="):
                    param = param[5:]
                    meshes[param] = mesh
        return meshes

    @property
    def mesh(self):
        keys = [e for e in self.meshes.keys()]
        return self.meshes[keys[0]]
