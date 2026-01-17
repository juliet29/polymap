update-deps:
  uv add /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/utils4plans


trial-all:
  uv run snakemake -c 3 -k all --configfile "msd.yaml"


test-move path:
  echo "Processing file: {{path}}"
  uv run preproc trial-move "{{path}}"
