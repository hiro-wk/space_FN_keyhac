from keyhac import *
import time, os, urllib

def configure(keymap):
    
    # 編集エディタをvs codeにする
    EDITOR_PATH = r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe"\
			.format(os.environ.get("USERNAME"))
    if not os.path.exists(EDITOR_PATH):
        EDITOR_PATH = "notepad.exe"
    keymap.editor = EDITOR_PATH

    # # クリップボード履歴有効化
    # keymap.clipboard_history.enableHook(True)
    # # 履歴の最大サイズ
    # keymap.clipboard_history.maxnum = 200
    # keymap.clipboard_history.quota = 10*1024*1024
    # # 履歴から Ctrl+Enter で引用貼り付けするときの記号
    # keymap.quote_mark = "> "

    class variables():
        pass

    # set_mark
    variables.is_marked = False

    # リージョンを拡張する際に、順方向に拡張すると True、逆方向に拡張すると False になる
    variables.forward_direction = None
    
    def delay(sec=0.02):
        time.sleep(sec)
 
    def mark(func):
        def _func(*args,**kwargs):
            if variables.is_marked:
                # D-Shift だと、M-< や M-> 押下時に、D-Shift が解除されてしまう。その対策。
                keymap.InputKeyCommand("D-LShift", "D-RShift")()
                delay()
                func()
                keymap.InputKeyCommand("U-LShift", "U-RShift")()

            else:
                func(*args,**kwargs)
        return _func

    def set_mark():
        variables.is_marked = ~variables.is_marked
        print('set mark')

    def esc():
        keymap.InputKeyCommand('Esc')()
        variables.is_marked = False
        print('unset mark')
    
    @mark
    def forward(modifier=''):
        keymap.InputKeyCommand(modifier+'Right')()    
    @mark
    def backward(modifier=''):
        keymap.InputKeyCommand(modifier+'Left')()  
    @mark
    def upward(modifier=''):
        keymap.InputKeyCommand(modifier+'Up')()   
    @mark
    def downward(modifier=''):
        keymap.InputKeyCommand(modifier+'Down')()   
    @mark
    def to_home(modifier=''):
        keymap.InputKeyCommand(modifier+'Home')()   
    @mark
    def to_end(modifier=''):
        keymap.InputKeyCommand(modifier+'End')()
    @mark
    def to_forward_char(modifier=''):
        keymap.InputKeyCommand(modifier+'C-Right')()
    @mark
    def to_backward_char(modifier=''):
        keymap.InputKeyCommand(modifier+'C-Left')()

    
    def delete_back():
        keymap.InputKeyCommand('Back')()
        variables.is_marked = False
    def delete_forward():
        keymap.InputKeyCommand('Delete')()
        variables.is_marked = False
    def cut():
        keymap.InputKeyCommand("C-x")()
        variables.is_marked = False
    def copy():
        keymap.InputKeyCommand("C-c")()
        variables.is_marked = False
    # 必ずテキストして貼り付け
    def paste():
        setClipboardText(getClipboardText())
        keymap.InputKeyCommand("C-v")()
        variables.is_marked = False
    def kill_line():
        variables.is_marked = True
        to_end()
        cut()

    # imeのON、OFF
    def switch_ime(flag):
        # バルーンヘルプを表示する時間(ミリ秒)
        BALLOON_TIMEOUT_MSEC = 500
        # if not flag:
        if flag:
            ime_status = 1
            message = u"[あ]"
        else:
            ime_status = 0
            message = u"[_A]"
        # IMEのON/OFFをセット
        keymap.wnd.setImeStatus(ime_status)
        # IMEの状態をバルーンヘルプで表示
        keymap.popBalloon("ime_status", message, BALLOON_TIMEOUT_MSEC)
        
    def ime_on():
        switch_ime(True)
    
    def ime_off():
        switch_ime(False)
  
    # 設定を適用したくないアプリケーション
    disable_apps = (,)
    def to_be_keyhacked(window):
        if window.getProcessName() in disable_apps: 
	        return False
        else:
	        return True

    # def replaceKey_with_check(from_key, to_key, check_func=lambda x:True):
    #     if check_func(keymap.getWindow()):
    #         print(keymap.getWindow().getProcessName())
    #         keymap.replaceKey(from_key, to_key)
    #     else:
    #         keymap.replaceKey(to_key, from_key)
    # replaceKey_with_check("Space", 236, check_func=to_be_keyhacked)


    # カーソル移動に使うUser1
    # スペース
    #Spaceに仮想キーコード236を割り当て
    keymap.replaceKey("Space", 236)
    #236にU1を割り当て
    keymap.defineModifier(236, "User1")
    
    # global key map
    keymap_global = keymap.defineWindowKeymap(check_func=to_be_keyhacked)
  
    # Win+9：キーフックOFF
    keymap_global["S-C-k"] = lambda: keymap.enableHook(False)
 
    keymap_global["C-S-v"] = keymap.command_ClipboardList

    # IME
    keymap_global["O-RShift"] = ime_on
    keymap_global["O-LShift"] = ime_off

    #スペースキーのみを押した時は本来の動作をする
    keymap_global["O-236"] = "Space"
    # 連続スペース
    keymap_global["User1-b"] = "Space"

    # 高速変換対応
    keymap_global["User1-Enter"] = keymap.InputKeyCommand("Space", "Enter")

    # カーソル移動
    for modifier in ("", "S-"):#, "C-", "A-", "C-S-", "C-A-", "S-A-", "C-A-S-"):
        def _wrap(func, modifier):
            return lambda: func(modifier=modifier)
        keymap_global[modifier + "User1-i"] = _wrap(upward, modifier)
        keymap_global[modifier + "User1-j"] = _wrap(backward, modifier)
        keymap_global[modifier + "User1-k"] = _wrap(downward, modifier)
        keymap_global[modifier + "User1-l"] = _wrap(forward, modifier)
        keymap_global[modifier + "User1-u"] = _wrap(to_home, modifier)
        keymap_global[modifier + "User1-o"] = _wrap(to_end, modifier)
        keymap_global[modifier + "User1-Comma"] = _wrap(to_backward_char,modifier)
        keymap_global[modifier + "User1-Period"] = _wrap(to_forward_char,modifier)
    
    # kill line
    keymap_global["User1-Semicolon"] = kill_line

    # set_mark
    keymap_global["User1-f"] = set_mark
    keymap_global['User1-Caps'] = set_mark

    # escでreset_mark
    keymap_global["Esc"] = esc
    keymap_global["User1-g"]  = "Esc"
    
    # 削除
    keymap_global["User1-h"] = delete_back 
    keymap_global["User1-d"] = delete_forward

    # copy, cut, paste
    keymap_global["User1-x"] = cut

    keymap_global["User1-c"] = copy
    keymap_global["User1-v"] = paste

    # 特殊
    keymap_global['User1-a'] = "C-a"
    keymap_global["User1-z"] = "C-z"
    keymap_global["S-User1-z"] = "S-C-z" 
    keymap_global['User1-w'] = "C-w"
    keymap_global["User1-t"] = "C-t" #alphabetize
    keymap_global["User1-Slash"] = "C-Slash"

    # partially azik
    def azik_tyouon():
        if keymap.getWindow().getImeStatus() == 1:
            keymap.InputKeyCommand('Minus')()
        else:
            keymap.InputKeyCommand('Quote')()
    def azik_hatsuon():
        if keymap.getWindow().getImeStatus() == 1:
            keymap.InputKeyCommand('l')()
            keymap.InputKeyCommand('t')()
            keymap.InputKeyCommand('u')()
        else:
            keymap.InputKeyCommand('Semicolon')()
    def azik_nn():
        if keymap.getWindow().getImeStatus() == 1:
            keymap.InputKeyCommand('n')() 
            keymap.InputKeyCommand('n')()
        else:
            keymap.InputKeyCommand('q')()

    keymap_global["Quote"] = azik_tyouon
    keymap_global["Semicolon"] = azik_hatsuon
    keymap_global["q"] = azik_nn


    def copy_string(sec = 0.05):
        keymap.InputKeyCommand("C-C")()
        delay(sec)
        return getClipboardText()


    # 選択した URL を開く
    def open_path():
        path = (copy_string()).strip()
        if path.startswith("http"):
            run_path = path
        else: # http以外で始まっているものはファイルパスとみなす
            if path.startswith("file:///"):
                path = path.replace("file:///", "") # file:/// を削除
            path = urllib.parse.unquote(path)
            if not os.path.exists(path):
                return None
            run_path = path
        os.startfile(run_path)
        # keymap.ShellExecuteCommand("start", run_path, None, None)()
    keymap_global["User1-e"] = open_path

    def search_on_google(prefix = r"http://www.google.com/search?q=", suffix = u""):
        def _search_on_google():
            text = copy_string()
            os.startfile(prefix + text + suffix)
        return _search_on_google
    def open_google():
        def _open_google():
            os.startfile("http://www.google.com/")
        return _open_google
    keymap_global["User1-s"] = search_on_google()
    keymap_global["User1-n"] = open_google()
