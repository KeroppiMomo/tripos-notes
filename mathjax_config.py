from pathlib import Path
import file_manager

import config

def generate():
    preamble = Path(config.MATHJAX_PREAMBLE).read_text()
    mathjax_config = Path(config.MATHJAX_CONFIG_FORMAT).read_text()
    escaped_preamble = preamble \
        .replace("\\", "\\\\") \
        .replace("`", "\\`") \
        .replace("$", "\\$")
    mathjax_config_formatted = mathjax_config.replace("{{preamble}}", escaped_preamble)
    (file_manager.OUTPUT_ROOT_PATH / "mathjax-config.js").write_text(mathjax_config_formatted)

