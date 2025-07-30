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
from dipend.__seedwork.strategy_interface import StrategyInterface
from dipend.exceptions.can_not_construct_dependency_exception import (
    CanNotConstructDependencyException,
)
from .resolve_lifecycle_strategy_input import ResolveLifecycleStrategyInput


class BaseResolveLifecycleStrategy(
    StrategyInterface[ResolveLifecycleStrategyInput, Any]
):
    def _construct(self, input_data: ResolveLifecycleStrategyInput) -> Any:
        implementation_details = input_data.dependency_registry.implementation_details

        if implementation_details.instance is not None:
            return implementation_details.instance

        if implementation_details.builder is not None:
            return implementation_details.builder()

        if implementation_details.class_constructor is None:
            raise CanNotConstructDependencyException(
                [input_data.dependency_registry.dependency_id]
            )

        return implementation_details.class_constructor(
            *input_data.resolved_class_constructor_dependencies
        )
