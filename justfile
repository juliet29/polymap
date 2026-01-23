update-deps:
  uv add /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/utils4plans


trial-some:
  uv run snakemake -c 3 -k some --configfile "config/msd.yaml"
trial-all:
  uv run snakemake -c 3 -f -k all --configfile "config/msd.yaml"

trial-hard:
  uv run snakemake -c 3 -k some --configfile "config/msd_hard.yaml"

test-move path:
  echo "Processing file: {{path}}"
  uv run preproc trial-move "{{path}}"
