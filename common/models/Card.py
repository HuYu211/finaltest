# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from config.DB import db


class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    card_name = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    card_content = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    study_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    last_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    fromid = db.Column(db.String(50))