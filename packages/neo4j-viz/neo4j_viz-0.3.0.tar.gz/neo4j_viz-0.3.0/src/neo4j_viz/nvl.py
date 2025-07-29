from __future__ import annotations

import json
import uuid
from importlib.resources import files

from IPython.display import HTML

from .node import Node
from .options import RenderOptions
from .relationship import Relationship


class NVL:
    def __init__(self) -> None:
        # at which point we get None?
        base_folder = files("neo4j_viz")
        resource_folder = base_folder / "resources"
        nvl_entry_point = resource_folder / "nvl_entrypoint"

        js_path = nvl_entry_point / "base.js"
        with js_path.open("r", encoding="utf-8") as file:
            self.library_code = file.read()

        styles_path = nvl_entry_point / "styles.css"
        with styles_path.open("r", encoding="utf-8") as file:
            self.styles = file.read()

        icons = resource_folder / "icons"

        zoom_in_path = icons / "zoom-in.svg"
        with zoom_in_path.open("r", encoding="utf-8") as file:
            self.zoom_in_svg = file.read()

        zoom_out_path = icons / "zoom-out.svg"
        with zoom_out_path.open("r", encoding="utf-8") as file:
            self.zoom_out_svg = file.read()

        screenshot_path = icons / "screenshot.svg"
        with screenshot_path.open("r", encoding="utf-8") as file:
            self.screenshot_svg = file.read()

    def unsupported_field_type_error(self, e: TypeError, entity: str) -> Exception:
        if "not JSON serializable" in str(e):
            return ValueError(f"A field of a {entity} object is not supported: {str(e)}")
        return e

    def render(
        self,
        nodes: list[Node],
        relationships: list[Relationship],
        render_options: RenderOptions,
        width: str,
        height: str,
        show_hover_tooltip: bool,
    ) -> HTML:
        try:
            nodes_json = json.dumps([node.to_dict() for node in nodes])
        except TypeError as e:
            raise self.unsupported_field_type_error(e, "node")
        try:
            rels_json = json.dumps([rel.to_dict() for rel in relationships])
        except TypeError as e:
            raise self.unsupported_field_type_error(e, "relationship")

        render_options_json = json.dumps(render_options.to_dict())
        container_id = str(uuid.uuid4())

        if show_hover_tooltip:
            hover_element = f"document.getElementById('{container_id}-tooltip')"
            hover_div = f'<div id="{container_id}-tooltip" class="tooltip" style="display: none;"></div>'
        else:
            hover_element = "null"
            hover_div = ""

        # Using a different varname for every instance, so that a notebook
        # can use several instances without unwanted interactions.
        # The first part of the UUID should be "unique enough" in this context.
        nvl_varname = "graph_" + container_id.split("-")[0]
        download_name = nvl_varname + ".png"

        js_code = f"""
        var {nvl_varname} = new NVLBase.NVL(
            document.getElementById('{container_id}'),
            {hover_element},
            {nodes_json},
            {rels_json},
            {render_options_json},
        );
        """
        full_code = self.library_code + js_code

        html_output = f"""
        <style>
            {self.styles}
        </style>
        <div id="{container_id}" style="width: {width}; height: {height}; position: relative;">
            <div style="position: absolute; z-index: 2147483647; right: 0; top: 0; padding: 1rem">
                <button type="button" title="Save as PNG" onclick="{nvl_varname}.nvl.saveToFile({{ filename: '{download_name}' }})" class="icon">
                    {self.screenshot_svg}
                </button>
                <button type="button" title="Zoom in" onclick="{nvl_varname}.nvl.setZoom({nvl_varname}.nvl.getScale() + 0.5)" class="icon">
                    {self.zoom_in_svg}
                </button>
                <button type="button" title="Zoom out" onclick="{nvl_varname}.nvl.setZoom({nvl_varname}.nvl.getScale() - 0.5)" class="icon">
                    {self.zoom_out_svg}
                </button>
            </div>
            {hover_div}
        </div>

        <script>
            getTheme = () => {{
                const backgroundColorString = window.getComputedStyle(document.body, null).getPropertyValue('background-color')
                const colorsArray = backgroundColorString.match(/\d+/g);
                const brightness = Number(colorsArray[0]) * 0.2126 + Number(colorsArray[1]) * 0.7152 + Number(colorsArray[2]) * 0.0722
                return brightness < 128 ? "dark" : "light"
            }}
            document.documentElement.className = getTheme()

            {full_code}
        </script>
        """

        return HTML(html_output)  # type: ignore[no-untyped-call]
