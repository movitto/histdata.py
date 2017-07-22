clean:
	rm -rf data/
	rm -rf tools/*.zip

sync:
	cd tools; ./sync.sh

split:
	cd tools; ./split.py

groups:
	cd tools; ./groups.py

all: sync split groups
.PHONY: all
