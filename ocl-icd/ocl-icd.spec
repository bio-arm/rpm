#
# spec file for package ocl-icd
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           ocl-icd
Version:        2.3.1
Release:        2.1
Summary:        OpenCL ICD Bindings
License:        BSD-2-Clause
URL:            https://github.com/OCL-dev/ocl-icd
Source:         https://github.com/OCL-dev/ocl-icd/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        baselibs.conf
# PATCH-FEATURE-OPENSUSE n_UsrShare.patch boo#1173005, comment#8
Patch0:         n_UsrShare.patch
BuildRequires:  libtool
BuildRequires:  opencl-headers >= 2.2
BuildRequires:  pkgconfig
BuildRequires:  ruby
BuildRequires:  pkgconfig(egl)

%description
OpenCL is a royalty-free standard for cross-platform, parallel programming
of modern processors found in personal computers, servers and
handheld/embedded devices.

This package provides an Installable Client Driver Bindings (ICD Bindings).
The provided libOpenCL library is able to load any free or non-free installed
ICD (driver backend).

%package     -n libOpenCL1
Summary:        OpenCL ICD Bindings
Suggests:       pocl
%if (0%{?sle_version} >= 150100 || 0%{?suse_version} >= 1550)
Requires(post): update-alternatives
Requires(pre):  update-alternatives
%endif

%description -n libOpenCL1
OpenCL is a royalty-free standard for cross-platform, parallel programming
of modern processors found in personal computers, servers and
handheld/embedded devices.

This package provides an Installable Client Driver Bindings (ICD Bindings).
The provided libOpenCL library is able to load any free or non-free installed
ICD (driver backend).

%package        devel
Summary:        Development files of ocl-icd
Requires:       libOpenCL1 = %{version}
Requires:       opencl-headers >= 2.2
Requires:       pkgconfig(egl)

%description    devel
This package provides the files needed to build OpenCL client drivers that
use ocl-icd for ICD functionality.

%prep
%autosetup -p1

%build
./bootstrap
%configure --enable-official-khronos-headers
%make_build stamp-generator stamp-generator-dummy
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf instdocs
mv %{buildroot}%{_datadir}/doc/%{name} instdocs
%if (0%{?sle_version} >= 150100 || 0%{?suse_version} >= 1550)
install -d %{buildroot}/%{_sysconfdir}/alternatives \
           %{buildroot}/%{_libdir}/ocl-icd
mv %{buildroot}/%{_libdir}/libOpenCL.so.1* %{buildroot}/%{_libdir}/ocl-icd
ln -snf ocl-icd/libOpenCL.so.1 %{buildroot}/%{_libdir}/libOpenCL.so
# dummy target for update-alternatives
ln -s %{_sysconfdir}/alternatives/libOpenCL.so.1 %{buildroot}/%{_libdir}/libOpenCL.so.1
ln -s %{_libdir}/ocl-icd/libOpenCL.so.1 %{buildroot}/%{_sysconfdir}/alternatives/libOpenCL.so.1
%endif

%if (0%{?sle_version} >= 150100 || 0%{?suse_version} >= 1550)
%post -n libOpenCL1
# apparently needed when updating from a pre update-alternatives package ...
rm -f %{_libdir}/libOpenCL.so.1.*
%{_sbindir}/update-alternatives --force --install \
   %{_libdir}/libOpenCL.so.1 libOpenCL.so.1 %{_libdir}/ocl-icd/libOpenCL.so.1  50
/sbin/ldconfig

%preun -n libOpenCL1
if [ "$1" = 0 ] ; then
   %{_sbindir}/update-alternatives --remove libOpenCL.so.1  %{_libdir}/ocl-icd/libOpenCL.so.1
fi
%else
%post -n libOpenCL1 -p /sbin/ldconfig
%endif

%postun -n libOpenCL1 -p /sbin/ldconfig

%if (0%{?sle_version} >= 150100 || 0%{?suse_version} >= 1550)
%posttrans -n libOpenCL1
if [ "$1" = 0 ] ; then
  if ! [ -f %{_libdir}/libOpenCl.so.1 ] ; then
      "%{_sbindir}/update-alternatives" --auto libOpenCL.so.1
  fi
fi
%endif

%check
%make_build check

%files -n libOpenCL1
%doc README
%if (0%{?sle_version} >= 150100 || 0%{?suse_version} >= 1550)
%dir %{_libdir}/ocl-icd
%{_libdir}/ocl-icd/libOpenCL.so.1*
%ghost %{_libdir}/libOpenCL.so.1
%ghost %{_sysconfdir}/alternatives/libOpenCL.so.1
%else
%{_libdir}/libOpenCL.so.1*
%endif

