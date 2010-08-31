from robofab.ufoLib import fontInfoAttributesVersion2, validateFontInfoVersion2ValueForAttribute

defaultLeftKerningGroupPrefix = "@KERN_LEFT_"
defaultRightKerningGroupPrefix = "@KERN_RIGHT_"


class RelaxedInfo(object):

    """
    This object that sets only valid info values
    into the given info object.
    """

    def __init__(self, info):
        self._object = info

    def __getattr__(self, attr):
        if attr in fontInfoAttributesVersion2:
            return getattr(self._object, attr)
        else:
            return super(RelaxedInfo, self).__getattr__(attr)

    def __setattr__(self, attr, value):
        if attr in fontInfoAttributesVersion2:
            if validateFontInfoVersion2ValueForAttribute(attr, value):
                setattr(self._object, attr, value)
        else:
            super(RelaxedInfo, self).__setattr__(attr, value)

def copyAttr(src, srcAttr, dest, destAttr):
    if not hasattr(src, srcAttr):
        return
    value = getattr(src, srcAttr)
    setattr(dest, destAttr, value)
