Name:           libssh
Version:        0.9.4
Release:        6
Summary:        A library implementing the SSH protocol
License:        LGPLv2+
URL:            http://www.libssh.org

Source0:        https://www.libssh.org/files/0.9/%{name}-%{version}.tar.xz
Source1:        https://www.libssh.org/files/0.9/%{name}-%{version}.tar.xz.asc
Source2:        https://cryptomilk.org/gpgkey-8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D.gpg#/%{name}.keyring

Patch1:         libssh-0.9.4-fix-version.patch
Patch2:         CVE-2020-16135-1.patch
Patch3:         CVE-2020-16135-2.patch
Patch4:         CVE-2020-16135-3.patch
Patch5:         CVE-2020-16135-4.patch
Patch6:         CVE-2021-3634.patch
Patch7:         backport-Add-errno-reset-with-strtoul-call.patch
Patch8:         backport-auth-Fix-error-returned-in-ssh_userauth_try_publicke.patch
Patch9:         backport-client-Do-not-close-the-socket-if-it-was-set-via-opt.patch
Patch10:        backport-libsshpp-Fix-openForward-to-not-set-sourcehost-to-NU.patch
Patch11:        backport-sftp-fix-the-length-calculation-of-packet-in-sftp_wr.patch

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
* Fri Sep 02 2022 gaihuiying <eaglegai@163.com> - 0.9.4-6
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:backport upstream patches:
       add errno while reset with strtoul call
       fix error returned in ssh_userauth_try_publicke
       client do not close the socket if it was set via opt
       fix openForward to not set sourcehost to NULL
       fix the length calculation of packet in sftp_write

* Mon Sep 13 2021 heyaohua<heyaohua1@huawei.com> - 0.9.4-5
- Type:CVE
- CVE:CVE-2021-3634
- SUG:NA
- DESC:fix CVE-2021-3634

* Tue Aug 3 2021 Jianmin <jianmin@iscas.ac.cn> - 0.9.4-4
- Type:enchancement
- CVE:NA
- SUG:NA
- DESC:remove libssh-help dependency for libssh

* Mon Nov 09 2020 xihaochen <xihaochen@huawei.com> - 0.9.4-3
- Type:requirement
- CVE:NA
- SUG:NA
- DESC:add libssh-help dependency for libssh

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
