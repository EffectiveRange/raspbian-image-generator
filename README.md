# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/EffectiveRange/raspbian-image-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| image\_generator/\_\_init\_\_.py      |        6 |        0 |        0 |        0 |    100% |           |
| image\_generator/buildConfigurator.py |      130 |        0 |       30 |        9 |     94% |80->83, 83->88, 90->93, 93->96, 101->exit, 168->166, 177->184, 205->exit, 214->218 |
| image\_generator/buildInitializer.py  |       43 |        0 |       10 |        2 |     96% |58->exit, 62->58 |
| image\_generator/fileUtility.py       |       12 |        0 |        2 |        1 |     93% |  13->exit |
| image\_generator/imageBuilder.py      |       63 |        0 |       22 |        6 |     93% |61->69, 62->61, 64->66, 66->62, 67->62, 102->exit |
| image\_generator/imageGenerator.py    |       88 |        1 |       16 |        5 |     94% |27->26, 113, 121->exit, 136->142, 148->exit |
| image\_generator/targetConfig.py      |       16 |        0 |        0 |        0 |    100% |           |
|                             **TOTAL** |  **358** |    **1** |   **80** |   **23** | **95%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/EffectiveRange/raspbian-image-generator/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/EffectiveRange/raspbian-image-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/EffectiveRange/raspbian-image-generator/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/EffectiveRange/raspbian-image-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FEffectiveRange%2Fraspbian-image-generator%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/EffectiveRange/raspbian-image-generator/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.