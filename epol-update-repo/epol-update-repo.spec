Name:           openeuler-extra-repos
Version:        22.03
Release:        LTS%{?dist}
Summary:        A package that adds some additional repositories to /etc/yum.repos.d/openEuler.repo

License:        ASL 2.0
URL:            https://github.com/bio-arm/rpms/

%description
A package that adds EPOL/update to /etc/yum.repos.d/openEuler.repo


%post
if ! grep -q EPOL/update /etc/yum.repos.d/openEuler.repo; then
    cat << EOF >> /etc/yum.repos.d/openEuler.repo

[EPOL_update]
name=EPOL_update
baseurl=http://repo.openeuler.org/openEuler-22.03-LTS/EPOL/update/main/$basearch/
enabled=1
gpgcheck=1
gpgkey=http://repo.openeuler.org/openEuler-22.03-LTS/OS/$basearch/RPM-GPG-KEY-openEuler

EOF
fi