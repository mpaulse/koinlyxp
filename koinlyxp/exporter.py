#  Copyright (c) 2021 Marlon Paulse
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import argparse
import datetime
import json
import os
import pytz
import requests

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pytz.tzinfo import DstTzInfo
from requests import Session

__all__ = [
    "run"
]

BASE_API_URL = "https://api.koinly.io/api"


@dataclass
class UserInfo:
    base_currency: str
    base_currency_usd_rate: Decimal
    timezone: DstTzInfo


def get_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        prog="koinlyxp",
        description="KoinlyXP - koinly.io portfolio and transaction data exporter")
    arg_parser.add_argument(
        "auth_token",
        metavar="AUTH-TOKEN",
        action="store",
        help="the koinly.io authorization token received after logging into the site")
    return arg_parser.parse_args()


def get_user_info(http_session: Session) -> UserInfo:
    rsp_body = http_session.get(f"{BASE_API_URL}/sessions").json()
    user = rsp_body.get("user")
    if isinstance(user, dict):
        currency_info = user.get("base_currency")
        if not isinstance(currency_info, dict):
            raise Exception("No base currency information found for user")
        base_currency = currency_info.get("symbol")
        if not isinstance(base_currency, str):
            raise Exception("No base currency symbol information found for user")
        base_currency_usd_rate = currency_info.get("usd_rate")
        if not isinstance(base_currency_usd_rate, str):
            raise Exception("No base currency USD rate information found for user")
        timezone_name = user.get("timezone")
        if not isinstance(timezone_name, str):
            raise Exception("No timezone information found for user")
        return UserInfo(
            base_currency=base_currency,
            base_currency_usd_rate=Decimal(base_currency_usd_rate),
            timezone=pytz.timezone(timezone_name))


def get_list(
        data_type: str,
        http_session: Session, url: str,
        url_params: dict[str, any] = None,
        data_type_description: str = None) -> list[dict]:
    data = []
    if url_params is None:
        url_params = {}
    if data_type_description is None:
        data_type_description = data_type
    print(f"Fetching {data_type_description}...")
    page = 1
    while True:
        url_params["page"] = page
        rsp_body = http_session.get(url, params=url_params).json()
        rsp_data = rsp_body.get(data_type)
        if rsp_data is None:
            break
        if isinstance(rsp_data, list):
            for entry in rsp_data:
                data.append(entry)
        meta = rsp_body.get("meta")
        if meta is None:
            break
        page_info = meta.get("page")
        if page_info is None:
            break
        total_items = page_info.get("total_items")
        if isinstance(total_items, int):
            print(f"Fetched {len(data)} / {total_items}")
        total_pages = page_info.get("total_pages")
        if isinstance(total_pages, int) and page < total_pages:
            page += 1
        else:
            break
    return data


def get_asset_accounts(assets: list[dict], http_session: Session) -> dict:
    asset_accounts: dict[str, list[dict]] = {}
    for asset in assets:
        currency_info = asset.get("currency")
        if isinstance(currency_info, dict):
            id = currency_info.get("id")
            symbol = currency_info.get("symbol")
            if isinstance(id, int) and isinstance(symbol, str):
                asset_accounts[symbol] = \
                    get_list(
                        "accounts",
                        http_session,
                        f"{BASE_API_URL}/accounts",
                        {"per_page": 50, "q[currency_id_eq]": id},
                        f"{symbol} accounts")
    return asset_accounts


def get_tax_reports(dt_now: datetime, http_session: Session) -> dict[int, dict]:
    print(f"Fetching tax reports for {dt_now.year} and {dt_now.year - 1}...")
    return {
        dt_now.year: http_session.get(f"{BASE_API_URL}/stats/{dt_now.year}").json(),
        dt_now.year - 1: http_session.get(f"{BASE_API_URL}/stats/{dt_now.year - 1}").json()
    }


def get_stats(dt_from: datetime, dt_to: datetime, user_info: UserInfo, http_session: Session) -> dict:
    dt_format = "%a %b %d %Y %H:%M:%S GMT%z"
    dt_from = user_info.timezone.localize(dt_from).strftime(dt_format)
    dt_to = user_info.timezone.localize(dt_to).strftime(dt_format)
    print(f"Fetching stats for {dt_from} to {dt_to}...")
    return http_session.get(f"{BASE_API_URL}/stats", params={"from": dt_from, "to": dt_to}).json()


def run():
    args = get_args()

    dt_now = datetime.now()
    dt_year_start = datetime(dt_now.year, 1, 1, 0, 0, 0)
    dt_year_end = datetime(dt_now.year, 12, 31, 23, 59, 59)

    http_session = requests.session()
    http_session.headers["x-auth-token"] = args.auth_token

    user_info = get_user_info(http_session)
    transactions = get_list("transactions", http_session, f"{BASE_API_URL}/transactions", {"order": "date"})
    assets = get_list("assets", http_session, f"{BASE_API_URL}/assets")
    asset_accounts = get_asset_accounts(assets, http_session)
    tax_reports = get_tax_reports(dt_now, http_session)
    current_year_stats = get_stats(dt_year_start, dt_year_end, user_info, http_session)

    dt_format = '%Y-%m-%dT%H-%M-%S'
    output_dir = f"koinly_{dt_now.strftime(dt_format)}"
    os.mkdir(output_dir)
    print(f"Saving to directory {output_dir}...")
    with open(f"{output_dir}/transactions.json", "w") as f:
        f.write(json.dumps(transactions, indent=4))
    with open(f"{output_dir}/assets.json", "w") as f:
        f.write(json.dumps(assets, indent=4))
    with open(f"{output_dir}/asset_accounts.json", "w") as f:
        f.write(json.dumps(asset_accounts, indent=4))
    for year, tax_report in tax_reports.items():
        with open(f"{output_dir}/tax_report_{year}.json", "w") as f:
            f.write(json.dumps(tax_report, indent=4))
    with open(
            f"{output_dir}/stats_{dt_year_start.strftime(dt_format)}_to_{dt_year_end.strftime(dt_format)}.json",
            "w") as f:
        f.write(json.dumps(current_year_stats, indent=4))


if __name__ == "__main__":
    run()
