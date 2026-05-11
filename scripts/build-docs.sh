#!/usr/bin/env bash
# Build docs in site/

for lang in en ru; do  # en should be the first language as it clears the root of the site
    if [ $lang == "en" ]; then
      output=site
      rm -rf $output
    else
      output=site/$lang
    fi

    echo $output, $lang
    sed "s/LANGUAGE/$lang/g" docs/zensical.yaml > docs/_zensical.yaml
    sed -i'' -e "s@OUTPUT@$output@g" docs/_zensical.yaml

    zensical build --config-file docs/_zensical.yaml
done
