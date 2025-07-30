#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from dataclasses import InitVar, dataclass, field
from itertools import islice
from typing import Any, Iterable, List, Mapping, MutableMapping, Union

import dpath
import requests

from airbyte_cdk.sources.declarative.decoders import Decoder, JsonDecoder
from airbyte_cdk.sources.declarative.extractors.record_extractor import RecordExtractor
from airbyte_cdk.sources.declarative.interpolation.interpolated_string import InterpolatedString
from airbyte_cdk.sources.types import Config


@dataclass
class KeyValueExtractor(RecordExtractor):
    """
    Extractor that combines keys and values from two separate extractors.

    The `keys_extractor` and `values_extractor` extract records independently
    from the response. Their outputs are zipped together to form key-value mappings.

    Each key from `keys_extractor` should correspond to a key in the resulting dictionary,
    and each value from `values_extractor` is the value for that key.

    Example:
      keys_extractor -> yields: ["name", "age"]
      values_extractor -> yields: ["Alice", 30]
      result: { "name": "Alice", "age": 30 }
    """

    keys_extractor: RecordExtractor
    values_extractor: RecordExtractor

    def extract_records(self, response: requests.Response) -> Iterable[MutableMapping[Any, Any]]:
        keys = list(self.keys_extractor.extract_records(response))
        values = self.values_extractor.extract_records(response)

        while True:
            chunk = list(islice(values, len(keys)))
            if not chunk:
                break
            yield dict(zip(keys, chunk))
