# attestation

Automatically send your attestation letters.

----------------------------------

## Installation

To install clone this repository and then run:

```shell
pip install -e .
```

## Usage

After installation you need to modify the first lines of the file `src/attestation/_template.py`.
You will want to modify `PI_name`, `role`, `address`, and you might want to inform `signature_path` and `logo_path` as **absolute** paths.

Setting `signature_path` or `logo_path` to the empty string will ignore them.

Once you have modified these variables you can ran the code as follow

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"attestation" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

----------------------------------

This library was generated using [Cookiecutter] and a custom made template based on [@napari]'s [cookiecutter-napari-plugin] template.


[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
[tox]: https://tox.readthedocs.io/en/latest/

[file an issue]: https://github.com/GuignardLab/attestation/issues

