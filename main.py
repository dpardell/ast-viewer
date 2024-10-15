import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element, ElementTree
from graphviz import Digraph
import argparse


class XMLASTParser:
    def __init__(self, input_type):
        self.input_type = input_type

    def parse(self, ast_data) -> Element:
        if self.input_type == "string":
            return et.fromstring(ast_data)
        elif self.input_type == "file":
            return et.parse(ast_data).getroot()


class XMLGraphBuilder:
    def build_graph(
        self, graph: Digraph, ast_node: Element, parent=None, count={"id": 0}
    ):
        node_value = ast_node.attrib.get("val", "")

        unique_name = f"node_{count['id']}"
        count["id"] += 1

        graph.node(unique_name, label=node_value)

        if parent is not None:
            graph.edge(parent, unique_name)

        for child in ast_node:
            self.build_graph(graph, child, parent=unique_name, count=count)


def create_digraph(ast_data, parser, builder, format):
    ast = parser.parse(ast_data)
    digraph = Digraph(name="AST", comment="Visualization of the AST", format=format)
    builder.build_graph(digraph, ast)

    return digraph


def display_digraph(graph, output_file):
    graph.render(output_file, view=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file name")
    parser.add_argument(
        "output", type=str, help="base for output file name (do not include extension)"
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="xml",
        help="parser mode: xml, json (not supported yet)",
    )
    parser.add_argument("-F", "--format", type=str, default="png", help="png, svg")
    args = parser.parse_args()

    if args.mode == "xml":
        parser = XMLASTParser(input_type="file")
    else:
        parser.print_help()
        return

    builder = XMLGraphBuilder()

    graph = create_digraph(args.input, parser, builder, args.format)
    display_digraph(graph, args.output)


if __name__ == "__main__":
    main()
