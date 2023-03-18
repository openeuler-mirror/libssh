Name:           libssh
Version:        0.9.6
Release:        6
Summary:        A library implementing the SSH protocol
License:        LGPLv2+
URL:            http://www.libssh.org

Source0:        https://www.libssh.org/files/0.9/%{name}-%{version}.tar.xz
Source1:        https://www.libssh.org/files/0.9/%{name}-%{version}.tar.xz.asc
Source2:        https://cryptomilk.org/gpgkey-8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D.gpg#/%{name}.keyring

Patch0:         backport-Add-errno-reset-with-strtoul-call.patch
Patch1:         backport-auth-Fix-error-returned-in-ssh_userauth_try_publicke.patch
Patch2:         backport-client-Do-not-close-the-socket-if-it-was-set-via-opt.patch
Patch3:         backport-libsshpp-Fix-openForward-to-not-set-sourcehost-to-NU.patch
Patch4:         backport-sftp-fix-the-length-calculation-of-packet-in-sftp_wr.patch
Patch5:         backport-options-Parse-hostname-by-last.patch
Patch6:         backport-torture_options-Add-test-for-in-login-name.patch
Patch7:         backport-session-Initialize-pointers.patch
Patch8:         backport-tests-Ensure-the-mode-of-the-created-file-is.patch
Patch9:         backport-session-socket_callbacks.data-will-be-set-t.patch
Patch10:        backport-config-Avoid-false-positive-report-from-Cov.patch
Patch11:        backport-kdf-Avoid-endianess-issues.patch
Patch12:        backport-misc-rename-gettimeofday-symbol.patch
Patch13:        backport-misc-Fix-format-truncation-in-ssh_path_expa.patch
Patch14:        backport-misc-Fix-expanding-port-numbers.patch
Patch15:        backport-session-Initialize-the-port-with-the-standa.patch
Patch16:        backport-tests-Add-test-for-expanding-port-numbers.patch
Patch17:        backport-socket-Add-error-message-if-execv-fails.patch
Patch18:        backport-config-Escape-brackets-in-ProxyCommand-build-from.patch
Patch19:        backport-packet-do-not-enqueue-outgoing-packets-after-sending.patch

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
%doc ChangeLog README

%changelog
* Sat Mar 18 2023 renmingshuai <renmingshuai@huawei.com> - 0.9.6-6
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:config: Escape brackets in ProxyCommand build from ProxyJump
       packet: do not enqueue outgoing packets after sending

* Tue Oct 18 2022 gaihuiying <eaglegai@163.com> - 0.9.6-5
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:backport some upstream patches:
       Avoid false positive report from Coveritt CID 1470006
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

* Fri Sep 02 2022 zengweifeng <zwfeng@huawei.com> - 0.9.6-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add errno while reset with strtoul call
       fix error returned in ssh_userauth_try_publicke
       client do not close the socket if it was set via opt
       fix openForward to not set sourcehost to NULL
       fix the length calculation of packet in sftp_write

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