%files devel
%doc README NEWS
%license COPYING
%doc instdocs/*
%{_libdir}/libOpenCL.so
%{_libdir}/pkgconfig/OpenCL.pc
%{_libdir}/pkgconfig/ocl-icd.pc
%{_includedir}/ocl_icd.h

%changelog
* Wed May 17 2023 Dominique Leuenberger <dimstar@opensuse.org>
- Fix build against recent opencl: pass
  - -enable-official-khronos-headers to configure.
* Fri Aug 20 2021 Martin Hauke <mardnh@gmx.de>
- Update to version 2.3.1
  * Khronos Header Compatibility
- Remove patch (included upstream):
  * 0001-Updated-to-support-latest-Khronos-headers.patch
* Tue Aug 17 2021 Marcus Meissner <meissner@suse.com>
- overwrite the libopenCL.so.1 link in %%post of baselibs. (bsc#1189433)
* Tue Jun 15 2021 Christophe Giboudeaux <christophe@krop.fr>
- Add upstream change to fix build:
  * 0001-Updated-to-support-latest-Khronos-headers.patch
* Wed Mar 31 2021 Martin Hauke <mardnh@gmx.de>
- Update to version 2.3.0
  * Change OCL_ICD_LAYERS to OPENCL_LAYERS to conform to
    upecification
  * Updated layer support around official CL/cl_layer.h
  * Updated OpenCL Headers
  * Fixed typo in manpage
* Sat Dec 12 2020 Martin Hauke <mardnh@gmx.de>
- Update to version 2.2.14
  * Added experimental support for layers
* Sat Oct 24 2020 Martin Hauke <mardnh@gmx.de>
- Update to version 2.2.13
  * Removed warnings and use uniform warning suppression
  * Switched Khornos Headers to OpenCL3.0
  * Added OpenCL 3.0 support
  * Fix warning in gcc10
  * Updated loader and headers to support
    clSetContextDestructorCallback.
  * Call clGetDeviceIDs directly through the dispatch table
- Drop patch:
  * ocl-icd-gcc10.patch (fixed upstream)
* Mon Aug 31 2020 Stefan Dirsch <sndirsch@suse.com>
- added patch markups to specfile for better documentation
* Sat Aug 22 2020 Stefan Dirsch <sndirsch@suse.com>
- n_UsrShare.patch
  * first try /etc/OpenCL/vendors, then /usr/share/OpenCL/vendors
  (boo#1173005, comment#8)
- supersedes configure option --enable-custom-vendordir
* Tue Jun 23 2020 Stefan Dirsch <sndirsch@suse.com>
- switch from /usr/etc/OpenCL/vendors to /usr/share/OpenCL/vendors
  for vendor specific .icd files (boo#1173005)
* Thu Jun 18 2020 Stefan Dirsch <sndirsch@suse.com>
- switch to /usr/etc/OpenCL/vendors for vendor specific .icd files
  (boo#1173005); currently I'm only aware of Mesa using it (taking
  care about adjusting this myself); NVIDIA is using its own
  libOpenCL ...
* Wed Jun  3 2020 Dominique Leuenberger <dimstar@opensuse.org>
- Add ocl-icd-gcc10.patch: Fix build with gcc10 (boo#1172436).
* Sat May 30 2020 Marcus Meissner <meissner@suse.com>
- add baselibs.conf to build 32bit binaries for Wine (bsc#1172303)
* Wed Feb 26 2020 Tomáš Chvátal <tchvatal@suse.com>
- Remove condition for SLE11 build as it is unresolvable anyway
- Require update-alternatives only where really needed
- Require opencl-headers in the develpackage as otherwise all
  those that pull the devel would need to do it on their own.
* Mon Aug  5 2019 Antoine Belvire <antoine.belvire@opensuse.org>
- Update to version 2.2.12:
  * Switched khronos headers to OpenCL 2.2.
  * Added OpenCL 2.2 support.
- Update URL to GitHub repository since previous URL is not
  accessible anymore.
- Only suggest pocl instead of recommending it.
- Add check section.
* Sat Jan 19 2019 mardnh@gmx.de
- Add missing Requires(post): update-alternatives
* Mon Jan 14 2019 sndirsch@suse.com
- limit usage of update-alernatives to sle15-sp1/Leap 15.1 and newer
* Sun Jan 13 2019 sndirsch@suse.com
- sle15/Leap15 and newer: switch to usage of update-alternatives,
  so the package no longer conflicts with nvidia packages
  (boo#1108304)
* Sat Jul  8 2017 mardnh@gmx.de
- Recommend pocl when installing libOpenCL to get a better
  "out of the box" OpenCL experience for (open)SUSE users.
* Sun Jan 22 2017 mpluskal@suse.com
- Update to version 2.2.11:
  * Add autoconf option for custom vendors .icd path
  * Make vendordir relative to
  * Hack the docs to reflect configured vendordir
  * Revert "By default, use platforme specific clGetPlatformInfo"
  * Do not deference the plateform structure before checking it is an ICD
  * Cleanup --enable-custom-vendordir usage
  * [doc] ensure that files are correctly distributed and/or cleaned up
  * [doc] improve doc
  * [build] add notice message about what is choosen
- Changes for version 2.2.10:
  * Suppress warning due to shadowed variable name
  * Static-const-ify ICD loader info strings
  * Fallback to dispatch table for clGetPlatformInfo
  * By default, use platforme specific clGetPlatformInfo
- Changes for version 2.2.9:
  * Update clGetICDLoaderInfoOCLICD to report version 2.1.
  * Report the correct supported OpenCL version when asked
  * Add support for OPENCL_VENDOR_PATH envvar
* Mon Feb 15 2016 mardnh@gmx.de
- Fix BuildRequires: ocl_icd.h includes CL/cl_egl.h
* Tue Jan 26 2016 mpluskal@suse.com
- Update to 2.2.7
  * See NEWS for full list of changes
* Sun Sep  6 2015 mpluskal@suse.com
- Update to 2.2.7
  * See NEWS for full list of changes
- Cleanup spec file with spec-cleaner
* Thu Aug  7 2014 mardnh@gmx.de
- update to version 2.1.3
  * Brice Videau (3):
    Moved some declarations to the header as they are needed in the generated
    part now.
    If we have no valid platforms non can be valid.
    In case a NULL platform is passed to the loader, the default platform is
    selected if it exists and is valid.
  * Vincent Danjean (5):
    Rewrote initialization comments
    All generated file ends with "_gen" suffix (but installed once)
    [build] add tests for default platform selection
    Refactor code for selection of default platform
    Release 2.1.3
* Thu Nov  7 2013 Rene.vanPaassen@gmail.com
- added buildroot define for sle
- modifying generated and build-in source, for older gcc, removing some
  pragma GCC diagnostic statements
