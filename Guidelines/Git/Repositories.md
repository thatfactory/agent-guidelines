# Git Repositories

Use these rules when cloning repositories or configuring remotes.

## SSH-first cloning

Clone a repository over SSH when the working copy may be used to commit, push, or open a pull request:

```sh
git clone git@github.com:<owner>/<repository>.git
```

- Prefer an SSH `origin` so command-line tools and Git clients such as Fork can reuse the machine's GitHub SSH authentication.
- Do not create a push-capable working copy with an HTTPS `origin` unless the user or environment explicitly requires HTTPS.
- After cloning for development, use `git remote -v` to confirm that fetch and push URLs are correct.
- If an existing development clone has an HTTPS `origin`, change it only when requested or when the task explicitly includes remote setup:

  ```sh
  git remote set-url origin git@github.com:<owner>/<repository>.git
  ```

HTTPS remains appropriate for deliberately read-only retrieval, ephemeral automation, or environments where SSH credentials are unavailable. A public Git subtree remote may also remain HTTPS because consumers fetch tagged content without pushing to the guideline repository.
