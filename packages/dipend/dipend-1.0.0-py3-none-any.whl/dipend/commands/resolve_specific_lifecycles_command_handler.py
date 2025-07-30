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

from ..__seedwork.handler_interface import HandlerInterface
from .resolve_specific_lifecycles_command import ResolveSpecificLifecyclesCommand
from ..dependency.dependency_store import DependencyStore
from ..dependency.dependency_resolver import DependencyResolver


class ResolveSpecificLifecyclesCommandHandler(HandlerInterface[ResolveSpecificLifecyclesCommand, None]):
    def __init__(
        self,
        dependency_store: DependencyStore,
        dependency_resolver: DependencyResolver,
    ):
        self._dependency_store = dependency_store
        self._dependency_resolver = dependency_resolver

    def handle(self, input_data: ResolveSpecificLifecyclesCommand):
        sorted_dependencies = self._dependency_store.get_sorted_dependencies_ids()

        for dependency_id in sorted_dependencies:
            dependency_registry = self._dependency_store.get_dependency(dependency_id)

            if dependency_registry.lifecycle in input_data.lifecycles:
                self._dependency_resolver.resolve(dependency_id)
