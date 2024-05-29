include $(TOPDIR)/rules.mk

PKG_NAME:=cairo
PKG_VERSION:=1.18.0
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.xz
PKG_SOURCE_URL:=https://www.cairographics.org/releases/
PKG_HASH:=243a0736b978a33dee29f9cca7521733b78a65b5418206fef7bd1c3d4cf10b64

PKG_MAINTAINER:=krishna <krishna@hottunalabs.net>

PKG_INSTALL:=1

include $(INCLUDE_DIR)/package.mk
include $(INCLUDE_DIR)/meson.mk

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

MESON_OPTIONS += \
	-Dfontconfig=enabled \
	-Dfreetype=enabled \
	-Dpng=enabled \
	-Dglib=enabled \
	-Dxcb=disabled \
	-Dxlib=disabled \
	-Dzlib=enabled \
	-Dglib=enabled

define Build/InstallDev
	$(INSTALL_DIR) $(1)/usr/include $(1)/usr/lib $(1)/usr/lib/pkgconfig
	$(CP) $(PKG_INSTALL_DIR)/usr/include/cairo $(1)/usr/include/
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcairo.so* $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcairo-gobject.so* $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/pkgconfig $(1)/usr/lib/
endef

define Package/cairo/install
	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcairo.so* $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcairo-gobject.so* $(1)/usr/lib
endef

$(eval $(call BuildPackage,cairo))
