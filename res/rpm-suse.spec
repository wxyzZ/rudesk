Name:       homedesk
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/homedesk/
mkdir -p %{buildroot}/usr/share/homedesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/homedesk %{buildroot}/usr/bin/homedesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/lib/homedesk/libsciter-gtk.so
install $HBB/res/homedesk.service %{buildroot}/usr/share/homedesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/homedesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/homedesk.svg
install $HBB/res/homedesk.desktop %{buildroot}/usr/share/homedesk/files/
install $HBB/res/homedesk-link.desktop %{buildroot}/usr/share/homedesk/files/

%files
/usr/bin/homedesk
/usr/lib/homedesk/libsciter-gtk.so
/usr/share/homedesk/files/homedesk.service
/usr/share/icons/hicolor/256x256/apps/homedesk.png
/usr/share/icons/hicolor/scalable/apps/homedesk.svg
/usr/share/homedesk/files/homedesk.desktop
/usr/share/homedesk/files/homedesk-link.desktop

%changelog
# let's skip this for now

# https://www.cnblogs.com/xingmuxin/p/8990255.html
%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop homedesk || true
  ;;
esac

%post
cp /usr/share/homedesk/files/homedesk.service /etc/systemd/system/homedesk.service
cp /usr/share/homedesk/files/homedesk.desktop /usr/share/applications/
cp /usr/share/homedesk/files/homedesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable homedesk
systemctl start homedesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop homedesk || true
    systemctl disable homedesk || true
    rm /etc/systemd/system/homedesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/homedesk.desktop || true
    rm /usr/share/applications/homedesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
