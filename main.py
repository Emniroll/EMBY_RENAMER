import glob
import os
import re
import shutil


class Renamer:
    def __init__(self, root_path):
        self.root_path = root_path

    def one_season(self):
        # 创建season1文件夹
        season1_dir = os.path.join(self.root_path, "season1")
        os.makedirs(season1_dir)
        # 把所有东西全部移入文件夹内
        for item in glob.glob(self.root_path + "/*"):
            shutil.move(item, season1_dir)

    def rename(self, path, season_num):
        # 查找所有视频
        video_list = []
        for extension in [".mp4", ".mkv", ".ts"]:
            videos = glob.glob(path + "/*" + extension)
            # videos = glob.glob(path + "/*" + extension)
            if videos:
                video_list.extend(list(videos))
        video_list.sort()
        # 判断是否是名称中是否只有序号发生变化
        # video_numbers = len(video_list)
        a = [re.search('.*{}.*'.format(str(index + 1)), video_name) is not None for index, video_name in
             enumerate(video_list)]
        print(video_list)
        print(a)


if __name__ == '__main__':
    path = r"/home/chenjiasheng/DAV/Resource/EMBY/DONGMAN/悠久持有者"
    namer = Renamer(path)
    namer.rename(path)
