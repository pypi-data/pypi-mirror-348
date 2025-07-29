# Python wrapper for the E3.series COM interface

python e3series is a wrapper library for the E3.series COM interface.
The library enhances the automatic code completion and static program verification for python programs that automate E3.series.

This library requires a working instance of the software Zuken E3.series.

## Getting Started

Install the library via pip:
```
pip install e3series
```

Use the library:
```python
import e3series as e3

app = e3.Application()
app.PutInfo(0, "hello, world!")
```

For more samples you can visit the git repository [https://github.com/Pat711/E3SeriesPythonSamples](https://github.com/Pat711/E3SeriesPythonSamples).


## Releasenotes

#### Version 0.3
- Added `e3series.tools.E3seriesOutput` to redirect the output of the print function to the E3.series message window.

#### Version 0.2
- First Release. Contains wrappers for all COM-Objects of the E3.series release 26.0.

#### Version 0.1
- Placeholder package with no content.