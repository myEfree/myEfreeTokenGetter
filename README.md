# myEfree Token Getter

This is a simple script to get the refresh token to use when creating an account on [myEfree](https://portal.myefree.tech).

## Usage

First step is to create a python virtual environment and install the dependencies.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

You also need to install the `chromedriver` for your browser. You can download it from [here](https://googlechromelabs.github.io/chrome-for-testing/).

After that, you can run the script.

```bash
$ python main.py
```

Then go to [myEfree Registration Page](https://portal.myefree.tech/register) and create your account using the generated refreshToken!
