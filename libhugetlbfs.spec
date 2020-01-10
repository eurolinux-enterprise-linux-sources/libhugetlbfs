Name: libhugetlbfs
Version: 2.16
Release: 12%{?dist}
Summary: A library which provides easy access to huge pages of memory
Group: System Environment/Libraries
License: LGPLv2+
URL: http://libhugetlbfs.sourceforge.net/
Source0: http://downloads.sourceforge.net/libhugetlbfs/%{name}-%{version}.tar.gz
Patch0: libhugetlbfs-2.16-s390.patch
Patch1: libhugetlbfs-2.15-fortify.patch
Patch2: libhugetlbfs-2.16-misalign_test.patch
Patch3: libhugetlbfs-2.17-aarch64.patch
Patch4: libhugetlbfs-2.16-makefile_cflags.patch
Patch5: libhugetlbfs-2.16-makefile_segments.patch
Patch6: libhugetlbfs-2.16-mounts_warning.patch
Patch7: libhugetlbfs-2.16-ppc64le-support.patch
Patch8: libhugetlbfs-2.16-plt_extrasz_fix.patch
Patch9: libhugetlbfs-2.16-map_high_truncate.patch
Patch10:libhugetlbfs-2.20-tests-linkhuge_rw-function-ptr-may-not-refer-to-text.patch
Patch11:libhugetlbfs-2.20-do-not-assume-default-huge-page-size-is-first.patch

BuildRequires: glibc-devel
BuildRequires: glibc-static

%define ldscriptdir %{_datadir}/%{name}/ldscripts

%description
libhugetlbfs is a library which provides easy access to huge pages of memory.
It is a wrapper for the hugetlbfs file system. Applications can use huge pages
to fulfill malloc() requests without being recompiled by using LD_PRELOAD.
Alternatively, applications can be linked against libhugetlbfs without source
modifications to load BSS or BSS, data, and text segments into large pages.

%package devel
Summary:	Header files for libhugetlbfs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%description devel
Contains header files for building with libhugetlbfs.

%package utils
Summary:	Userspace utilities for configuring the hugepage environment
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
%description utils
This packages contains a number of utilities that will help administrate the
use of huge pages on your system.  hugeedit modifies binaries to set default
segment remapping behavior. hugectl sets environment variables for using huge
pages and then execs the target program. hugeadm gives easy access to huge page
pool size control. pagesize lists page sizes available on the machine.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .s390
%patch1 -p1 -b .fortify
%patch2 -p1 -b .misalign_test
%patch3 -p1 -b .aarch64
%patch4 -p1 -b .makefile_cflags
%patch5 -p1 -b .makefile_segments
%patch6 -p1 -b .mounts_warning
%patch7 -p1 -b .ppc64le_support
%patch8 -p1 -b .plt_extrasz_fix
%patch9 -p1 -b .map_high_truncate
%patch10 -p1 -b .linkhuge_rw-func
%patch11 -p1 -b .default-huge-page

%build
ln -s sys-elf64ppc.S sys-elf64lppc.S
ln -s elf64ppc.c elf64lppc.c
# Parallel builds are not reliable
make BUILDTYPE=NATIVEONLY

%install
make install PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LDSCRIPTDIR=%{ldscriptdir} BUILDTYPE=NATIVEONLY
make install-helper PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LDSCRIPTDIR=%{ldscriptdir} BUILDTYPE=NATIVEONLY
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d
touch $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d/hugepages.conf

# remove statically built libraries:
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
# remove unused sbin directory
rm -fr $RPM_BUILD_ROOT/%{_sbindir}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libhugetlbfs.so*
%{_datadir}/%{name}/
%{_mandir}/man7/libhugetlbfs.7.gz
%ghost %config(noreplace) %{_sysconfdir}/security/limits.d/hugepages.conf
%exclude %{_libdir}/libhugetlbfs_privutils.so
%doc README HOWTO LGPL-2.1 NEWS

%files devel
%{_includedir}/hugetlbfs.h
%{_mandir}/man3/getpagesizes.3.gz
%{_mandir}/man3/free_huge_pages.3.gz
%{_mandir}/man3/get_huge_pages.3.gz
%{_mandir}/man3/gethugepagesize.3.gz
%{_mandir}/man3/gethugepagesizes.3.gz
%{_mandir}/man3/free_hugepage_region.3.gz
%{_mandir}/man3/get_hugepage_region.3.gz
%{_mandir}/man3/hugetlbfs_find_path.3.gz
%{_mandir}/man3/hugetlbfs_find_path_for_size.3.gz
%{_mandir}/man3/hugetlbfs_test_path.3.gz
%{_mandir}/man3/hugetlbfs_unlinked_fd.3.gz
%{_mandir}/man3/hugetlbfs_unlinked_fd_for_size.3.gz

%files utils
%{_bindir}/hugeedit
%{_bindir}/hugeadm
%{_bindir}/hugectl
%{_bindir}/pagesize
%{_bindir}/huge_page_setup_helper.py
%exclude %{_bindir}/cpupcstat
%exclude %{_bindir}/oprofile_map_events.pl
%exclude %{_bindir}/oprofile_start.sh
%{_mandir}/man8/hugeedit.8.gz
%{_mandir}/man8/hugectl.8.gz
%{_mandir}/man8/hugeadm.8.gz
%{_mandir}/man1/pagesize.1.gz
%{_mandir}/man1/ld.hugetlbfs.1.gz
%exclude %{_mandir}/man8/cpupcstat.8.gz
%exclude /usr/lib/perl5/TLBC

