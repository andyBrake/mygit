import cmpl
import config
import xml_utils

if __name__ == '__main__':
    cfg = None
    cmp = None

    #only get the first enable project to process
    for project_name,enable, root_path, raid, burner, firepath in xml_utils.iter_pro():
        if not enable:
            print("project %s is not enable, skip it."%project_name)
            continue

        cfg = config.Config (project_name, root_path, raid, burner, firepath)
        cmp = cmpl.Cmpl(cfg)
        break

    #start to process the project
    print("=======================================================================")

    #cmp.compile()
    #cmp.show()

    #cmp.start_to_adjust()
    cmp.fix_addr2ftk()


    print("=======================================================================")