#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	hashable
Summary:	A class for types that can be converted to a hash value
Summary(pl.UTF-8):	Klasa dla typów, które można przekształcić do wartości hasza
Name:		ghc-%{pkgname}
Version:	1.3.0.0
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/hashable
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	72b9550b7f56dae4cfdd45ff5d1746a6
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/hashable
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.0
BuildRequires:	ghc-bytestring >= 0.9
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.0
BuildRequires:	ghc-bytestring-prof >= 0.9
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.0
Requires:	ghc-bytestring >= 0.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package defines a class, Hashable, for types that can be
converted to a hash value. This class exists for the benefit of
hashing-based data structures. The package provides instances for
basic types and a way to combine hash values.

%description -l pl.UTF-8
Ten pakiet definiuje klasę Hashable, przeznaczoną dla typów, które
można przekształcić na wartość hasza. Klasa jest przeznaczona dla
struktur danych opartych na haszowaniu. Pakiet dostarcza instancje
dla typów podstawowych oraz sposób łączenia wartości haszy.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.0
Requires:	ghc-bytestring-prof >= 0.9

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for %{pkgname} ghc package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname} ghc package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShashable-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShashable-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShashable-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable/Generic
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable/Generic/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable/Generic/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShashable-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Hashable/Generic/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
