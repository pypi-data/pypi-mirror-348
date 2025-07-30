import io

from rdflib import Dataset, Graph

from pyjelly import jelly
from pyjelly.options import LookupPreset, StreamOptions, StreamTypes
from pyjelly.serialize.streams import Stream
from tests.e2e_tests.ser_des.base_ser_des import (
    BaseSerDes,
    QuadGraphType,
    TripleGraphType,
)
from tests.utils.ordered_memory import OrderedMemory
from tests.utils.rdflib_workarounds import fixup_graph


class RdflibSerDes(BaseSerDes):
    """
    Serialization and deserialization using rdflib.

    Args:
        BaseSerDes (_type_): _description_

    Returns:
        _type_: _description_

    """

    name = "rdflib"

    def __init__(self) -> None:
        super().__init__(name=self.name)

    def read_quads(self, in_bytes: bytes) -> QuadGraphType:
        g = Dataset()
        g.parse(data=in_bytes, format="nquads")
        fixup_graph(g)
        return g

    def write_quads(self, in_graph: QuadGraphType) -> bytes:
        destination = io.BytesIO()
        in_graph.serialize(destination=destination, format="nquads")
        return destination.getvalue()

    def read_quads_jelly(self, in_bytes: bytes) -> QuadGraphType:
        g = Dataset()
        g.parse(data=in_bytes, format="jelly")
        fixup_graph(g)
        return g

    def write_quads_jelly(
        self, in_graph: QuadGraphType, preset: LookupPreset, frame_size: int
    ) -> bytes:
        destination = io.BytesIO()
        options = StreamOptions(
            stream_types=StreamTypes(
                logical_type=jelly.LOGICAL_STREAM_TYPE_FLAT_QUADS,
                physical_type=jelly.PHYSICAL_STREAM_TYPE_QUADS,
            ),
            lookup_preset=preset,
        )
        stream = Stream.from_options(options, frame_size=frame_size)
        in_graph.serialize(destination=destination, format="jelly", stream=stream)
        return destination.getvalue()

    def read_triples(self, in_bytes: bytes) -> TripleGraphType:
        g = Graph(store=OrderedMemory())
        g.parse(data=in_bytes, format="nt")
        fixup_graph(g)
        return g

    def write_triples(self, in_graph: TripleGraphType) -> bytes:
        destination = io.BytesIO()
        in_graph.serialize(destination=destination, format="nt")
        return destination.getvalue()

    def read_triples_jelly(self, in_bytes: bytes) -> TripleGraphType:
        g = Graph()
        g.parse(data=in_bytes, format="jelly")
        fixup_graph(g)
        return g

    def write_triples_jelly(
        self, in_graph: TripleGraphType, preset: LookupPreset, frame_size: int
    ) -> bytes:
        destination = io.BytesIO()
        options = StreamOptions(
            stream_types=StreamTypes(
                logical_type=jelly.LOGICAL_STREAM_TYPE_FLAT_TRIPLES,
                physical_type=jelly.PHYSICAL_STREAM_TYPE_TRIPLES,
            ),
            lookup_preset=preset,
        )
        stream = Stream.from_options(options, frame_size=frame_size)
        in_graph.serialize(destination=destination, format="jelly", stream=stream)
        return destination.getvalue()
