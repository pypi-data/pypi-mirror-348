import petl as _petl

def apply(table: _petl.Table, pipeline, *args, **kwargs):
    return pipeline(table, *args, **kwargs)

_petl.Table.apply = apply
_petl.Table.__and__ = apply
