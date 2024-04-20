# Mistletoe Extensions

This is an extension of the [mistletoe python library](https://github.com/miyuchina/mistletoe) to add a renderer for modernCV and a MudBlazor web page. It is not highly configurable without changing the source code so use it at your own risk.

By default it will render the example file. You can also pass in a git repository (if you have ssh access) and relative filename or point to a specific file in your local system.

## Custom Syntax
I have given an example md file to show some of the custom syntax I used to make both the md readable and also easily parseable into tokens to be used in the modernCV output.

The main missing piece is for personal info. This can be done as follows.

```
`email`    [example@gmail.com](mailto:example@gmail.com) |
`mobile`   [+1 237 565 8492](tel:+2375658492) |
`homepage` [www.example.org](https://www.example.org) |
`github`   [TheToby1](https://github.com/TheToby1) |
`linkedin` [TobyBurns](https://www.linkedin.com/in/tobyburns/)
```

## Installation and Usage
Mistletoe should install through conda-forge with the requirements.txt file:

`conda config --append channels conda-forge`

The v0.9.0 (at the time of writing) on pip should also work.

It is recommended to set up a conda environment to run it in:

`conda create --name cvtools --file requirements.txt`
`conda activate cvtools`

And then run with something like:

`python render.py cv_example.md`

There are a couple of extra arguments you can use. You can check these with:

`python .\render.py --help`