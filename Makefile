DATA_DIR=./data

all: $(DATA_DIR)/entries.csv

clean:
	rm -rf $(DATA_DIR)

$(DATA_DIR)/entries.csv: $(DATA_DIR)
	scrapy crawl entry -o $@ -L INFO

$(DATA_DIR):
	mkdir $(DATA_DIR)
