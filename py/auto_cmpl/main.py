import cmpl
import config
import xml_utils
from tkinter import *


def notify(success=True):
    window = Tk()
    window.title('build finish')
    window.geometry('400x100')

    label = Label(window,text = 'Build Notify')
    label.pack()

    if success:
        l2 = Label(window, fg='black', bg='green', text='Success', width=50, height=3).pack()
    else:
        l2 = Label(window, fg='lightblue', bg='red', text='Fail', width=50, height=3).pack()

    if success:
        text = 'OK, build success!'
    else:
        text = 'Oh! build failed!'

    #jump to the top
    window.wm_attributes('-topmost',1)

    # 进入消息循环
    window.mainloop()
    return

def get_cfg():
    cfg = None
    cmp = None

    for project_name,enable, root_path, raid, burner, firepath in xml_utils.iter_pro():
        if not enable:
            print("project %s is not enable, skip it."%project_name)
            continue

        cfg = config.Config (project_name, root_path, raid, burner, firepath)
        cmp = cmpl.Cmpl(cfg)
        break
    return cfg, cmp

if __name__ == '__main__':
    cfg, cmp = get_cfg()

    if cmp == None or cfg == None:
        print("no project to process.")
        exit(0)
    #start to process the project
    print("=======================================================================")
    cmp.compile()
    if not cmp.build_ok():
        cmp.start_to_adjust()
    print("=======================================================================")

    notify()
