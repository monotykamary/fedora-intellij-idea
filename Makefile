rpmbuild-dir := $(HOME)/rpmbuild
sources-dir := $(rpmbuild-dir)/SOURCES

intellij-version := 2017.1.5
intellij-dist := ideaIC-$(intellij-version)-no-jdk.tar.gz
intellij-dist-url := https://download.jetbrains.com/idea/$(intellij-dist)

$(rpmbuild-dir):
	rpmdev-setuptree

$(sources-dir)/$(intellij-dist):
	wget -NP $(sources-dir) $(intellij-dist-url)

build.txt: $(sources-dir)/$(intellij-dist)
	tar --no-wildcards-match-slash --strip-components=1 -O \
	    -xf $(sources-dir)/$(intellij-dist) 'idea-IC-*/build.txt' > $@
	cat build.txt
