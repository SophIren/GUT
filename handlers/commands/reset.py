from handlers.branch_info_handler import BranchInfoHandler
from handlers.tree.tree_info import TreeInfoHandler


class ResetHandler(TreeInfoHandler, BranchInfoHandler):
    def handle(self, to_commit: str):
        (self.HEADS_DIR_PATH / self.current_commit).write_text(to_commit)
