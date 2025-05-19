# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/pagesmith/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                           |    Stmts |     Miss |   Cover |   Missing |
|----------------------------------------------- | -------: | -------: | ------: | --------: |
| src/pagesmith/\_\_about\_\_.py                 |        1 |        0 |    100% |           |
| src/pagesmith/chapter\_detector.py             |       55 |        1 |     98% |        64 |
| src/pagesmith/html\_page\_splitter.py          |      154 |       17 |     89% |37, 109-110, 127, 132, 141, 153, 166, 171-175, 178, 192-193, 229, 270 |
| src/pagesmith/page\_splitter.py                |       51 |        2 |     96% |   127-128 |
| src/pagesmith/parser.py                        |       22 |        0 |    100% |           |
| src/pagesmith/refine\_html.py                  |      187 |       24 |     87% |93-95, 174, 252, 263-272, 340, 378, 383, 397-406 |
| src/pagesmith/refine\_html\_beautiful\_soup.py |      107 |      107 |      0% |     4-317 |
|                                      **TOTAL** |  **577** |  **151** | **74%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/andgineer/pagesmith/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/pagesmith/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/andgineer/pagesmith/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/pagesmith/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fandgineer%2Fpagesmith%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/pagesmith/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.