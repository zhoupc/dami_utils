import xml.etree.ElementTree as ET
from typing import Optional, List, Dict
from latex2svg import latex2svg, default_params
import urllib.parse
import re
from tabulate import tabulate
import base64


class DrawIO:

    def __init__(self):
        self.root: Optional[ET.Element] = None
        self.diagram: Optional[ET.Element] = None

    def load(self, file_path: str) -> None:
        """Load a DrawIO file from the given file path."""
        tree = ET.parse(file_path)
        self.root = tree.getroot()
        self.diagram = self.root.find(".//diagram")
        if self.diagram is None:
            raise ValueError("No diagram found in the DrawIO file")

    def save(self, file_path: str) -> None:
        """Save the current DrawIO content to the given file path."""
        if self.root is None:
            raise ValueError("No DrawIO content to save")
        tree = ET.ElementTree(self.root)
        tree.write(file_path, encoding="UTF-8", xml_declaration=True)

    def get_elements(self) -> List[Dict[str, str]]:
        """Get all elements from the diagram, including their positions."""
        if self.diagram is None:
            return []
        elements = []
        for element in self.diagram.findall(".//mxCell"):
            element_data = {
                "id": element.get("id", ""),
                "value": element.get("value", ""),
                "style": element.get("style", ""),
                "parent": element.get("parent", ""),
                "vertex": element.get("vertex", ""),
                "edge": element.get("edge", ""),
            }

            # Get geometry information
            geometry = element.find("mxGeometry")
            if geometry is not None:
                element_data["x"] = geometry.get("x", "")
                element_data["y"] = geometry.get("y", "")
                element_data["width"] = geometry.get("width", "")
                element_data["height"] = geometry.get("height", "")

            elements.append(element_data)
        return elements

    def list_elements(self) -> None:
        """List all elements in the diagram in a table format with specified order."""
        elements = self.get_elements()
        if not elements:
            print("No elements found in the diagram.")
            return

        # Define the order of columns
        columns = [
            'id', 'position', 'size', 'style', 'value', 'vertex', 'edge'
        ]

        # Prepare the table data
        table_data = []
        for element in elements:
            row = [
                element.get('id', ''),
                f"({element.get('x', '')},{element.get('y', '')})",
                f"({element.get('width', '')},{element.get('height', '')})",
                self._truncate(element.get('style', '')),
                self._truncate(element.get('value', '')),
                element.get('vertex', ''),
                element.get('edge', '')
            ]
            table_data.append(row)

        # Print the table
        print(tabulate(table_data, headers=columns, tablefmt="grid"))

    @staticmethod
    def _truncate(s: str, max_length: int = 10) -> str:
        """Truncate a string to a maximum length."""
        return (s[:max_length] + '...') if len(s) > max_length else s

    def add_element(self, element_data: Dict[str, str]) -> None:
        """Add a new element to the diagram."""
        if self.diagram is None:
            raise ValueError("No diagram loaded")
        new_element = ET.SubElement(self.diagram, "mxCell")
        for key, value in element_data.items():
            new_element.set(key, value)

    def update_element(self, element_id: str, new_data: Dict[str,
                                                             str]) -> None:
        """Update an existing element in the diagram."""
        if self.diagram is None:
            raise ValueError("No diagram loaded")
        element = self.diagram.find(f".//mxCell[@id='{element_id}']")
        if element is None:
            raise ValueError(f"Element with id '{element_id}' not found")
        for key, value in new_data.items():
            element.set(key, value)

    def remove_element(self, element_id: str) -> None:
        """Remove an element from the diagram."""
        if self.diagram is None:
            raise ValueError("No diagram loaded")
        element = self.diagram.find(f".//mxCell[@id='{element_id}']")
        if element is None:
            raise ValueError(f"Element with id '{element_id}' not found")
        self.diagram.remove(element)

    def insert_latex_equation(self,
                              equation: str,
                              position: tuple[int, int],
                              fontsize: int = 12,
                              params: Optional[Dict] = None) -> str:
        """
        Convert a LaTeX equation to SVG and insert it into the DrawIO diagram at a specific location.

        :param equation: LaTeX equation string
        :param position: (x, y) tuple for the top-left corner of the equation
        :param fontsize: Font size for the equation (in pt, default 12pt)
        :param params: Additional parameters to pass to latex2svg
        :return: ID of the inserted element
        """
        if self.diagram is None:
            raise ValueError("No diagram loaded")

        x, y = position

        # Prepare params for latex2svg
        svg_params = default_params.copy()
        svg_params['fontsize'] = fontsize
        if params:
            svg_params.update(params)

        # Convert LaTeX equation to SVG
        svg_output = latex2svg(equation, params=svg_params)
        svg_string = svg_output['svg']

        # Convert SVG string to base64
        svg_base64 = base64.b64encode(
            svg_string.encode('utf-8')).decode('utf-8')

        # Create a unique ID for the new element
        new_id = f"latex_{len(self.get_elements()) + 1}"

        # Create the image element
        image_element = ET.SubElement(self.diagram, "mxCell")
        image_element.set("id", new_id)
        image_element.set(
            "style",
            f"shape=image;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/svg+xml;base64,{svg_base64};"
        )
        image_element.set("vertex", "1")
        image_element.set("parent", "1")

        # Set the geometry
        geometry = ET.SubElement(image_element, "mxGeometry")
        geometry.set("x", str(x))
        geometry.set("y", str(y))
        geometry.set("width", str(svg_output["width"]))
        geometry.set("height", str(svg_output["height"]))
        geometry.set("as", "geometry")

        return new_id

    def create_new(self) -> None:
        """Create a new empty DrawIO diagram."""
        self.root = ET.Element("mxfile")
        self.diagram = ET.SubElement(self.root, "diagram")
        self.diagram.set("id", "1")
        self.diagram.set("name", "Page-1")

        # Add default elements
        default_elements = [
            {
                "id": "0"
            },
            {
                "id": "1",
                "parent": "0"
            },
        ]
        for elem in default_elements:
            self.add_element(elem)
