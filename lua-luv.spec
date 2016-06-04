%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
# for compiled modules
%global lualibdir %{_libdir}/lua/%{luaver}

%define vermagic1 1.9.0
%define vermagic2 3

Name:           lua-luv
Version:        %{vermagic1}_%{vermagic2}
Release:        1%{?dist}
Summary:        Bare libuv bindings for lua

License:        Apache 2.0
URL:            https://luarocks.org/modules/tarruda/mpack
Source0:        https://github.com/luvit/luv/releases/download/%{vermagic1}-%{vermagic2}/luv-%{vermagic1}-%{vermagic2}.tar.gz

BuildRequires:  cmake >= 2.8
BuildRequires:  pkgconfig(libuv)
BuildRequires:  lua-devel >= %{luaver}
%if 0%{?rhel} == 6
Requires:       lua >= %{luaver}
Requires:       lua < 5.2
%else
Requires:       lua(abi) >= %{luaver}
%endif

%description
This library makes libuv available to lua scripts. It was made for the luvit
project but should usable from nearly any lua project.


%prep
%setup -q -n luv-%{vermagic1}-%{vermagic2}


%build
mkdir build-lua
pushd build-lua
%cmake \
    -DLUA_BUILD_TYPE=System \
    -DWITH_LUA_ENGINE=Lua \
    -DBUILD_SHARED_LIBS=ON \
    -DWITH_SHARED_LIBUV=ON \
    ..
make %{?_smp_mflags}
popd


%install
rm -rf %{buildroot}
pushd build-lua
# project doesn't honor LIB_INSTALL_DIR and friends, hence manual install
# %make_install
install -d %{buildroot}%{lualibdir}
install -p -m 755 luv.so %{buildroot}%{lualibdir}
popd


%files
%license LICENSE.txt
%doc  README.md
%{lualibdir}/*


%changelog
* Sat Jun 04 2016 Jajauma's Packages <jajauma@yandex.ru> - 1.9.0_3-1
- Public release
