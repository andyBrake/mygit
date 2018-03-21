使用方法：
一、第一步配置cfg.xml文件，该文件中第一个enable的工程会作为项目的操作目标
配置格式如下：
<project name="Main_project" >
    <root>C:\Users\huangfa\workspace\gitProject\dualcore\</root>  #此为工程的根目录
    <enable>true</enable>                                         #true表示操作这个工程，false表示不操作。当多个工程enable时，以从上到下第一个enable工程为准
	<raid>true</raid>                                             #true表示编译raid版本，false表示non raid
	<burner>true</burner>                                         #true表示拷贝产生的bin文件到下面的目录去，并且会自动进行备份。普通使用场景下建议设为false
    <fire>C:\Users\huangfa\workspace\firmware_version\fireinto\FW\nvme_B0_image\</fire>  #配合上面一项使用，burner为false时，可以不配置该项
</project>
注意：路径名一定是\结尾哦！不要遗漏

二、build 工程
执行main.py就会开始完整的编译过程，会先删除老的输出文件，再进行编译，最后再检查编译结果。
编译的信息会输出到工程根目录下的两个文件build_result.txt和fitered_result.txt中。其中fitered_result.txt是过滤掉了某些warning信息的，方便定位编译问题。
注意，编译结束后，会有弹窗弹出提示结果。所以在编译期间可以放心做其他事情，不会遗漏编译结果的^_^!

三、编译结果处理
编译成功后会输出“generate the image file success!”等信息。
编译失败后，有两种情况。一种是代码语法问题，直接编译失败。此时会提示有编译错误，可根据fitered_result.txt去定位；
第二种错误是语法正确，mem map失败，build 失败后有类似输出：
```
CORE 0
ignore PROGRAM_LOADI
ignore DATA_LOAD
ignore CORE_0_SAFE_CODE_DATA
section CORE_0_UNSAFE_CODE_DATA need to decrease size(41984, 41856).
	section : CORE_0_UNSAFE_CODE_DATA old max size : 41984[0xa400], new max size : 41856[0xa380] 
	set CORE_0_UNSAFE_CODE_DATA_SIZE 41856.
section CORE_0_UNSAFE_INIT need to decrease size(16384, 4816).
	section : CORE_0_UNSAFE_INIT old max size : 16384[0x4000], new max size : 4832[0x12e0] 
	set CORE_0_INIT_CODE_SIZE 4832.
ignore PWR_UNSAFE_INIT
ignore SHARED_DATA

CORE 1
ignore PROGRAM_LOADI
ignore DATA_LOAD
ignore DATA_MATE
section CORE_1_SAFE_CODE_DATA need to decrease size(48128, 47628).
	section : CORE_1_SAFE_CODE_DATA old max size : 48128[0xbc00], new max size : 47648[0xba20] 
	set CORE_1_SAFE_CODE_DATA_SIZE 47648.
ignore PWR_SAFE_INIT
section CORE_1_UNSAFE_CODE_DATA need to increase size(235904, 236000).
	section : CORE_1_UNSAFE_CODE_DATA old max size : 235904[0x39980], new max size : 236000[0x399e0] 
	set CORE_1_UNSAFE_CODE_DATA_SIZE 236000.
section CORE_1_UNSAFE_INIT need to decrease size(79872, 78160).
	section : CORE_1_UNSAFE_INIT old max size : 79872[0x13800], new max size : 78176[0x13160] 
	set CORE_1_INIT_CODE_SIZE 78176.
ignore PWR_UNSAFE_INIT
ignore SHARED_DATA
```
这说明检查出了有size不足的section，只需要关心需要increase的section，上面只有CORE_1_UNSAFE_CODE_DATA_SIZE这个section，在代码中修改这个宏的定义为236000即可。
然后重新编译，注意这种修改section size之后的编译，在build成功后，还需要修改ftk文件，否则上电会失败。

四、自动修改ftk文件
执行modify_ftk.py会自动完成ftk文件的修改,注意修改了ftk文件之后还需要再执行main.py一次重新编译工程产生新的image。
执行modify_ftk之后的显示大致如下，unmatch的key就是在ftk文件中会被修改的section.
=======================================================================
	unmatch-key C0_UNSAFE_CODE_DATA 0x20060180 0x200601e0
change [C0_BTCM] addr[0x00045800] to [0x00045800]
change [C0_UNSAFE_CODE_DATA] addr[0x20060180] to [0x200601e0]
change [INIT_CODE_BASE] addr[0x2006a580] to [0x2006a5e0]
change [C1_UNSAFE_CODE_DATA] addr[0x20026800] to [0x20026800]
change [C1_INIT_CODE_BASE] addr[0x2006e580] to [0x2006e5e0]
=======================================================================

