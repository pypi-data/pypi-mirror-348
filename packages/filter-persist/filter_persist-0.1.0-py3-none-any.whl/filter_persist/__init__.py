import os
import streamlit.components.v1 as components

_RELEASE = False  # Set to False during dev

if not _RELEASE:
    _component_func = components.declare_component(
        "custom_aggrid",
        url="http://localhost:3001",  # Frontend dev server
    )
else:
    build_dir = os.path.join(os.path.dirname(__file__), "frontend", "build")
    # build_dir = os.path.join(os.path.dirname(__file__), "../frontend/build")
    _component_func = components.declare_component(
        "custom_aggrid",
        path=build_dir
    )


def custom_aggrid(data, column_defs, filter_model=None, key=None):
    return _component_func(
        data=data,
        columnDefs=column_defs,
        filterModel=filter_model,
        key=key,
        default={}
    )
