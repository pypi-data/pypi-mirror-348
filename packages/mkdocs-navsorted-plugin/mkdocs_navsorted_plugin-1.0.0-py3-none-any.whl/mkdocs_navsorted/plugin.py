import sys
from pathlib import Path

import mkdocs
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import File
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page

log = get_plugin_logger(__name__)


class FilePatched(File):
    """Patched File allows us to have compiled files
    and directories without numeric prefixes.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dest_uri = self._unprefix_uri(self.dest_uri)

    @classmethod
    def _unprefix_uri(cls, uri: str) -> str:
        # strip numeric prefixes for every URI part
        parts = []
        for part in Path(uri).parts:

            prefix, _, url = part.partition('_')
            if prefix.isdigit():
                part = url

            parts.append(part)

        return f"{Path().joinpath(*parts)}"


class SortedPlugin(mkdocs.plugins.BasePlugin):

    def _restruct(self, items: list) -> list:
        unindexed = []
        items_to_sort = []

        for idx, item in enumerate(items):

            if children := item.children:
                item.children = self._restruct(children)  # do it recursively

            if isinstance(item, Section):
                prefix, _, title = item.title.partition(' ')

                if prefix.isdigit():
                    item.title = title.capitalize()
                    idx = int(prefix)

                else:
                    unindexed.append(item)
                    continue

            elif isinstance(item, Page):
                prefix, _, title = item.file.name.partition('_')
                if prefix.isdigit():
                    idx = int(prefix)

                else:
                    unindexed.append(item)
                    continue

            items_to_sort.append((item, idx))

        # sort by indexes (if any)
        # then add unindexed in original order
        result = [
            item
            for item, idx in
            sorted(items_to_sort, key=lambda item: (item[1], item[0].title or ''))
        ] + unindexed

        return result

    def on_startup(self, *args, **kwargs):
        name = 'File'
        patched = FilePatched

        log.debug(f"Applying patch '{name}' -> {patched.__name__} ...")
        modules = sys.modules

        for key, module in modules.items():
            if key.startswith('mkdocs') and 'config_options' not in key:
                if hasattr(module, name):
                    print(f"{key=}")
                    setattr(modules[key], name, patched)

    def on_nav(self, nav: Navigation, *args, **kwargs) -> Navigation | None:
        log.debug("Restructuring navigation ...")
        nav.items = self._restruct(nav.items)
        return nav
