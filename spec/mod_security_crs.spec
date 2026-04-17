Summary: ModSecurity Rules for Migration
Name: mod_security_crs
Version: 4.25.0
Release: 0%{?dist}
License: ASL 2.0
URL: https://coreruleset.org
Group: System Environment/Daemons

Source0: https://codeload.github.com/german-gonzalez-ruiz/crs-migration/tar.gz/refs/tags/v%{version}
BuildArch: noarch
Requires: mod_security >= 2.9.6
Obsoletes: mod_security_crs-extras < 3.0.0

%description
This package provides the base rules for mod_security.

%prep
%setup -q -n crs-migration-%{version}

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules
install -d %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules

# To remove old CRS version
rm -rf %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules/*
find %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/ -type l -xtype l -delete

# To exclude rules (pre/post)
mv rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
mv rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf

install -m0644 rules/* %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules/
mv crs-setup.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/crs-setup.conf

# activate base_rules
for f in `ls %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules/` ; do
    ln -s %{_datarootdir}/mod_modsecurity_crs/rules/$f %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/$f;
done

%files
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/activated_rules/*
%config %{_sysconfdir}/httpd/modsecurity.d/crs-setup.conf
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/local_rules/*
%{_datarootdir}/mod_modsecurity_crs


%changelog
* Fri Apr 17 2026 German Gonzalez <ggonzalez@tilsor.com.uy> - 1.0.0
- CRS Migration to CRS v4.25.0

* Wed Mar 04 2026 German Gonzalez <ggonzalez@tilsor.com.uy> - 1.0.0-RC1
- Migration to CRS v4.24.0
