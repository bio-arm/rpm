Name:           openeuler-extra-repos
Version:        22.03
Release:        LTS%{?dist}
Summary:        A package that adds some additional repositories to /etc/yum.repos.d/openEuler.repo

License:        ASL 2.0
URL:            https://github.com/bio-arm/rpms/
BuildArch:      noarch

Source1:        oe-extra-repos.repo

%description
A package that adds EPOL/update to /etc/yum.repos.d/openEuler.repo

%install
install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/yum.repos.d

%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/oe-extra-repos.repo

