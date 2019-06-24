# deduplicator

Some python to find (and delete) duplicate files.

## Usage

- `./go run -d=DIR` will scan DIR for duplicates
- `./go run -d=DIR -o=output.txt` will scan DIR for duplicates and output list of files found to output.txt
- if you don't want to mess about with Python/pipenv, then `./go build` will create a dockerised version that can be run in the same way as `./go run` but with `./go docker-run`
  - note that for saving of output with Docker using the `./go` wrapper, it expects -o to be a file in the `./output/` directory, e.g.
    `./go run-docker -d=test/ -o=./output/results.txt`

Run `./go init` to get started, and `./go watch-tests` to have continually running tests in the background.

## TODO

- [ ] Finish test coverage
- [ ] Allow multiple paths
