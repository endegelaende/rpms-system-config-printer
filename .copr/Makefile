.PHONY: srpm

srpm:
	dnf install -y spectool rpm-build 2>/dev/null || true
	spectool -g -C . system-config-printer.spec
	rpmbuild -bs system-config-printer.spec \
		--define "_sourcedir $$(pwd)" \
		--define "_specdir $$(pwd)" \
		--define "_srcrpmdir $(outdir)" \
		--define "dist %{nil}"
