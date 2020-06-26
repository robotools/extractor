import extractor
import defcon
from ufo2ft import compileTTF

ufo = defcon.Font()
extractor.extractUFO("data/ibm_plex/IBM Plex Serif-Text-FL.ttf", ufo)
ufo.save("data/ibm_plex/IBM Plex Serif-Text-FL_extracted.ufo")
ufo = defcon.Font("data/ibm_plex/IBM Plex Serif-Text-FL_extracted.ufo")
ttf = compileTTF(ufo)
ttf.save("data/ibm_plex/IBM Plex Serif-Text-ufo2ft.ttf")
ttf.saveXML("data/ibm_plex/IBM Plex Serif-Text-ufo2ft.ttx")


# ufo = defcon.Font()
# extractor.extractUFO("data/font_a/font-normal-fl.ttf", ufo)
# ufo.save("data/font_a/font-normal-fl_extracted.ufo")
# ufo = defcon.Font("data/font_a/font-normal-fl_extracted.ufo")
# ttf = compileTTF(ufo)
# ttf.save("data/font_a/font-normal-ufo2ft.ttf")
# ttf.saveXML("data/font_a/font-normal-ufo2ft.ttx")
