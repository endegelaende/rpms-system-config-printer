.PHONY: srpm

FEDORA_LOOKASIDE = https://src.fedoraproject.org/repo/pkgs/rpms/system-config-printer
TARBALL = system-config-printer-1.5.18.tar.xz
SHA512 = 33dc9c52d92f4234e055fb10a99cadd58424dcdb62554797b44bdd5319f1c3662bd2fa33417ac3a3f5ec51216d64e81e1897f3e671eb49f6be34057d7c38f3f4

srpm:
	curl -fsSL -o $(TARBALL) "$(FEDORA_LOOKASIDE)/$(TARBALL)/sha512/$(SHA512)/$(TARBALL)"
	rpmbuild -bs system-config-printer.spec \
		--define "_sourcedir $$(pwd)" \
		--define "_specdir $$(pwd)" \
		--define "_srcrpmdir $(outdir)" \
		--define "dist %{nil}"
