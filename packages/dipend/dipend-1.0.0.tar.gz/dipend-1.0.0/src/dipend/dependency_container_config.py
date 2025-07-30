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

from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class DependencyContainerConfig:
    """
    Configuration settings for DependencyContainer.

    Attributes:
        disable_default_resolve_lifecycle_strategies (Optional[bool]):
            Whether to disable default resolve lifecycle strategies.
        disable_default_token_type_checkers (Optional[bool]):
            Whether to disable default token type checkers.
        disable_default_token_name_strategies (Optional[bool]):
            Whether to disable default token name strategies.
        disable_build_required (Optional[bool]):
            Whether to disable build requirement.
        custom_dependency_container_token (Optional[Any]):
            Custom token for dependency container.
    """

    disable_default_resolve_lifecycle_strategies: Optional[bool] = field(default=False)
    disable_default_token_type_checkers: Optional[bool] = field(default=False)
    disable_default_token_name_strategies: Optional[bool] = field(default=False)
    build_singletons_required: Optional[bool] = field(default=False)
    custom_dependency_container_token: Optional[Any] = None
