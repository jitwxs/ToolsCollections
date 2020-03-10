import os,time

def get_new_path(work_str, op_type, op_status, parent, filename):
    new_path = None
    # 添加操作
    if op_status == '1':
        if op_type == '1':
            new_path = os.path.join(parent, work_str + filename)
        elif op_type == '2':
            try:
                separator_index = filename.rindex('.')
                new_path = os.path.join(parent, filename[:separator_index] + work_str + filename[separator_index:])
            except:
                pass
    # 删除操作
    elif op_status == '2':
        if op_type == '1':
            if filename.startswith(work_str):
                new_path = os.path.join(parent, filename[len(work_str):])
        elif op_type == '2':
            try:
                separator_index = filename.rindex('.')
                prefix = filename[:separator_index]
                suffix = filename[separator_index:]
                if prefix.endswith(work_str):
                    new_path = os.path.join(parent, prefix[:(len(prefix) - len(work_str))] + suffix)
            except:
                pass

    return new_path

def work_func(work_dir, work_str, op_type, op_status, has_recursion):
    # 开启递归
    if has_recursion == '1':
        for parent, dirs, files in os.walk(work_dir,  followlinks=False):
            for filename in files:
                try:
                    old_path = os.path.join(parent, filename)
                    new_path = get_new_path(work_str, op_type, op_status, parent, filename)
                    # 重命名
                    if new_path != None:
                        os.rename(old_path, new_path)
                except:
                    pass
    elif has_recursion == '2':
        for filename in os.listdir(work_dir):
            try:
                old_path = os.path.join(work_dir, filename)
                new_path = get_new_path(work_str, op_type, op_status, work_dir, filename)
                # 重命名
                if new_path != None:
                    os.rename(old_path, new_path)
            except:
                pass


if __name__ == '__main__':
    print('欢迎使用文件前缀/后缀处理工具！')
    print('作者：Jiwxs')
    print('===============================================')
    
    work_dir = input('Step1：请指定工作目录（相对/绝对路径）：')
    while True:
        op_status = input('Step2：请指定操作模式【1：添加；2：删除】：')
        if op_status == '1' or op_status == '2':
            break
        else:
            print('【错误】参数非法')
    while True:
        op_type = input('Step3：请指定操作类型【1：前缀；2：后缀】')
        if op_type == '1' or op_type == '2':
            break
        else:
            print('【错误】参数非法')
    while True:
        has_recursion = input('Step4：请指定是否递归操作【1：是；2：否】')
        if has_recursion == '1' or has_recursion == '2':
            break
        else:
            print('【错误】参数非法')
    work_str = input('Step5：请指定操作串：');

    print('您即将对 {} 路径下的文件执行 {} {} 操作，是否递归：{}'.format(
        work_dir, '添加' if op_status == '1' else '删除', '前缀' if op_type == '1' else '后缀', '是' if has_recursion == '1' else '否'))
    has_ok = input('是否确认执行（y）？')
    if has_ok == 'y':
        work_func(work_dir, work_str, op_type, op_status, has_recursion)

    
