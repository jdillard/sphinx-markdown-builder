"""Custom translator for single markdown file output."""

# pyright: reportImplicitOverride=false

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx import addnodes

from sphinx_markdown_builder.translator import MarkdownTranslator

if TYPE_CHECKING:  # pragma: no cover
    from sphinx_markdown_builder.singlemarkdown import SingleFileMarkdownBuilder


class SingleMarkdownTranslator(MarkdownTranslator):
    """Translator that ensures proper content inclusion for a single markdown file."""

    def __init__(self, document: nodes.document, builder: "SingleFileMarkdownBuilder"):
        super().__init__(document, builder)
        # Track docnames as we traverse (like HTML translator)
        self.docnames: list[str] = []

    def visit_start_of_file(self, node: nodes.Element) -> None:
        """Handle start_of_file nodes created by inline_all_toctrees.

        This is similar to how the HTML5 translator handles it - just add an anchor.
        """
        docname = node["docname"]
        self.docnames.append(docname)
        # Add anchor for document linking (like singlehtml does)
        self.add(f'<a id="document-{docname}"></a>', prefix_eol=2)

    def depart_start_of_file(self, node: nodes.Element) -> None:
        """Clean up after start_of_file node."""
        self.docnames.pop()
