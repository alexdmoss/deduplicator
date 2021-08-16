# deduplicator

Some python to find (and delete) duplicate files.

Code for image duplicate detection pinched from [https://github.com/philipbl/duplicate-images](https://github.com/philipbl/duplicate-images) - I didn't want the mongoDB store, but the pHashing was super-useful.

---

## Usage

Uses [Poetry](https://python-poetry.org/docs/), so `poetry install` and then:

1. `poetry run deduplicator`
2. `poetry run pytest`

Adding the `--images` flag will ignore non-image files, and attempt to compare images based on size, content, etc. If you run this against a large directory of images **it will thrash your CPU for a while**.

If you want to edit the "fuzziness" of the image search, the `FUZZINESS` variable is currently hard-coded at the top of `./deduplicator/images.py` if you're getting lots of false matches. I found 90% was letting too much through, and experimented before setting on 80.

## TODO

- [ ] Fix debug logging not working
- [ ] Fix dockerised version and add instructions
- [ ] Makefile
- [ ] Finish test coverage
- [ ] Allow multiple paths?