%changelog
* Tue Jun 07 2016 Petr holasek <pholasek@redhat.com> - 2.16-12
- linkhuge_rw test fix (#1240568)
- hugeadm fix for firestone ppc systems (#1258622)

* Mon Dec 15 2014 Petr Holasek <pholasek@redhat.com> - 2.16-11
- map_high_truncate_2 test fix (#1161677)

* Thu Nov 06 2014 Petr Holasek <pholasek@redhat.com> - 2.16-10
- fix plt_extrasz() always returning 0 on ppc64le (#1160217)

* Wed Aug 13 2014 Petr Holasek <pholasek@redhat.com> - 2.16-9
- ppc64le support (#1125576)

* Tue Jul 29 2014 Petr Holasek <pholasek@redhat.com> - 2.16-8
- Fixed malloc failures in testsuite
- Fixed warning when /etc/mtab is symlink

* Mon Mar 03 2014 Petr Holasek <pholasek@redhat.com> - 2.16-7
- Compiling with -fstack-protector-strong flag (#1070772)

* Wed Feb 12 2014 Petr Holasek <pholasek@redhat.com> - 2.16-6
- Backport patches from 2.17 for AArch64 support.

* Tue Feb 11 2014 Petr Holasek <pholasek@redhat.com> - 2.16-5
- Fix of misalign test (#1034549)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.16-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.16-3
- Mass rebuild 2013-12-27

* Sun May 12 2013 Anton Arapov <anton@redhat.com> - 2.16-2
- Fortify code
- Fix s390 build issues (#960107)

* Mon Apr 29 2013 Peter Robinson <pbrobinson@fedoraproject.org> - 2.16-1
- Upstream 2.16 release (adds ARM support)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 08 2012 Eric B Munson <emunson@mgebm.net> - 2.15
- Update for upstream 2.15 release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 24 2012 Eric B Munson <emunson@mgebm.net>
- Update for upstream 2.13 release

* Wed Jul 20 2011 Eric B Munson <emunson@mgebm.net>
- Update for upstream 2.12 release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 05 2010 Eric B Munson <ebmunson@us.ibm.com> 2.8-1
- Update for upstream 2.8 release

* Wed Feb 10 2010 Eric B Munson <ebmunson@us.ibm.com> 2.7-2
- Include patch that fixes build on ppc

* Tue Jan 05 2010 Eric B Munson <ebmunson@us.ibm.com> 2.7-1
- Update for upstream 2.7 release

* Fri Oct 02 2009 Jarod Wilson <jarod@redhat.com> 2.6-3
- Add hopefully-about-to-be-merged-upstream hugeadm enhancements
- Add huge pages setup helper script, using new hugeadm enhancements

* Thu Sep 03 2009 Nils Philippsen <nils@redhat.com> 2.6-2
- fix building on s390x

* Mon Aug 31 2009 Eric Munson <ebmunson@us.ibm.com> 2.6-1
- Updating for the libhugetlbfs-2.6 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Eric Munson <ebmunson@us.ibm.com> 2.5-2
- Update Group for -utils package to Applications/System

* Tue Jun 30 2009 Eric Munson <ebmunson@us.ibm.com> 2.5-1
- Updating for the libhugetlbfs-2.5 release

* Tue Jun 02 2009 Eric Munson <ebmunson@us.ibm.com> 2.4-2
- Adding patch to remove S390 32 bit build

* Fri May 29 2009 Eric Munson <ebmunson@us.ibm.com> 2.4-1
- Updating for the libhugetlbfs-2.4 release

* Wed Apr 15 2009 Eric Munson <ebmunson@us.ibm.com> 2.3-1
- Updating for the libhugetlbfs-2.3 release

* Wed Feb 11 2009 Eric Munson <ebmunson@us.ibm.com> 2.2-1
- Updating for the libhugetlbfs-2.2 release

* Fri Dec 19 2008 Eric Munson <ebmunson@us.ibm.com> 2.1.2-1
- Updating for libhugetlbfs-2.1.2 release

* Fri Dec 19 2008 Eric Munson <ebmunson@us.ibm.com> 2.1.1-1
- Updating for libhugetlbfs-2.1.1 release

* Thu Dec 18 2008 Josh Boyer <jwboyer@gmail.com> 2.1-2
- Fix broken dependency caused by just dropping -test
  subpackage

* Thu Oct 16 2008 Eric Munson <ebmunson@us.ibm.com> 2.1-1
- Updating for libhuge-2.1 release
- Adding -devel and -utils subpackages for various utilities
  and devel files.

* Wed May 14 2008 Eric Munson <ebmunson@us.ibm.com> 1.3-1
- Updating for libhuge-1.3 release

* Tue Mar 25 2008 Eric Munson <ebmunson@us.ibm.com> 1.2-1
- Removing test rpm target, and excluding test files

* Mon Mar 26 2007 Steve Fox <drfickle@k-lug.org> - 1.1-1
- New release (1.1)
- Fix directory ownership

* Wed Aug 30 2006 Steve Fox <drfickle@k-lug.org> - 0.20060825-1
- New release (1.0-preview4)
- patch0 (Makefile-ldscript.diff) merged upstream

* Tue Jul 25 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-4
- Bump for build system

* Tue Jul 25 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-3
- Don't use parallel build as it has random failures

* Thu Jul 20 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-2
- Fix the Makefile so that the ld.hugetlbfs script doesn't store the
  DESTDIR in the path to the ldscripts dir

* Fri Jul 7 2006 Steve Fox <drfickle@k-lug.org> - 0.20060706-1
- New release which includes a fix for the syscall macro removal in the
  Rawhide kernels

* Thu Jun 29 2006 Steve Fox <drfickle@k-lug.org> - 0.20060628-1
- First Fedora package
