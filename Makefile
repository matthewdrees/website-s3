.SUFFIXES:

# In 2017 switched to a new style of index and photo creation.
# Leave the 2016 folders and earlier in the old format and don't
# regenerate. TODO: Update script to use old content. This involves
# working with the older, smaller images.
#OLD_CONTENT_FOLDERS := $(wildcard content/2014/*) \
#                       $(wildcard content/2015/*) \
#                       $(wildcard content/2016/*) \

CONTENT_FOLDERS := $(wildcard content/2018/*)

OUT_FOLDERS := $(patsubst content/%,out/%,$(CONTENT_FOLDERS))

MP4S := $(patsubst content/%,out/%,$(shell find content -name "*.mp4"))
OGVS := $(patsubst %.mp4,%.ogv,$(MP4S))

OUT_INDEX_HTMLS := $(addsuffix /index.html,$(OUT_FOLDERS))

.PHONY : all
all: $(MP4S) $(OGVS) $(OUT_INDEX_HTMLS) out/index.html

out/index.html : $(OUT_INDEX_HTMLS)
	python genindex.py --input content --output out

out/%.mp4 : content/%.mp4
	mkdir -p $(dir $@)
	cp $< $@
	python genmovie.py -j $< -m $@

out/%.ogv : content/%.mp4
	ffmpeg -i $< -c:v libtheora -q:v 7 -c:a libvorbis -q:a 4 $@
 
out/%/index.html : content/%/a.json
	mkdir -p $(dir $@)
	python genfolderindex.py --inputpath $(dir $<) --outputpath $(dir $@)

