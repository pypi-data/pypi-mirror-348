"""Sphinx event functions and directives.

Sphinx extension machinery

.. py:data:: logger
   :type: sphinx.util.logging.SphinxLoggerAdapter

   Module level logger. No idea how to see or store these log messages

"""

from __future__ import annotations

from pathlib import (
    Path,
    PurePosixPath,
)

from docutils import nodes
from sphinx.addnodes import toctree as toctree_node
from sphinx.errors import ExtensionError
from sphinx.transforms import SphinxTransform
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.matching import Matcher

from ._compat import findall
from .api import (
    Document,
    FileItem,
    GlobItem,
    RefItem,
    SiteMap,
    UrlItem,
)
from .filename_suffix import stem_natural
from .parsing_strictyaml import parse_toc_yaml

logger = logging.getLogger(__name__)


def create_warning(
    app,
    doctree,
    category,
    message,
    *,
    line=None,
    append_to=None,
    wtype="etoc",
):
    """Generate a warning, logging it if necessary.

    If the warning type is listed in the ``suppress_warnings`` configuration,
    then ``None`` will be returned and no warning logged.

    :param app: Sphinx app instance
    :type: sphinx.application.Sphinx
    :param doctree: document where the issue occurred
    :type doctree: docutils.nodes.document
    :param category: category of warning (ref, glob, toctree, tableofcontents)
    :type category: str
    :param message: warning message to log
    :type message: str
    :param line: Default None. line number
    :type line: int | None
    :param append_to: Default None. Node element
    :type append_to: docutils.nodes.Element | None
    :param wtype:

       Default "etoc". Warning type. ``etoc`` means coming from Sphinx
       extension ``etoc``

    :type wtype: str
    :returns: docutils system message
    :rtype: docutils.nodes.system_message | None
    """
    message = f"{message} [{wtype}.{category}]"
    kwargs = {"line": line} if line is not None else {}

    if not logging.is_suppressed_warning(wtype, category, app.config.suppress_warnings):
        msg_node = doctree.reporter.warning(message, **kwargs)
        if append_to is not None:
            append_to.append(msg_node)
        return msg_node
    return None


def remove_suffix(docname, suffixes):
    """Remove any suffixes

    :param docname:

       docname. May or may not contain a suffix. May or may not contain a relative path

    :type docname: str
    :param suffixes:

       From sphinx option ``source_suffix``. Default ``.rst``. if wanting
       to support markdown requires both ``.rst`` and ``.md``

    :type suffixes: list[str]
    :returns: docname without the suffix
    :rtype: str

    .. deprecated:: 1.1.0

       Use
       :py:func:`filename_suffix.stem_natural <sphinx_external_toc_strict.filename_suffix.stem_natural>`
       instead

    """
    for suffix in suffixes:
        if docname.endswith(suffix):
            return docname[: -len(suffix)]
    return docname


def parse_toc_to_env(app, config):
    """Parse the external toc file and store it in the Sphinx environment.

    Also, change the ``master_doc`` and add to ``exclude_patterns`` if necessary.

    :param app: Sphinx app instance
    :type app: sphinx.application.Sphinx
    :param config:

       Sphinx environment configuration settings as supplied by
       ``pyproject.toml`` and ``conf.py``

    :type config: sphinx.config.Config
    """
    # TODO this seems to work in the tests, but I still want to double check
    external_toc_path = PurePosixPath(app.config["external_toc_path"])
    if not external_toc_path.is_absolute():
        path = Path(app.srcdir) / str(external_toc_path)
    else:
        path = Path(str(external_toc_path))
    if not path.exists():
        raise ExtensionError(f"[etoc] `external_toc_path` does not exist: {path}")
    if not path.is_file():
        raise ExtensionError(f"[etoc] `external_toc_path` is not a file: {path}")
    try:
        site_map = parse_toc_yaml(path)
    except Exception as exc:
        raise ExtensionError(f"[etoc] {exc}") from exc
    config.external_site_map = site_map  # type: ignore[attr-defined]

    # Update the master_doc to the root doc of the site map
    # root_doc = remove_suffix(site_map.root.docname, config.source_suffix)
    root_doc = stem_natural(site_map.root.docname)
    if config["master_doc"] != root_doc:
        logger.info("[etoc] Changing master_doc to '%s'", root_doc)
    config["master_doc"] = root_doc

    if config["external_toc_exclude_missing"]:
        # add files not specified in ToC file to exclude list
        new_excluded = site_map.new_excluded(
            app.srcdir,
            config["source_suffix"],
            config["exclude_patterns"],
        )
        if new_excluded:
            excluded_count = len(new_excluded)
            msg_info = f"[etoc] Excluded {excluded_count!s} extra file(s) not in toc"
            logger.info(msg_info)
            msg_debug = f"[etoc] Excluded extra file(s) not in toc: {new_excluded!r}"
            logger.debug(msg_debug)
            # Note, don't `extend` list, as it alters the default `Config.config_values`
            config["exclude_patterns"] = config["exclude_patterns"] + new_excluded


