"""Vercel entry point for the Dash application."""

from app import app as dash_app


app = dash_app.server
