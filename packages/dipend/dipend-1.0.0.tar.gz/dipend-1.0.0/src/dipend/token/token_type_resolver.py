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
from ..__seedwork.dictionary import Dictionary
from ..enums.token_type_enum import TokenTypeEnum
from ..__seedwork.base_checker import CheckerInterface
from .checkers.class_token_type_checker import ClassTokenTypeChecker
from .checkers.string_token_type_checker import StringTokenTypeChecker


class TokenTypeResolver:
    def __init__(self):
        self._checkers = Dictionary[str, CheckerInterface]()

    def set_default_token_type_checkers(self):
        self._checkers.set(TokenTypeEnum.CLASS_CONSTRUCTOR, ClassTokenTypeChecker())
        self._checkers.set(TokenTypeEnum.STRING, StringTokenTypeChecker())

    def set_token_type_checker(
        self,
        token_type: str,
        token_type_checker: CheckerInterface,
    ):
        self._checkers.set(token_type, token_type_checker)

    def get_token_type(self, token: Any) -> str:
        for token_type, token_type_checker in self._checkers.items():
            if token_type_checker.execute(token):
                return token_type

        return "UNKNOWN"
