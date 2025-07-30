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

from typing import Any
from inspect import isclass
from builtins import __dict__ as builtins_dict
from ...__seedwork.base_checker import CheckerInterface


class ClassTokenTypeChecker(CheckerInterface[Any]):
    def execute(self, input_data: Any) -> bool:
        return (
            isclass(input_data)
            and hasattr(input_data, "__dict__")
            and input_data not in builtins_dict.values()
        )
