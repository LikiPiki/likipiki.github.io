# Likipiki Blog — [likipiki.github.io](https://likipiki.github.io/)

My [Hugo](https://gohugo.io/) blog using the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## Requirements

- [Hugo Extended 0.168.0](https://github.com/gohugoio/hugo/releases/tag/v0.168.0),
  matching `HUGO_VERSION` in [the deployment workflow](.github/workflows/hugo.yml).
- Git, including the PaperMod submodule pinned by this repository.

## Local development

```bash
git clone --recurse-submodules https://github.com/LikiPiki/likipiki.github.io.git
cd likipiki.github.io
hugo version
hugo server
```

Open the local URL printed by Hugo (normally `http://localhost:1313/`).
Use `hugo server -D` to include draft posts.

For an existing clone, initialize the theme with:

```bash
git submodule update --init --recursive
```

## Creating a post

The default archetype is [`archetypes/default.md`](archetypes/default.md).

```bash
hugo new content posts/my-post.md
```

## Production build and deployment

```bash
hugo --minify --panicOnWarning
python3 scripts/check-site.py public
```

The generated site is written to `public/`. Generated files are ignored by Git.
The asset check validates exact URL casing, including on case-insensitive macOS.
Pushes to `main` trigger the GitHub Actions workflow, which builds the site and
deploys it to GitHub Pages. The workflow can also be started manually.

## Updating Hugo and the theme

Update `HUGO_VERSION` in the workflow and use the same release locally. PaperMod
is pinned to a specific commit; to fetch its latest `master` revision:

```bash
git submodule update --remote --checkout themes/PaperMod
hugo --minify --panicOnWarning
```

Review the theme changes and check the home page, posts, archive, search, code
highlighting, and light/dark themes before committing the new submodule revision.
The current theme requires Hugo 0.158.0 or newer.

Local template overrides live in `layouts/archives.html` and `layouts/_partials/`.
They preserve Russian dates and month names and load Yandex Metrika using the
counter configured in `config.toml`.

## Contribution

Fork the repository, make your changes, check the production build, and open a
pull request.

---

You can find me on Telegram: [t.me/likipiki](https://t.me/likipiki).
