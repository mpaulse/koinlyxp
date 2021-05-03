# KoinlyXP

![Build status](https://github.com/mpaulse/koinlyxp/workflows/KoinlyXP%20build/badge.svg)

A simple command-line application written in Python that allows you to export your cryptocurrency portfolio and
transaction information from [koinly.io](https://koinly.io) for offline back-up purposes.

## Installation:
- Requires Python 3.9+.
- Download the latest WHL [release](https://github.com/mpaulse/koinlyxp/releases/latest) file.
- Install with pip:
    ```
    pip install koinlyxp-version-py3-none-any.whl
    ```  
- Alternatively, install directly from this github repository:
    ```
    pip install git+https://github.com/mpaulse/koinlyxp#egg=koinlyxp
    ```

## Usage:
- Log into your [koinly.io](http://koinly.io) account and obtain the authorization token
  received from the server using in the browser Developer Tools. Look for the x-auth-token header sent
  in HTTP requests or the data returned in the /api/sessions response body.
- Run koinlyxp with the authorization token. For example:
    ```
    koinlyxp Pewi83249r23DSrgfw92934re32-dsfk3UWr
    ```
- For more usage help information, type:
    ```
    koinlyxp -h
    ```
- After use, log out of [koinly.io](http://koinly.io) to invalidate the authorization token.
