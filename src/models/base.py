# # -*- coding:utf-8 -*-
# from contextlib import contextmanager
#
# from flask_sqlalchemy import SQLAlchemy
#
# __all__ = ["db"]
#
#
# class _SQLAlchemy(SQLAlchemy):
#     @contextmanager
#     def auto_commit(self):
#         try:
#             yield
#             self.session.commit()
#         except Exception:
#             self.session.rollback()
#             raise
#
#
# db = _SQLAlchemy(session_options={"expire_on_commit": False})
