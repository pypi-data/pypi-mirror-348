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
from inspect import _empty
from ..__seedwork.handler_interface import HandlerInterface
from ..token.token_store import TokenStore
from ..dependency.dependency_store import DependencyStore
from ..dependency.implementation_details import ImplementationDetails
from ..dependency.dependency_registry import DependencyRegistry
from ..dependency.dependency_resolver import DependencyResolver
from ..helpers.inspect_class_helper import InspectClassHelper
from ..exceptions.can_not_construct_dependency_exception import (
    CanNotConstructDependencyException,
)
from .add_dependency_command import (
    AddDependencyCommand,
)


class AddDependencyCommandHandler(HandlerInterface[AddDependencyCommand, None]):
    def __init__(
        self,
        token_store: TokenStore,
        dependency_store: DependencyStore,
        dependency_resolver: DependencyResolver,
    ):
        self._token_store = token_store
        self._dependency_store = dependency_store
        self._dependency_resolver = dependency_resolver

    def _get_class_constructor_dependencies_ids(self, dependency_id: str, class_constructor: Callable):
        class_constructor_dependencies_tokens: list[Any] = []
        mapped_dependencies: dict[int, list[Any]] = {}

        if hasattr(class_constructor, "__di_mapped_dependency"):
            mapped_dependencies = getattr(class_constructor, "__di_mapped_dependency")

        class_constructor_dependencies_tokens = InspectClassHelper.get_constructor_dependencies(class_constructor)

        class_constructor_dependencies_ids: list[str] = []

        for index, class_constructor_dependency_token in enumerate(class_constructor_dependencies_tokens):
            if class_constructor_dependency_token == _empty:
                raise CanNotConstructDependencyException([dependency_id])

            mapped_dependency = mapped_dependencies.get(index, [])

            class_constructor_dependencies_ids.append(
                self._token_store.retrieve_or_create_dependency_id_by_tokens(
                    [class_constructor_dependency_token, *mapped_dependency],
                )
            )

        return class_constructor_dependencies_ids

    def handle(
        self,
        input_data: AddDependencyCommand,
    ) -> Any:
        dependency_id = self._token_store.retrieve_or_create_dependency_id_by_tokens(input_data.tokens)

        class_constructor_dependencies_ids: list[str] = []

        if input_data.class_constructor is not None:
            class_constructor_dependencies_ids = self._get_class_constructor_dependencies_ids(dependency_id, input_data.class_constructor)

        implementation_details = ImplementationDetails(
            input_data.class_constructor,
            class_constructor_dependencies_ids,
            input_data.builder,
            input_data.instance,
        )

        registry = DependencyRegistry(
            dependency_id,
            input_data.lifecycle,
            implementation_details,
        )

        self._dependency_store.add_dependency(registry)
