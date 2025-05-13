# select-git-author

A command-line tool to **interactively select or add a Git author** before
committing. Useful when working with multiple identities (e.g., personal, work,
open-source).

## ✨ Features

- Choose an author from a predefined list (`~/.git_authors`)
- Add and save a new author interactively
- Automatically sets `GIT_AUTHOR_NAME` and `GIT_AUTHOR_EMAIL`
- Optionally sets `GIT_COMMITTER_NAME` and `GIT_COMMITTER_EMAIL`

## 📦 Installation

```bash
pip install select-git-author
```


## 🚀 Usage

```bash
commit [GIT_COMMIT_ARGS...]
```

### Options

- `--author` – Specify an author from the list. If not provided, will prompt.
- `--set-commitor / --no-commitor` – Also set the Git committer fields (default: true)

### Example

```bash
commit -m "Update feature"
```

If no `--author` is given, you'll see an interactive menu like:

```
? Select Git author:
❯ Alice Dev <alice@example.com>
  Bob QA <bob@example.org>
  Add new author
```

If you choose "Add new author", it will prompt for name and email, and optionally save it.

## 🧠 Author Configuration

To predefine available authors, create a file at:

```
~/.git_authors
```

Format (one per line):

```
Alice Dev <alice@example.com>
Bob QA <bob@example.org>
```

## 📝 License

MIT
