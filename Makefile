define HELP

Commands:
  help               print this help text
  setup_requirements install additional requirements
endef
export HELP

help:
	@echo "$${HELP}"

setup_conda:
	@if [ -z "$${CONDA_SHLVL:+x}" ]; then echo "Conda is not installed." && exit 1; fi
	@conda create -y -n conda_metrics-env python=3.8
	@echo "\n\nConda environment has been created. To activate run \"conda activate conda_metrics-env\"."

setup_requirements:
	@conda install -y -n conda_metrics-env --file requirements.txt