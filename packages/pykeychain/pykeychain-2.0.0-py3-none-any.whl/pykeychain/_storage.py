from __future__ import annotations

import io
import re

import sh


class AlreadyExistsException(Exception):
    """Item already exists."""


class NotFoundException(Exception):
    """Item not found."""


class Storage:
    def __init__(self, service: str) -> None:
        self.service = service

    def get_password(self, account: str) -> str:
        out = io.StringIO()
        try:
            sh.security(
                "find-generic-password",
                "-w",
                s=self.service,
                a=account,
                _out=out,
            )
        except sh.ErrorReturnCode_44 as e:
            raise NotFoundException from e

        output = out.getvalue()
        return output[:-1]

    def save_password(self, account: str, password: str) -> None:
        try:
            sh.security(
                "add-generic-password",
                s=self.service,
                a=account,
                w=password,
            )
        except sh.ErrorReturnCode_45 as e:
            raise AlreadyExistsException from e

    def delete(self, account: str) -> None:
        try:
            sh.security(
                "delete-generic-password",
                s=self.service,
                a=account,
            )
        except sh.ErrorReturnCode_44 as e:
            raise NotFoundException from e

    def item_exists(self, account: str) -> bool:
        try:
            self.get_password(account)
        except NotFoundException:
            return False
        return True

    def get_all_accounts(self) -> list[str]:
        """Return all accounts in keychain in current service name.

        Each section has this structure:
            keychain:
                ...
                svce"<blob>="pytotp_client"
                ...
                acct"<blob>="my_account"
                ...

        :return list[str] - account names
        """
        out = io.StringIO()
        sh.security(
            "dump-keychain",
            "-r",
            _out=out,
        )
        output = out.getvalue().split(sep="\n")

        accounts: list[str] = []
        is_service_found = False
        last_account: str | None = None

        for line in output:
            if match := re.match(r'\s*"acct"<blob>="(?P<account>.+)"', line):
                last_account = match["account"]
            if f'"svce"<blob>="{self.service}"' in line:
                is_service_found = True
            if line.startswith("keychain:"):
                if is_service_found and last_account:
                    is_service_found = False
                    accounts.append(last_account)
                    last_account = None

        return accounts

    def search_accounts(self, search_pattern: str) -> list[str]:
        """Get all accounts whose names contain search pattern."""
        result: list[str] = []
        accounts = self.get_all_accounts()
        for account in accounts:
            if search_pattern in account:
                result.append(account)

        return result
