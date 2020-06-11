from flask_restx import Namespace
from flask import request
from src import db
from flask_restx import Resource, fields, abort
from src.utils import server_group_join, get_group_id

ns = Namespace("api/twitter", description="Twitter wrapper")
