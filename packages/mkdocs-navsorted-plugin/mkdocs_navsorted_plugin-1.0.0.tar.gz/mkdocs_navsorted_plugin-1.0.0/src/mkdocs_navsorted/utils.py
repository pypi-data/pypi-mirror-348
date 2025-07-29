from mkdocs import config
from mkdocs.commands import build


def build_docs(conf: str = None):
    cfg = config.load_config(conf)
    cfg.plugins.on_startup(command='build', dirty=False)

    try:
        build.build(cfg)

    finally:
        cfg.plugins.on_shutdown()
