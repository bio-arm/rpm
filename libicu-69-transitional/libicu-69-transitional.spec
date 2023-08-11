Name: libicu-69-transitional
Version: 69
Release: 991%{?dist}
Summary: A "transitional" package for libicu from .69 to .72
License: ASL 2.0
URL: https://example.com

BuildRequires: libicu
BuildRequires: patchelf

%description
A package that copies .so.72.* files of the current libicu libraries to .so.69
and modifies their soname to libicu*.so.69
It should be used only when one needs to install a package that depends on
libicu-69 from openEuler 22.03 LTS (SP0).

%install

mkdir -p %{buildroot}%{_libdir}
cp %{_libdir}/libicui18n.so.72.* %{buildroot}%{_libdir}/libicui18n.so.69
patchelf --set-soname libicui18n.so.69 %{buildroot}%{_libdir}/libicui18n.so.69
cp %{_libdir}/libicuuc.so.72.* %{buildroot}%{_libdir}/libicuuc.so.69
patchelf --set-soname libicuuc.so.69 %{buildroot}%{_libdir}/libicuuc.so.69
cp %{_libdir}/libicudata.so.72.* %{buildroot}%{_libdir}/libicudata.so.69
patchelf --set-soname libicudata.so.69 %{buildroot}%{_libdir}/libicudata.so.69

%files
%{_libdir}/*.so.69

%changelog
* Fri Aug 11 2023 Martin Grigorov <mgrigorov@apache.org> - 69-991
- First version of the package