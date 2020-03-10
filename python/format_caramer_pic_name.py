import os,time

work_dir='./xx'

for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
    for filename in filenames:
        file_path = os.path.join(parent, filename)

        ctime = os.path.getmtime(file_path)
        time_local = time.localtime(ctime)
        dt = time.strftime("IMG_%Y%m%d_%H%M%S.jpg",time_local)

        old_src = os.path.join(parent, filename)
        new_src = os.path.join(parent, dt)
        print('Old Src = %s' % old_src)
        print('New Src = %s' % new_src)
##        os.rename(old_src, new_src)
