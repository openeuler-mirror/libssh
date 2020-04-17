Name:           libssh
Version:        0.8.3
Release:        8
Summary:        A library implementing the SSH protocol
License:        LGPLv2+
URL:            https://www.libssh.org
Source0:        https://www.libssh.org/files/0.8/%{name}-%{version}.tar.xz
Source1:        https://www.libssh.org/files/0.8/%{name}-%{version}.tar.xz.asc
Source2:        https://cryptomilk.org/gpgkey-8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D.gpg#/%{name}.keyring 

Patch1:         libssh-0.8.3-fix-covscan-errors.patch
Patch2:         libssh-0.8.3-fixes-the-oss-fuzz-bug.patch

#patches6000-patches6007 come from https://git.libssh.org/
Patch6000:      libssh-stable-0p8-CVE-2018-10933-part1.patch
Patch6001:	libssh-stable-0p8-CVE-2018-10933-part2.patch
Patch6002:	libssh-stable-0p8-CVE-2018-10933-part3.patch
Patch6003:	libssh-stable-0p8-CVE-2018-10933-part4.patch
Patch6004:	libssh-stable-0p8-CVE-2018-10933-part5.patch
Patch6005:	libssh-stable-0p8-CVE-2018-10933-part6.patch
Patch6006:	libssh-stable-0p8-CVE-2018-10933-part7.patch
Patch6007:	libssh-stable-0p8-CVE-2018-10933-part8.patch
Patch6008:      0001-CVE-2019-14889.patch
Patch6009:      0002-CVE-2019-14889.patch
Patch6010:      0003-CVE-2019-14889.patch
Patch6011:      0004-CVE-2019-14889.patch
Patch6012:      0005-CVE-2019-14889.patch
Patch6013:      CVE-2020-1730.patch

BuildRequires:  cmake libcmocka-devel krb5-devel zlib-devel pkgconfig
BuildRequires:  doxygen gcc-c++ gnupg2 openssl-devel

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
    -DUNIT_TESTING=ON

%make_build VERBOSE=1
make docs

popd

%install
make DESTDIR=%{buildroot} install/fast -C obj

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
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files help
%defattr(-,root,root)
%doc README ChangeLog obj/doc/html

%changelog
* Fri Apr 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.8.3-8
- Type:cves
- ID:CVE-2020-1730
- SUG:NA
- DESC:fix CVE-2020-1730

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
