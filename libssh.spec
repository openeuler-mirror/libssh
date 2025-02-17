Name:           libssh
Version:        0.10.4
Release:        4
Summary:        A library implementing the SSH protocol
License:        LGPLv2+
URL:            http://www.libssh.org

Source0:        https://www.libssh.org/files/0.9/%{name}-%{version}.tar.xz
Source1:        https://www.libssh.org/files/0.9/%{name}-%{version}.tar.xz.asc
Source2:        https://cryptomilk.org/gpgkey-8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D.gpg#/%{name}.keyring

Patch0:         backport-config-Escape-brackets-in-ProxyCommand-build-from.patch
Patch1:         backport-packet-do-not-enqueue-outgoing-packets-after-sending.patch
Patch2:         backport-examples-Fix-build-issue-with-new-clang-15.patch
Patch3:         backport-0001-CVE-2023-1667-packet_cb-Log-more-verbose-error-if-si.patch
Patch4:         backport-0002-CVE-2023-1667-packet-Do-not-allow-servers-to-initiat.patch
Patch5:         backport-0003-CVE-2023-1667-kex-Remove-needless-function-argument.patch
Patch6:         backport-0004-CVE-2023-1667-kex-Factor-out-the-kex-mapping-to-inte.patch
Patch7:         backport-0005-CVE-2023-1667-dh-Expose-the-callback-cleanup-functio.patch
Patch8:         backport-0006-CVE-2023-1667-kex-Correctly-handle-last-fields-of-KE.patch
Patch9:         backport-0007-CVE-2023-1667-kex-Add-support-for-sending-first_kex_.patch
Patch10:        backport-0008-CVE-2023-1667-tests-Client-coverage-for-key-exchange.patch
Patch11:        backport-0009-CVE-2023-1667-tests-Send-a-bit-more-to-make-sure-rek.patch
Patch12:        backport-0001-CVE-2023-2283-pki_crypto-Fix-possible-authentication.patch
Patch13:        backport-0002-CVE-2023-2283-pki_crypto-Remove-unnecessary-NUL.patch

BuildRequires:  cmake gcc-c++ gnupg2 openssl-devel pkgconfig zlib-devel
BuildRequires:  krb5-devel libcmocka-devel openssh-clients openssh-server
BuildRequires:  nmap-ncat

Recommends:     crypto-policies

Provides: libssh_threads.so.4()(64bit)

%description
The ssh library was designed to be used by programmers needing a working SSH
implementation by the mean of a library. The complete control of the client is
made by the programmer. With libssh, you can remotely execute programs, transfer
files, use a secure and transparent tunnel for your remote programs. With its
Secure FTP implementation, you can play with remote files easily, without
third-party programs others than libcrypto (from openssl).

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package_help

%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -p1

%build
if test ! -e "obj"; then
  mkdir obj
fi
pushd obj

%cmake .. \
    -DUNIT_TESTING=ON \

%make_build VERBOSE=1

popd

%install
make DESTDIR=%{buildroot} install/fast -C obj
install -d -m755 %{buildroot}%{_sysconfdir}/libssh

pushd %{buildroot}%{_libdir}
for i in libssh.so*;
do
    _target="${i}"
    _link_name="${i%libssh*}libssh_threads${i##*libssh}"
    if [ -L "${i}" ]; then
        _target="$(readlink ${i})"
    fi
    ln -s "${_target}" "${_link_name}"
done;
popd

%ldconfig_scriptlets

%check
pushd obj
ctest --output-on-failure
popd

%files
%defattr(-,root,root)
%doc AUTHORS BSD
%license COPYING
%{_libdir}/*.so.4*

%files devel
%defattr(-,root,root)
%{_includedir}/libssh/
%{_libdir}/cmake/libssh/
%{_libdir}/pkgconfig/libssh.pc
%{_libdir}/*.so

%files help
%defattr(-,root,root)
%doc CHANGELOG README

%changelog
* Wed May 24 2023 renmingshuai <renmingshuai@huawei.com> - 0.10.4-4
- Type:CVE
- Id:CVE-2023-1667,CVE-2023-2283
- SUG:NA
- DESC:fix CVE-2023-1667 and CVE-2023-2283

* Mon Apr 3 2023 Chenxi Mao <chenxi.mao@suse.com> - 0.10.4-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:Backport patches to fix build error if compiler switch to clang.

* Sat Mar 18 2023 renmingshuai <renmingshuai@huawei.com> - 0.10.4-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:config: Escape brackets in ProxyCommand build from ProxyJump
       packet: do not enqueue outgoing packets after sending

* Thu Oct 20 2022 zengweifeng<zwfeng@huawei.com> - 0.10.4-1
- Type:requirement
- Id:NA
- SUG:NA
- DESC:update to 0.10.4

* Thu Oct 20 2022 zengweifeng<zwfeng@huawei.com> - 0.9.6-5
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:avoid false positive report from Coveritt CID 1470006
       kdf: Avoid endianess issues
       misc: Fix format truncation in ssh_path_expand_escape()
       misc: Fix expanding port numbers
       misc: rename gettimeofday symbol
       session: Initialize the port with the standard port (22)
       session->socket_callbacks.data will be set to ssh_packet_socket_callback
       socket: Add error message if execv fails
       tests: Add test for expanding port numbers

* Thu Oct 13 2022 xinghe <xinghe2@h-partners.com> - 0.9.6-4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:options: Parse hostname by last '@'
       torture_options: Add test for '@' in login name
       session: Initialize pointers
       tests: Ensure the mode of the created file is what we set

* Fri Sep 02 2022 gaihuiying <eaglegai@163.com> - 0.9.6-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:backport upstream patches

* Wed Mar 16 2022 xihaochen <xihaochen@h-partners.com> - 0.9.6-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:remove obsolete lib

* Fri Dec 03 2021 gaihuiying <gaihuiying1@huawei.com> - 0.9.6-1
- Type:requirement
- Id:NA
- SUG:NA
- DESC:update libssh to 0.9.6

* Mon Sep 13 2021 heyaohua<heyaohua1@huawei.com> - 0.9.5-2
- Type:CVE
- Id:CVE-2021-3634
- SUG:NA
- DESC:fix CVE-2021-3634

* Fri Jan 29 2021 xihaochen <xihaochen@huawei.com> - 0.9.5-1
- Type:requirements                                                                                                                                            
- Id:NA
- SUG:NA
- DESC:update libssh to 0.9.5

* Thu Aug 6 2020 zhaowei <zhaowei23@huawei.com> - 0.9.4-2
- Type:CVE
- Id:CVE-2020-16135
- SUG:NA
- DESC:fix CVE-2020-16135

* Mon Apr 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.9.4-1
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:update to 0.9.4

* Sun Jan 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.8.3-7
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:bugfix in build process

* Sun Jan 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.8.3-6
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: fixes cves

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.8.3-5
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: fixes the oss fuzz bug

* Thu Sep 12 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.8.3-4
- Package init
