# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024-2025 Anna <cyber@sysrq.in>

"""
Asynchronous wrapper for Repology API v1.
"""

import warnings
from collections.abc import Mapping, Sequence, Set
from pathlib import PurePosixPath
from typing import Any

import aiohttp
from pydantic import TypeAdapter

from repology_client._client import _json_api
from repology_client.constants import (
    API_V1_URL,
    HARD_LIMIT,
    MAX_PROBLEMS,
    MAX_PROJECTS,
)
from repology_client.exceptions import (
    InvalidInput,
    RepoNotFound,
)
from repology_client.types import (
    Package,
    Problem,
    ProjectsRange,
)
from repology_client.utils import ensure_session

package_set_adapter: TypeAdapter = TypeAdapter(Set[Package])
problem_list_adapter: TypeAdapter = TypeAdapter(Sequence[Problem])


async def api(endpoint: str, params: dict | None = None, *,
              session: aiohttp.ClientSession | None = None) -> Any:
    """
    Do a single API v1 request.

    :param endpoint: API endpoint (example: ``/projects``)
    :param params: URL query string parameters
    :param session: :external+aiohttp:py:mod:`aiohttp` client session

    :raises repology_client.exceptions.EmptyResponse: on empty response
    :raises repology_client.exceptions.InvalidInput: on invalid endpoint
        parameter
    :raises aiohttp.ClientResponseError: on HTTP errors
    :raises ValueError: on JSON decode failure

    :returns: decoded JSON response
    """

    return await _json_api(API_V1_URL, endpoint, params, session=session)


async def get_packages(project: str, *,
                       session: aiohttp.ClientSession | None = None) -> Set[Package]:
    """
    Access the ``/api/v1/project/<project>`` endpoint to list packages for a
    single project.

    :param project: project name on Repology
    :param session: :external+aiohttp:py:mod:`aiohttp` client session

    :raises repology_client.exceptions.EmptyResponse: on empty response
    :raises repology_client.exceptions.InvalidInput: if ``project`` is an empty
        string
    :raises aiohttp.ClientResponseError: on HTTP errors

    :returns: set of packages
    """

    if not project:
        raise InvalidInput(f"Not a valid project name: {project}")

    async with ensure_session(session) as aiohttp_session:
        endpoint = PurePosixPath("/project") / project
        data = await api(str(endpoint), session=aiohttp_session)
    return package_set_adapter.validate_python(data)


async def get_projects(start: str = "", end: str = "", count: int = 200, *,
                       session: aiohttp.ClientSession | None = None,
                       **filters: Any) -> Mapping[str, Set[Package]]:
    """
    Access the ``/api/v1/projects/`` endpoint to list projects.

    If both ``start`` and ``end`` are given, only ``start`` is used.

    :param start: name of the first project to start with
    :param end: name of the last project to end with
    :param count: maximum number of projects to fetch
    :param session: :external+aiohttp:py:mod:`aiohttp` client session

    :raises repology_client.exceptions.EmptyResponse: on empty response
    :raises aiohttp.ClientResponseError: on HTTP errors

    :returns: project to packages mapping
    """

    if count > HARD_LIMIT:
        warnings.warn(f"Resetting count to {HARD_LIMIT} to prevent API abuse")
        count = HARD_LIMIT

    proj_range = ProjectsRange(start=start, end=end)
    if start and end:
        warnings.warn("The 'start..end' range format is not supported by Repology API")
        proj_range.end = ""

    result: dict[str, set[Package]] = {}
    async with ensure_session(session) as aiohttp_session:
        while True:
            endpoint = PurePosixPath("/projects")
            if proj_range:
                endpoint /= str(proj_range)

            batch = await api(f"{endpoint}/", filters, session=aiohttp_session)
            for project in batch:
                result[project] = set()
                for package in batch[project]:
                    result[project].add(Package.model_validate(package))

            if len(result) >= count:
                break
            if len(batch) == MAX_PROJECTS:
                # we probably hit API limits, so…
                # …choose lexicographically highest project as a new start
                proj_range.start = max(batch)
                # …make sure we haven't already hit the requested end
                if end and proj_range.start >= end:
                    break
                # …and drop end condition as unsupported
                proj_range.end = ""
            else:
                break

    return result


async def get_problems(repo: str, maintainer: str = "",
                       start: str = "", count: int = 200, *,
                       session: aiohttp.ClientSession | None = None) -> Sequence[Problem]:
    """
    Access the endpoints to get problems for specific repository or maintainer.

    :param repo: repository name on Repology
    :param maintainer: maintainer e-mail address
    :param start: name of the first project to start with
    :param count: maximum number of projects to fetch
    :param session: :external+aiohttp:py:mod:`aiohttp` client session

    :raises repology_client.exceptions.InvalidInput: if ``repo`` is an empty
        string
    :raises repology_client.exceptions.EmptyResponse: on empty response
    :raises repology_client.exceptions.RepoNotFound: when there is no such repo
        on Repology
    :raises aiohttp.ClientResponseError: on HTTP errors (except 404)

    :returns: sequence of problems
    """

    if not repo:
        raise InvalidInput(f"Not a valid repository name: {repo}")

    if count > HARD_LIMIT:
        warnings.warn(f"Resetting count to {HARD_LIMIT} to prevent API abuse")
        count = HARD_LIMIT

    endpoint = PurePosixPath("/repository") / repo / "problems"
    if maintainer:
        endpoint = PurePosixPath("/maintainer") / maintainer / "problems-for-repo" / repo

    query = {}
    if start:
        query["start"] = start

    result: list[Problem] = []
    async with ensure_session(session) as aiohttp_session:
        while True:
            try:
                batch = await api(str(endpoint), query, session=aiohttp_session)
            except aiohttp.ClientResponseError as err:
                if err.status == 404:
                    raise RepoNotFound(repo) from err
                raise
            result.extend(problem_list_adapter.validate_python(batch))

            if len(result) >= count:
                break
            if len(batch) == MAX_PROBLEMS:
                # we probably hit API limits, so…
                # …choose lexicographically highest project as a new start
                query["start"] = max(item["project_name"] for item in batch)
            else:
                break

    return result
