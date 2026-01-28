# Repo hygiene notes

## Remove macOS metadata before committing
From repo root (preview first):
- Find:
  find . -name '.DS_Store' -o -name '__MACOSX' -o -name '._*' -print

Then delete (after confirming the list looks safe):
- .DS_Store and AppleDouble files:
  find . -name '.DS_Store' -delete
  find . -name '._*' -delete

- __MACOSX directories (if any):
  find . -type d -name '__MACOSX' -prune -exec rm -rf {} +

## Outputs in git
You intend to include outputs and outputs_glue_axes in the repo for reruns.
The .gitignore in this patch does NOT ignore these directories, but it does ignore SNAPSHOT* intermediates.
