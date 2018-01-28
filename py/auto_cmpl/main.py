import cmpl
import config
import xml_utils

if __name__ == '__main__':
    cfg = None
    compile = None

    for project_name, root_path, raid, burner, firepath in xml_utils.iter_pro():
        cfg = config.Config (project_name, root_path, raid, burner, firepath)
        compile = cmpl.Cmpl(cfg)
        #break

    cfg.show()
    #only test one compiler
    compile.compile()
    #compile.show()