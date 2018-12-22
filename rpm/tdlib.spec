Name:    tdlib
Summary: Cross-platform library for building Telegram clients
Version: 1.3.0
Release: 2
Group:   Development/Libraries
License: BSL-1.0
URL:     https://github.com/minlexx/td
Source0: %{name}-%{version}.tar.gz

BuildRequires: cmake >= 3.1
BuildRequires: opt-gcc7
BuildRequires: gperf
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: git

Obsoletes: tdlibjson < 1.3
Obsoletes: tdlibjson-devel < 1.3

%description
%{summary}.

%changelog
* Tue Dec 25 2018 Alexey Min <alexey.min@gmail.com>
- 1.3.0-2: SailfishOS packaging


%package devel
Summary:    Development files for Telegram TD library
Group:      Development/Libraries
%description devel
Library for building Telegram clients.
Provides both C++ interface, static libraries (tdlib) 
and C-like JSON interface (tdlib-json).
Development files for both tdlib and tdlib-json libraries.

%package json
Summary:    C-like JSON interface to TD library
Group:      Development/Libraries
%description json
C-like JSON interface to TDlib.


%prep
%setup -q

%build

%define cmake_install make DESTDIR=%{?buildroot} install

SOURCE_DIR=`pwd`
mkdir -p %{_builddir}/build
cd %{_builddir}/build

unset CFLAGS
unset CXXFLAGS
# We need very custom CFLAGS, so we need to overwrite distro-provided with ours,
#  respecting distro preferences of course. So these are distro-default CFLAGS
#  only with "-O2 -g -pipe" removed to save memory.
%ifarch armv7hl
export CFLAGS="-Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector \
    --param=ssp-buffer-size=4 -Wformat -Wformat-security -fmessage-length=0 \
    -march=armv7-a -mfloat-abi=hard -mfpu=neon -mthumb -Wno-psabi"
export CXXFLAGS=${CFLAGS}
%endif

%ifarch i386 i486 i586 i686
# TODO: x86 build cflags
export CFLAGS="-g -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector \
    --param=ssp-buffer-size=4 -Wformat -Wformat-security -fmessage-length=0 \
    -Wno-psabi"
export CXXFLAGS=${CFLAGS}
%endif

%{_bindir}/cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    -DCMAKE_C_COMPILER=/opt/gcc7/bin/gcc \
    -DCMAKE_CXX_COMPILER=/opt/gcc7/bin/g++ \
    -DCMAKE_CXX_FLAGS_RELEASE="-O0" \
    -DCMAKE_EXE_LINKER_FLAGS="-L/opt/gcc7/lib -static-libstdc++ -static-libgcc" \
    -DCMAKE_MODULE_LINKER_FLAGS="-L/opt/gcc7/lib -static-libstdc++ -static-libgcc" \
    -DCMAKE_SHARED_LINKER_FLAGS="-L/opt/gcc7/lib -static-libstdc++ -static-libgcc" \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_INSTALL_RPATH="/opt/gcc7/lib" \
    -DBUILD_TESTING=OFF \
    $SOURCE_DIR

# make %{?_smp_mflags}
make -j1


%install
cd %{_builddir}/build
%cmake_install

%post json
/sbin/ldconfig

%postun json
/sbin/ldconfig


%files json
%defattr(-,root,root,-)
%{_libdir}/libtdjson.so
%{_libdir}/libtdjson.so.1.3.0


%files devel
%defattr(-,root,root,-)
%{_libdir}/libtdactor.a
%{_libdir}/libtdclient.a
%{_libdir}/libtdcore.a
%{_libdir}/libtddb.a
%{_libdir}/libtdnet.a
%{_libdir}/libtdsqlite.a
%{_libdir}/libtdutils.a
%{_libdir}/libtdjson_static.a
%{_libdir}/libtdjson_private.a
%dir %{_includedir}/td
%dir %{_includedir}/td/telegram
%{_includedir}/td/telegram/td_api.h
%{_includedir}/td/telegram/td_api.hpp
%{_includedir}/td/telegram/td_json_client.h
%{_includedir}/td/telegram/td_log.h
%{_includedir}/td/telegram/tdjson_export.h
%{_includedir}/td/telegram/Client.h
%{_includedir}/td/telegram/Log.h
%dir %{_includedir}/td/tl
%{_includedir}/td/tl/TlObject.h
%dir %{_libdir}/cmake/Td
%{_libdir}/cmake/Td/TdTargets.cmake
%{_libdir}/cmake/Td/TdTargets-release.cmake
%{_libdir}/cmake/Td/TdConfig.cmake
%{_libdir}/cmake/Td/TdConfigVersion.cmake
