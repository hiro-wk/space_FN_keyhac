from keyhac import *
import time

def configure(keymap):
    
    class variables(): 
        pass

    # set_mark
    variables.is_marked = False

    # リージョンを拡張する際に、順方向に拡張すると True、逆方向に拡張すると False になる
    variables.forward_direction = None
    
    def delay(sec=0.02):
        time.sleep(sec)

    # def mark(func, forward_direction):
    #     def _func():
    #         if variables.is_marked:
    #             # D-Shift だと、M-< や M-> 押下時に、D-Shift が解除されてしまう。その対策。
    #             keymap.InputKeyCommand("D-LShift", "D-RShift")()
    #             delay()
    #             func()
    #             keymap.InputKeyCommand("U-LShift", "U-RShift")()

    #             # fakeymacs.forward_direction が未設定の場合、設定する
    #             if variables.forward_direction is None:
    #                 variables.forward_direction = forward_direction
    #         else:
    #             variables.forward_direction = None
    #             func()
    #     return _func    
    def mark(func):
        def _func():
            if variables.is_marked:
                # D-Shift だと、M-< や M-> 押下時に、D-Shift が解除されてしまう。その対策。
                keymap.InputKeyCommand("D-LShift", "D-RShift")()
                delay()
                func()
                keymap.InputKeyCommand("U-LShift", "U-RShift")()

            else:
                func()
        return _func    

    def set_mark():
        variables.is_marked = ~variables.is_marked
    def esc():
        keymap.InputKeyCommand('Esc')
        variables.is_marked = False
    
    @mark
    def forward():
        keymap.InputKeyCommand('Right')()    
    @mark
    def backward():
        keymap.InputKeyCommand('Left')()  
    @mark
    def upward():
        keymap.InputKeyCommand('Up')()   
    @mark
    def downward():
        keymap.InputKeyCommand('Down')()   
    @mark
    def to_home():
        keymap.InputKeyCommand('Home')()   
    @mark
    def to_end():
        keymap.InputKeyCommand('End')()
    
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
    def paste():
        keymap.InputKeyCommand("C-v")()
        variables.is_marked = False

    def kill_line():
        variables.is_marked = True
        keymap.InputKeyCommand("End")
        cut()

    def alphabetize():
        keymap.InputKeyCommand("C-t")()

    # カーソル移動に使うUser1
    # スペース
    #Spaceに仮想キーコード236を割り当て
    keymap.replaceKey( "Space", 236 )
    #236にU1を割り当て
    keymap.defineModifier( 236, "User1" )

    # global key map 
    keymap_global = keymap.defineWindowKeymap()
    
    #スペースキーのみを押した時は本来の動作をする
    keymap_global[ "O-236" ] = "Space"

    # 高速変換対応
    keymap_global["User1-Enter"] = keymap.InputKeyCommand("Space", "Enter")

    # カーソル移動
    keymap_global["User1-i"] = upward
    keymap_global["User1-j"] = backward 
    keymap_global["User1-k"] = downward
    keymap_global["User1-l"] = forward # "Right" 
    keymap_global["User1-u"] = to_home 
    keymap_global["User1-o"] = to_end

    keymap_global["User1-Semicolon"] = kill_line

    # set_mark
    keymap_global["User1-a"] = set_mark
    # escでreset_mark
    keymap_global["Esc"] = esc
    
    # 削除
    keymap_global["User1-h"] = delete_back 
    keymap_global["User1-d"] = delete_forward

    # copy, cut, paste
    keymap_global["User1-x"] = cut
    keymap_global["User1-c"] = copy
    keymap_global["User1-v"] = paste

    keymap_global["User1-z"] = "C-z"

    keymap_global["User1-t"] = alphabetize
