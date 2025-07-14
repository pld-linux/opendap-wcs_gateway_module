#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	WCS Request module for the OPeNDAP data server
Summary(pl.UTF-8):	Moduł żądań WCS dla serwera danych OPeNDAP
Name:		opendap-wcs_gateway_module
Version:	1.1.0
Release:	4
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/wcs_gateway_module-%{version}.tar.gz
# Source0-md5:	1527f2207b30dd8528745a61dc6574aa
Patch0:		%{name}-versions.patch
Patch1:		%{name}-includes.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.10
%{?with_tests:BuildRequires:	bes >= 3.8.0}
BuildRequires:	bes-devel >= 3.8.0
%{?with_tests:BuildRequires:	cppunit-devel >= 1.12.0}
BuildRequires:	curl-devel >= 7.10.6
BuildRequires:	libdap-devel >= 3.10.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml2-devel >= 1:2.5.7
BuildRequires:	pkgconfig
Requires:	bes >= 3.8.0
Requires:	curl >= 7.10.6
Requires:	libdap >= 3.10.0
Requires:	libxml2 >= 1:2.5.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the WCS request module that is to be loaded in to the OPeNDAP
Back-End Server (BES). It makes a WCS request, which returns a netcdf
or hdf file, then reads the reponse files and returns DAP responses
that are compatible with DAP2 and the dap-server software.

%description -l pl.UTF-8
Ten pakiet zawiera moduł żądań WCS ładowany do serwera backendu danych
(BES) OPeNDAP. Tworzy żądania WCS, zwracające pliki netcdf lub hdf, a
następnie odczytuje pliki odpowiedzi i zwraca odpowiedzi DAP zgodne z
oprogramowaniem DAP2 i dap-server.

%prep
%setup -q -n wcs_gateway_module-%{version}
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT_URI ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/wcsg.conf
%attr(755,root,root) %{_libdir}/bes/libwcs_gateway_module.so
