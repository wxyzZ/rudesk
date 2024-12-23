Name:       homedesk
Version:    1.32.5
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://homedesk.com
Vendor:     homedesk <info@homedesk.com>
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/lib/homedesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/lib/homedesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/homedesk.service -t "%{buildroot}/usr/share/homedesk/files"
install -Dm 644 $HBB/res/homedesk.desktop -t "%{buildroot}/usr/share/homedesk/files"
install -Dm 644 $HBB/res/homedesk-link.desktop -t "%{buildroot}/usr/share/homedesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/homedesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/homedesk.svg"

%files
/usr/lib/homedesk/*
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
ln -s /usr/lib/homedesk/homedesk /usr/bin/homedesk
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
    rm /usr/bin/homedesk || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
