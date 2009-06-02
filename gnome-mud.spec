Summary:	A mudclient for the GNOME platform
Name:		gnome-mud
Version:	0.11.2
Release:	%mkrel 3
License:	GPLv2+
Group:		Games/Adventure
URL:		http://live.gnome.org/GnomeMud
Source0:	http://fr2.rpmfind.net/linux/gnome.org/sources/gnome-mud/0.11/%name-%version.tar.bz2
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
BuildRequires:	desktop-file-utils

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

%build
%configure2_5x --disable-schemas-install --bindir=%{_gamesbindir} --datadir=%{_gamesdatadir}
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mv %buildroot%_gamesdatadir/applications %buildroot%_datadir/
mv %buildroot%_gamesdatadir/icons %buildroot%_datadir/

desktop-file-install --vendor='' \
	--dir=%buildroot%_datadir/applications \
	--add-category='GTK;AdventureGame' \
	%buildroot%_datadir/applications/*.desktop

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
%{_gamesdatadir}/%name
%{_mandir}/man6/%name.*
