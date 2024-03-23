from pathlib import Path
import shutil

import config

import parsing
import utils
import mathjax_config
import file_manager

if __name__ == "__main__":
    if config.CLEAR_OUTPUT_FOLDER:
        if file_manager.OUTPUT_ROOT_PATH.exists():
            shutil.rmtree(file_manager.OUTPUT_ROOT_PATH)

    file_manager.OUTPUT_ROOT_PATH.mkdir(exist_ok=True)

    mathjax_config.generate()
    shutil.copytree(config.STATIC_FOLDER, file_manager.OUTPUT_ROOT_PATH, dirs_exist_ok=True)

    parsing.registerParsers()
    initialFilePaths = [Path(pathName).expanduser() for pathName in config.INITIAL_FILES]
    file_manager.generateAllBare(initialFilePaths)
    file_manager.generateAllFormatted()
