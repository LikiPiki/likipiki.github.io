# Likipiki Blog [likipi.gitlab.io](https://likipiki.gitlab.io/)

This is my [hugo](https://gohugo.io/) blog. 

## Installation

1. Clone the repository by SHH or HTTP.
2. Install [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme:
	```bash
	cd likipiki.gitlab.io
	git submodule init
	git submodule update
	```
3. Run hugo server:
	```bash
	hugo server
	```
	
## Contribution
If you can contribute to my repository:
1. Fork repository.
2. Clone it to your local machine.
3. Edit some content.
4. Create pull-request.

## Page creation

Default archetype is [`archetype/default.md`](https://gitlab.com/likipiki/likipiki.gitlab.io/-/blob/master/archetypes/default.md)
```
hugo new posts/my-post.md
```

## Update theme

Update [PaperMod theme](https://github.com/adityatelange/hugo-PaperMod.git) to
latest commit. Do it carefully, and fix all merge conflicts if need!

```
git submodule update --remote --merge
```

---
You can find me in telegram [t.me/likipiki](https://t.me/likipiki)
