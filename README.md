# Electric Objects NYTimes Frontpage

Update Electric Objects with NYTimes frontpage daily.

![](/screenshot.jpg)

## Prerequisites

1. Electric Objects device and account (unfortunately no longer for sale).
2. S3 bucket
3. Server with cron

## Setup

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run script

```
export AWS_ACCESS_KEY_ID=<key>
export AWS_SECRET_ACCESS_KEY=<secret>
python ./update_eo_nytimes.py --user=<eo-login-email> --password=<eo-password> --bucket=<bucket-name> --region=<aws-region> --device=<eo-device-id>
```

The easiest way to get your EO device ID is to go to the [set url](https://www.electricobjects.com/set_url) page, inspect element on the Device dropdown, and find the device ID there.

You can optionally provide a date using the `--date` parameter on the script. It looks like the NYTimes front page scans are available going back to 2016.

## Cron job

The Cron job runs at 10AM UTC (6AM EDT).

```
PYTHONPATH=<path-to-this-project>
AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
0 10 * * * <path-to-this-project>/venv/bin/python <path-to-this-project>/update_eo_nytimes.py --user=<eo-login-email> --password=<eo-password --bucket=<bucket-name> --device=<eo-device-id> 2>&1 >> <path-to-this-project>/update_eo_nytimes.log
```

## Credits

The Electric Objects API wrapper is based on a [Gist from Harper Reed](https://gist.github.com/harperreed/693288fc14ad35f75d09).

This project was inspired by a much more ambitious project that [displays the NYTimes front page on a 31 inch e-ink screen](https://onezero.medium.com/the-morning-paper-revisited-35b407822494).

## License

Copyright &copy; Brian Donohue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
