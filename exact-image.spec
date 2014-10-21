# TODO: ruby (when ready)
#
# Conditional build:
%bcond_without	evas	# Edisplay support
%bcond_without	gif	# GIF support
%bcond_without	lua	# Lua API
%bcond_without	perl	# Perl API
%bcond_without	php	# PHP API
%bcond_without	python	# Python API
%bcond_with	ruby	# Ruby API [not finished as of 0.8.9]

%ifarch %{x8664}
%undefine	with_lua
%undefine	with_perl
%undefine	with_python
%endif
%define		php_name	php%{?php_suffix}
%include	/usr/lib/rpm/macros.perl
Summary:	A fast, modern and generic image processing library
Summary(pl.UTF-8):	Szybka, nowoczesna i ogólna biblioteka do przetwarzania obrazu
Name:		exact-image
Version:	0.8.9
Release:	2
License:	GPL v2
Group:		Applications/Graphics
Source0:	http://dl.exactcode.de/oss/exact-image/%{name}-%{version}.tar.bz2
# Source0-md5:	a8694722cd7cc9aa9407950a8440f0cd
Patch0:		%{name}-libs.patch
Patch1:		exactimage_0.8.5-1.patch
Patch2:		%{name}-giflib.patch
Patch3:		%{name}-evas.patch
Patch4:		%{name}-install.patch
URL:		http://www.exactcode.de/site/open_source/exactimage/
BuildRequires:	OpenEXR-devel >= 1.2.0
BuildRequires:	agg-devel >= 2.3
%{?with_evas:BuildRequires:	evas-devel >= 0.9.9}
BuildRequires:	expat-devel
# pkgconfig(freetype) >= 9.5.0
BuildRequires:	freetype-devel >= 2.1.6
%{?with_gif:BuildRequires:	giflib-devel >= 5}
BuildRequires:	jasper-devel
BuildRequires:	lcms-devel >= 1.10
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.5
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
%{?with_lua:BuildRequires:	lua51-devel >= 5.1}
BuildRequires:	perl-devel >= 1:5.8.0
%{?with_php:BuildRequires:	%{php_name}-devel >= 5.2.0}
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel >= 1:2.5.0}
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_ruby:BuildRequires:	ruby-devel >= 1.8.5}
%{?with_perl:BuildRequires:	swig-perl >= 1.3.32}
%{?with_php:BuildRequires:	swig-php >= 1.3.32}
%{?with_python:BuildRequires:	swig-python >= 1.3.32}
BuildRequires:	xorg-lib-libX11-devel >= 1.3
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A fast, modern and generic (template based) C++ image processing
library, alternative to ImageMagick.

%description -l pl.UTF-8
Szybka, nowoczesna i ogólna (oparta na szablonach) biblioteka C++
do przetwarzania obrazu, będąca alternatywą dla biblioteki
ImageMagick.

%package -n lua-ExactImage
Summary:	ExactImage API for Lua language
Summary(pl.UTF-8):	API ExactImage dla języka Lua
Group:		Development/Languages
Requires:	lua51

%description -n lua-ExactImage
ExactImage API for Lua language.

%description -n lua-ExactImage -l pl.UTF-8
API ExactImage dla języka Lua.

%package -n perl-ExactImage
Summary:	ExactImage API for Perl
Summary(pl.UTF-8):	API ExactImage dla Perla
Group:		Development/Languages/Perl

%description -n perl-ExactImage
ExactImage API for Perl.

%description -n perl-ExactImage -l pl.UTF-8
API ExactImage dla Perla.

%package -n %{php_name}-ExactImage
Summary:	ExactImage API for PHP
Summary(pl.UTF-8):	API ExactImage dla PHP
Group:		Development/Languages/Perl
%{?requires_php_extension}

%description -n %{php_name}-ExactImage
ExactImage API for PHP.

%description -n %{php_name}-ExactImage -l pl.UTF-8
API ExactImage dla PHP.

%package -n python-ExactImage
Summary:	ExactImage API for Python
Summary(pl.UTF-8):	API ExactImage dla Pythona
Group:		Development/Languages/Python

%description -n python-ExactImage
ExactImage API for Python.

%description -n python-ExactImage -l pl.UTF-8
API ExactImage dla Pythona.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
./configure \
	--prefix=%{_prefix} \
	%{!?with_evas:--without-evas} \
	%{!?with_gif:--without-libungif} \
	%{!?with_lua:--without-lua} \
	%{!?with_perl:--without-perl} \
	%{!?with_php:--without-php} \
	%{!?with_python:--without-python}

%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcflags}" \
	Q=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PERL_INSTALLDIR=%{perl_vendorarch} \
	PHP_INSTALLDIR=%{_libdir}/php \
	PYTHON_LIBDIR=%{py_sitedir} \
	api/lua/libdir=%{_libdir}/lua \
	Q=

%if %{with python}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/bardecode
%attr(755,root,root) %{_bindir}/e2mtiff
%attr(755,root,root) %{_bindir}/econvert
%attr(755,root,root) %{_bindir}/edentify
%{?with_evas:%attr(755,root,root) %{_bindir}/edisplay}
%attr(755,root,root) %{_bindir}/empty-page
%attr(755,root,root) %{_bindir}/hocr2pdf
%attr(755,root,root) %{_bindir}/optimize2bw

%if %{with lua}
%files -n lua-ExactImage
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lua/ExactImage.so
%endif

%if %{with perl}
%files -n perl-ExactImage
%defattr(644,root,root,755)
%attr(755,root,root) %{perl_vendorarch}/ExactImage.so
%{perl_vendorarch}/ExactImage.pm
%endif

%if %{with php}
%files -n %{php_name}-ExactImage
%defattr(644,root,root,755)
%attr(755,root,root) %{php_extensiondir}/ExactImage.so
%{php_extensiondir}/ExactImage.php
%endif

%if %{with python}
%files -n python-ExactImage
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_ExactImage.so
%{py_sitedir}/ExactImage.py[co]
%endif
