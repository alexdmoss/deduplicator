# deduplicator

Some python to help find (and delete) duplicate files and similar images. Customised particularly to help me sort through many backups of photos collected over the years - some cropped and lower quality copies and such.

Code for image duplicate detection pinched from [https://github.com/philipbl/duplicate-images](https://github.com/philipbl/duplicate-images) - I didn't want the mongoDB store, but the pHashing was super-useful.

---

## Usage

Uses [Poetry](https://python-poetry.org/docs/), so `poetry install` and then:

1. `poetry run deduplicator --dir /path/to/search --output /file/to/save/results`
2. `poetry run pytest`

### Options

#### Deletion

Setting `--delete` will delete any EXACT MATCH (based on file-hash) files it finds after the first. Using this option means **how you organise the directory is important** for which original is kept - see [data setup](#data-setup) below.

This option **only runs for md5 hash matching of files currently**. The image fuzziness is still a bit too experimental for me to be confident in deleting :)

#### Images

Adding the `--images` flag will ignore non-image files, and attempt to compare images based on size, content, etc. It will still detect duplicates (as they should be a perfect match!).

If you run this against a large directory of images **it will thrash your CPU for a while**.

If you want to edit the "fuzziness" of the image search, the `FUZZINESS` variable is currently hard-coded at the top of `./deduplicator/images.py` if you're getting lots of false matches. I found 90% was letting too much through, and experimented before setting on 80.

---

## Data Setup

How you arrange the files in the one directory it searches affects how the results are displayed

## TODO

- [ ] Fix dockerised version and add instructions
- [ ] Finish test coverage
- [ ] Allow multiple paths?
