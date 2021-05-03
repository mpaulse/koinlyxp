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
import requests

__all__ = [
    "run"
]

BASE_API_URL = "https://api.koinly.io/api/"

def get_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        prog="koinlyxp",
        description="KoinlyXP - koinly.io portfolio and transaction data exporter")
    arg_parser.add_argument(
        "-f",
        dest="format",
        action="store",
        default="json",
        choices=["json"],
        help="the output format")
    arg_parser.add_argument(
        "auth_token",
        metavar="AUTH-TOKEN",
        action="store",
        help="the koinly.io authorization token received after logging into the site")
    return arg_parser.parse_args()


def run():
    args = get_args()
    http = requests.session()
    http.headers["x-auth-token"] = args.auth_token
    data = http.get(f"{BASE_API_URL}/transactions?per_page=20&order=date").json()
    print(data)

if __name__ == "__main__":
    run()
