[![Test](https://github.com/acdh-oeaw/acdh-id-reconciler/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-id-reconciler/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/acdh-id-reconciler.svg)](https://badge.fury.io/py/acdh-id-reconciler)
[![codecov](https://codecov.io/gh/acdh-oeaw/acdh-id-reconciler/branch/main/graph/badge.svg?token=WY0Q1GRIG1)](https://codecov.io/gh/acdh-oeaw/acdh-id-reconciler)
[![flake8 Lint](https://github.com/acdh-oeaw/acdh-id-reconciler/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-id-reconciler/actions/workflows/lint.yml)

# acdh-id-reconciler
python package to reconcile GND and GeoNames IDs via WikiData.


## install

`pip install acdh-id-reconciler`

## use

### from GND to WikiData and GeoNames ID

```python
from acdh_id_reconciler import gnd_to_geonames

test = "https://d-nb.info/gnd/4010858-2"
results = gnd_to_geonames(test)
print(results)
# {'wikidata': 'http://www.wikidata.org/entity/Q261664', 'gnd': '4010858-2', 'geonames': '2781124'}
```