# KoinlyXP

![Build status](https://github.com/mpaulse/koinlyxp/workflows/KoinlyXP%20build/badge.svg)

A simple command-line application written in Python that allows you to export your cryptocurrency portfolio and
transaction information from [koinly.io](https://koinly.io) for offline back-up and record-keeping purposes.

## Installation:
- Requires Python 3.9+.
- Download the latest WHL [release](https://github.com/mpaulse/koinlyxp/releases/latest) file.
- Install with pip:
    ```
    pip install koinlyxp-version-py3-none-any.whl
    ```  
- Or install directly from this github repository:
    ```
    pip install git+https://github.com/mpaulse/koinlyxp#egg=koinlyxp
    ```

## Usage:
- Log into your [koinly.io](http://koinly.io) account and obtain the browser user agent and authorization token
  received from the server using the browser Developer Tools. Look for the x-auth-token header sent
  in HTTP requests or the data returned in the /api/sessions response body.
- Run koinlyxp with your authorization token and user agent. For example:
    ```
    koinlyxp Pewi83249r23DSrgfw92934re32-dsfk3UWr "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    ```
- Human-readable CSV files and raw JSON data fetched from koinly will be saved in a timestamped
  output directory:
  - assets: Information about the cryptocurrency assets held in the portfolio.
  - asset_accounts: Cryptocurrency asset holdings per account/wallet.
  - stats: Amounts sent and received, income, expenses, etc. for the current year.
  - tax_report: Tax report information for the current and previous years.
- After use, log out of [koinly.io](http://koinly.io) to invalidate the authorization token.  
