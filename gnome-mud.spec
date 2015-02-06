%define url_ver %(echo %{version} | cut -d. -f1,2)

Summary:	A mudclient for the GNOME platform
Name:		gnome-mud
Version:	0.11.2
Release:	8
License:	GPLv2+
Group:		Games/Adventure
Url:		http://live.gnome.org/GnomeMud
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-mud/%{url_ver}/%{name}-%{version}.tar.bz2

BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnet-2.0)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:  pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libpcre)
Buildrequires:	pkgconfig(vte)

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
%configure2_5x \
	--disable-schemas-install \
	--bindir=%{_gamesbindir} \
	--datadir=%{_gamesdatadir}
%make

%install
%makeinstall_std

mv %buildroot%_gamesdatadir/applications %buildroot%_datadir/
mv %buildroot%_gamesdatadir/icons %buildroot%_datadir/

desktop-file-install --vendor='' \
	--dir=%buildroot%_datadir/applications \
	--add-category='GTK;AdventureGame' \
	%buildroot%_datadir/applications/*.desktop

%find_lang %{name} --with-gnome


%preun
%preun_uninstall_gconf_schemas gnome-mud

%files -f %{name}.lang
%doc AUTHORS COPYING README INSTALL ROADMAP
%config(noreplace) %{_sysconfdir}/gconf/schemas/gnome-mud.schemas
%{_gamesbindir}/gnome-mud
%{_datadir}/applications/gnome-mud.desktop
%{_iconsdir}/*/*/*/*
%{_gamesdatadir}/%{name}
%{_mandir}/man6/%{name}.*
