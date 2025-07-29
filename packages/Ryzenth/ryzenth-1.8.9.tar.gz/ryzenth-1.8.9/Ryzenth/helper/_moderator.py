#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019-2025 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import logging
from datetime import datetime as dt

import httpx

from Ryzenth._errors import WhatFuckError

LOGS = logging.getLogger("[Ryzenth]")

class ModeratorAsync:
    def __init__(self, parent):
        self.parent = parent

    async def antievalai(
        self,
        query: str,
        version: str,
        to_dict_by_loads=False,
        dot_access=False
    ):
        version_params = {
            "v1": "v1",
            "v2": "v2"
        }
        _version = version_params.get(version)
        if not _version:
            raise ValueError("Invalid Version Name")

        url = f"{self.parent.base_url}/v1/ai/akenox/antievalai-{_version}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    params={"query": query},
                    headers=self.parent.headers,
                    timeout=self.parent.timeout
                )
                response.raise_for_status()
                if to_dict_by_loads:
                    try:
                        return {
                            "author": "TeamKillerX",
                            f"timestamps": dt.now(),
                            f"is_detect": json.loads(response.json()["results"])["is_detect"],
                            "source": "Powered by Ryzenth API"
                        }
                    except json.decoder.JSONDecodeError:
                        return {
                            "author": "TeamKillerX",
                            f"timestamps": dt.now(),
                            f"is_detect": False,
                            "source": "Powered by Ryzenth API"
                        }
                return self.parent.obj(response.json() or {}) if dot_access else response.json()
            except httpx.HTTPError as e:
                LOGS.error(f"[ASYNC] Error: {str(e)}")
                raise WhatFuckError("[ASYNC] Error fetching") from e

class ModeratorSync:
    def __init__(self, parent):
        self.parent = parent

    def antievalai(
        self,
        query: str,
        version: str,
        to_dict_by_loads=False,
        dot_access=False
    ):
        version_params = {
            "v1": "v1",
            "v2": "v2"
        }
        _version = version_params.get(version)
        if not _version:
            raise ValueError("Invalid Version Name")

        url = f"{self.parent.base_url}/v1/ai/akenox/antievalai-{_version}"
        try:
            response = httpx.get(
                url,
                params={"query": query},
                headers=self.parent.headers,
                timeout=self.parent.timeout
            )
            response.raise_for_status()
            if to_dict_by_loads:
                try:
                    return {
                        "author": "TeamKillerX",
                        f"timestamps": dt.now(),
                        f"is_detect": json.loads(response.json()["results"])["is_detect"],
                        "source": "Powered by Ryzenth API"
                    }
                except json.decoder.JSONDecodeError:
                    return {
                        "author": "TeamKillerX",
                        f"timestamps": dt.now(),
                        f"is_detect": False,
                        "source": "Powered by Ryzenth API"
                    }
            return self.parent.obj(response.json() or {}) if dot_access else response.json()
        except httpx.HTTPError as e:
            LOGS.error(f"[SYNC] Error fetching from antievalai {e}")
            raise WhatFuckError("[SYNC] Error fetching from antievalai") from e
