Summary:	A mudclient for the GNOME platform
Name:		gnome-mud
Version:	0.11
Release:	%mkrel 1
License:	GPLv2+
Group:		Games/Strategy
URL:		http://amcl.sourceforge.net/
Source0:	http://fr2.rpmfind.net/linux/gnome.org/sources/gnome-mud/0.11/%name-%version.tar.bz2
Patch0:		gnome-mud-0.11-fix-str.patch
Patch1:		gnome-mud-0.11-fix-desktop.patch
BuildRoot:	%_tmppath/%name-buildroot
Buildrequires:	libvte-devel
%if %mdkversion < 200810 
BuildRequires:	libgstreamer0.10-devel
%else
BuildRequires:	gstreamer0.10-devel
%endif
BuildRequires:	intltool libgnet2-devel pcre-devel
BuildRequires:	libGConf2-devel gnome-doc-utils
BuildRequires:  libglade2.0-devel

%description
GNOME-Mud is a mudclient for the GNOME platform. Features include:

  * ANSI
  * Aliases
  * Triggers
  * Variables
  * Profiles
  * Multiple connections
  * Python scripting
  * C modules
  * and much much more... 

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
%configure2_5x --disable-schemas-install
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %name --with-gnome

%post
%if %mdkversion < 200900
%update_menus
%post_install_gconf_schemas gnome-mud
%update_scrollkeeper
%endif

%preun
%preun_uninstall_gconf_schemas gnome-mud

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_scrollkeeper
%endif

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README INSTALL ROADMAP
%config(noreplace) %{_sysconfdir}/gconf/schemas/gnome-mud.schemas
%{_gamesbindir}/gnome-mud
%{_datadir}/applications/gnome-mud.desktop
%{_iconsdir}/*/*/*/*
%{_datadir}/%name
%{_mandir}/man6/%name.*
