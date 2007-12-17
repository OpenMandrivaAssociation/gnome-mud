#rpm spec file for gnome-mud

%define name gnome-mud
%define version 0.10.7
%define release %mkrel 3

%define section Amusement/Strategy
%define title Gnome-mud

%define Summary GNOME-Mud is a mudclient for the GNOME platform.

Summary:	%Summary
Name:		%name
Version:	%version
Release:	%release
License:	GPL
Group:		Games/Strategy
URL:		http://amcl.sourceforge.net/

Source0:	%name-%version.tar.bz2
Source1:	%name-32.png
Source2:	%name-16.png
Source3:	%name.png

Buildrequires:	python pygtk2.0-devel libvte-devel libgnome2-devel
BuildRequires:  libgnomeui2-devel, perl-XML-Parser
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

%build
%configure2_5x

%make WARN_CFLAGS=""

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%find_lang %name --with-gnome

# menu
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name): \
command="%_gamesbindir/%name" \
needs="x11" \
icon="%name.png" \
section="%section" \
title="%title" \
longtitle="%Summary" \
xdg="true"
EOF

# icon
mkdir -p %buildroot/{%_liconsdir,%_iconsdir,%_miconsdir}
install -m 644 src/pixmaps/%name.png %buildroot/%_datadir/pixmaps/%name.png
install -m 644 %SOURCE1 %buildroot/%_miconsdir/%name.png
install -m 644 %SOURCE2 %buildroot/%_liconsdir/%name.png
install -m 644 %SOURCE3 %buildroot/%_iconsdir/%name.png


%post
%update_menus
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gnome-mud.schemas > /dev/null
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi
touch %{_datadir}/gnome/help/%{name}/C/%{name}.html
if [ -x %{_bindir}/yelp-pregenerate ]; then %{_bindir}/yelp-pregenerate %{_datadir}/gnome/help/%{name}/*/%name.xml > /dev/null; fi

%preun
if [ $1 -eq 0 ]; then
  GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gnome-mud.schemas > /dev/null
fi

%postun
%{clean_menus}
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README INSTALL ROADMAP
%config(noreplace) %{_sysconfdir}/gconf/schemas/gnome-mud.schemas
%{_gamesbindir}/gnome-mud
%{_datadir}/applications/gnome-mud.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%name/*.png
%{_datadir}/omf/gnome-mud/
%{_datadir}/%name/*.glade
%{_mandir}/man6/%name.*
%_menudir/%name
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png



