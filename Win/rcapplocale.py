#coding=utf-8

# Creates a right-click context menu to launch an application under a specified
# foreign language code-page, specified below. This script is used solely to
# create the right-click item.
# 17 Aug 13 - @bbaskin
import _winreg as wreg  #python2
import os

AppLocale = r"%SystemRoot%\AppPatch\AppLoc.exe"
''' --------> win32api.GetKeyboardLayoutName()
# Out[610]: '00000804'  # 0804
'''
# Language = "0436" # Afrikaans - South Africa
# Language = "041c" # Albanian - Albania
# Language = "0484" # Alsatian
# Language = "045e" # Amharic - Ethiopia
# Language = "0401" # Arabic - Saudi Arabia
# Language = "1401" # Arabic - Algeria
# Language = "3c01" # Arabic - Bahrain
# Language = "0c01" # Arabic - Egypt
# Language = "0801" # Arabic - Iraq
# Language = "2c01" # Arabic - Jordan
# Language = "3401" # Arabic - Kuwait
# Language = "3001" # Arabic - Lebanon
# Language = "1001" # Arabic - Libya
# Language = "1801" # Arabic - Morocco
# Language = "2001" # Arabic - Oman
# Language = "4001" # Arabic - Qatar
# Language = "2801" # Arabic - Syria
# Language = "1c01" # Arabic - Tunisia
# Language = "3801" # Arabic - U.A.E.
# Language = "2401" # Arabic - Yemen
# Language = "042b" # Armenian - Armenia
# Language = "044d" # Assamese
# Language = "082c" # Azeri (Cyrillic)
# Language = "042c" # Azeri (Latin)
# Language = "046d" # Bashkir
# Language = "042d" # Basque
# Language = "0423" # Belarusian
# Language = "0445" # Bengali (India)
# Language = "0845" # Bengali (Bangladesh)
# Language = "141A" # Bosnian (Bosnia/Herzegovina)
# Language = "047e" # Breton
# Language = "0402" # Bulgarian
# Language = "0455" # Burmese
# Language = "0403" # Catalan
# Language = "045c" # Cherokee - United States
Language = "0804" # Chinese - People's Republic of China 
# Language = "1004" # Chinese - Singapore
# Language = "0404" # Chinese - Taiwan
# Language = "0c04" # Chinese - Hong Kong SAR
# Language = "1404" # Chinese - Macao SAR
# Language = "0483" # Corsican
# Language = "041a" # Croatian
# Language = "101a" # Croatian (Bosnia/Herzegovina)
# Language = "0405" # Czech
# Language = "0406" # Danish
# Language = "048c" # Dari
# Language = "0465" # Divehi
# Language = "0413" # Dutch - Netherlands
# Language = "0813" # Dutch - Belgium
# Language = "0466" # Edo
# Language = "0409" # English - United States
# Language = "0809" # English - United Kingdom
# Language = "0c09" # English - Australia
# Language = "2809" # English - Belize
# Language = "1009" # English - Canada
# Language = "2409" # English - Caribbean
# Language = "3c09" # English - Hong Kong SAR
# Language = "4009" # English - India
# Language = "3809" # English - Indonesia
# Language = "1809" # English - Ireland
# Language = "2009" # English - Jamaica
# Language = "4409" # English - Malaysia
# Language = "1409" # English - New Zealand
# Language = "3409" # English - Philippines
# Language = "4809" # English - Singapore
# Language = "1c09" # English - South Africa
# Language = "2c09" # English - Trinidad
# Language = "3009" # English - Zimbabwe
# Language = "0425" # Estonian
# Language = "0438" # Faroese
# Language = "0429" # Farsi
# Language = "0464" # Filipino
# Language = "040b" # Finnish
# Language = "040c" # French - France
# Language = "080c" # French - Belgium
# Language = "2c0c" # French - Cameroon
# Language = "0c0c" # French - Canada
# Language = "240c" # French - Democratic Rep. of Congo
# Language = "300c" # French - Cote d'Ivoire
# Language = "3c0c" # French - Haiti
# Language = "140c" # French - Luxembourg
# Language = "340c" # French - Mali
# Language = "180c" # French - Monaco
# Language = "380c" # French - Morocco
# Language = "e40c" # French - North Africa
# Language = "200c" # French - Reunion
# Language = "280c" # French - Senegal
# Language = "100c" # French - Switzerland
# Language = "1c0c" # French - West Indies
# Language = "0462" # Frisian - Netherlands
# Language = "0467" # Fulfulde - Nigeria
# Language = "042f" # FYRO Macedonian
# Language = "0456" # Galician
# Language = "0437" # Georgian
# Language = "0407" # German - Germany
# Language = "0c07" # German - Austria
# Language = "1407" # German - Liechtenstein
# Language = "1007" # German - Luxembourg
# Language = "0807" # German - Switzerland
# Language = "0408" # Greek
# Language = "046f" # Greenlandic
# Language = "0474" # Guarani - Paraguay
# Language = "0447" # Gujarati
# Language = "0468" # Hausa - Nigeria
# Language = "0475" # Hawaiian - United States
# Language = "040d" # Hebrew
# Language = "0439" # Hindi
# Language = "040e" # Hungarian
# Language = "0469" # Ibibio - Nigeria
# Language = "040f" # Icelandic
# Language = "0470" # Igbo - Nigeria
# Language = "0421" # Indonesian
# Language = "045d" # Inuktitut
# Language = "083c" # Irish
# Language = "0410" # Italian - Italy
# Language = "0810" # Italian - Switzerland
# Language = "0411" # Japanese
# Language = "0486" # K'iche
# Language = "044b" # Kannada
# Language = "0471" # Kanuri - Nigeria
# Language = "0860" # Kashmiri
# Language = "0460" # Kashmiri (Arabic)
# Language = "043f" # Kazakh
# Language = "0453" # Khmer
# Language = "0487" # Kinyarwanda
# Language = "0457" # Konkani
# Language = "0412" # Korean
# Language = "0440" # Kyrgyz (Cyrillic)
# Language = "0454" # Lao
# Language = "0476" # Latin
# Language = "0426" # Latvian
# Language = "0427" # Lithuanian
# Language = "046e" # Luxembourgish
# Language = "043e" # Malay - Malaysia
# Language = "083e" # Malay - Brunei Darussalam
# Language = "044c" # Malayalam
# Language = "043a" # Maltese
# Language = "0458" # Manipuri
# Language = "0481" # Maori - New Zealand
# Language = "0471" # Mapudungun
# Language = "044e" # Marathi
# Language = "047c" # Mohawk
# Language = "0450" # Mongolian (Cyrillic)
# Language = "0850" # Mongolian (Mongolian)
# Language = "0461" # Nepali
# Language = "0861" # Nepali - India
# Language = "0414" # Norwegian (Bokmål)
# Language = "0814" # Norwegian (Nynorsk)
# Language = "0482" # Occitan
# Language = "0448" # Oriya
# Language = "0472" # Oromo
# Language = "0479" # Papiamentu
# Language = "0463" # Pashto
# Language = "0415" # Polish
# Language = "0416" # Portuguese - Brazil
# Language = "0816" # Portuguese - Portugal
# Language = "0446" # Punjabi
# Language = "0846" # Punjabi (Pakistan)
# Language = "046B" # Quecha - Bolivia
# Language = "086B" # Quecha - Ecuador
# Language = "0C6B" # Quecha - Peru
# Language = "0417" # Rhaeto-Romanic
# Language = "0418" # Romanian
# Language = "0818" # Romanian - Moldava
# Language = "0419" # Russian
# Language = "0819" # Russian - Moldava
# Language = "043b" # Sami (Lappish)
# Language = "044f" # Sanskrit
# Language = "043c" # Scottish Gaelic
# Language = "046c" # Sepedi
# Language = "0c1a" # Serbian (Cyrillic)
# Language = "081a" # Serbian (Latin)
# Language = "0459" # Sindhi - India
# Language = "0859" # Sindhi - Pakistan
# Language = "045b" # Sinhalese - Sri Lanka
# Language = "041b" # Slovak
# Language = "0424" # Slovenian
# Language = "0477" # Somali
# Language = "042e" # Sorbian
# Language = "0c0a" # Spanish - Spain (Modern Sort)
# Language = "040a" # Spanish - Spain (Traditional Sort)
# Language = "2c0a" # Spanish - Argentina
# Language = "400a" # Spanish - Bolivia
# Language = "340a" # Spanish - Chile
# Language = "240a" # Spanish - Colombia
# Language = "140a" # Spanish - Costa Rica
# Language = "1c0a" # Spanish - Dominican Republic
# Language = "300a" # Spanish - Ecuador
# Language = "440a" # Spanish - El Salvador
# Language = "100a" # Spanish - Guatemala
# Language = "480a" # Spanish - Honduras
# Language = "580a" # Spanish - Latin America
# Language = "080a" # Spanish - Mexico
# Language = "4c0a" # Spanish - Nicaragua
# Language = "180a" # Spanish - Panama
# Language = "3c0a" # Spanish - Paraguay
# Language = "280a" # Spanish - Peru
# Language = "500a" # Spanish - Puerto Rico
# Language = "540a" # Spanish - United States
# Language = "380a" # Spanish - Uruguay
# Language = "200a" # Spanish - Venezuela
# Language = "0430" # Sutu
# Language = "0441" # Swahili
# Language = "041d" # Swedish
# Language = "081d" # Swedish - Finland
# Language = "045a" # Syriac
# Language = "0428" # Tajik
# Language = "045f" # Tamazight (Arabic)
# Language = "085f" # Tamazight (Latin)
# Language = "0449" # Tamil
# Language = "0444" # Tatar
# Language = "044a" # Telugu
# Language = "041e" # Thai
# Language = "0851" # Tibetan - Bhutan
# Language = "0451" # Tibetan - People's Republic of China
# Language = "0873" # Tigrigna - Eritrea
# Language = "0473" # Tigrigna - Ethiopia
# Language = "0431" # Tsonga
# Language = "0432" # Tswana
# Language = "041f" # Turkish
# Language = "0442" # Turkmen
# Language = "0480" # Uighur - China
# Language = "0422" # Ukrainian
# Language = "0420" # Urdu
# Language = "0820" # Urdu - India
# Language = "0843" # Uzbek (Cyrillic)
# Language = "0443" # Uzbek (Latin)
# Language = "0433" # Venda
# Language = "042a" # Vietnamese
# Language = "0452" # Welsh
# Language = "0488" # Wolof
# Language = "0434" # Xhosa
# Language = "0485" # Yakut
# Language = "0478" # Yi
# Language = "043d" # Yiddish
# Language = "046a" # Yoruba
# Language = "0435" # Zulu
# Language = "04ff" # HID (Human Interface Device)


