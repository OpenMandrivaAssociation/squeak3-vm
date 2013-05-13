%define major	3.10
%define minor	4
%define vmver	%{major}-%{minor}
%define source	Squeak-%{vmver}

Name:		squeak3-vm
Version:	%{major}.%{minor}
Release:	1
Summary:	The Squeak virtual machine
Group:		Development/Other
License:	MIT
URL:		http://squeakvm.org/unix
Source0:	http://ftp.squeak.org/%{major}/unix-linux/%{source}.src.tar.gz
Source2:	squeak-desktop-files.tar.gz
Patch0:		squeak-vm-rpath.patch
Patch1: 	squeak-vm-install-inisqueak.patch
Patch2: 	squeak-vm-imgdir.patch
Patch3: 	squeak-vm-tail-options.patch
Patch4: 	squeak-vm-dprintf.patch
Patch5: 	squeak-vm-libv4l.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(post):	desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	X11-devel
BuildRequires:	x11-proto-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	gcc
BuildRequires:	desktop-file-utils
BuildRequires:	libalsa-devel
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(theora)
BuildRequires:	speex-devel
BuildRequires:	dbus-devel
BuildRequires:	pango-devel
BuildRequires:	gstreamer0.10-devel
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(xext)
BuildRequires:	ext2fs-devel
BuildRequires:	dbus-devel
BuildRequires:	pkgconfig(uuid)
Requires:	zenity

%description
Squeak is a full-featured implementation of the Smalltalk programming
language and environment based on (and largely compatible with) the original
Smalltalk-80 system.

This package contains just the Squeak virtual machine.

%prep
%setup -q -n %{source} -a 2
find platforms -name '*.[ch]' -exec chmod ug=rw,o=r {} \;

%patch0 -p1 -b .rpath
%patch1 -p1 -b .install-inisqueak
%patch2 -p1 -b .imgdir
%patch3 -p1 -b .tail-options
%patch4 -p1
%patch5 -p1

%build
mkdir -p bld
cd bld

CPPFLAGS=-DSUGAR ../platforms/unix/config/configure --prefix=%{_prefix} --mandir=%{_mandir} --datadir=%{_datadir} --libdir=%{_libdir}

%make

%install
make -C bld install ROOT=%{buildroot}

# these files will be put in std RPM doc location
rm -rf %{buildroot}%{_prefix}/doc/squeak

# install the desktop stuff
install -D --mode=u=rwx,go=rx mysqueak %{buildroot}%{_bindir}/mysqueak3
install -D --mode=u=rw,go=r mysqueak.1 %{buildroot}%{_mandir}/man1/mysqueak.1
install -D --mode=u=rw,go=r squeak.xml %{buildroot}%{_datadir}/mime/packages/squeak.xml
install -D --mode=u=rw,go=r squeak.desktop %{buildroot}%{_datadir}/applications/squeak.desktop
install -D --mode=u=rw,go=r squeak.png %{buildroot}%{_datadir}/pixmaps/squeak.png

%define icons_dir %{buildroot}%{_datadir}/icons/gnome
for size in 16 24 32 48 64 72 96
do
  mkdir -p %{icons_dir}/${size}x${size}/mimetypes
  install -m0644 squeak${size}.png %{icons_dir}/${size}x${size}/mimetypes/application-x-squeak-image.png
  install -m0644 squeaksource${size}.png %{icons_dir}/${size}x${size}/mimetypes/application-x-squeak-source.png
done

cd %{buildroot}%{_libdir}/squeak/%{vmver}
DOTDOTS=$(echo %{_libdir}/squeak/%{vmver} | sed -e 's:/[^/]\+:../:g')
ln -s ${DOTDOTS}%{_datadir}/squeak/SqueakV39.sources .
ln -s ${DOTDOTS}%{_datadir}/squeak/SqueakV3.sources .

rm -f %{buildroot}%{_bindir}/squeak
mv %{buildroot}%{_bindir}/inisqueak{,3}
ln -sf %{_libdir}/squeak/%{vmver}/squeak %{buildroot}%{_bindir}/squeak3
perl -pi -e 's|\binisqueak\b|inisqueak3|;' %{buildroot}%{_bindir}/mysqueak3

%files
%doc platforms/unix/ChangeLog platforms/unix/doc/{README*,LICENSE,*RELEASE_NOTES}
%{_bindir}/*
%{_libdir}/squeak/%{vmver}
%{_mandir}/man*/*
%{_datadir}/squeak
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%{_datadir}/icons/gnome/*/mimetypes/*.png


%changelog
* Wed Feb 29 2012 Paulo Andrade <pcpa@mandriva.com.br> 3.10.4-1
+ Revision: 781429
- Import a squeak 3 vm (for testing purposes in case of issues with squeak 4)
- Import a squeak 3 vm (for testing purposes in case of issues with squeak 4)

