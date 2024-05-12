import qrcode
import qrcode.image.svg
from qrcode.image.pure import PyPNGImage
import io

# define a method to choose which factory metho to use
# possible values 'basic' 'fragment' 'path'

method = "basic"

data = "https://tenki.jp/forecaster/t_yoshida/2024/05/05/28639.html"

if method == 'basic':
    # Simple factory, just a set of rects.
    factory = qrcode.image.svg.SvgImage
elif method == 'fragment':
    # Fragment factory (also just a set of rects)
    factory = qrcode.image.svg.SvgFragmentImage
elif method == 'path':
    # Combined path factory, fixes white space that may occur when zooming
    factory = qrcode.image.svg.SvgPathImage

# Set data to qrcode
img = qrcode.make(data, image_factory = factory)
#f = io.StringIO()
stream = io.BytesIO()
img.save(stream)

print(stream.getvalue().decode())
# Save svg file somewhere
img.save("qrcode.svg")
img2 = qrcode.make(data, image_factory=PyPNGImage)
img2.save("qrcode.png")
