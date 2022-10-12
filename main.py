import glob
import os
import re
import shutil

video_extensions = ["mp4", "mkv", "ts"]


class Explorer:
    def __init__(self, root_path):
        self.renamer = Renamer()

        self.root_path = root_path

    def main(self):
        for root, dirs, files in os.walk(self.root_path):
            if root != self.root_path:
                continue
            dir_names = dirs
            file_names = files

        # 同时没有season文件夹并且有至少5个视频
        season_flag = all(["season" not in dir_name for dir_name in dir_names])
        video_num = sum([int(file_name.split(".")[-1] in video_extensions) for file_name in file_names])
        if season_flag and video_num >= 5:
            self.one_season(season_num=1)

        # 已经分好season文件夹
        if not season_flag and all(["season" in dir_name for dir_name in dir_names]):
            for dir_name in dir_names:
                season_num = int(dir_name.replace("season", ""))
                self.renamer.season_rename(os.path.join(self.root_path, dir_name), season_num)

    def one_season(self, season_num):
        # 创建season1文件夹
        season_dir = os.path.join(self.root_path, "season" + str(season_num))
        os.makedirs(season_dir)
        # 把所有东西全部移入文件夹内
        for item in glob.glob(os.path.join(self.root_path, "*")):
            shutil.move(item, season_dir)
        self.renamer.season_rename(season_dir, season_num)


class Renamer:
    def __init__(self):
        pass

    def check_regular(self, video_list):
        video_list.sort()
        result = all([re.search('.*{}.*'.format(str(index + 1)), video_name) is not None for index, video_name in
                      enumerate(video_list)])
        return result

    def season_rename(self, path, season_num):
        # 查找所有视频
        video_list = []
        for extension in video_extensions:
            videos = glob.glob(os.path.join(path, "*." + extension))
            if videos:
                video_list.extend(list(videos))
        video_list.sort()
        # 判断是否是名称中是否只有序号发生变化
        regular_flag = self.check_regular(video_list)
        if regular_flag:
            self.video_rename(video_list, season_num)
            return True
        else:
            return False

    # 删除op ed
    def remove_song(self, path):
        pass

    # 给确认只有正片的视频和同名字幕重命名
    def video_rename(self, video_list, season_num):
        for index, video_path in enumerate(video_list):
            video_name = os.path.basename(video_path)
            video_root = os.path.dirname(video_path)
            base_name = ".".join(video_name.split(".")[:-1])
            new_base_name = "S" + str(season_num).zfill(2) + "E" + str(index + 1).zfill(2)

            # 查找同名所有文件
            all_files = os.listdir(video_root)
            same_names = []
            for file in all_files:
                if base_name in file:
                    same_names.append(os.path.join(video_root, file))
            single_ass_flag = (len(same_names) <= 2)
            for same_name in same_names:
                extension = same_name.split(".")[-1]

                # 如果是字幕，只有一个或是简中就给加上".default"
                if ("sc" in same_name.split(".") or single_ass_flag) and extension in ["ass", "ssa"]:
                    os.rename(same_name, same_name.replace(base_name, new_base_name + ".default"))
                # 不是字幕就正常命名
                else:
                    os.rename(same_name, same_name.replace(base_name, new_base_name))


if __name__ == '__main__':
    path = r"/home/chenjiasheng/DAV/Resource/EMBY/DONGMAN/重启咲良田"
    namer = Explorer(path)
    namer.main()
