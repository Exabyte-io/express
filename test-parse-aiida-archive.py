import json
from express import ExPrESS

kwargs = {
    "path": "./tests/fixtures/aiida-archive/test-001/",
}

express_ = ExPrESS("aiida-archive", **kwargs)
print(json.dumps(express_.parser.structures(), indent=2))
