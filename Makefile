.SUFFIXES:

2014_CONTENT_FOLDERS := $(wildcard content/2014/*)
2015_CONTENT_FOLDERS := $(wildcard content/2015/*)
2016_CONTENT_FOLDERS := $(wildcard content/2016/*)

CONTENT_FOLDERS := $(2014_CONTENT_FOLDERS) \
                   $(2015_CONTENT_FOLDERS) \
                   $(2016_CONTENT_FOLDERS)

OUT_FOLDERS := $(patsubst content/%,out/%,$(CONTENT_FOLDERS))

OUT_IMAGE_FOLDERS := $(addsuffix /images,$(OUT_FOLDERS))

$(shell mkdir -p $(OUT_IMAGE_FOLDERS))

IMAGES := $(patsubst content/%,out/%,$(shell find content -name "*.jpg"))

MP4S := $(patsubst content/%,out/%,$(shell find content -name "*.mp4"))
OGVS := $(patsubst %.mp4,%.ogv,$(MP4S))

OUT_INDEX_HTMLS := $(addsuffix /index.html,$(OUT_FOLDERS))
OUT_INDEX_JPGS := $(patsubst %.html,%.jpg,$(OUT_INDEX_HTMLS))

.PHONY : all
#all: $(IMAGES) $(MP4S) $(OGVS) $(OUT_INDEX_HTMLS) $(MOVIE_HTMLS) out/index.html
all: $(IMAGES) $(MP4S) $(OGVS) $(OUT_INDEX_HTMLS) $(OUT_INDEX_JPGS) out/index.html

out/index.html : $(OUT_INDEX_HTMLS)
	python3.5 genindex.py --input content --output out

out/%.jpg : content/%.jpg
	cp $< $@
	sips -Z 1000 $@

out/%.mp4 : content/%.mp4
	cp $< $@
	python genmovie.py -j $< -m $@

out/%.ogv : content/%.mp4
	ffmpeg2theora -o $@ -p padma $<
 
out/%/index.html : content/%/a.json
	python3.5 genfolderindex.py -j $< -l $@

out/%/index.jpg : content/%/a.json
	python3.5 genindexjpg.py --input $< --output $@
	sips -Z 400 $@

