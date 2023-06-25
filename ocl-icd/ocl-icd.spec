Name:                ocl-icd
Version:             2.2.14
Release:             2
Summary:             OpenCL ICD Bindings
License:             BSD
URL:                 https://github.com/OCL-dev/ocl-icd/tree/v%{version}
Source0:             https://github.com/OCL-dev/ocl-icd/archive/refs/tags/v%{version}.tar.gz

BuildRequires:       gcc automake autoconf make libtool opencl-headers ruby rubygems

%description
%{summary}.

%package devel
Summary:             Development files for %{name}
Requires:            %{name}%{?_isa} = %{version}-%{release} opencl-headers
%description devel
This package contains the development files for %{name}.

%prep
%autosetup -p1

%build
autoreconf -vfi
%configure
%make_build

%install
%make_install
rm -vf %{buildroot}%{_libdir}/*.la
rm -vrf %{buildroot}%{_defaultdocdir}

%check
make check
%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS README
%{_libdir}/libOpenCL.so.*

%files devel
%doc ocl_icd_loader_gen.map ocl_icd_bindings.c
%{_includedir}/ocl_icd.h
%{_libdir}/libOpenCL.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/OpenCL.pc

%changelog
* Sun Jun 25 2023 yangxingyu <yangxingyu13@huawei.com> - 2.2.14
- update to 2.2.14

* Fri Jul 30 2021 sunguoshuai <sunguoshuai@huawei.com> - 2.2.12-2
- ocl-icd fix build error with gcc 10

* Mon Jul 27 2020 maminjie <maminjie1@huawei.com> - 2.2.12-1
- package init
