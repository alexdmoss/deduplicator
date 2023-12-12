# deduplicator

Some python to help find (and delete) duplicate files and similar images. Customised particularly to help me sort through many backups of photos collected over the years - some cropped and lower quality copies and such.

Code for image duplicate detection pinched from [https://github.com/philipbl/duplicate-images](https://github.com/philipbl/duplicate-images) - I didn't want the mongoDB store, but the pHashing was super-useful.

---

## Usage

Uses [Poetry](https://python-poetry.org/docs/), so `poetry install` and then:

1. `poetry run deduplicator --dir /path/to/search --output /file/to/save/results`
2. `poetry run parse --input /path/to/image-results --output /path/to/save/output` - utility script to ask questions of the output
3. For development, `poetry run pytest`

e.g.

```sh
poetry run deduplicator --dir mocks/ --output output/out.txt --images
```

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

How you arrange the files in the one directory it searches affects how the results are displayed - they are listed in the order they are found, which effectively becomes alphabetically. To illustrate:

```txt
+-- backups
|   +-- duplicate-1.jpg
+-- for-web
|   +-- duplicate-2.jpg
+-- originals
|   +-- duplicate.jpg
```

Because `backups` comes ahead of `for-web` and `originals`, the results with be listed as `backups/duplicate-1.jpg, for-web/duplicate-2.jpg, originals/duplicate.jpg`, and **only** the backup will be kept if you run with `--delete` set.

In this example, `originals` might be the highest quality / correctly organised image that you want to keep, so some renaming would be a good idea:

```txt
+-- 01-originals
|   +-- duplicate.jpg
+-- 02-backups
|   +-- duplicate-1.jpg
+-- 03-for-web
|   +-- duplicate-2.jpg
```

Now `01-originals/duplicate.jpg` will be kept, and the other two duplicates deleted. Happy days!

---

## To Do

- [ ] Fix dockerised version and add instructions
- [ ] Finish test coverage
- [ ] Refactoring once tests in place - yield, list comp, data structures
- [ ] Allow multiple paths?
- [ ] I regret ditching the DB to store things. On large directories, it takes a long time! Upserting would be better

---

## Results

| State                       | # Files | Execution Time |
| --------------------------- | ------- | -------------- |
| Before file dupe detection  | 66,497  | N/A            |
| After file dupe dedection   | 27,153  | ~12m30s        |
| After delete 100% matches   | 23,031  |                |
| After delete 95% matches    | 15,252  | (needed multiple runs, likely bug) |
