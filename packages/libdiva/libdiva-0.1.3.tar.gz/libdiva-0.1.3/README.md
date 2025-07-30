# libdiva

a Project Diva format library and command-line tool

## installation

open a terminal session and install using pip:

`pip install libdiva`

alternatively, clone the repo and install locally:

```
git clone https://github.com/Flipleerr/libdiva
cd libdiva
pip install .
```

libdiva should now be installed. test by running `libdiva --help`.

## supported formats

libdiva supports the following formats:

- `dlt`: format used on the PS3 and Vita onwards, has information about files inside of DLC
- 'DIVAFILE': encryption format used in F 2nd and X
- 'FARC': compression format used in F 2nd and X

## usage examples

`libdiva dlt --write file.dlt --entries "data"`

`libdiva divafile --encrypt file.txt`

`libdiva extract file.farc extracted`

> [!TIP]
> you can also use libdiva like a proper library by entering `import libdiva` in your script.

## to-do

- [ ] FARC support (extract and repack)
- [ ] DLT boilerplate
- [ ] support for other Project Diva formats (`.cpk`, Dreamy Theater and F files, etc.)
- [ ] proper documentation or wiki
- [ ] refactor codebase
- [ ] a verbose option (-v or --verbose)

> [!NOTE]
> feel free to try your hand at any of these issues - any improvements help!

## contributing

all contributions to libdiva are welcome! to start:

1. fork the repo
2. clone it using `git clone https://github.com/USERNAME/libdiva (REPLACE 'USERNAME' WITH YOUR OWN!)`
3. create a new branch in the repo
4. make your changes

then submit a pull request!

> [!IMPORTANT]
> keep in mind that **GitHub Actions will automatically lint your code** when creating a pull request. if pylint fails, you'll be asked to fix the issues before merging. you can run pylint locally to check before pushing.