def add_changed_toctrees(
    app,
    env,
    added,
    changed,
    removed,
):
    """Add docs with new or changed toctrees to changed list

    :param app: Sphinx app instance
    :type app: sphinx.application.Sphinx
    :param env: Sphinx app environment
    :type env: sphinx.environment.BuildEnvironment
    :param added: Added documents
    :type added: set[str]
    :param changed: Changed documents
    :type changed: set[str]
    :param removed: Removed documents
    :type removed: set[str]
    :returns: Documents changed
    :rtype: set[str]
    """
    previous_map = getattr(app.env, "external_site_map", None)
    # move external_site_map from config to env
    site_map: SiteMap
    app.env.external_site_map = site_map = app.config.external_site_map  # type: ignore[attr-defined]
    # Compare to previous map, to record docnames with new or changed toctrees
    if not previous_map:
        return set()
    filenames = site_map.get_changed(previous_map)
    # set_files = {remove_suffix(name, app.config.source_suffix) for name in filenames}
    set_files = {stem_natural(name) for name in filenames}

    return set_files


class TableOfContentsNode(nodes.Element):
    """A placeholder for the insertion of a toctree (in ``insert_toctrees``)

    :ivar attributes: keyword arguments forwarded to parent class
    :vartype: typing.Any
    """

    def __init__(self, **attributes):
        """Class constructor."""
        super().__init__(rawsource="", **attributes)


class TableofContents(SphinxDirective):  # type: ignore[misc]
    """Insert a placeholder for toctree insertion."""

    # TODO allow for name option of tableofcontents (to reference it)
    def run(self):
        """Insert a ``TableOfContentsNode`` node

        :returns: list of ToC nodes
        :rtype: list[sphinx_external_toc_strict.events.TableOfContentsNode]
        """
        node = TableOfContentsNode()
        self.set_source_info(node)
        return [node]


