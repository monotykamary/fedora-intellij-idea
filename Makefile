results-dir := results
spec-file := intellij-idea-community.spec
mock-config := default.cfg

version != grep ^Version: $(spec-file) | awk '{print $$2}'
release != grep ^Release: $(spec-file) | awk -F'( +|%)' '{print $$2}'

$(results-dir):
	mkdir -pv $@

deps: intellij-idea-community.spec
	./spectool.pl --get-files $<

srpm := results/intellij-idea-community-$(version)-$(release).*.src.rpm
$(error $(srpm))
$(srpm): intellij-idea-community.spec | deps
	rpmbuild -v -bs $< --define "_sourcedir $(PWD)" --define "_srcrpmdir $(results-dir)"

rpms: $(srpm) | $(results-dir)
	mock -r $(mock-config) --rebuild *.src.rpm --resultdir $(results-dir)

.PHONY: deps
