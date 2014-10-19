#
# Conditional build:
%bcond_without	evas	# Edisplay support
%bcond_with	gif	# GIF support
%bcond_without	lua	# Lua API
%bcond_without	perl	# Perl API
%bcond_with	php	# PHP API
%bcond_without	python	# Python API

%ifarch %{x8664}
%undefine	with_lua
%undefine	with_perl
%undefine	with_python
%endif
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
URL:		http://www.exactcode.de/site/open_source/exactimage/
BuildRequires:	OpenEXR-devel >= 1.2.0
BuildRequires:	agg-devel >= 2.3
%{?with_evas:BuildRequires:	evas-devel >= 0.9.9}
BuildRequires:	expat-devel
# pkgconfig(freetype) >= 9.5.0
BuildRequires:	freetype-devel >= 2.1.6
%{?with_gif:BuildRequires:	giflib4-devel}
BuildRequires:	jasper-devel
BuildRequires:	lcms-devel >= 1.10
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.5
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
%{?with_lua:BuildRequires:	lua51-devel >= 5.1}
BuildRequires:	perl-devel >= 1:5.8.0
%{?with_php:BuildRequires:	php-devel >= 5.2.0}
%{?with_python:BuildRequires:	python-devel >= 1:2.5.0}
BuildRequires:	ruby-devel >= 1.8.5
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcflags}" \
	Q=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Q=

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
