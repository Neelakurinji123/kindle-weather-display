include $(TOPDIR)/rules.mk

PKG_NAME:=cairo
PKG_VERSION:=1.16.0
PKG_RELEASE:=2

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.xz
PKG_SOURCE_URL:=https://www.cairographics.org/releases/
PKG_HASH:=5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331

PKG_MAINTAINER:=Mathew McBride <matt@traverse.com.au>

PKG_FIXUP:=autoreconf
PKG_INSTALL:=1

include $(INCLUDE_DIR)/package.mk

#TARGET_LDFLAGS+= \
#	-Wl,-rpath-link=$(STAGING_DIR)/usr/lib

define Package/cairo
  SECTION:=xorg-libraries
  CATEGORY:=Xorg
  SUBMENU:=libraries
  TITLE:=Text layout and rendering library
  DEPENDS:=+fontconfig +libfreetype +pixman +libpng +zlib +glib2 +liblzo +fontconfig
  URL:=http://www.cairo.org/
endef

define Package/cairo/description
 Drawing library
endef

CONFIGURE_ARGS += \
	--enable-trace=no \
	--enable-interpreter=no \
	--disable-directfb \
	--enable-ft \
	--enable-gobject \
	--enable-lzo \
	--disable-glesv2 \
	--disable-vg \
	--disable-xlib \
	--disable-xcb \
	--without-x \
	--disable-xlib-xrender \
	--disable-ps \
	--disable-pdf \
	--enable-png \
	--disable-script \
	--enable-svg \
	--disable-tee \
	--disable-xml

CONFIGURE_VARS += \
	CXX="$(TARGET_CC)"

define Build/InstallDev
	$(INSTALL_DIR) $(1)/usr/include $(1)/usr/lib $(1)/usr/lib/pkgconfig
	$(CP) $(PKG_INSTALL_DIR)/usr/include/cairo $(1)/usr/include/
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcairo.{a,la,so*} $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcairo-gobject.{a,la,so*} $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/pkgconfig $(1)/usr/lib/
endef

define Package/cairo/install
	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcairo.{a,la,so*} $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcairo-gobject.{a,la,so*} $(1)/usr/lib
endef

$(eval $(call BuildPackage,cairo))
