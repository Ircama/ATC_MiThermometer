# Enabling uploading atc_mi_advertising.zip to GH Release

https://github.com/pvvx/ATC_MiThermometer/settings/actions

In the left sidebar, click  Actions, then click General.

Go down to the "Workflow permissions" section.

Select "Read and write permissions".

Press SAVE.

# Tagging

Push all changes:

```shell
git commit -a
git push
```

_After pushing the last commit_, add a local tag (shall be added AFTER the commit that needs to rebuild the exe):

```shell
git tag # list local tags
git tag v1.0.0
```

Push this tag to the origin, which starts the rebuild workflow (GitHub Action):

```shell
git push origin v1.0.0
git ls-remote --tags https://github.com/pvvx/ATC_MiThermometer # list remote tags
```
