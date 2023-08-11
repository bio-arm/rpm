Name: libicu-69-transitional
Version: 69
Release: 991%{?dist}
Summary: A transitional package for libicu
License: GPL-2.0-only
URL: https://example.com

BuildRequires: libicu

%description
A package that creates symbolic links of the current libicu libraries to .so.69

%install

mkdir -p %{buildroot}%{_libdir}
cp %{_libdir}/libicui18n.so.72 %{buildroot}%{_libdir}/libicui18n.so.69
cp %{_libdir}/libicuuc.so.72 %{buildroot}%{_libdir}/libicuuc.so.69
cp %{_libdir}/libicudata.so.72 %{buildroot}%{_libdir}/libicudata.so.69

%files
%{_libdir}/*.so.69

%changelog
* Fri Aug 11 2023 Martin Grigorov <mgrigorov@apache.org> - 69-991
- First version of the package