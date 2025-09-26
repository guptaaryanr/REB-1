# Release Checklist for REB-1

## Pre-release
- [ ] Ensure `CHANGELOG.md` has an entry for the new version.
- [ ] Bump version in `pyproject.toml`, `reb1/__init__.py`, and `ros_reb1/setup.py`.
- [ ] Run full test suite (`pytest`, notebook, ROS node if available).
- [ ] Regenerate demo dataset if schema changed.
- [ ] Update `paper.md` if needed.

## Release
- [ ] Commit and push all changes.
- [ ] Create a git tag:
  ```bash
  git tag -a v0.1.0 -m "REB-1 v0.1.0"
  git push origin v0.1.0
  ```
- [ ] Draft a GitHub Release linked to the tag.

## Zenodo DOI
- [ ] Ensure Zenodo is linked to the repository.
- [ ] On first release, mint a DOI and update CITATION.cff.