def CreateContextMenuEntry(AL_path, language):
    cmdline = '%s "%%1" /L%s' % (AL_path, language)
    try:
        shellkey = wreg.OpenKey(wreg.HKEY_CLASSES_ROOT, r"exefile\shell", 0, wreg.KEY_ALL_ACCESS)
    except WindowsError:
        print "[!] Error: Could not open key. Ensure script is ran as Administrator"
        return False
    appkey = wreg.CreateKey(shellkey, "Execute with AppLocale")
    cmdkey = wreg.CreateKey(appkey, "command")
    wreg.SetValue(cmdkey, "", wreg.REG_SZ, cmdline)
    return True


if __name__ == "__main__":
    try:
        print "Using language %s" % Language
    except NameError:
        print "[!] Language variable not set."
        print "[!] Edit this script with a text editor and uncomment the desired language."
        quit()
    
    AppLocale_path = os.path.expandvars(AppLocale)
    if not os.path.exists(AppLocale_path):
        print "Unable to find AppLocale.exe. Expected at: %s" % AppLocale_path
        print "If AppLocale is not installed, retrieve from: http://www.microsoft.com/en-us/download/details.aspx?id=13209"
        quit()
    result = CreateContextMenuEntry(AppLocale_path, str(Language))
    if not result:
        print "Error setting registry key"
    else:
        print "Right-click context menu set successfully as 'Execute with AppLocale'"
