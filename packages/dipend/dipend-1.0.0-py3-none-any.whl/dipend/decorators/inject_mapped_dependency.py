# Copyright 2025 Saulo V. Alvarenga. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Callable
from inspect import isclass
from builtins import __dict__ as builtins_dict
from ..exceptions.decorator_exception import DecoratorException


def inject_mapped_dependency(constructor_index: int, qualifier_token: Any):
    def decorator(cls: Callable):
        is_class = isclass(cls) and hasattr(cls, "__dict__") and cls not in builtins_dict.values()

        if not is_class:
            raise DecoratorException("inject_mapped_dependency is a class decorator.")

        if not isinstance(constructor_index, int):
            raise DecoratorException("constructor_index must be an int.")

        if not hasattr(cls, "__di_mapped_dependency"):
            setattr(cls, "__di_mapped_dependency", {})

        cls.__di_mapped_dependency[constructor_index] = [qualifier_token]

        return cls

    return decorator
