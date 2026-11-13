#!/usr/bin/env python3
"""Получение проверенной локальной сборки Fuse.js для поискового скрипта PaperMod."""

import base64
import hashlib
import io
from pathlib import Path
import tarfile
import urllib.request


VERSION = "7.5.0"
INTEGRITY = "sQtrEfA+ez/3G0cCZecF70oqpCRttCexYUG4mUrtWL49ULUzUyxokt5kyqwtKzj1270RaKih+hcP3qLcumccow=="


def main():
    url = f"https://registry.npmjs.org/fuse.js/-/fuse.js-{VERSION}.tgz"
    with urllib.request.urlopen(url, timeout=30) as response:
        package = response.read()
    digest = base64.b64encode(hashlib.sha512(package).digest()).decode()
    if digest != INTEGRITY:
        raise SystemExit("SHA-512 архива Fuse.js не совпадает с закреплённым значением")
    with tarfile.open(fileobj=io.BytesIO(package), mode="r:gz") as archive:
        source = archive.extractfile("package/dist/fuse.basic.min.cjs").read().decode()
    if f"Fuse.js v{VERSION}" not in source:
        raise SystemExit("Версия Fuse.js в файле не совпадает с ожидаемой")
    header, body = source.split("*/", 1)
    output = (
        header + "*/\nvar Fuse = (function () {\nvar module = { exports: {} };\n"
        + body.strip() + "\nreturn module.exports;\n})();\n"
    )
    path = Path(__file__).resolve().parents[1] / "assets/js/fuse.basic.min.js"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output, encoding="utf-8")
    print(f"Fuse.js {VERSION}: SHA-512 проверен, сохранён {path.relative_to(path.parents[2])}")


if __name__ == "__main__":
    main()
