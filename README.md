# deduplicator

Some python to find (and delete) duplicate files.

Code for image duplicate detection pinched from https://github.com/philipbl/duplicate-images - I didn't want the mongoDB store, but the pHashing was super-useful.

---

## Usage

Without arguments you will be prompted with the help.

There is a bash wrapper script because I am lazy:

- `./go run -d=DIR` will scan DIR for duplicates
- `./go run -d=DIR -o=output.txt` will scan DIR for duplicates and output list of files found to output.txt
- Adding the `--images` flag will ignore non-image files, and attempt to compare images based on size, content, etc. If you run this against a large directory of images **it will thrash your CPU for a while**.
  - you want to change the `FUZZINESS` variable at the top of `./deduplicator/images.py` if you're getting lots of false matches. I found 90% was letting too much through, and experimented before setting on 80.

- if you don't want to mess about with Python/pipenv, then `./go build` will create a dockerised version that can be run in the same way as `./go run` but with `./go docker-run`
  - note that for saving of output with Docker using the `./go` wrapper, it expects -o to be a file in the `./output/` directory, e.g.
    `./go run-docker -d=test/ -o=./output/results.txt`

## TODO

- [ ] Finish test coverage
- [ ] Allow multiple paths
