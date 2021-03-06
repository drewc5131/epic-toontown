from panda3d.core import *

if __debug__:
    loadPrcFile('etc/Configrc.prc')

import builtins

class game:
    name = 'toontown'
    process = 'client'


builtins.game = game()
import time
import os
import sys
import random
import builtins
try:
    launcher
except:
    from toontown.launcher.ToontownDummyLauncher import ToontownDummyLauncher
    launcher = ToontownDummyLauncher()
    builtins.launcher = launcher
    
from libotp.settings.JSONSettings import JSONSettings
builtins.settings = JSONSettings()
if 'fullscreen' not in settings:
    settings['fullscreen'] = False
if 'music' not in settings:
    settings['music'] = True
if 'sfx' not in settings:
    settings['sfx'] = True
if 'musicVol' not in settings:
    settings['musicVol'] = 1.0
if 'sfxVol' not in settings:
    settings['sfxVol'] = 1.0
if 'loadDisplay' not in settings:
    settings['loadDisplay'] = 'pandagl'
if 'toonChatSounds' not in settings:
    settings['toonChatSounds'] = True
if 'aspectRatio' not in settings:
    settings['aspectRatio'] = 0
if 'textureQuality' not in settings:
    settings['textureQuality'] = 3
if 'speakerMode' not in settings:
    settings['speakerMode'] = 0
if 'detailDistance' not in settings:
    settings['detailDistance'] = 2
if 'displayMode' not in settings:
    settings['displayMode'] = 0
if 'res' not in settings:
    settings['res'] = [1280, 720]
if 'camSensitivityX' not in settings:
    settings['camSensitivityX'] = 0.31
if 'camSensitivityY' not in settings:
    settings['camSensitivityY'] = 0.21
if 'controllerBrand' not in settings:
    settings['controllerBrand'] = 0
loadPrcFileData('Settings: res', 'win-size 800 300')
loadPrcFileData('Settings: fullscreen', 'fullscreen 0')
loadPrcFileData('Settings: undecorated', 'undecorated 0')
loadPrcFileData('Settings: music', 'audio-music-active %s' % settings['music'])
loadPrcFileData('Settings: sfx', 'audio-sfx-active %s' % settings['sfx'])
loadPrcFileData('Settings: musicVol', 'audio-master-music-volume %s' % settings['musicVol'])
loadPrcFileData('Settings: sfxVol', 'audio-master-sfx-volume %s' % settings['sfxVol'])
loadPrcFileData('Settings: loadDisplay', 'load-display %s' % settings['loadDisplay'])
loadPrcFileData('Settings: toonChatSounds', 'toon-chat-sounds %s' % settings['toonChatSounds'])
loadPrcFileData('Settings: Speaker Mode',
                'fmod-speaker-mode %s' % ["stereo", "quad", "surround", "5.1", "7.1"][settings['speakerMode']])
loadPrcFileData('', 'ffmpeg-prefer-libvpx 1')

launcher.setRegistry('EXIT_PAGE', 'normal')
pollingDelay = 0.5
print('ToontownStart: Polling for game2 to finish...')
while not launcher.getGame2Done():
    time.sleep(pollingDelay)

print('ToontownStart: Game2 is finished.')
print('ToontownStart: Starting the game.')
if launcher.isDummy():
    http = HTTPClient()
else:
    http = launcher.http
tempLoader = Loader()
backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/loading-background'))
from direct.gui import DirectGuiGlobals
print('ToontownStart: setting default font')
from . import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
from . import ToonBase
ToonBase.ToonBase()
if base.win == None:
    print('Unable to open window; aborting.')
    sys.exit()
launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)
backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
backgroundNodePath.setPos(0.0, 0.0, 0.0)
backgroundNodePath.setScale(render2d, VBase3(1))
backgroundNodePath.find('**/fg').setBin('fixed', 20)
backgroundNodePath.find('**/bg').setBin('fixed', 10)
base.graphicsEngine.renderFrame()
DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
from . import TTLocalizer
from otp.otpbase import OTPGlobals
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)
if base.musicManagerIsValid:
    music = base.musicManager.getSound('phase_3/audio/bgm/tt_theme.ogg')
    if music:
        music.setLoop(1)
        music.setVolume(0.9)
        music.play()
    print('ToontownStart: Loading default gui sounds')
    DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
    DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
else:
    music = None
from . import ToontownLoader
from direct.gui.DirectGui import *
serverVersion = base.config.GetString('server-version', 'no_version_set')
print('ToontownStart: serverVersion: ', serverVersion)
version = OnscreenText(serverVersion, pos=(-1.3, -0.975), scale=0.06, fg=Vec4(0, 0, 1, 0.6), align=TextNode.ALeft)
loader.beginBulkLoad('init', TTLocalizer.LoaderLabel, 138, 0, TTLocalizer.TIP_NONE)
from .ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *
from toontown.distributed import ToontownClientRepository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
cr.music = music
del music
base.initNametagGlobals()
base.cr = cr
loader.endBulkLoad('init')
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
if not launcher.isDummy():
    base.startShow(cr, launcher.getGameServer())
else:
    base.startShow(cr)
backgroundNodePath.reparentTo(hidden)
backgroundNodePath.removeNode()
del backgroundNodePath
del backgroundNode
del tempLoader
version.cleanup()
del version
base.loader = base.loader
builtins.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)
if autoRun and launcher.isDummy() and (not Thread.isTrueThreads() or __name__ == '__main__'):
    try:
        base.run()
    except SystemExit:
        raise
    except:
        from otp.otpbase import PythonUtil
        print(PythonUtil.describeException())
        raise
