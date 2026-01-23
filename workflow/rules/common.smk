
configfile: "config/config.yaml"
INPUT_PATH = config["pathvars"]["input_loc"]
SAMPLES = [i.stem for i in Path(INPUT_PATH).iterdir() if i.suffix == ".json"]
SMALL_SAMPLES = SAMPLES[0:5]
