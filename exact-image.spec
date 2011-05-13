Summary:	A fast, modern and generic image processing library
Name:		exact-image
Version:	0.8.5
Release:	1
License:	GPL v2
Group:		Applications/Graphics
Source0:	http://dl.exactcode.de/oss/exact-image/%{name}-%{version}.tar.bz2
# Source0-md5:	54c5dc9afd86ec573e7e2e9a80f45c71
Patch0:		%{name}-libs.patch
URL:		http://www.exactcode.de/site/open_source/exactimage/
BuildRequires:	OpenEXR-devel >= 1.2.0
BuildRequires:	agg-devel >= 2.3
BuildRequires:	evas-devel >= 0.9.9
BuildRequires:	jasper-devel
BuildRequires:	lcms-devel >= 1.10
#BuildRequires:	libpng12-devel >= 1.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-cxx-devel
BuildRequires:	libungif-devel
BuildRequires:	lua51-devel
BuildRequires:	perl-devel >= 5.8.0
BuildRequires:	php-devel >= 5.2.0
BuildRequires:	python-devel >= 2.5.0
BuildRequires:	ruby >= 1.8.5
BuildRequires:	swig-perl >= 1.3.32
BuildRequires:	swig-php >= 1.3.32
BuildRequires:	swig-python >= 1.3.32
BuildRequires:	xorg-lib-libX11-devel >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A fast, modern and generic (template) based C++ image processing library,
alternative to ImageMagick.

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=%{_prefix} --without-libpng --without-php \
%ifarch %{x8664}
	--without-lua --without-perl --without-python
%endif
%{__make} \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/*
