import attrs

from .alias import AliasMX, extract_alias
from .cast import CastMX
from .column import prepare_column
from .marks import MARKS_FIELD, MARKS_TYPE
from .operation import OperationMX
from .utils import CompileABC, SelectMX


def _convert_items(value):
    return tuple(prepare_column(i) for i in value)


@attrs.frozen(eq=False)
class Array(CompileABC, CastMX, AliasMX, OperationMX, SelectMX):
    _items: tuple[CompileABC, ...] = attrs.field(alias='items', converter=_convert_items)
    _marks: MARKS_TYPE = MARKS_FIELD
    _FMT: str = attrs.field(default='ARRAY[%s]')

    def _build(self, params: list | dict) -> str:
        if alias := extract_alias(self):
            return alias

        res = self._FMT % ', '.join(i._build(params) for i in self._items)
        if self._marks:
            res = self._marks.build(res)
        return res


@attrs.frozen(eq=False)
class Tuple(Array):
    _FMT: str = attrs.field(default='(%s)')
