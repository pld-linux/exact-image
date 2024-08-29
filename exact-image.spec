# TODO: ruby (when ready)
#
# Conditional build:
%bcond_with	evas	# Edisplay support
%bcond_without	gif	# GIF support
%bcond_without	lua	# Lua API
%bcond_without	perl	# Perl API
%bcond_with	php	# PHP API
%bcond_without	python	# Python API
%bcond_with	ruby	# Ruby API [still not finished as of 0.9.2]

%define		php_name	php%{?php_suffix}
Summary:	A fast, modern and generic image processing library
Summary(pl.UTF-8):	Szybka, nowoczesna i ogólna biblioteka do przetwarzania obrazu
Name:		exact-image
Version:	1.2.1
Release:	1
License:	GPL v2
Group:		Applications/Graphics
Source0:	http://dl.exactcode.de/oss/exact-image/%{name}-%{version}.tar.bz2
# Source0-md5:	f0afb7874ad44a3b0096a9882fa70457
Patch0:		%{name}-libs.patch
Patch1:		%{name}-ub.patch
Patch2:		%{name}-make.patch
Patch3:		%{name}-evas.patch
Patch4:		%{name}-install.patch
Patch5:		%{name}-gif.patch
Patch6:		%{name}-heif.patch
Patch7:		%{name}-jasper.patch
Patch8:		%{name}-jxl.patch
URL:		http://www.exactcode.de/site/open_source/exactimage/
BuildRequires:	OpenEXR-devel >= 1.2.0
BuildRequires:	agg-devel >= 2.3
%{?with_evas:BuildRequires:	evas-devel >= 0.9.9}
BuildRequires:	expat-devel >= 1.95
# pkgconfig(freetype) >= 9.5.0
BuildRequires:	freetype-devel >= 2.1.6
%{?with_gif:BuildRequires:	giflib-devel >= 5.1}
BuildRequires:	jasper-devel
BuildRequires:	lcms-devel >= 1.10
BuildRequires:	libheif-devel >= 1.16
BuildRequires:	libjpeg-devel
BuildRequires:	libjxl-devel >= 0.6
BuildRequires:	libpng-devel >= 2:1.5
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtiff-devel
%{?with_lua:BuildRequires:	lua51-devel >= 5.1}
BuildRequires:	perl-devel >= 1:5.8.0
%{?with_php:BuildRequires:	%{php_name}-devel >= 5.2.0}
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel >= 1:2.5.0}
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.745
%{?with_ruby:BuildRequires:	ruby-devel >= 1.9}
BuildRequires:	sed >= 4.0
%{?with_perl:BuildRequires:	swig-perl >= 1.3.32}
%{?with_php:BuildRequires:	swig-php >= 3.0.12}
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
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%if %{with php}
%if "%(php%{?php_suffix}-config --version)" >= "7.0"
%{__sed} -i -e 's/-php5/-php7/' api/php/Makefile
%endif
%endif

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
	CXXFLAGS="%{rpmcxxflags}" \
	Q=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PERL_INSTALLDIR=%{perl_vendorarch} \
	PHP_INSTALLDIR=%{php_extensiondir} \
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
