# -*- coding:utf-8 -*-
import os
import shutil
import time
from django.conf import settings

from app.libs.base_qiniu import video_qiniu
from app.models import Video, VideoSub
def check_and_get_video_type(type_obj, type_value, message):
    try:
       type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}
    return {'code': 0, 'msg': 'success'}

def remove_path(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)







def handle_video(video_file, video_id, number):

    in_path = os.path.join(settings.BASE_DIR, r'app\dashboard\temp_in')
    out_path = os.path.join(settings.BASE_DIR, r'app\dashboard\temp_out')
    temp_path = video_file.temporary_file_path()
    name = '{}_{}'.format(int(time.time()), video_file.name)
    path_name = '/'.join([in_path, name])
    shutil.copyfile(temp_path, path_name)

    out_name = '{}_{}'.format(int(time.time()), video_file.name.split('.')[0])
    out_path_name = '/'.join([out_path, out_name])


    dir = os.getcwd()
    # 获取当前文件路径，因为我这里把ffmpeg工具放到了代码路径，所以需要获取一下当前路径，这个根据大家实际情况写
    dir2 = '/ffmpeg/bin/ffmpeg.exe'  # ffmpeg具体位置
    ff = dir + dir2  # 组合路径
    result = eval(repr(ff).replace('\\', '/'))
    # 转换反斜杠为斜杠，因为获取到的路径是反斜杠的，需要转换成斜杠，转换后会发现是双斜杠，所以需要下面再转换下
    ff = result.replace('//', '/')

    command =' -i {} -c copy {}.mp4'.format(path_name, out_path_name)
    cmd = ff + command

    os.system(cmd)

    out_name = '.'.join([out_path_name, 'mp4'])
    print(out_path_name)
    print(out_name)
    if not os.path.exists(out_name):
        return False
    final_name = '{}_{}'.format(int(time.time()), video_file.name)
    video_qiniu.put(final_name, out_name)
    print(final_name)
    url = 'http://' +'r9v3bcv79.hb-bkt.clouddn.com' + '/' + final_name
    print(url)
    if url:
        video = Video.objects.get(pk=video_id)

        try:
            VideoSub.objects.create(
                video=video,
                url=url,
                number=number
            )
            return True
        except:
            return False
        finally:
            remove_path([out_name, path_name])

    remove_path([out_name, path_name])

    return False

