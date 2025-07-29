# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import pytest

from pglift import databases, exceptions
from pglift.models import PostgreSQLInstance
from pglift.models.interface import Database, DatabaseDropped


@pytest.mark.anyio
async def test_standby_database_apply(
    pg_version: str, standby_pg_instance: PostgreSQLInstance
) -> None:
    with pytest.raises(
        exceptions.InstanceReadOnlyError,
        match=f"^{pg_version}/standby is a read-only standby instance$",
    ):
        await databases.apply(standby_pg_instance, Database(name="test"))


@pytest.mark.anyio
async def test_standby_database_drop(
    pg_version: str, standby_pg_instance: PostgreSQLInstance
) -> None:
    with pytest.raises(
        exceptions.InstanceReadOnlyError,
        match=f"^{pg_version}/standby is a read-only standby instance$",
    ):
        await databases.drop(standby_pg_instance, DatabaseDropped(name="test"))