def insert_toctrees(app, doctree):
    """Create the toctree nodes and add it to the document.

    Adapted from `sphinx/directives/other.py::TocTree`

    :param app: Sphinx app instance
    :type app: sphinx.application.Sphinx
    :param doctree: Document into which insert tableofcontents directive
    :type doctree: docutils.nodes.document
    """
    # check for existing toctrees and raise warning
    for node in findall(doctree)(toctree_node):
        create_warning(
            app,
            doctree,
            "toctree",
            "toctree directive not expected with external-toc",
            line=node.line,
        )

    toc_placeholders: list[TableOfContentsNode] = list(
        findall(doctree)(TableOfContentsNode)
    )

    site_map: SiteMap = app.env.external_site_map  # type: ignore[attr-defined]
    doc_item: Document | None = site_map.get(app.env.docname)

    # check for matches with suffix
    # TODO check in sitemap, that we do not have multiple docs of the same name
    # (strip extensions on creation)
    for suffix in app.config.source_suffix:
        if doc_item is not None:
            break
        doc_stem = stem_natural(app.env.docname)
        if len(doc_stem) == 0:
            suf_doc = Path(f"bob{app.env.docname}").suffix
        else:
            suf_doc = Path(app.env.docname).suffix
        if len(suf_doc) == 0:
            # docname -- no suffix
            doc_item = site_map.get(app.env.docname + suffix)
        else:
            if suf_doc != suffix:
                # docname -- different suffix
                doc_item = site_map.get(f"{doc_stem}{suffix}")
            else:
                # docname -- matching suffix
                doc_item = site_map.get(doc_stem)

    is_no_document_or_descendants = doc_item is None or not doc_item.subtrees
    if is_no_document_or_descendants:
        if toc_placeholders:
            create_warning(
                app,
                doctree,
                "tableofcontents",
                "tableofcontents directive in document with no descendants",
            )
        for node in toc_placeholders:
            node.replace_self([])
        return

    # TODO allow for more than one tableofcontents, i.e. per part?
    for node in toc_placeholders[1:]:
        create_warning(
            app,
            doctree,
            "tableofcontents",
            "more than one tableofcontents directive in document",
            line=node.line,
        )
        node.replace_self([])

    # initial variables
    all_docnames = app.env.found_docs.copy()
    all_docnames.remove(app.env.docname)  # remove current document
    excluded = Matcher(app.config.exclude_patterns)

    node_list: list[nodes.Element] = []

    for toctree in doc_item.subtrees:
        subnode = toctree_node()
        subnode["parent"] = app.env.docname
        subnode.source = doctree["source"]
        subnode.line = 1
        subnode["entries"] = []
        subnode["includefiles"] = []
        subnode["maxdepth"] = toctree.maxdepth
        subnode["caption"] = toctree.caption
        # TODO this wasn't in the original code,
        # but alabaster theme intermittently raised `KeyError('rawcaption')`
        subnode["rawcaption"] = toctree.caption or ""
        subnode["glob"] = any(isinstance(entry, GlobItem) for entry in toctree.items)
        subnode["hidden"] = False if toc_placeholders else toctree.hidden
        subnode["includehidden"] = False
        subnode["numbered"] = (
            0
            if toctree.numbered is False
            else (999 if toctree.numbered is True else int(toctree.numbered))
        )
        subnode["titlesonly"] = toctree.titlesonly
        wrappernode = nodes.compound(classes=["toctree-wrapper"])
        wrappernode.append(subnode)

        for entry in toctree.items:
            if isinstance(entry, UrlItem):
                t_sphinx_renderable: tuple[str, str] = next(entry.render())
                subnode["entries"].append(t_sphinx_renderable)
            elif isinstance(entry, RefItem):
                # Very similar to UrlItem, except needs app to retrieve from inventory
                t_sphinx_renderable: tuple[str, str] = next(entry.render(app))
                subnode["entries"].append(t_sphinx_renderable)
            elif isinstance(entry, FileItem):
                t_sphinx_renderable: tuple[str, str] = next(entry.render(site_map))
                _, docname = t_sphinx_renderable

                if docname not in app.env.found_docs:
                    if excluded(app.env.doc2path(docname, base=False)):
                        message = (
                            "toctree contains reference to excluded "
                            f"document {docname!r}"
                        )
                    else:
                        message = (
                            "toctree contains reference to nonexisting "
                            f"document {docname!r}"
                        )

                    create_warning(app, doctree, "ref", message, append_to=node_list)
                    app.env.note_reread()
                else:
                    subnode["entries"].append(t_sphinx_renderable)
                    subnode["includefiles"].append(docname)
            elif isinstance(entry, GlobItem):
                doc_count = 0
                for t_sphinx_renderable in entry.render(all_docnames):
                    _, docname = t_sphinx_renderable
                    all_docnames.remove(docname)  # don't include it again
                    subnode["entries"].append(t_sphinx_renderable)
                    subnode["includefiles"].append(docname)
                    doc_count += 1

                is_no_docs = doc_count == 0
                if is_no_docs:
                    message = (
                        f"toctree glob pattern '{entry}' didn't match any documents"
                    )
                    create_warning(app, doctree, "glob", message, append_to=node_list)

        # reversing entries can be useful when globbing
        if toctree.reversed:
            subnode["entries"] = list(reversed(subnode["entries"]))
            subnode["includefiles"] = list(reversed(subnode["includefiles"]))

        node_list.append(wrappernode)

    if toc_placeholders:
        toc_placeholders[0].replace_self(node_list)
    elif doctree.children and isinstance(doctree.children[-1], nodes.section):
        # note here the toctree cannot not just be appended to the end of the doc,
        # since `TocTreeCollector.process_doc` expects it in a section
        # otherwise it will result in the child documents being on the same level as this document
        # TODO check if there is this is always ok
        doctree.children[-1].extend(node_list)
    else:
        doctree.children.extend(node_list)


class InsertToctrees(SphinxTransform):  # type: ignore[misc]
    """Create the toctree nodes and add it to the document.

    This needs to occur at least before the ``DoctreeReadEvent`` (priority 880),
    which triggers the `TocTreeCollector.process_doc` event (priority 500)

    .. py:attribute:: default_priority
       :type: int
       :value: 100
       :noindex:

       Priority of inserted tableofcontents node

    """

    default_priority = 100

    def apply(self, **kwargs):
        """Calls insert_toctrees
        :ivar kwargs: Keyword arguments
        :vartype: typing.Any
        """
        insert_toctrees(self.app, self.document)


def ensure_index_file(app, exception):
    """Ensure that an index.html exists for HTML builds.

    This is required when navigating to the site, without specifying a page,
    which will then route to index.html by default.

    :param app: Sphinx app instance
    :type app: sphinx.application.Sphinx
    :param exception: Exception to throw when file missing
    :type exception: Exception | None
    """
    index_path = Path(app.outdir).joinpath("index.html")
    if (
        exception is not None
        or "html" not in app.builder.format
        or app.config.master_doc == "index"
        # TODO: rewrite the redirect if master_doc has changed since last build
        or index_path.exists()
    ):
        return

    # root_name = remove_suffix(app.config.master_doc, app.config.source_suffix)
    root_name = stem_natural(app.config.master_doc)

    if app.builder.name == "dirhtml":
        redirect_url = f"{root_name}/index.html"
    else:
        # Assume a single index for all non dir-HTML builders
        redirect_url = f"{root_name}.html"

    redirect_text = f'<meta http-equiv="Refresh" content="0; url={redirect_url}" />\n'
    index_path.write_text(redirect_text, encoding="utf8")
    logger.info("[etoc] missing index.html written as redirect to '%s.html'", root_name)
