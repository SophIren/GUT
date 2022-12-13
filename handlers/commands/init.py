from gut_settings import GutSettings


class InitHandler(GutSettings):
    def handle(self) -> None:
        self.objects_dir_path.mkdir(exist_ok=True, parents=True)
        self.heads_dir_path.mkdir(exist_ok=True, parents=True)

        self.index_file_path.touch(exist_ok=True)
        self.head_file_path.touch(exist_ok=True)

        self.default_head_file_path.touch(exist_ok=True)
        self.head_file_path.write_text(str(self.default_head_file_path))
