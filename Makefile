clean:
	rm -rf data/
	rm -rf tools/year/*.zip
	rm -rf tools/month/*.zip

sync:
	cd tools; ./sync.sh

split:
	cd tools; ./split.py

groups:
	cd tools; ./groups.py

extrapolate:
	cd tools; ./extrapolate.py

all: sync split
.PHONY: all
